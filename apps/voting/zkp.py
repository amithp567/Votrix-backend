import json
import subprocess
import tempfile
import os

BASE_DIR = os.path.dirname(__file__)

def verify_zkp(proof, public_signals):
    with tempfile.TemporaryDirectory() as tmp:
        proof_path = os.path.join(tmp, "proof.json")
        public_path = os.path.join(tmp, "public.json")

        with open(proof_path, "w") as f:
            json.dump(proof, f)

        with open(public_path, "w") as f:
            json.dump(public_signals, f)

        result = subprocess.run(
            ["node", "verify.js", proof_path, public_path],
            cwd=os.path.join(BASE_DIR, "../zkp/verifier"),
            capture_output=True,
            text=True
        )

        print("🧪 verifier stdout:", result.stdout)
        print("🧪 verifier stderr:", result.stderr)

        return result.returncode == 0
