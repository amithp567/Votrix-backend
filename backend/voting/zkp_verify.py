import subprocess
import json
import os
import hashlib
from django.conf import settings


def verify_zkp(proof, publicSignals):
    print("🔍 BACKEND VERIFY INPUT")
    print("Public Signals:", publicSignals)
    print("Proof keys:", proof.keys())

    # 🔹 PROJECT ROOT (one level above backend/)
    project_root = os.path.abspath(
        os.path.join(settings.BASE_DIR, "..")
    )
    print("📂 PROJECT ROOT:", project_root)

    # 🔹 Verifier directory
    verifier_dir = os.path.join(
        project_root,
        "zkp",
        "verifier"
    )
    print("📂 VERIFIER DIR:", verifier_dir)

    # 🔹 Verification key path
    vk_path = os.path.join(
        project_root,
        "zkp",
        "circuits",
        "verification_key.json"
    )
    print("📂 VK PATH:", vk_path)

    # 🔹 Load verification key
    with open(vk_path, "r") as f:
        vk = json.load(f)

    print(
        "🔐 VK SHA256:",
        hashlib.sha256(json.dumps(vk, sort_keys=True).encode()).hexdigest()
    )

    # 🔹 Call Node verifier
    result = subprocess.run(
        ["node", "verify.mjs"],
        cwd=verifier_dir,
        input=json.dumps({
            "proof": proof,
            "publicSignals": publicSignals
        }),
        text=True,
        capture_output=True
    )

    print("🧪 NODE STDOUT:", result.stdout)
    print("🧪 NODE STDERR:", result.stderr)
    print("🧪 NODE EXIT CODE:", result.returncode)

    return "VALID" in result.stdout
