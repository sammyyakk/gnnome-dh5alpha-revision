# Correction for development-team2/NOTES.md — stale K-12 graph run

`development-team2/` is a local working directory that was never committed to any repository
(it is mentioned in `docs/run1_run2_evidence_report.md` of abhiraj-arya2006/gnnome-dh5alpha but not present in
that repo, in sammyyakk/genome-sequencing (branches main, team1, team2) or in any of its forks). The text below
is meant to be pasted at the top of that NOTES.md, replacing the entry that reports the stale-graph run as a success.

---

**CORRECTION (2026-11-15).** The GNNome run on "DH5α" that loaded `graph_1.gfa` at 2026-07-09 22:15:34 UTC was
**not** a DH5α assembly and must not be reported as a success or as a failure of GNNome.

- That `graph_1.gfa` (SHA-256 `62176d9d91749b6f8fdd5794b05da1a5070ec7e5e23b9963018ab7ee642dcdfc`, 2,561 segments /
  27,451 links) is the Raven graph of GNNome's **E. coli K-12 example reads** (`example/ecoli.fasta.gz`). Rebuilding it
  with the Raven `print_graphs` fork (commit `3207c8d`, `-p0`) from those reads reproduces the file **byte for byte**.
- 200/200 sampled segments are substrings of the K-12 reads and 0/200 of the DH5α reads.
- Scored against CP017100.1 (QUAST 5.3.0, `--min-identity 80`) the resulting contig has 23 misassemblies (5 local) —
  exactly the misassemblies obtained by scoring the K-12 reference NC_000913.3 itself against CP017100.1. They are
  K-12 vs NEB 5-alpha strain differences. There is no ~210 kb inversion (1-to-1 nucmer: 3 reverse blocks of
  770–1,204 bp, all inside repeat copies).
- **No other result used this graph.** Every run in the revision (Run 2, real ONT reads, 27 replicates, Run 1R)
  passes two guards: 200/200 GFA segments are exact substrings of that run's own reads (30/30 graphs), and every
  GNNome / greedy input graph matches its GFA node-for-node and edge-for-edge (181/181 runs). No two runs share a
  graph hash, and none equals `62176d9d…`. The original Run 1 graph (`b12099…0270`) and Run 2 graph (`6d5df98…`)
  were built from DH5α reads (evidence report §3.3), and the Run 2 GNNome contig reproduces byte for byte from the
  Run 2 graph.

Evidence: `revision/results/stale_k12/` and `revision/REVISION.md` §3.7 in
github.com/sammyyakk/gnnome-dh5alpha-revision.
