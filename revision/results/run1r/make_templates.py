"""Seeded templates for Run 1R: lengths ~ Normal(18500, 2200) (truncated >= 1000), uniform start on the
linear CP017100.1, strand 50/50, until total = 60 x genome. Template ID encodes truth: t<idx>_<start0>_<end0>_<strand>."""
import random, sys
ref, out, seed, depth = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
seq = "".join(l.strip() for l in open(ref) if not l.startswith(">")).upper()
G = len(seq); rng = random.Random(seed); comp = str.maketrans("ACGT", "TGCA")
tot, i = 0, 0
with open(out, "w") as f:
    while tot < depth * G:
        L = max(1000, int(round(rng.gauss(18500, 2200))))
        s = rng.randrange(0, G - L + 1); st = rng.choice("+-")
        frag = seq[s:s + L]
        if st == "-": frag = frag.translate(comp)[::-1]
        i += 1; tot += L
        f.write(f">t{i:06d}_{s}_{s+L}_{st}\n{frag}\n")
print(f"templates={i} bases={tot} depth={tot/G:.2f}")
