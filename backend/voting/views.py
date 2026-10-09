import json
import subprocess
import os
import hashlib
from django.conf import settings
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .zkp_verify import verify_zkp
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Vote
from elections.models import Election, Candidate
@method_decorator(csrf_exempt, name='dispatch')
class CastVoteView(APIView):
    def post(self, request):
        print("\n🔥 CAST VOTE HIT 🔥")
        print("PAYLOAD:", request.data)

        election_id = request.data.get("election_id")
        candidate_id = request.data.get("candidate_id")
        proof = request.data.get("proof")
        publicSignals = request.data.get("publicSignals")
        
        # 🔥 ADD THIS: Get the voter's unique ID from the frontend payload
        voter_id = request.data.get("voter_id") 

        # Update validation to require voter_id
        if not all([election_id, candidate_id, proof, publicSignals, voter_id]):
            return Response(
                {"error": "Missing required fields"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            election = Election.objects.get(id=election_id)
        except Election.DoesNotExist:
            return Response(
                {"error": "Election not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        election.refresh_status()

        if not election.is_active:
            return Response(
                {"error": "Voting has not started or has ended"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            root = publicSignals[0]
        except Exception:
            return Response(
                {"error": "Invalid public signals"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify ZKP (Proves they are in the Merkle Tree)
        if not verify_zkp(proof, [root]):
            return Response(
                {"error": "Invalid ZKP"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔥 THE FIX: Hash the election_id with the UNIQUE voter_id 
        # instead of the shared Merkle root.
        backend_nullifier = hashlib.sha256(
            f"{election_id}-{voter_id}".encode()
        ).hexdigest()

        if Vote.objects.filter(nullifier=backend_nullifier).exists():
            return Response(
                {"error": "Already voted"},
                status=status.HTTP_400_BAD_REQUEST
            )

        Vote.objects.create(
            election=election,
            candidate_id=candidate_id,
            nullifier=backend_nullifier
        )

        return Response(
            {"message": "Vote cast successfully"},
            status=status.HTTP_201_CREATED
        )
    
class ElectionResultView(APIView):
    def get(self, request, election_id):
        # 1️⃣ Fetch election
        try:
            election = Election.objects.get(id=election_id)
        except Election.DoesNotExist:
            return Response(
                {"error": "Election not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # 2️⃣ Sync election status based on time
        election.refresh_status()

        # 3️⃣ Block results until election ends
        if election.is_active or timezone.now() < election.end_time:
            return Response(
                {"error": "Results available only after election ends"},
                status=status.HTTP_403_FORBIDDEN
            )

        # 4️⃣ Aggregate vote counts per candidate
        results = (
            Candidate.objects
            .filter(election=election)
            .annotate(votes=Count("vote"))
            .values("id", "name", "party", "votes")
            .order_by("-votes")
        )

        # 5️⃣ Final response
        return Response(
            {
                "election": {
                    "id": election.id,
                    "name": election.name,
                    "panchayat": election.panchayat.name,
                    "start_time": election.start_time,
                    "end_time": election.end_time,
                    "status": "ENDED",
                },
                "results": list(results),
            },
            status=status.HTTP_200_OK
        )
