from .poseidon import poseidon_pair

LEVELS = 20
ZERO = "0"


class MerkleTree:
    def __init__(self, leaves):
        self.levels = []
        self.build(leaves)

    def build(self, leaves):
        # start with leaves
        current = leaves[:]
        self.levels.append(current)

        # build fixed-depth tree
        for _ in range(LEVELS):
            next_level = []

            for i in range(0, len(current), 2):
                left = current[i]
                right = current[i + 1] if i + 1 < len(current) else ZERO
                next_level.append(poseidon_pair(left, right))

            current = next_level
            self.levels.append(current)

    def root(self):
        return self.levels[-1][0]

    def get_proof(self, index):
        path = []
        indices = []

        for level in self.levels[:-1]:
            if index % 2 == 0:
                # right sibling
                sibling_index = index + 1
                sibling = level[sibling_index] if sibling_index < len(level) else ZERO
                path.append(sibling)
                indices.append(0)
            else:
                # left sibling
                path.append(level[index - 1])
                indices.append(1)

            index //= 2

        return path, indices
