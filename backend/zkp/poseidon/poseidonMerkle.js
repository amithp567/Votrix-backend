import { buildPoseidon } from "circomlibjs";

const poseidon = await buildPoseidon();
const F = poseidon.F;

function hashPair(a, b) {
  return F.toString(poseidon([BigInt(a), BigInt(b)]));
}

export function buildMerkleTree(leaves) {
  let levels = [];
  let current = leaves.map(BigInt);

  levels.push(current);

  while (current.length > 1) {
    let next = [];
    for (let i = 0; i < current.length; i += 2) {
      const left = current[i];
      const right = i + 1 < current.length ? current[i + 1] : left;
      next.push(hashPair(left, right));
    }
    current = next;
    levels.push(current);
  }

  return {
    root: current[0],
    levels
  };
}

export function getProof(levels, index) {
  let pathElements = [];
  let pathIndices = [];

  for (let level of levels.slice(0, -1)) {
    if (index % 2 === 0) {
      const sibling = index + 1 < level.length ? level[index + 1] : level[index];
      pathElements.push(sibling);
      pathIndices.push(0);
    } else {
      pathElements.push(level[index - 1]);
      pathIndices.push(1);
    }
    index = Math.floor(index / 2);
  }

  return { pathElements, pathIndices };
}
