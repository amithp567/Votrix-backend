from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import subprocess
from .biometric import enroll_fingerprint, match_fingerprint

from django.conf import settings

from .serializers import VoterRegistrationSerializer
from .models import Voter
from .merkle import MerkleTree
from .poseidon import poseidon_leaf
import os

LEVELS = 20
ZERO = "0"

# ======================================================
# Poseidon hash helper
# ======================================================
def poseidon_hash(value: str) -> str:
    result = subprocess.run(
        ["node", "hashLeaf.mjs", value],
        cwd=os.path.join(settings.BASE_DIR, "zkp", "poseidon"),
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Poseidon hash failed: {result.stderr}")

    return result.stdout.strip()


# ======================================================
# REGISTER VOTER
# ======================================================
class RegisterVoterView(APIView):
    def post(self, request):

        serializer = VoterRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print("🔐 Starting fingerprint enrollment...")

        finger_id = enroll_fingerprint()

        if not finger_id:
            return Response(
                {"error": "Fingerprint capture failed"},
                status=400
            )

        # 🔥 ZKP leaf (UNCHANGED)
        fingerprint_string = f"finger_{finger_id}"
        leaf = poseidon_leaf(fingerprint_string)

        voter = serializer.save(
            fingerprint_id=finger_id,
            merkle_leaf=leaf
        )

        print("✅ Registered:", voter.name, "ID:", finger_id)

        return Response({"message": "Voter registered"}, status=201)


# ======================================================
# MERKLE ROOT
# ======================================================
class MerkleRootView(APIView):
    def get(self, request):
        leaves = list(
            Voter.objects.order_by("id")
            .values_list("merkle_leaf", flat=True)
        )

        if not leaves:
            return Response({"error": "No voters"}, status=400)

        tree = MerkleTree(leaves)
        return Response({"root": tree.root()}, status=200)


# ======================================================
# MERKLE PROOF
# ======================================================
class MerkleProofView(APIView):
    def post(self, request):
        print("🔥 MERKLE PROOF VIEW HIT")

        finger_id = request.data.get("fingerprint_id")

        if not finger_id:
            return Response({"error": "Fingerprint ID required"}, status=400)

        try:
            finger_id = int(finger_id)
        except ValueError:
            return Response({"error": "Invalid fingerprint_id"}, status=400)

        # 🔥 SAME LOGIC (ZKP SAFE)
        fingerprint_string = f"finger_{finger_id}"
        leaf = poseidon_leaf(fingerprint_string)

        voters = list(Voter.objects.order_by("id"))
        leaves = [v.merkle_leaf for v in voters]

        if not leaves:
            return Response({"error": "No voters"}, status=400)

        if leaf not in leaves:
            return Response({"error": "Voter not found"}, status=404)

        index = leaves.index(leaf)
        tree = MerkleTree(leaves)

        path, indices = tree.get_proof(index)

        # pad
        path += [ZERO] * (LEVELS - len(path))
        indices += [0] * (LEVELS - len(indices))

        return Response({
            "leaf": leaf,
            "root": tree.root(),
            "pathElements": path,
            "pathIndices": indices,
        }, status=200)


# ======================================================
# VERIFY VOTER (FIXED)
# ======================================================
class VerifyVoterView(APIView):
    def post(self, request):

        panchayat_id = request.data.get("panchayat")

        if not panchayat_id:
            return Response(
                {"error": "Panchayat required"},
                status=400
            )

        print("🔐 Starting fingerprint verification...")

        finger_id = match_fingerprint()

        print("FINGER ID:", finger_id)

        if not finger_id:
            return Response(
                {"error": "Fingerprint not recognized"},
                status=401
            )

        # 🔥 FIX: use fingerprint_id instead of merkle
        voter = Voter.objects.filter(
            fingerprint_id=finger_id,
            panchayat_id=panchayat_id
        ).first()

        if not voter:
            return Response(
                {"error": "Voter not eligible"},
                status=401
            )

        print("✅ Voter verified:", voter.name)

        return Response({
            "message": "Voter verified",
            "fingerprint_id": finger_id,
            "voter_id": voter.id,
        }, status=200)