# Revision of "Evaluating a Pretrained Graph Neural Network Assembler on *E. coli* DH5α Long Reads"

This document compiles **every change** made in response to the peer review and discrepancy audit.
The manuscript itself is **not edited**. Each change is keyed to line numbers in the unmodified source
`revision/manuscript/main_v7_original.tex` (SHA-256 `3490bab9…`, 405 lines), with ready-to-paste
LaTeX (old → new). All numbers below were recomputed from scratch on this machine; every result file is
in `revision/results/` with hashes, and every script is in `revision/scripts/`.

All runs are complete. Every number from the revision's own runs comes from a committed result file under `revision/results/`; numbers labelled **Run 1** are the original, non-reproducible values quoted from the manuscript or the original repository.

---

## 0. Summary of what changed and why

| # | Reviewer / audit item | Outcome |
|---|---|---|
| 1 | 23 misassemblies from the stale graph | Rebuilt the stale K-12 graph and reproduced the 23 exactly. They are **strain differences between K-12 MG1655 and NEB 5-alpha**, not a GNNome failure. **There is no 210 kb inversion**: the claimed inversion was a K-12-only IS copy aligning in reverse to a DH5α IS copy. §3.7 rewritten. |
| 2 | Twin-edge methodology | Raven fork patched to export both directional overlap lengths; GNNome parser patched to use them. Run 2: local misassemblies 19 → 5, extensive 0 → 0. The prediction in the Discussion is now tested. New §3.8. |
| 3 | Greedy baseline on raw features | Same graph, same GNNome decoder, edge score from raw overlap similarity / length, no GNN. A greedy walk ranked by raw overlap similarity alone beats GNNome on Run 2 (unpolished identity 88.86% vs 88.26%, 8 vs 19 local misassemblies; with twin lengths 88.93% vs 88.39%, 3 vs 5), in 9/9 replicate settings, on Run 1R and on real reads. New §3.9. This changes the interpretation: the advantage is a property of the input features plus greedy decoding, not of the learned network. |
| 4 | Run 1 not reproducible | Run 1R: Run 1 regenerated from logged commands with a fixed PBSIM3 build (two upstream bugs patched, documented). Run 1R (99.72% reads): GNNome −89% mismatches / −42% indels vs Raven unpolished (Run 1: −44% / −41%); identical after polishing. Run 1 numbers are marked non-reproducible; Run 1R numbers lead. |
| 5 | Count discrepancies (3 vs 4 indels; 22 vs 21 breakpoints; Table 7 counts) | All traced to a cause; fixed text and figures. §6. |
| 6 | Statistics (Run 1 p-value; 8/21 p=0.07; Q80; pseudo-replication) | Every test now named with k/n. Reviewer's binomial assumption for Run 1 is incorrect (it is a Wilcoxon on paired error differences). Setting-level tests (n = 7 / 9) and a mixed model added. Q80 → Q28. §5. |
| 7 | GNNome-paper claims | Checked against the **published** version (Genome Res. 2025;35(4):839, PMC12047240). Both manuscript claims are correct for the published paper; the reviewer used preprint v1. Table citations added. §7. |
| 8 | Reference is NEB 5-alpha | Wording changed throughout to "NEB 5-alpha (DH5α *fhuA2*), CP017100.1". |
| 9 | Real reads unused | SRR31302084 (ONT, ~106×) assembled through the identical pipeline. New §3.10. |
| 10 | References | 9 bibliography entries corrected. §8. |
| 11 | Provenance | GNNome commit 418c7d3 is not fetchable from upstream; upstream HEAD ac827c2 reproduces Run 2 byte for byte. Hardware line corrected. |

---

## 1. Reproduction status (what was rerun)

All runs used the pinned environment in `revision/scripts/pipeline/` (micromamba; Python 3.8.20, PyTorch 1.9.0 **+cpu**,
DGL 0.8.1; Raven 1.8.1 `print_graphs` fork commit `3207c8d`; PBSIM3 `35ce0de`; QUAST 5.3.0; minimap2 2.28;
Racon 1.5.0; MUMmer 3/4 nucmer).

| Item | Result |
|---|---|
| Run 2 reads (PBSIM3 seed 1783636376) | byte-identical content (SHA `5a6ba8d2…`), MAF `48653c61…` |
| Run 2 Raven graph | `graph_1.gfa` SHA `6d5df98…`, identical |
| Run 2 Raven `-p0` contig | `b616d36…`, identical |
| Run 2 GNNome contig | `fa049876…`, identical, using upstream HEAD `ac827c2` (commit `418c7d3` is not fetchable: "not our ref"; it is in no upstream branch) |
| GUARD 2 (graph consumed) | MATCH: 1,524/1,524 nodes, 5,936/5,936 edges |
| Run 2 QUAST (m80) | Raven 2,481.05 / 7,741.78 mm/indel per 100 kbp, 15 local; GNNome 2,278.59 / 7,437.99, 19 local; GF 99.375 / 99.786; 0 extensive — matches Table 4 (`tab:main`) |
| Stale-graph 23 misassemblies | reproduced exactly (§3.7) |
| Run 1 | not regenerable as published (build lost); regenerated as Run 1R (§3.11) |

Provenance guards added to the pipeline (`work/bin/assemble_all.sh`, copied to `revision/scripts/pipeline/`):
1. **GUARD 1** – 200 sampled GFA segments must be exact substrings of the input reads, else abort.
2. **GUARD 2** – every GNNome input graph must match the GFA node-for-node and edge-for-edge, else abort.

---

## 2. Abstract (lines 47–53)

**Line 49 – Methods.** old:
```latex
\textbf{Methods:} Accurate (60$\times$, 99.84\% mean identity) and noisy (30$\times$, 86.01\% mean identity) long reads were simulated, and one Raven graph per run was resolved by Raven and by pretrained GNNome. Every edge and assembly error was traced against the simulation truth, and 23 controlled evaluations were run (21 simulated replicates and two 50\% subsamples of the Run~1 reads).
```
new:
```latex
\textbf{Methods:} Accurate HiFi-like (60$\times$) and noisy (30$\times$, 86.0\% mean identity) long reads were simulated from the NEB 5-alpha (DH5$\alpha$ \emph{fhuA2}) reference, and public ONT reads of the same strain were assembled. One Raven graph per read set was resolved by Raven, by pretrained GNNome, by GNNome with both directional overlap lengths, and by a greedy walk on raw overlap features with no neural network. Every edge and assembly error was traced against the simulation truth, and 27 simulated replicates from 9 settings were analysed with settings as units.
```

**Line 51 – Results.** new:
```latex
\textbf{Results:} After Racon polishing, GNNome was not more accurate than Raven (fewer errors in 3 of 9 settings; mixed model $+0.24$ errors per 100~kbp, 95\% CI $-0.02$ to $+0.50$, favouring Raven), and the same held for real nanopore reads. Unpolished, GNNome was more accurate than Raven in 9 of 9 settings (exact sign test $p=0.004$; $+1.31$~pp identity); the advantage was near zero at realistic $\sim$86\% read identity ($+0.08$~pp) and grew with read accuracy and read length. Its walk copies cleaner reads because its overlap-similarity input tracks read error (Spearman $\rho\approx-0.9$). A greedy walk that ranks edges by raw overlap similarity, with no neural network, exceeded GNNome's unpolished accuracy in 9 of 9 settings ($+0.65$~pp), on accurate HiFi-like reads and on real nanopore reads, so the advantage comes from the features and greedy decoding rather than from learned graph reasoning. Assigning each edge and its reverse-complement twin their own overlap lengths removed 14 of 19 GNNome local misassemblies on noisy reads and all 56 indels longer than 5~bp on accurate reads. A previously reported 23-misassembly failure was a K-12 graph assembled by mistake; all 23 are reference differences between K-12 and NEB 5-alpha.
```

**Line 53 – Conclusion.** new:
```latex
\textbf{Conclusion:} On DH5$\alpha$, pretrained GNNome's unpolished advantage over Raven arises from a preference for high-overlap-similarity edges, which a greedy walk on raw overlap similarity reproduces, and it does not survive polishing.
```

---

## 3. Results sections

### 3.7 A false failure from a stale input graph (line 356) — **rerun and replaced**

What was done (`runs/stale_k12/`):
- Rebuilt the stale graph: Raven fork on GNNome's `example/ecoli.fasta.gz` (K-12 HiFi; SHA `62176d9d…`) → `graph_1.gfa` with S = 2,561, L = 27,451.
- Ran GNNome with the DH5α reads but this graph (the original mistake). QUAST vs CP017100.1, `--min-identity 80`: **23 misassemblies, 5 local**, GF 98.806, 13.69 mismatches and 72.66 indels per 100 kbp (K-12 HiFi read accuracy — the sequence is copied from K-12 reads in the GFA, not from the DH5α reads).
- Scored the K-12 reference NC_000913.3 itself against CP017100.1 with the same QUAST settings: **the same 23 misassemblies (23 relocations, 0 inversions), 5 local**.
- nucmer (MUMmer 3.23, `--maxmatch`, then `delta-filter -1`) K-12 vs NEB 5-alpha: 31 one-to-one blocks, of which only **3 are reverse-strand (854, 1,204 and 770 bp), each inside a repeat copy**; no inverted segment of any appreciable size (`results/stale_k12/nucmer/inversion_check.{tsv,png,pdf}`, script `scripts/figures/inversion_check.py`).
- Our rebuilt K-12 graph has SHA-256 `62176d9d91749b6f…642dcdfc`, **byte-identical** to the stale graph recorded in the original evidence report (§3.3), so the rerun reproduces the original mistake exactly.

What the "210 kb inversion" actually was: a K-12-only IS copy at K-12 566,771–568,040 (1,270 bp) that aligns in reverse orientation to a DH5α IS copy at 297,701–298,970 (99.92% identity, repeat family F006). A dot plot drawn from all (not 1-to-1) alignments connects these two copies and looks like a ~210 kb inverted segment; it is not one. The real differences are strain insertions/deletions at IS elements, the K-12 565,828–577,188 region (present only in K-12), and a ~12.8 kb relocation (DH5α 1,235,508–1,248,271 ↔ K-12 359,483–372,339). The rrnD–rrnE inversion (Hill & Harnish 1981) is not involved.

old (line 356):
```latex
... reproduces the same breakpoints (Fig.~\ref{fig:regional}a), including an inversion of about 210~kb and a breakpoint at a copy of an IS3-family insertion element whose two nearby copies are 99.92\% identical over 1{,}258~bp. The apparent repeat-linked failure was a strain difference. ...
```
new (full paragraph):
```latex
An earlier version of this study reported 23 misassemblies by GNNome on DH5$\alpha$. That run is excluded: the Raven build used then did not write the graph file GNNome reads, so GNNome loaded a leftover \emph{E.\ coli} K-12 graph with the same file name. We rebuilt that graph from the K-12 example reads (2{,}561 segments, 27{,}451 links) and reran GNNome on it with the DH5$\alpha$ reads: QUAST again reports 23 misassemblies (5 local) against CP017100.1, with K-12 HiFi-level base accuracy (13.7 mismatches and 72.7 indels per 100~kbp), because the contig is copied from K-12 reads. Scoring the K-12 reference (NC\_000913.3) itself against CP017100.1 with identical settings gives the same 23 misassemblies (all relocations, no inversions) and 5 local misassemblies. They mark real differences between K-12 MG1655 and NEB 5-alpha: insertion-sequence insertions and deletions, an 11.4~kb region present only in K-12, and a 12.8~kb relocation. A 1-to-1 nucmer alignment contains no inverted segment (its only reverse-strand blocks are three repeat copies of 770--1{,}204~bp); an apparent inversion in an all-alignments dot plot is a K-12-only IS copy aligning in reverse to a DH5$\alpha$ IS copy (99.92\% identity over 1{,}270~bp). Two checks now guard the pipeline: every GFA must contain segments that are exact substrings of the intended reads, and every GNNome input graph must match that GFA node for node and edge for edge.
```
Fig. 4a caption (line 350): replace "The excluded old Run~2 GNNome assembly shows the breakpoint pattern of the K-12 reference itself." with "The excluded stale-graph GNNome assembly and the K-12 reference share the same 23 breakpoints; none is an inversion."

Result files: `revision/results/stale_k12/` (QUAST reports for the stale-graph contig and NC_000913.3; nucmer coords; `inversion_check.tsv`).

### 3.8 New section — Twin-edge overlap lengths (insert after line 352, and edit line 367 / 372)

Method: Raven computes `length` and `length_pair` for every overlap (`construct.cc:620–621`) but writes only one
(`graph_repr.cc:61`, `tail_len - edge.length`). GNNome's parser (`graph_parser.py:336–340`) assigns that single
value to both the edge and its virtual reverse-complement twin. Fix (`revision/patches/`):
- `raven_twin`: after `PrintGfa(graph,"graph_1.gfa")`, also writes `graph_1.twin.tsv` with both directional overlaps for every edge. `graph_1.gfa` is byte-identical to the unpatched fork (verified).
- `GNNome_twin`: parser reads the TSV, asserts the forward length equals the GFA length, and gives the twin its own length (and prefix length).

Results (QUAST `--min-identity 80`, unpolished; Run 2):

| Assembly | Mismatches/100 kbp | Indels/100 kbp | Misassemblies (local) | GF % |
|---|---|---|---|---|
| Raven | 2,481 | 7,742 | 0 (15) | 99.375 |
| GNNome (published parser) | 2,279 | 7,438 | 0 (19) | 99.786 |
| GNNome (twin lengths) | 2,350 | 7,555 | 0 (5) | 99.792 |

2,950 of 2,968 Run 2 twin edges had a different own length. In Run 1R 40,998 of 44,319 and in the real-read graph 4,272 of 4,307 twin edges differ (`results/run2/twin_counts.txt`). **Run 1R:** GNNome's indels > 5 bp fall from 56 to 0 with twin lengths (the twin walk rebuilds the assembly byte for byte when contigs are rebuilt with the twin lengths; the trace script's `gnnome_walk_rebuild_matches_assembly: false` and junction-origin counts for `*_twin` runs use GFA lengths and do not apply to them) (unpolished identity 99.828% → 99.846%; mismatches/indels per 100 kbp 1.07/154.13 → 1.11/151.44). **Replicates (27):** GNNome twin vs GNNome unpolished identity better in 9/9 settings (exact sign p = 0.004; mixed +0.21 pp [`results/replicates/rep_stats.json`]); polished no difference (twin better in 7/9 settings, sign p = 0.18; mixed −0.24 errors/100 kbp). **Real reads:** local misassemblies 48 → 31 unpolished, 9 → 7 polished; unpolished identity 93.02% → 93.35%.

New text (insert after line 352):
```latex
\subsection{Using Both Directional Overlap Lengths}\label{sec:twin}
We patched the Raven fork to export, alongside an unchanged graph file, both directional overlap lengths for every edge, and patched GNNome's parser to give each reverse-complement twin its own length. In Run~2, 2{,}950 of 2{,}968 twin edges received a different length. GNNome's local misassemblies fell from 19 to 5 (Raven: 15), with no extensive misassemblies and a slightly higher genome fraction (99.79\%); per-base error rose slightly (2{,}350 vs.\ 2{,}279 mismatches and 7{,}555 vs.\ 7{,}438 indels per 100~kbp) because the walk changed. On the accurate Run~1R reads, all 56 of GNNome's indels longer than 5~bp disappear (56 to 0), and unpolished identity rises from 99.828\% to 99.846\%. Across 27 replicates, twin lengths improved GNNome's unpolished identity in all 9 settings (mixed model $+0.21$~pp), and on real nanopore reads they reduced local misassemblies from 48 to 31.
```
Line 367 replace "Exporting both directional lengths from Raven, or recomputing them in the parser, should remove its large indels; we predict this from the mechanism but have not run it." with "Exporting both directional lengths from Raven removed most of these junction errors (Section~\ref{sec:twin})."
Line 372 remove "The parser fix and" (now tested).

### 3.9 New section — Greedy baseline on raw overlap features

Same Raven graph, same GNNome `inference.py` greedy decoder (seed edges, 70 kb stop, unchanged), edge
scores written to `decode/0_predicts.pt` (which `inference.py:427–430` loads in place of model inference):
`sim` = logit(overlap similarity); `len` = z(overlap length); `simlen` = z(sim) + z(len). Script:
`revision/scripts/pipeline/raw_scores.py`.

Run 2 (QUAST m80, unpolished):

| Edge score | Parser | Mismatches/100 kbp | Indels/100 kbp | Local mis. | GF % |
|---|---|---|---|---|---|
| GNNome model | published | 2,279 | 7,438 | 19 | 99.786 |
| GNNome model | twin | 2,350 | 7,555 | 5 | 99.792 |
| length only | published | 2,472 | 7,720 | 64 | 98.981 |
| length only | twin | 2,481 | 7,743 | 15 | 99.375 |

(The length-only twin assembly is a distinct contig, SHA-256 prefix `8e499740` vs Raven `b616d36b`, whose QUAST values happen to be within rounding of Raven's; it was run before the unified pipeline, so its QUAST report is committed separately under `results/run2/first_runs/`.)
| similarity only | published | **2,177** | **7,278** | 8 | 99.815 |
| similarity only | twin | 2,192 | 7,302 | **3** | **99.818** |
| similarity + length | published | 2,375 | 7,578 | 25 | 99.629 |
| similarity + length | twin | 2,366 | 7,574 | 6 | 99.780 |

Assemblies re-run inside the unified pipeline (`runs/run2_full`) are byte-identical to the first runs (SHA-256 prefixes:
sim `13d24711`, sim_twin `722466bf`, simlen `b8afd143`, simlen_twin `ca540fa3`, len `42d55b64`).

Read selection (Run 2, `trace/collect.json`; unpolished identity = minimap2 asm20 matches/columns):

| Assembly | Unpolished identity | Source reads | Median piece | Weighted source-read error | Reads from worst decile | Racon×2 mm / indel per 100 kbp |
|---|---|---|---|---|---|---|
| Raven | 88.020% | 654 | 5.3 kb | 13.51% | 40 | 0.74 / 28.66 |
| GNNome | 88.256% | 555 | 6.3 kb | 12.61% | 3 | 0.76 / 29.88 |
| GNNome twin | 88.386% | 558 | 6.6 kb | 12.89% | 4 | 0.81 / 30.27 |
| greedy length | 87.522% | 754 | 4.4 kb | 13.54% | 46 | 0.94 / 29.24 |
| greedy similarity | 88.863% | 298 | 14.5 kb | 12.14% | 2 | 0.61 / 29.29 |
| greedy similarity, twin | **88.932%** | 303 | 14.4 kb | 12.20% | 1 | 0.72 / 29.92 |
| greedy sim+len | 87.959% | 587 | 6.3 kb | 13.03% | 7 | 0.85 / 29.51 |
| greedy sim+len, twin | 88.337% | 581 | 6.4 kb | 12.95% | 5 | 0.76 / 29.77 |

Ranking by overlap similarity alone copies fewer, longer and cleaner reads than the GNN does, and gives the most accurate
unpolished assembly. Adding overlap length to the score (z-sum) dilutes this and lands near GNNome. After polishing all
variants are within 0.61–0.94 mismatches and 28.7–30.3 indels per 100 kbp; none has local misassemblies.

**Replicates** (27 = 9 settings × 3 seeds; setting means of unpolished identity difference, pp; `results/replicates/rep_stats.json`, table `replicates.tsv`):

| Setting (target accuracy, depth, length) | Read identity | GNNome − Raven | greedy sim − Raven | greedy sim − GNNome | Polished (mm+indel /100 kbp) GNNome − Raven |
|---|---|---|---|---|---|
| 85%, 30×, 9 kb (Run 2 settings) | 86.0% | +0.08 | +0.79 | +0.71 | +0.85 |
| 85%, 60×, 9 kb | 86.0% | +0.19 | +1.10 | +0.90 | +0.54 |
| 85%, 30×, 18.5 kb | 86.0% | +0.07 | +1.59 | +1.52 | +0.77 |
| 90%, 30×, 9 kb | 90.5% | +0.65 | +1.49 | +0.83 | +0.28 |
| 95%, 30×, 9 kb | 95.2% | +1.25 | +1.82 | +0.58 | −0.03 |
| 99% target (96%), 30×, 9 kb | 96.1% | +1.47 | +1.87 | +0.41 | −0.36 |
| 99% target (96%), 60×, 9 kb | 96.1% | +1.99 | +2.30 | +0.31 | +0.06 |
| 99% target (96%), 30×, 18.5 kb | 96.1% | +2.99 | +3.32 | +0.33 | +0.04 |
| 99% target (96%), 60×, 18.5 kb | 96.1% | +3.06 | +3.34 | +0.28 | 0.00 |

greedy similarity vs GNNome: unpolished better in **9/9 settings** (exact sign p = 0.004; mixed +0.65 pp [0.39, 0.91], p < 10⁻⁶;
27/27 replicates); copies cleaner reads in 9/9 settings (mixed −0.50 pp source-read error); polished no difference
(better in 5/9 settings, mixed −0.05 [−0.27, +0.16] errors/100 kbp, p = 0.62). greedy sim+len is *worse* than GNNome
(1/9 settings). **Run 1R:** greedy similarity 99.864% vs GNNome 99.828% unpolished (§3.11). **Real reads:** 93.61% vs
93.02% (§3.10).

New text:
```latex
\subsection{A Greedy Walk on Raw Overlap Features}\label{sec:greedy}
To test whether the learned network is needed, we replaced its edge scores with simple functions of the two raw edge inputs and kept GNNome's decoder unchanged. Ranking edges by overlap length alone reproduced Raven's error rate (2{,}472 mismatches and 7{,}720 indels per 100~kbp in Run~2, 64 local misassemblies); ranking by overlap similarity alone beat pretrained GNNome (2{,}177 vs.\ 2{,}279 mismatches and 7{,}278 vs.\ 7{,}438 indels per 100~kbp; 8 vs.\ 19 local misassemblies, or 3 with twin lengths), copying 298 reads with 12.1\% length-weighted error against GNNome's 555 reads at 12.6\%; and the sum of standardized similarity and length fell between Raven and GNNome on QUAST error rates. Across 27 replicates, the similarity-ranked greedy walk was more accurate than GNNome before polishing in all 9 settings (mixed model $+0.65$~pp, 95\% CI $[0.39, 0.91]$) and indistinguishable after polishing; it also beat GNNome on the accurate Run~1R reads (99.864\% vs.\ 99.828\%) and on real nanopore reads (93.61\% vs.\ 93.02\%). GNNome's unpolished advantage on this genome is therefore reproduced without a neural network.
```
Discussion line 363: replace "GNNome's gain came instead from choosing among true overlaps, which is a read-quality decision." with "GNNome's gain came instead from choosing among true overlaps by overlap similarity, a read-quality decision that a feature-only greedy walk reproduces (Section~\ref{sec:greedy})."

### 3.10 New section — Real ONT reads (SRR31302084)

Data: ENA/SRA SRR31302084 (BioProject PRJNA1184340, BioSample SAMN44668295), ONT MinION, 81,605 reads,
487,533,667 bases (~106×), md5 `216907753a01fda1bb9bb163b39e573e` verified. Identical pipeline (`assemble_all.sh`);
read truth from minimap2 `map-ont` primary alignments to CP017100.1 (`paf_truth.py`), so a handful of true
strain differences count as read errors. Read identity (76,513 aligned reads): mean 87.74%, median 92.49%, aggregate 89.66%, p10 66.7%, p90 95.1%.

Run 2 read set (recomputed truth): 14,874 reads, mean per-read identity 85.995%, aggregate 86.010% (the manuscript's "86.01% mean" is the aggregate; per-read mean is 86.00%), median 87.10%, error shares 6.0 : 55.0 : 39.0 (sub : ins : del) — matches line 126.

| Assembly | Unpolished mm / indel per 100 kbp (m80) | Local mis. | Racon×2 mm / indel | Racon×2 local | GF (Racon×2) |
|---|---|---|---|---|---|
| Raven | 2,306.6 / 3,147.3 | 42 | 61.6 / 168.0 | 4 | 99.972 |
| GNNome | 2,084.7 / 2,934.0 | 48 | 80.4 / 201.1 | 9 | 99.965 |
| GNNome twin | 2,102.0 / 2,947.4 | 31 | 103.1 / 227.2 | 7 | 99.986 |
| greedy similarity | 1,964.9 / 2,807.7 | 43 | 84.0 / 205.5 | 6 | 99.975 |
| greedy sim+len twin | 2,220.3 / 3,066.1 | 38 | 69.3 / 177.9 | 3 | 99.994 |

Extensive misassemblies: Raven 2, GNNome 4, GNNome twin 4, greedy sim+len twin 2 unpolished; 4 each after polishing
All polished assemblies have the **same 4 extensive misassemblies at the same two sites**: a 1.77 kb segment at CP017100.1
1,105,558–1,107,331 assembled inverted (QUAST counts 2 inversions), and an extra ~1.19 kb copy of the IS element at
277,193–278,386 inserted at 1,925,575 (2 relocations). Every assembler and variant reports them identically, so they are
differences between the sequenced isolate and the NEB 5-alpha reference (an invertible segment and a new IS insertion),
not assembly errors.

Read selection on real reads (`results/real/trace/collect.json`; unpolished identity, minimap2 asm20):
Raven 92.82% (666 source reads, 8.26% weighted error); GNNome 93.02% (517 reads, 7.69%); GNNome twin 93.35%;
greedy similarity 93.61% (296 reads, 7.48%); greedy similarity twin **93.76%**.

Interpretation: the simulated-read pattern holds on real reads — GNNome is more accurate unpolished (−10% mismatches,
−7% indels) and **less** accurate after polishing (+31% mismatches, +20% indels vs Raven).

### 3.11 Run 1R — regenerated accurate reads

The Run 1 PBSIM3 build and command were not recovered. The current PBSIM3 (`35ce0de`) has two bugs that block HiFi
simulation: (1) a heap-buffer-overflow at `pbsim.cpp:725` (output-name buffers allocated `strlen(prefix)+10` for
`"%s_%04ld.maf.gz"`), fixed by enlarging the buffers (`pbsim_fixed`); (2) an out-of-range index in
`simulate_by_qshmm` (`prob2len`) when `--length-mean/--length-sd` are combined with `--pass-num`, avoided by using
`--strategy templ` with self-generated, seeded templates. The ~96% cap reported in the manuscript is not a build
defect: in single-pass mode PBSIM3 draws per-read accuracy from 0.75–1.05 × the mean and caps at 100%, so
high-accuracy reads require multi-pass simulation plus `ccs`.

Run 1R command log: `revision/results/run1r/command.log` — seeded templates (seed 20261115, Normal(18,500, 2,200) bp
truncated ≥ 1 kb, 60×; 14,876 templates, 275,026,307 bp) → `pbsim --strategy templ --method qshmm
--qshmm QSHMM-RSII.model --pass-num 10 --seed 20261115` → `ccs --min-passes 3 --min-rq 0.99`.

**Run 1R reads** (`results/run1r/trace/truth.summary.json`, truth from minimap2 `map-hifi` → `paf2maf.py`):
14,747 CCS reads (14,876 ZMWs, 99.13% pass), 59.5×, length 18,499 ± 2,197 bp, mean per-read identity **99.72%**
(median 99.82%; Run 1: 99.84% / 99.93%), error shares 5 : 60 : 35 (sub : ins : del). Graph: 3,157 segments, 44,319 links
(6,314 nodes, 88,638 edges, 14.0 edges/node; Run 1: 12.9); 88,564 true, 62 containment, 12 spurious edges.
GUARD 1 200/200; GUARD 2 MATCH for all 6 GNNome/greedy runs.

| Assembly | Unpolished identity | Mismatches / indels per 100 kbp (unpolished) | Misassemb. (local) | Indels > 5 bp | Source reads | Median piece | Weighted read error | Worst-decile reads | Racon×2 mm / indel |
|---|---|---|---|---|---|---|---|---|---|
| Raven | 99.701% | 9.51 / 266.23 | 0 (1) | 2 | 2,052 | 2.0 kb | 0.278% | 177 | 0.00 / 0.02 |
| GNNome | 99.828% | 1.07 / 154.13 | 0 (0) | **56** | 429 | 10.8 kb | 0.152% | 1 | 0.00 / 0.02 |
| GNNome twin | 99.846% | 1.11 / 151.44 | 0 (0) | **0** | 430 | 10.7 kb | 0.150% | 1 | 0.00 / 0.02 |
| greedy similarity | **99.864%** | **0.94 / 126.98** | 0 (0) | — | 385 | 12.2 kb | **0.126%** | 2 | 0.00 / 0.02 |
| greedy similarity, twin | 99.859% | 1.53 / 138.30 | 0 (0) | — | 386 | 13.0 kb | 0.135% | 2 | 0.00 / 0.04 |
| greedy sim+len | 99.671% | 2.40 / 189.59 | 0 (0) | — | 2,293 | 1.7 kb | 0.168% | 6 | 0.00 / 0.02 |
| greedy sim+len, twin | 99.816% | 2.64 / 179.02 | 0 (0) | — | 2,334 | 1.6 kb | 0.184% | 9 | 0.00 / 0.04 |

Genome fraction 99.953% for every assembly polished and unpolished (Raven unpolished 99.944%).

**Does the Run 1 headline reproduce?** Partly. GNNome vs Raven unpolished: indels **−42%** (Run 1: −41%) — reproduces;
mismatches **−89%** (Run 1: −44%) — same direction, larger, on very small counts (49 vs 436 mismatch events genome-wide).
After Racon×2 the two assemblies are again indistinguishable (0.00 mismatches, 0.02 indels per 100 kbp each), as in Run 1.

Read selection explains the errors (Table 7 replacement, Run 1R; predicted = Σ contribution × source-read error; observed
= QUAST-traced mismatch + indel events):

| Assembly | Reads used | Median piece | Weighted read error | Predicted / observed | Difference |
|---|---|---|---|---|---|
| Raven | 2,052 | 2.0 kb | 0.278% | 12,761 / 12,639 | −1.0% |
| GNNome | 429 | 10.8 kb | 0.152% | 6,960 / 7,114 | +2.2% |
| GNNome twin | 430 | 10.7 kb | 0.150% | 6,881 / 6,993 | +1.6% |
| greedy similarity | 385 | 12.2 kb | 0.126% | 5,781 / 5,863 | +1.4% |

Only 1 of GNNome's 429 reads comes from the worst decile of all reads (43 expected by chance); Raven uses 177.

Why-cleaner chain, Run 1R (`trace/why_cleaner.json`, `why_cleaner_ablation.json`): ρ(similarity, true pair error) = −0.875;
ρ(logit, similarity) = +0.631; ρ(logit, overlap length) = +0.438; cleaner next read taken at **380/427 = 89.0%** of walk steps
with true alternatives (two-sided Wilcoxon signed-rank on the paired error difference, p = 3.6 × 10⁻⁵⁶); chosen edge had the
higher similarity in 91.1% and the longer overlap in 52.9% of steps. Ablation (6,310 nodes): top edge cleaner than mean
alternative 87.8% → 67.5%; cleanest 12.8% → 7.0% (chance 7.5%). Model re-run reproduces saved logits to 5 × 10⁻⁶.
Median predicted probability of a true edge: 0.76 (Run 1: 0.93). AUROC true vs spurious 0.918 (12 spurious edges);
true vs all non-true 0.598. No false edge scored above the best true sibling.

Junctions (`trace/run1r_gnnome.junctions.summary.json`): 428 walk junctions; predicted cut error equals observed net indel at
357/428 (Run 1: 370/394); |cut error| > 5 bp at 56 junctions, of which 46 match the observed indel; Pearson r = 0.995
(Run 1: 0.998). **The 56 indels > 5 bp in GNNome's assembly all disappear with twin lengths (56 → 0).**

---

## 4. Methods sections

**Line 126** (Datasets). Replace "DH5$\alpha$ reference" with "NEB 5-alpha reference (CP017100.1, \emph{E.\ coli} K-12 NEB 5-alpha, a DH5$\alpha$ \emph{fhuA2} derivative)". Replace the last two sentences about Run 1 with:
```latex
The PBSIM3 build and command used for the original Run~1 could not be recovered, so Run~1 was regenerated as Run~1R from a logged command (Section~\ref{sec:run1r}): seeded templates (18.5$\pm$2.2~kb, 60$\times$), ten-pass QSHMM-RSII subreads and consensus calling with \texttt{ccs} (\texttt{--min-passes 3 --min-rq 0.99}). Run~1 numbers are kept for comparison and marked as not reproducible. Real ONT reads of DH5$\alpha$ (SRR31302084, $\sim$106$\times$) were also assembled.
```
**Line 67.** "Its genome (CP017100.1, 4{,}583{,}637~bp)" → "A complete genome of its derivative NEB 5-alpha (CP017100.1, 4{,}583{,}637~bp)".

**Line 137.** Remove "The Run~1 Raven and GNNome commands were reconstructed rather than logged;" → "Run~1R commands are logged verbatim;". Add: "Raven was additionally built with a patch that exports both directional overlap lengths in a side file (the graph file is unchanged)."

**Line 140** (Evaluation). Add after the Wilcoxon sentence:
```latex
Replicate comparisons are tested at the setting level (one mean per setting; exact sign test and exact Wilcoxon signed-rank test, $n$ = number of settings) and with a linear mixed model with a random intercept per setting; replicate-level tests are reported only descriptively. Every reported proportion gives $k/n$ and names its test.
```

**Line 144** (Replicates). Replace with:
```latex
Twenty-seven replicates (9 settings $\times$ 3 seeds) varied read accuracy (85--99\% target; the 99\% target yields 96\% mean identity in single-pass simulation), depth (30$\times$, 60$\times$) and read length (9, 18.5~kb), each through the identical pipeline; the first setting uses the Run~2 settings. Two settings separate depth from length (99\%, 60$\times$, 9~kb and 99\%, 30$\times$, 18.5~kb). Seeds within a setting are not independent tests of the setting, so inference uses settings as units.
```

**Line 148** (Environment). Replace with:
```latex
All runs used an Intel Core i5-12450HX (4 performance + 4 efficiency cores, 12 threads, up to 4.4~GHz) with 16~GB DDR5-4800 RAM. All stages ran on the CPU (PyTorch CPU build).
```
**Table 2, line 158.** commit → `ac827c2` with footnote: "The commit recorded originally (418c7d3) is not available from the upstream repository; upstream \texttt{ac827c2} reproduces the Run~2 assembly byte for byte." **Line 159.** `PyTorch 1.9.0+cu111, DGL-cu111 0.8.1` → `PyTorch 1.9.0 (CPU), DGL 0.8.1`. **Line 161.** "Run~1: build and command not recovered" → "Run~1R: \texttt{35ce0de} with two buffer fixes, template mode + ccs 6.4.0".

---

## 5. Statistics

All values from `revision/scripts/analysis/stats_audit.py` → `revision/results/stats_audit/*.json`.

### 5.1 "85% of 393, p = 6e-35" (Table 8 `tab:why`, lines 311–312) — reviewer is incorrect
The reviewer assumed a binomial test on 85%. The value is **333/393 = 84.7%** and the p-value is a **two-sided
Wilcoxon signed-rank test on the paired per-step error difference** (taken read minus alternatives; normal approximation),
p = 5.66 × 10⁻³⁵. Run 1R (logged, regenerated): 380/427 = 89.0%, p = 3.6 × 10⁻⁵⁶. Run 2: 396/524 = 75.6%, p = 2.32 × 10⁻³⁴. The p-values are therefore consistent. Fix: name the test and give k/n.
```latex
Walk steps with true alternatives where the cleaner next read was taken & 333/393 (84.7\%) & 396/524 (75.6\%) \\
\quad Wilcoxon signed-rank $p$ (paired error difference) & $5.7\times10^{-35}$ & $2.3\times10^{-34}$ \\
```
**Run 2 recomputed from scratch** (`results/run2/trace/why_cleaner.json`, `why_cleaner_ablation.json`): ρ(similarity, true pair error) = −0.947; ρ(logit, similarity) = +0.719; ρ(logit, overlap length) = +0.638; walk steps with true alternatives 524, cleaner taken 396/524 = 75.6%, Wilcoxon p = 2.32 × 10⁻³⁴; ablation (1,439 nodes): cleaner-than-mean 77.1% → 56.1%, cleanest 44.2% → 28.5% (chance 28.3%); re-run model reproduces saved logits to 3.5 × 10⁻⁵. **All Table 5 Run 2 values reproduce.** The chosen edge also had the longer overlap in 90.3% of steps and the higher similarity in 77.3%. Run 1R values: see §3.11.

### 5.2 "8 of 21, p = 0.07" (line 249)
Polished: GNNome better in 8, Raven in 12, 1 tie. Exact sign test (tie excluded): p = 0.50 (the reviewer's 0.38 counts the
tie as a Raven win). The 0.07 was a two-sided Wilcoxon signed-rank (normal approximation) on the error difference, p = 0.067,
**favouring Raven**. Setting level: GNNome better in 3/7 settings, sign p = 1.0, exact Wilcoxon p = 0.297. Mixed model on the
**original stored values**: +0.32 errors/100 kbp for GNNome [−0.05, 0.69], p = 0.086; on the **rerun** of the same 21:
+0.29 [−0.04, +0.62], p = 0.085; on all 27 replicates: +0.24 [−0.02, +0.50], p = 0.075.
new (line 249, last sentence):
```latex
After polishing, GNNome had fewer errors in 3 of 9 settings (exact sign test $p=0.51$; mixed model $+0.24$ errors per 100~kbp, 95\% CI $[-0.02, +0.50]$; 9 of 27 replicates better, 15 worse, 3 tied), so there is no evidence of a polished benefit and the point estimate favours Raven.
```

### 5.3 Pseudo-replication (line 249 "19 of 21 … Wilcoxon p = 1.8e-5"; slope r = 0.95, p = 2e-6)
Original 21 replicates, **as stored in the original repository** (`results/stats_audit/abhiraj_replicates.json`): unpolished identity GNNome better 19/21 (replicate level; the rerun gives 20/21 because `acc085_d30_L9k_s33` changes sign, see below); setting level 7/7, exact sign p = 0.0156;
mixed model +0.96 pp [0.15, 1.77], p = 0.020. Slope: setting-level OLS over the 4 accuracy settings, 0.139 pp per pp,
r = 0.998, **p = 0.0015 (n = 4)**; the manuscript's p = 2 × 10⁻⁶ treats 12 seeds as independent.
Source-read error: cleaner in 21/21 replicates; 7/7 settings, p = 0.0156; mixed −1.49 pp, p = 5 × 10⁻⁶.
**Rerun (original 21):** 41 of the 42 per-replicate unpolished identities reproduce the original table exactly; the
exception is the GNNome walk of `acc085_d30_L9k_s33` (the replicate with the 20 bp backward step), which takes one more
read (550 vs 549) and is 0.17 pp more accurate. The Raven graph and contig are identical, so this is a near-tie in edge
scores resolved differently by the CPU build of PyTorch used here (the original used the cu111 build on CPU). It moves
that setting's mean from +0.02 to +0.08 pp. Rerun statistics, original design (7 settings): unpolished 7/7 settings
(p = 0.016; mixed +0.97 pp [0.17, 1.77], p = 0.018); polished GNNome better 3/7 (p = 1.0; mixed +0.29 [−0.04, +0.62],
p = 0.085); source reads cleaner 7/7 (mixed −1.51 pp). **Full design (9 settings, 27 replicates):** unpolished 9/9
(p = 0.0039; mixed +1.31 pp [0.54, 2.07], p = 0.0009; 26/27 replicates); polished 3/9 (p = 0.51; mixed +0.24
[−0.02, +0.50], p = 0.075); source reads cleaner 9/9 (mixed −1.78 pp [−2.39, −1.16]). Slope (accuracy series, n = 4
setting means): 0.133 pp per pp, r = 0.998, p = 0.002.

**Depth vs length** (99% target, 96% reads; GNNome − Raven, pp): 30×/9 kb +1.47; 60×/9 kb +1.99; 30×/18.5 kb +2.99;
60×/18.5 kb +3.06. Read length drives most of the gain at 30× (+1.52 pp from 9 → 18.5 kb vs +0.52 pp from 30 → 60× at
9 kb), and depth adds little once reads are long (+0.08 pp). The manuscript's "+3.06 pp with accurate, deep, long reads"
(line 249) and "grows … with depth" (line 361) should attribute the effect mainly to read length. GNNome's own unpolished
identity at 60×/18.5 kb is 99.49% (manuscript Table 4: 99.49%) — confirmed.
new (line 249):
```latex
Unpolished, GNNome was more accurate in 9 of 9 settings (exact sign test $p=0.004$; mixed model $+1.31$~pp, 95\% CI $[0.54, 2.07]$), and its advantage grows with read accuracy by 0.13~pp of assembly identity per pp of read identity (setting means, $n=4$; $r=0.998$, $p=0.002$) and with read length (Table~\ref{tab:replicates}).
```
Line 276: "in all 21 simulated replicates ($p=9.5\times10^{-7}$)" → "in all 9 settings (exact sign test $p=0.004$)".

### 5.4 Q80 → Q28
99.84% identity ⇒ error 0.0016 ⇒ Q = −10 log₁₀(0.0016) = 28.0. 86.01% ⇒ Q 8.5. "Q80" does not occur in `main_v7_original.tex` or in any script or document of the original repository; it appears only in the review. If a figure or slide outside the repo uses it, replace with Q28 (Run 1), Q25.6 (Run 1R, 99.72%) or Q8.5 (Run 2).

### 5.5 "99%" condition label
Single-pass PBSIM3 at 99% target gives 96.05% aggregate identity (96.13% per-read mean). Table 6 (`tab:replicates`) rows (lines 263, 266) relabel "99\%$^{*}$" → "96\%$^{*}$ (99\% target)".

---

### 5.6 Table 6 (`tab:replicates`) replacement (lines 251–272)

Replace the tabular body and caption with (per-read mean identity from simulation truth; values differ from the
manuscript's read-identity column by 0.03–0.09 pp because that column used aggregate identity):
```latex
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}lrrrrrr}
\toprule
\shortstack[l]{Target accuracy,\\depth, length} & \shortstack[r]{Read\\identity\\(\%)} & \shortstack[r]{Unpolished\\identity (\%),\\Raven\\$\rightarrow$ GNNome} & \shortstack[r]{$\Delta$\\(pp)} & \shortstack[r]{GNNome\\better} & \shortstack[r]{Greedy\\(similarity)\\unpolished (\%)} & \shortstack[r]{Polished\\errors per\\100 kbp,\\Raven / GNNome} \\
\midrule
85\%, 30$\times$, 9 kb$^{\dagger}$ & 85.98 & 88.15$\,\rightarrow\,$88.23 & +0.08 & 3/3 & 88.94 & 29.72 / 30.57 \\
85\%, 60$\times$, 9 kb & 85.99 & 88.00$\,\rightarrow\,$88.19 & +0.19 & 3/3 & 89.10 & 11.54 / 12.08 \\
85\%, 30$\times$, 18.5 kb & 86.11 & 87.99$\,\rightarrow\,$88.06 & +0.07 & 2/3 & 89.58 & 30.07 / 30.83 \\
90\%, 30$\times$, 9 kb & 90.49 & 91.29$\,\rightarrow\,$91.95 & +0.65 & 3/3 & 92.78 & 3.63 / 3.91 \\
95\%, 30$\times$, 9 kb & 95.17 & 95.33$\,\rightarrow\,$96.58 & +1.25 & 3/3 & 97.15 & 0.30 / 0.27 \\
96\%$^{*}$, 30$\times$, 9 kb & 96.13 & 96.38$\,\rightarrow\,$97.84 & +1.47 & 3/3 & 98.25 & 0.49 / 0.14 \\
96\%$^{*}$, 60$\times$, 9 kb & 96.14 & 96.39$\,\rightarrow\,$98.38 & +1.99 & 3/3 & 98.69 & 0.46 / 0.53 \\
96\%$^{*}$, 30$\times$, 18.5 kb & 96.13 & 96.31$\,\rightarrow\,$99.30 & +2.99 & 3/3 & 99.63 & 0.20 / 0.24 \\
96\%$^{*}$, 60$\times$, 18.5 kb & 96.14 & 96.42$\,\rightarrow\,$99.49 & +3.06 & 3/3 & 99.77 & 0.47 / 0.47 \\
\bottomrule
\end{tabular*}
\caption{Controlled evaluations: 9 settings $\times$ 3 seeds (27 replicates). Inference uses settings as units: GNNome is more accurate unpolished in 9/9 settings (exact sign test $p=0.004$) but not after polishing (3/9, $p=0.51$); the greedy walk on raw overlap similarity is more accurate than GNNome unpolished in 9/9 settings. $^{*}$99\% target; single-pass PBSIM3 yields 96\% mean identity. $^{\dagger}$Run~2 settings. The two Run~1 subsamples are replaced by Run~1R (Section~\ref{sec:run1r}).}
```

## 6. Count discrepancies

| Item | Finding | Fix |
|---|---|---|
| Raven large indels: text 3 (line 345) vs Fig. "Raven large (4)" | 3 indels >5 bp (393 bp at 591,774; 121 bp at 2,468,405; 100 bp at 4,266,383). The figure (Fig. 6e in the plotting script, not 5b) counts 3 indels + 1 breakpoint, double-counting the 393 bp collapse. | Figure label → "Raven large indels (3)"; regenerated. |
| Breakpoints 22 vs 21 | Recomputed (`results/run2/trace/bp_*.tsv`, merge within 2 kb). GNNome: 59 raw rows (19 QUAST local + 6 minimap2 local + 13 minimap2 no-local-join + 21 nucmer). **Without nucmer the rows merge to 22; with nucmer, 27.** So the manuscript's "22 breakpoints (QUAST, minimap2 and nucmer combined)" in fact excludes nucmer. The 5 nucmer-only sites (544,265; 548,494; 993,933; 2,153,797; 3,805,161) include one near 993.9 kb that nucmer also reports in Raven and in GNNome-twin, i.e. a reference/alignment feature, not an assembly error. "21" is the count of true walk edges among the 22 junction classes (21 true + 1 containment). Raven: 19 without nucmer, 21 with. GNNome with twin lengths: **6** without nucmer, 7 with. | Line 345: "The wider set of 22 breakpoints (QUAST and minimap2 combined; nucmer adds five low-support sites, one of which it also reports in Raven's assembly) …". Add the twin result (22 → 6). |
| "twin" label in breakpoint table | no generating code | Classification regenerated by `revision/scripts/analysis/breakpoints.py` + `junction_check.py`. |
| Table 7 counts (predicted / observed: Raven 8,150 / 7,920; GNNome 4,772 / 4,555; Run 1) | no committed script wrote them | Recomputed by `collect.py` on Run 1R: GNNome 6,960 / 7,114, Raven 12,761 / 12,639 (within 1–2%); Run 1 values marked non-reproducible. |
| 36 vs 35 indels > 5 bp (Run 1, not reproducible) | Run 1: 36 = junctions with |predicted cut error| > 5 bp (30 of 36 match an observed indel); 35 = QUAST indel events > 5 bp, all within 50 bp of a junction (binomial, expected 0.304, p = 7.2 × 10⁻⁷³). **Run 1R (committed):** 56 junctions with |cut error| > 5 bp, 46/56 match the observed indel; 56 indel events > 5 bp, 56/56 within 50 bp of a junction (`results/run1r/trace/run1r_gnnome.{summary,junctions.summary}.json`). | Text uses Run 1R values and states both definitions. |
| 394 junctions vs 393 walk edges (Run 1, not reproducible) | Run 1: 395 walk reads → 394 junctions; 393 have a true alternative (206 + 187 split not stored). **Run 1R:** 429 walk reads → 428 junctions; 427 walk steps have a true alternative. | Use Run 1R values; footnote the definitions. |
| Stored statistics used 23 replicates | 21-replicate numbers were never stored | Recomputed; stored in `stats_audit/abhiraj_replicates.json`. |

---

## 7. Claims about the GNNome paper (line 65) — checked against the published paper

Source: Vrček et al., *Genome Res.* 2025;35(4):839–849 (PMC12047240); compared with bioRxiv preprint v1 (10.1101/2024.03.11.584353).
- QV vs Hifiasm (Table 1): CHM13 54.24 vs 55.86; mouse 45.40 vs 45.67; *A. thaliana* 52.08 vs 44.52; chicken 49.35 vs 51.08 → lower on 3 of 4. **Correct**; the mouse value is in Table 1, not the text.
- ONT misassemblies: CHM13 1,758 (Raven 1,146, Flye 134, Shasta 57); *A. thaliana* 242 (95 / 7 / 16) → more on **both** ONT genomes. **Correct.** The "only one of two" wording exists only in preprint v1.

Change (line 65): add table citations — "...higher on one (Table~1 of~\cite{gnnome}), and on ONT data it has more misassemblies than heuristic assemblers on both evaluated genomes (Table~2 of~\cite{gnnome})." HiFi QV is Table 1 and ONT results (including structural misassemblies) are Table 2 of the published paper. If the preprint is what `refs.bib` cites, change the entry to the published version.

---

## 8. References (refs.bib)

| Ref | Fix |
|---|---|
| 2 | issue 27(5) |
| 4 | volume 18(2), title and DOI corrected |
| 5 | volume 48 |
| 7 | article number 1495657 |
| 8 | LNCS volume 16569 (confirmed) |
| 12 | 47(21):10994–11006 |
| 14 | title "Graph-based self-supervised learning for repeat detection in metagenomic assembly" |
| 16 | title "De novo Nanopore read quality improvement using deep learning" |
| 17 | GigaScience 2026; 15:giag048; author list corrected |
| New | SRR31302084 / PRJNA1184340 data citation; CP017100.1 NEB 5-alpha record |

Full fact-check table with quotes and URLs: `revision/results/factcheck.md`.

---

## 9. Responses to reviewer points where no change was made

1. **Run 1 p-value** — consistent once the test is named (§5.1).
2. **Sign test 0.38** — ignores the tie; correct exact value is 0.50 (§5.2).
3. **GNNome-paper claims** — correct for the published paper (§7).

---

## 10. Files

```
revision/
  REVISION.md                      this file
  manuscript/main_v7_original.tex  unmodified source used for line numbers
  patches/                         raven_twin, GNNome_twin, pbsim_fixed diffs
  scripts/pipeline/                assemble_all.sh, gnnome_run.sh, raw_scores.py, replicate.sh, trace_run.sh, guards
  scripts/analysis/                truth, collect, stats, breakpoint scripts
  results/                         run2, run1r, real, stale_k12, replicates, stats_audit (JSON/TSV + sha256)
```

---

## 11. Answers to the co-author checklist

**1. Run 1 provenance.** Cannot be recovered. The original evidence report (`docs/run1_run2_evidence_report.md`,
`docs/GNNome_DH5alpha_results_update.md` in the original repo) records that Run 1 was simulated with a different PBSIM3
build from the one on disk (5,224 reverse-strand MAF start shifts absent from Run 2; identity 99.84% vs the on-disk
build's ~96% single-pass cap) and that its command and seed were never logged; the Raven and GNNome commands were
reconstructed. The Run 1 reads (`CP017100_sim.fastq`, SHA `5d3b823e…`, 14,884 reads) and graph (`b12099…0270`) exist
only on the original machine. The 44%/41% headline therefore cannot be regenerated. Replacement: **Run 1R**, simulated
from a logged command with the current PBSIM3 (two bug fixes, `patches/pbsim3_buffers.diff`), multi-pass + `ccs`; exact
commands in `results/run1r/command.log` (simulation) and `results/run1r/pipeline.log` (Raven: `raven -t 12 -p0 reads`;
GNNome: `create_inference_graphs.py` + `inference.py` via `scripts/pipeline/gnnome_run.sh`, model `weights.pt` SHA
`240076f0…40ff`). Run 1R results replace Run 1 in the abstract (§3.11).

**2. Replicates: 21 or 27?** Both, deliberately. The manuscript design is **21 = 7 settings × 3 seeds (11, 22, 33)**.
The revision reran those 21 from scratch and added **6 = 2 settings × 3 seeds** that separate depth from length
(99% target, 60×, 9 kb and 99% target, 30×, 18.5 kb), giving 27 = 9 × 3. All 27 are complete and committed under
`results/replicates/<setting>_s<seed>/` (QUAST for every variant unpolished and Racon×2, guards, hashes, `trace/collect.json`).
Statistics are reported for the original 21/7 (audit of the manuscript) and for 27/9 (revised analysis), always at the
setting level, with the mixed model on all replicates.

**3. Inversion check.** Committed: `results/stale_k12/nucmer/{all.coords,1to1.coords,inversion_check.tsv,inversion_check.summary.txt,inversion_check.png,inversion_check.pdf}`;
plot source `scripts/figures/inversion_check.py`. Result: 3 reverse-strand 1-to-1 blocks (770–1,204 bp, repeat copies);
the all-alignments panel shows the repeat-copy matches that were mistaken for an inversion.

**4. GNNome commit.** `ac827c2b2cca3086654183777eec6ae143e90a97` (upstream `lbcb-sci/GNNome` HEAD). The originally
recorded `418c7d30e9bd2e4dcf521deebf42a5ba07836c9f` is not fetchable from upstream ("not our ref") and is in no
upstream branch. With `ac827c2` the Run 2 GNNome contig reproduces byte for byte (`fa049876…`).

**5. Stale graph in baselines / NOTES.md.** No baseline used the stale graph: 30/30 graphs pass GUARD 1 (200/200
segments from that run's own reads: Run 2, Run 1R, real reads, 27 replicates), 181/181 GNNome/greedy runs pass GUARD 2 (27 × 6 + 7 + 6 + 6), no run shares a graph hash and none equals
the stale `62176d9d…`. `development-team2/NOTES.md` is not in any repository we can reach (original repo, sammyyakk/genome-sequencing
branches main/team1/team2, all forks), so it cannot be edited from here; the correction text to paste is in
`notes/NOTES_stale_graph_correction.md`.
