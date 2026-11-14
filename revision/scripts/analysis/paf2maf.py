"""Convert minimap2 alignments of reads to the reference into a PBSIM3-style genome MAF,
so the original truth scripts (read_truth.py, junction_check.py, edge_discrepancy.py,
graph_truth.py via read_truth) run unchanged on read sets whose simulator MAF is not in
genome coordinates (Run 1R, PBSIM3 template mode) or that have no simulator truth.

Convention copied from PBSIM3 output:
  a
  s ref <ref_start> <ref_span> + <genome_len> <ref text with '-' for insertions>
  s <read> 0 <read_len> <strand> <read_len> <read text in forward-genome orientation>
Bases minimap2 soft-clipped at the read ends are written as insertions (ref '-') so the
read line always covers the full read. Only primary alignments are used; reads without a
primary alignment are listed in <out>.unaligned.txt and omitted.
usage: paf2maf.py <reads.fq[.gz]> <ref.fasta> <threads> <preset> <out.maf.gz>
"""
import gzip
import os
import re
import subprocess
import sys

reads, ref, T, preset, out = sys.argv[1:6]
MM = os.path.expanduser("~/projects/gnnome-revision/work/envs/tools/bin/minimap2")
G = sum(len(l.strip()) for l in open(ref) if not l.startswith(">"))
comp = str.maketrans("ACGTNacgtn", "TGCANtgcan")
op = lambda p: gzip.open(p, "rt") if p.endswith(".gz") else open(p)
seqs = {}
with op(reads) as f:
    for h in f:
        s = f.readline().strip(); f.readline(); f.readline()
        seqs[h[1:].split()[0]] = s
tok = re.compile(r"(=[A-Za-z]+|\*[a-z][a-z]|\+[a-z]+|-[a-z]+)")
p = subprocess.Popen([MM, "-t", T, "-c", "--cs=long", "--secondary=no", "-x", preset, ref, reads],
                     stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
done = set()
w = gzip.open(out, "wt")
for line in p.stdout:
    f = line.rstrip("\n").split("\t")
    tags = {t[:2]: t[5:] for t in f[12:]}
    if tags.get("tp") != "P" or f[0] in done:
        continue
    name, qlen, qs, qe, strand, rs, re_ = f[0], int(f[1]), int(f[2]), int(f[3]), f[4], int(f[7]), int(f[8])
    rt, qt = [], []
    for t in tok.findall(tags["cs"]):
        if t[0] == "=":
            rt.append(t[1:].upper()); qt.append(t[1:].upper())
        elif t[0] == "*":
            rt.append(t[1].upper()); qt.append(t[2].upper())
        elif t[0] == "+":
            rt.append("-" * (len(t) - 1)); qt.append(t[1:].upper())
        else:
            rt.append(t[1:].upper()); qt.append("-" * (len(t) - 1))
    rtxt, qtxt = "".join(rt), "".join(qt)
    s = seqs[name]
    fwd = s if strand == "+" else s.translate(comp)[::-1]          # read in forward-genome orientation
    # clipped read bases, in forward-genome orientation
    left = fwd[:qs] if strand == "+" else fwd[:qlen - qe]
    right = fwd[qe:] if strand == "+" else fwd[qlen - qs:]
    assert qtxt.replace("-", "") == fwd[len(left):len(fwd) - len(right)], name
    rtxt = "-" * len(left) + rtxt + "-" * len(right)
    qtxt = left + qtxt + right
    w.write(f"a\ns ref {rs} {re_ - rs} + {G} {rtxt}\ns {name} 0 {qlen} {strand} {qlen} {qtxt}\n\n")
    done.add(name)
p.wait()
w.close()
miss = [n for n in seqs if n not in done]
open(out.replace(".maf.gz", "") + ".unaligned.txt", "w").write("\n".join(miss) + ("\n" if miss else ""))
print(f"[paf2maf] reads={len(seqs)} aligned={len(done)} unaligned={len(miss)}")
