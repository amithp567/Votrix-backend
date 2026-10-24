import { buildPoseidon } from "circomlibjs";

const a = BigInt(process.argv[2]);
const b = BigInt(process.argv[3]);

async function main() {
  const poseidon = await buildPoseidon();
  const F = poseidon.F;

  const hash = F.toString(poseidon([a, b]));
  console.log(hash);

  process.exit(0); 
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
