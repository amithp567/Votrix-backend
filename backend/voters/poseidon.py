import subprocess
import os
from django.conf import settings

# cache ZERO so node is called only once
_POSEIDON_ZERO = None

def poseidon_zero():
    global _POSEIDON_ZERO
    if _POSEIDON_ZERO is None:
        _POSEIDON_ZERO = poseidon_leaf("0")
    return _POSEIDON_ZERO



def _run_node(script: str, *args: str) -> str:
    result = subprocess.run(
        ["node", script, *args],
        cwd=os.path.join(settings.BASE_DIR, "zkp", "poseidon"),
        capture_output=True,
        text=True,
        timeout=5  # 🔥 prevents infinite hang
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return result.stdout.strip()


def poseidon_leaf(value: str) -> str:
    """
    Poseidon hash of a single input (fingerprint)
    Returns DECIMAL STRING
    """
    return _run_node("hashLeaf.mjs", value)


def poseidon_pair(a: str, b: str) -> str:
    """
    Poseidon hash of two field elements
    """
    return _run_node("hashPair.mjs", a, b)


# def poseidon_zero() -> str:
#     """
#     Canonical Poseidon ZERO = Poseidon(0, 0)
#     """
#     global _POSEIDON_ZERO
#     if _POSEIDON_ZERO is None:
#         _POSEIDON_ZERO = poseidon_pair("0", "0")
#     return _POSEIDON_ZERO
