"""Collect per-assembler metrics for one run directory produced by assemble_all.sh.

For every assembly in <run>/asm/*.fasta (raven, gnnome, gnnome_twin, greedy_*):
  - QUAST unpolished (--min-identity 80) and Racon x2 (default) metrics
  - unpolished identity: minimap2 asm20 matches / alignment columns (same definition as the
    manuscript's Table 6, i.e. NOT derived from QUAST's per-100-kbp event counts)
  - read selection: the reads whose bases each assembly copies, with their length-weighted
    per-read error and the identity distribution of those reads
      * GNNome / greedy variants: from decode/0_walks.pkl; each walk read contributes its
        prefix up to the next junction (prefix = segment length - overlap length used by that
        parser: GFA length for the original parser, directional length for the twin fix)
      * Raven: oriented segments whose first 1 kb occurs uniquely in the Raven contig,
        ordered by contig position (same method as the original analysis)
  - read-set identity percentiles (all reads)
usage: collect.py <run_dir> <truth.reads.tsv> <out.json>
"""
import csv
import json
import os
import pickle
import statistics as st
import subprocess
import sys

run, truth, out = sys.argv[1:4]
W = os.path.expanduser("~/projects/gnnome-revision/work")
MM = f"{W}/envs/tools/bin/minimap2"
REF = os.environ.get("GNN_REF", f"{W}/data/CP017100.fasta")


def quast(p):
    try:
        return {r[0]: r[1] for r in csv.reader(open(p), delimiter="\t") if len(r) > 1}
    except FileNotFoundError:
        return {}


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def fasta(p):
    s, cur = [], []
    for l in open(p):
        if l.startswith(">"):
            if cur:
                s.append("".join(cur))
                cur = []
        else:
            cur.append(l.strip())
    if cur:
        s.append("".join(cur))
    return s


def identity(p):
    o = subprocess.run([MM, "-t", "8", "-cx", "asm20", "--secondary=no", REF, p], capture_output=True, text=True).stdout
    m = al = 0
    for l in o.splitlines():
        f = l.split("\t")
        m += int(f[9])
        al += int(f[10])
    return m / al if al else None


T, ident_of = {}, {}
with open(truth) as fh:
    hdr = fh.readline().rstrip("\n").split("\t")
    ii = hdr.index("identity")
    for l in fh:
        f = l.rstrip("\n").split("\t")
        T[f[0]] = 1 - float(f[ii])
ids = sorted(1 - e for e in T.values())
pct = lambda q: ids[min(len(ids) - 1, int(q * len(ids)))]
res = dict(run=os.path.basename(os.path.normpath(run)), reads_with_truth=len(T),
           read_identity_mean=st.mean(ids), read_identity_median=st.median(ids),
           read_identity_p90=pct(0.9), read_identity_p99=pct(0.99), assemblies={})

rcx = lambda s: s.translate(str.maketrans("ACGTN", "TGCAN"))[::-1]
segs, n2r, r2n, ol_gfa, ol_twin = {}, {}, {}, {}, {}
idx = 0
for line in open(f"{run}/raven/graph_1.gfa"):
    f = line.rstrip("\n").split("\t")
    if f[0] == "S":
        segs[idx], segs[idx + 1] = f[2], rcx(f[2])
        n2r[idx] = n2r[idx + 1] = f[1]
        r2n[f[1]] = (idx, idx + 1)
        idx += 2


def nodes(a, o1, b, o2):
    A, B = r2n[a], r2n[b]
    real = (A[0] if o1 == "+" else A[1], B[0] if o2 == "+" else B[1])
    virt = (B[1] if o2 == "+" else B[0], A[1] if o1 == "+" else A[0])
    return real, virt


for line in open(f"{run}/raven/graph_1.gfa"):
    f = line.rstrip("\n").split("\t")
    if f[0] == "L":
        real, virt = nodes(*f[1:5])
        o = int(f[5][:-1])
        ol_gfa[real] = ol_gfa[virt] = o
tw = f"{run}/raven/graph_1.twin.tsv"
if os.path.exists(tw):
    for i, line in enumerate(open(tw)):
        if i == 0:
            continue
        f = line.rstrip("\n").split("\t")
        real, virt = nodes(*f[0:4])
        ol_twin[real], ol_twin[virt] = int(f[4]), int(f[9])


def summarize(contrib):
    L = sum(c for _, c in contrib)
    known = [(r, c) for r, c in contrib if r in T]
    Lk = sum(c for _, c in known)
    rid = sorted(1 - T[r] for r, _ in known)
    q = lambda x: rid[min(len(rid) - 1, int(x * len(rid)))] if rid else None
    return dict(source_reads=len(contrib), source_bases=L,
                source_read_error_weighted=(sum(c * T[r] for r, c in known) / Lk) if Lk else None,
                source_read_identity_mean=st.mean(rid) if rid else None,
                source_read_identity_p10=q(0.1), source_read_identity_median=st.median(rid) if rid else None,
                source_reads_in_worst_decile=sum(1 for r, _ in known if 1 - T[r] <= pct(0.1)),
                source_contrib_median=st.median(c for _, c in contrib) if contrib else None)


for a in sorted(os.listdir(f"{run}/asm")):
    name = a[:-6]
    seqs = fasta(f"{run}/asm/{a}")
    r = dict(contigs=len(seqs), length=sum(map(len, seqs)), p0_identity=identity(f"{run}/asm/{a}"))
    for tag, sub in (("p0m80", f"p0_m80_{name}"), ("p0def", f"p0_def_{name}"), ("racon2", f"racon2_{name}")):
        qd = quast(f"{run}/quast/{sub}/report.tsv")
        for k, n in (("Genome fraction (%)", "gf"), ("# mismatches per 100 kbp", "mm"), ("# indels per 100 kbp", "indel"),
                     ("# misassemblies", "mis"), ("# local misassemblies", "localmis"), ("NGA50", "nga50"),
                     ("Total aligned length", "aligned"), ("Unaligned length", "unaligned")):
            r[f"{tag}_{n}"] = num(qd.get(k))
    if name == "raven":
        ctg = "".join(seqs)
        hits = []
        for n, s in segs.items():
            k = ctg.find(s[:1000])
            if k >= 0 and ctg.find(s[:1000], k + 1) < 0:
                hits.append((k, n))
        hits.sort()
        contrib = [(n2r[n], (hits[i + 1][0] if i + 1 < len(hits) else len(ctg)) - k) for i, (k, n) in enumerate(hits)]
    else:
        wp = f"{run}/gn_{name}/raven/decode/0_walks.pkl"
        walks = pickle.load(open(wp, "rb"))
        olx = ol_twin if name.endswith("twin") else ol_gfa
        contrib = []
        for w in walks:
            contrib += [(n2r[u], max(0, len(segs[u]) - olx[(u, v)])) for u, v in zip(w[:-1], w[1:])]
            contrib.append((n2r[w[-1]], len(segs[w[-1]])))
        r["walks"] = len(walks)
        r["walk_junctions"] = sum(len(w) - 1 for w in walks)
    r.update(summarize(contrib))
    res["assemblies"][name] = r
json.dump(res, open(out, "w"), indent=1)
print(f"{res['run']}: " + "  ".join(f"{k} id={v['p0_identity']:.5f} err={v['source_read_error_weighted'] or 0:.5f}" for k, v in res["assemblies"].items()))
