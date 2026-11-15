"""K-12 MG1655 (NC_000913.3) vs NEB 5-alpha (CP017100.1): is there a large inversion?
Inputs: nucmer (MUMmer 3.23, --maxmatch) show-coords -rclTH tables for all alignments and for
delta-filter -1 (1-to-1). Writes inversion_check.tsv (every reverse-strand block, with whether it
survives 1-to-1 filtering and whether it overlaps a CP017100.1 repeat copy) and a two-panel dot plot.
usage: inversion_check.py <all.coords> <1to1.coords> <out_prefix>
"""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

allc, one, out = sys.argv[1:4]
rd = lambda p: [l.rstrip("\n").split("\t") for l in open(p) if l.strip()]
A, O = rd(allc), rd(one)
key = lambda r: tuple(r[:4])
oneset = {key(r) for r in O}
with open(out + ".tsv", "w") as w:
    w.write("neb_start\tneb_end\tk12_start\tk12_end\tlen_neb\tidentity\tin_1to1\n")
    for r in A:
        if int(r[2]) > int(r[3]):
            w.write("\t".join(r[:5] + [r[6], str(key(r) in oneset)]) + "\n")
rev1 = [r for r in O if int(r[2]) > int(r[3])]
summary = (f"1-to-1 blocks: {len(O)}; reverse-strand 1-to-1 blocks: {len(rev1)} "
           f"(lengths {', '.join(r[4] for r in rev1)} bp); longest reverse 1-to-1 block: "
           f"{max((int(r[4]) for r in rev1), default=0)} bp")
open(out + ".summary.txt", "w").write(summary + "\n")
print(summary)
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
for a, rows, t in ((ax[0], A, "all alignments (--maxmatch)"), (ax[1], O, "1-to-1 (delta-filter -1)")):
    for r in rows:
        s1, e1, s2, e2 = map(int, r[:4])
        if int(r[4]) < 1000:
            continue
        a.plot([s1 / 1e6, e1 / 1e6], [s2 / 1e6, e2 / 1e6], color="#1f77b4" if s2 < e2 else "#d62728", lw=1.5)
    a.set_title(t, fontsize=10); a.set_xlabel("NEB 5-alpha CP017100.1 (Mb)"); a.set_ylabel("K-12 NC_000913.3 (Mb)")
fig.suptitle("Blue: forward; red: reverse strand (blocks >= 1 kb)", fontsize=9)
fig.tight_layout(); fig.savefig(out + ".png", dpi=150); fig.savefig(out + ".pdf")
