"""Per-read truth from a minimap2 alignment to the reference, for read sets without a
genome-coordinate MAF (Run 1R: PBSIM3 template mode; real SRR31302084 reads).
Writes <out>.reads.tsv with the same leading columns as read_truth.py
(read, strand, ref_start, ref_end, read_len, match, mismatch, ins, dele, identity)
and <out>.summary.json. Identity = matches / alignment columns of the primary
alignment (cs tag); reads without a primary alignment get identity NA and are excluded.
For real reads the reference is NEB 5-alpha (CP017100.1), so true strain differences
count as read errors (a few hundred bases genome-wide at most).
usage: paf_truth.py <reads.fq[.gz]> <ref.fasta> <threads> <out_prefix> [preset: map-hifi|map-ont]
"""
import json
import os
import re
import statistics as st
import subprocess
import sys

reads, ref, T, out = sys.argv[1:5]
preset = sys.argv[5] if len(sys.argv) > 5 else "map-hifi"
MM = os.path.expanduser("~/projects/gnnome-revision/work/envs/tools/bin/minimap2")
p = subprocess.Popen([MM, "-t", T, "-c", "--cs=short", "--secondary=no", "-x", preset, ref, reads],
                     stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
rows = {}
tok = re.compile(r"(:\d+|\*[a-z][a-z]|\+[a-z]+|-[a-z]+)")
for line in p.stdout:
    f = line.rstrip("\n").split("\t")
    tags = {t[:2]: t[5:] for t in f[12:]}
    if tags.get("tp") != "P":
        continue
    m = x = ins = dele = 0
    for t in tok.findall(tags["cs"]):
        if t[0] == ":":
            m += int(t[1:])
        elif t[0] == "*":
            x += 1
        elif t[0] == "+":
            ins += len(t) - 1
        else:
            dele += len(t) - 1
    # unaligned read ends count as errors (clipped bases)
    clip = int(f[1]) - (int(f[3]) - int(f[2]))
    cols = m + x + ins + dele + clip
    r = f[0]
    if r in rows and rows[r]["match"] >= m:
        continue
    rows[r] = dict(read=r, strand=f[4], ref_start=int(f[7]), ref_end=int(f[8]), read_len=int(f[1]),
                   match=m, mismatch=x, ins=ins + clip, dele=dele, identity=m / cols if cols else 0.0)
p.wait()
cols = ["read", "strand", "ref_start", "ref_end", "read_len", "match", "mismatch", "ins", "dele", "identity"]
with open(out + ".reads.tsv", "w") as w:
    w.write("\t".join(cols) + "\n")
    for r in rows.values():
        w.write("\t".join(str(r[c]) for c in cols) + "\n")
ids = sorted(r["identity"] for r in rows.values())
agg = sum(r["match"] for r in rows.values()) / sum(r["match"] + r["mismatch"] + r["ins"] + r["dele"] for r in rows.values())
q = lambda f: ids[min(len(ids) - 1, int(f * len(ids)))]
summ = dict(reads_aligned=len(rows), identity_aggregate=agg, identity_mean=st.mean(ids), identity_median=st.median(ids),
            identity_p10=q(0.10), identity_p90=q(0.90), identity_p99=q(0.99),
            phred_of_mean_error=-10 * __import__("math").log10(max(1e-12, 1 - st.mean(ids))))
json.dump(summ, open(out + ".summary.json", "w"), indent=1)
print(json.dumps(summ))
