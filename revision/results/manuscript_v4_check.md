# Check of the revised manuscript (v4 PDF, 15 pages) against the committed results

Checked: `Evaluating_a_Pretrained_Graph_Neural_Network_Assembler_on_E_coli__4_.pdf` (2026-11-15). Every number in the
abstract, Sections 2–4, Tables 1–4, Fig. 1 and the Fig. 5 caption that comes from the revision runs was compared with
`results/{run1r,run2,real}/quast/*/report.tsv`, `results/*/trace/*.json`, `results/replicates/rep_stats.json`,
`results/run2/twin_counts.txt` and `results/stale_k12/`. Values that come from the original (non-reproducible) Run 1,
the K-12 control, the window analysis and the repeat analysis were carried over from the original manuscript and were
not recomputed.

## Result

Everything matches except two small points in the manuscript. A third point was an error in this repository; the
manuscript had it right.

| # | Where | Manuscript says | Committed result | Fix |
|---|---|---|---|---|
| 1 | §3.8, Run 2 local misassemblies | "13 to twin-edge walk junctions (cut errors of 197–342 bp)" | The 13 QUAST local misassemblies that sit on walk junctions have \|cut error\| **203–342 bp** (284, 228, 306, 237, 220, 267, 342, 317, 203, 270, 213, 255, 249; `run2/trace/run2_gnnome.junctions.tsv`). The 197 bp junction (S1_8523→S1_4094, 570,153) is a minimap2-only breakpoint, not one of QUAST's 19. | "cut errors of 203–342 bp" |
| 2 | §3.2, polished mixed model | "p = 0.075" | p = 0.0745 (`rep_stats.json`, full_9x3 gnnome−raven d_pol), which rounds to **0.074** | "p = 0.074" (or "p = 0.07") |
| 3 | Repository, not manuscript | Manuscript: polished fewer errors in **2 of 9 settings, 1 tie, sign p = 0.29** | Older `rep_stats.json` / REVISION.md said 3/9, p = 0.51. Setting `acc099_d60_L18k` is an exact tie (Raven 0.46+0.48+0.46, GNNome 0.44+0.59+0.37, both 1.40/3), but float residue made the difference −1e-16, so it was counted as a GNNome win. **The manuscript is correct.** | Fixed: `rep_stats.py` rounds differences before the sign and Wilcoxon tests, and its Wilcoxon stays exact when there are ties. `rep_stats.json` and REVISION.md §5.2/§5.3, the abstract and the Table 6 caption were updated. Original 7-setting design: 2/7 better, 1 tie, sign p = 0.69, exact Wilcoxon p = 0.22 (was 3/7, p = 1.0, 0.297). Full design: exact Wilcoxon p = 0.11 (was 0.13). No other comparison changed. |

## Verified (all match)

- **Abstract:** 89% / 42% (Run 1R); 9/9 settings, 26/27 replicates, p = 0.004; +0.08 pp at ~86%; real reads 10% fewer mismatches (2,085 vs 2,307) and 7% fewer indels (2,934 vs 3,147); ρ ≈ −0.9 (−0.88, −0.95); greedy +0.65 pp in 9/9 settings; 56 indels > 5 bp removed; polished 2/9 settings.
- **Fig. 1 and §2.2–2.3:** Run 1R 14,747 reads, 59.5×, 18.5 ± 2.2 kb, 99.72% (Q25.6); Run 2 14,874 reads, 86.01% (Q8.5), seed 1783636376; real 81,605 reads, 487.5 Mb (~106×), 76,513 aligned, mean 87.7%, median 92.5%; graphs 3,157/44,319 (6,314/88,638, 14.0 per node, 93% transitive), 762/2,968 (1,524/5,936, 3.9, 74%), 829/4,307 (1,658/8,614, 5.2); guards 30/30 and 181/181.
- **Table 1 and Table 4:** every Run 1R, Run 2 and real-read value (mismatches, indels, extensive and local misassemblies, genome fraction, Racon ×2) matches QUAST. Source reads and read error also match: Run 1R 2,052/0.278, 429/0.152, 430/0.150, 385/0.126; Run 2 654/13.51, 555/12.61, 558/12.89, 754/13.54, 298/12.14, 303/12.20, 587/13.03; real 666/8.26, 517/7.69, 513/7.76, 296/7.48.
- **Table 2:** all read identities, Raven→GNNome identities, Δ, per-setting win counts, greedy identities and polished errors match the setting means.
- **§3.2 statistics:** mixed +1.31 pp [0.54, 2.07]; slope 0.13 pp per pp, r = 0.998; depth vs length +1.47 / +1.99 / +2.99 / +3.06; polished 9 / 15 / 3 replicates, +0.24 [−0.02, +0.50]; 29.4 vs 30.6 vs 36.3.
- **§3.3:** 429 reads, 10.8 kb, 0.152%; 2,052 reads, 2.0 kb, 0.278%; expected 6,960 / 12,761 vs observed 7,114 / 12,639; worst-decile reads 1 (43 expected) vs 177; Run 2 source-read error 27/27 replicates, mixed −1.78 pp [−2.39, −1.16].
- **Table 3 and §3.4:** −0.88 / −0.95; +0.63 / +0.72; 380/427 (89.0%), 396/524 (75.6%); p = 3.6e-56 and 2.3e-34; 87.8/67.5 and 77.1/56.1; 12.8/7.0 (7.5) and 44.2/28.5 (28.3); Run 2 ρ(length) 0.64, 90.3% / 77.3%; Run 1R 52.9% / 91.1%; logits reproduced to < 4e-5 (3.5e-5).
- **§3.5:** greedy vs GNNome Run 1R 0.94/1.07 and 127.0/154.1, identity 99.864 vs 99.828; 27/27 replicates, mixed +0.65 [0.39, 0.91]; simlen better in 1/9 settings; polished −0.05 [−0.27, +0.16]; Racon ranges 0.61–0.94 and 28.7–30.3 (Run 2), 0.00 and 0.02–0.04 (Run 1R); 0.7–1.5 pp vs 0.07–0.19 pp.
- **§3.6:** 88,564 / 62 / 12 and 5,874 / 58 / 4 edges; no spurious walk edge and no spurious edge scored above the best true sibling; AUROC 0.918 / 0.897 and 0.60 / 0.58; median probability 0.76 and 3e-9.
- **§3.8:** twin lengths differ for 2,950/2,968, 40,998/44,319 and 4,272/4,307 edges; 357/428 junctions, r = 0.995, 56 with cut error > 5 bp of which 46 match; 56/56 indels within 50 bp of a junction (0.53 expected); Raven 2 indels > 5 bp; 13 + 6 split of the 19 QUAST local misassemblies, with source-read identities 78.6–84.3%; twin lengths cut local misassemblies 19 to 5, genome fraction 99.792 vs 99.786, breakpoints 22 to 6, identity 99.828% to 99.846%, Run 2 2,350/7,555; replicates 9/9 settings, +0.21 [0.08, 0.35]; polished 7/9, p = 0.18.
- **§3.9:** duplication ratio 1.06 vs 0.985; extensive misassemblies 4 vs 2 unpolished and 4 for every assembly after Racon; polished 80.4/201.1 vs 61.6/168.0; greedy 1,965/2,808; twin local 48 to 31 and polished 103.1/227.2.
- **§3.10 and Fig. 5 caption:** 23 misassemblies (5 local), genome fraction 98.806%, 13.69 / 72.66; the K-12 reference gives the same 23; 31 one-to-one blocks; 3 reverse blocks of 770–1,204 bp (longest 1.2 kb).
