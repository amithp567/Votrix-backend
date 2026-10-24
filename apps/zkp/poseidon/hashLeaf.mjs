import { buildPoseidon } from "circomlibjs";

const input = process.argv[2];

async function main() {
  const poseidon = await buildPoseidon();
  const F = poseidon.F;

  // 🔥 CORRECT conversion: string → hex → BigInt
  const hex = Buffer.from(input, "utf8").toString("hex");
  const x = BigInt("0x" + hex);

  const hash = F.toString(poseidon([x]));
  console.log(hash);

  process.exit(0); // ✅ MUST EXIT
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
    