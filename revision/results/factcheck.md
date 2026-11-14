# Fact-check log: GNNome vs Raven on E. coli DH5α manuscript

Checked 2026-11-15. Main sources: NCBI E-utilities (PubMed, PMC, nuccore, SRA), the ENA portal API, the Crossref API, the arXiv API, the bioRxiv API and PDF, and GitHub (pbsim3 source and issues). Verdicts: **OK** (confirmed), **WRONG**, **INCOMPLETE**, **UNVERIFIED**.

---

## Part A: GNNome paper (Vrček et al. 2025, Genome Res 35(4):839–849)

**Sources.** I used the **published version**: the PMC full text, PMC12047240 (PMID 39472021), fetched as JATS XML via `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=PMC12047240&retmode=xml`. The human-readable copies are https://pmc.ncbi.nlm.nih.gov/articles/PMC12047240/ and https://genome.cshlp.org/content/35/4/839.full. I compared it with the bioRxiv preprint v1 (posted 2024-03-13; the only version, per the bioRxiv API) at https://www.biorxiv.org/content/10.1101/2024.03.11.584353v1.full.pdf. **The two versions differ in ways that matter (see A2).**

### A1. QV (Table 1, "Results on HiFi reads", published version)

| Genome | GNNome QV | Hifiasm QV | GNNome vs hifiasm |
|---|---|---|---|
| CHM13 | 54.24 | 55.86 | lower (−1.62) |
| *M. musculus* | **45.40** | **45.67** | lower (−0.27) |
| *A. thaliana* | 52.08 | 44.52 | higher (+7.56) |
| *G. gallus* | 49.35 | 51.08 | lower (−1.73) |

Other mouse QVs in Table 1: HiCanu 43.77, Verkko 45.72. Verkko has the best mouse QV.

Table footnote: "Quality value (QV) is per-base consensus accuracy, computed with yak by comparing k-mers in contigs to k-mers found in short reads (Cheng et al. 2021). Short reads were not available for G. gallus, so we computed QV with PacBio HiFi reads instead."

Text: "In terms of quality, GNNome produces assemblies with slightly lower QV for CHM13 and G. gallus than hifiasm, but with a notably higher QV than assemblies of all the other tools on A. thaliana." The paper's text does not comment on the mouse QV. Table 1 shows that it is lower.

| Claim | Verdict | Quote / data | URL | Corrected text |
|---|---|---|---|---|
| "per-base quality is lower than Hifiasm on three of the four genomes and higher on one" | **OK** | Lower on CHM13 (54.24 vs 55.86), mouse (45.40 vs 45.67) and chicken (49.35 vs 51.08); higher on *A. thaliana* (52.08 vs 44.52), all in Table 1 | PMC12047240 | Optional, more precise wording: "lower than hifiasm on CHM13, *M. musculus* and *G. gallus* (by 0.27–1.73 QV) and higher on *A. thaliana* (52.08 vs 44.52; Table 1)". Note that the chicken QV was computed from HiFi reads, not short reads. |

### A2. ONT evaluation (Table 2, "Results on ONT data")

ONT genomes evaluated: **CHM13 and *A. thaliana* (Col-0) only**, at about 120× coverage. GNNome was run on Raven v1.8.1 graphs and polished with Racon. It was compared with Raven, Flye v2.9.2 and Shasta v0.11.1.

Structural / local misassemblies in Table 2 (published version):

| Genome | GNNome | Raven | Flye | Shasta |
|---|---|---|---|---|
| CHM13 | 1758 / 1695 | 1146 / 952 | 134 / 123 | 57 / 190 |
| *A. thaliana* | 242 / 221 | 95 / 185 | 7 / 16 | 16 / 256 |

Published text: "On CHM13, GNNome again achieved far higher NG50 and NGA50 than any other assembler. However, we notice a gap between NG50 and NGA50, which is also accompanied by a higher number of misassemblies and lower QV. On A. thaliana NG50 and NGA50 are of similar values, and comparable to those achieved by Raven. **The number of complete single-copy genes on A. thaliana is higher than for other tools, but so is the number of misassemblies.**" It continues: "Both of these assemblers [Flye and Shasta] achieve an order of magnitude less misassemblies on both data sets".

The **"not present on A. thaliana" passage appears ONLY in bioRxiv preprint v1**, which had no misassembly columns in its tables: "It is also worth noting that GNNome assembly of CHM13 achieves substantially higher NG50 than NGA50. This indicates missassembly of certain regions, an issue which was not noticed in HiFi assemblies, likely coming from more accurate edge-predictions on HiFi graphs. These misassemblies are also indicated by the QV and the lower amount of complete single-copy genes found. Such behavior is also not present on A. thaliana, where NG50 and NGA50 achieved by GNNome are of similar value, and the number of complete single-copy genes found is higher than for other assemblers." I searched the published full text for "not present" and found no match.

| Claim | Verdict | Quote | URL | Corrected text |
|---|---|---|---|---|
| GNNome showed elevated misassemblies on ONT only for CHM13 (not on *A. thaliana*) | **WRONG per the published version** (true only of preprint v1 wording) | Published: "on A. thaliana ... higher than for other tools, but so is the number of misassemblies"; Table 2 shows 242 structural for GNNome vs 95/7/16 for the other three | PMC12047240 | "On ONT data (CHM13 and *A. thaliana*), GNNome produced more structural misassemblies than Raven, Flye and Shasta on both genomes (Table 2 of Vrček et al. 2025)." If the preprint is cited, cite it as the preprint and note that the published version revised this point. |
| ONT genomes evaluated | OK if stated as CHM13 + *A. thaliana* | "we compare the GNNome's assemblies of CHM13 and Col-0 strain of A. thaliana with Raven's ... The coverage of both samples is roughly 120×" | PMC12047240 | — |

### A3. Training data

Methods quote: "For training, the data were simulated from HG002 draft reference (v0.7) ... and PBSIM3 (Ono et al. 2022). The training set consisted of Chromosomes 1, 3, 5, 9, 12, and 18, while the validation set consisted of Chromosomes 6, 11, 17, 19, and 20." Also: "The chromosomes chosen for training were sampled 15 times each ... each chromosome in the validation set was sampled five times." Reads were simulated at 60× and masked during training to between 25× and 60×. Graphs were built with hifiasm v0.18.7-r514. The acrocentric chromosomes were excluded. **Verdict: OK** (6 training chromosomes: 1, 3, 5, 9, 12, 18; 5 validation chromosomes: 6, 11, 17, 19, 20).

### A4. Model

| Item | Source quote | Verdict |
|---|---|---|
| Layer type | "we devise a novel GNN layer named SymGatedGCN" | OK |
| Layers / hidden dimension | "The model used in this study had latent dimension d = 64, number of GNN layers L = 8, and three layers in the MLP classifier. Node and edge features were first linearly transformed to 16-dimensional tensors and then to the 64-dimensional latent space." | OK: 8 layers, d = 64 |
| Parameters | "This results in roughly 220,000 parameters" | OK: ~220k |
| Edge features | "the node features are only in-degree and out-degree of each node, while the edge features are the length and the similarity of the overlap, thus d_n = d_e = 2. Similarity is computed as overlap similarity = (overlap length − edit distance)/overlap length ... and was obtained with Edlib (Šošić and Šikić 2017)." | OK. The node features (in-degree and out-degree) could also be mentioned. |
| Decoding | "This is done by sampling the starting edges and running a greedy search from them." Forward and backward symmetric greedy walks; "100 starting edges give a good tradeoff"; "The decoding is performed as long as the found contigs are longer than 70 kb." | OK: greedy, 100 seeds, 70 kb contig cutoff |
| Other | Dropout 0.2; METIS partitions of ~50,000 nodes; α = 0.1; Adam, lr 1e-4; trained on one A100 40 GB in ~9 h 15 min; inference on CPU (AMD EPYC 7742); GNNome v0.4.0 | — |

### A5. Bacterial genomes

**None.** The test genomes are CHM13, *M. musculus* C57BL/6J, *A. thaliana* Col-0 and *G. gallus* bGalGal1 (maternal). The paper says: "Since our methodology is optimized for haploid genome assembly, we evaluate GNNome on the homozygous human genome CHM13 ... along with the inbred genomes of Mus musculus ... and Arabidopsis thaliana ... Additionally, we evaluate on the maternal genome of Gallus gallus". The published text contains no "bacteri", "prokaryot" or "coli". The synthetic repeat experiment uses "a short, synthetic genome" (Supplemental Note S1). That genome is not bacterial. **Verdict: a claim that no bacterial genome was evaluated is OK.**

---

## Part B: Strain and read data

### B1. CP017100.1

NCBI nuccore (GenBank flat file): https://www.ncbi.nlm.nih.gov/nuccore/CP017100.1
- `DEFINITION  Escherichia coli strain K-12 NEB 5-alpha chromosome, complete genome.`
- `/strain="K-12 NEB 5-alpha"`. Length 4,583,637 bp, circular. BioProject PRJNA341475, BioSample SAMN05725120. Assembled with HGAP.3/Quiver at 314× coverage (PacBio).
- Reference title: "Complete Genome Sequence of NEB 5-alpha, A Derivative of Escherichia coli K-12 DH5alpha".

Anton BP, Raleigh EA. Genome Announc. 2016 Nov 10;4(6):e01245-16. doi:10.1128/genomeA.01245-16. PMID 27834703, PMCID PMC5105096. Abstract: "Escherichia coli K-12 DH5α is one of the most popular and widely available laboratory strains, but, surprisingly, no complete genome sequence has been publicly available. Here, we report the complete, finished sequence of NEB 5-alpha (DH5α fhuA2). It should serve as a useful reference for researchers working with DH5α." https://pubmed.ncbi.nlm.nih.gov/27834703/

| Claim | Verdict | Corrected text |
|---|---|---|
| CP017100.1 is "E. coli DH5α" | **IMPRECISE**: the record is NEB 5-alpha | "the complete genome of *E. coli* K-12 NEB 5-alpha (a DH5α derivative, DH5α *fhuA2*; GenBank CP017100.1; Anton and Raleigh 2016)" |

### B2. SRR31302084

Sources: the ENA filereport API (`https://www.ebi.ac.uk/ena/portal/api/filereport?accession=SRR31302084&result=read_run&...`) and NCBI SRA runinfo (efetch db=sra).

| Field | Value |
|---|---|
| Organism / strain | *Escherichia coli* (taxid 562) / `DH5alpha` |
| Experiment title (ENA) | "MinION sequencing: WGS of E.coli DH5alpha-MinION sequencing dataset" |
| Platform / model | OXFORD_NANOPORE / MinION |
| Library | WGS, RANDOM, GENOMIC, SINGLE; library name EcoliP03; sample name "Sample P03" |
| Reads (spots) | 81,605 |
| Bases | 487,533,667 (avg length 5,974 bp; NCBI) |
| BioProject / study | PRJNA1184340 / SRP544324 |
| BioSample / sample | SAMN44668295 / SRS23173122; experiment SRX26680259 |
| Submitter | AMRITA VISHWA VIDYAPEETHAM (submission SRA2011970) |
| Dates | NCBI load 2024-11-10, release 2024-12-14; ENA first_public 2024-12-29 |
| ENA FASTQ | `ftp.sra.ebi.ac.uk/vol1/fastq/SRR313/084/SRR31302084/SRR31302084_1.fastq.gz` (https:// or ftp://), **513,696,900 bytes**, md5 `216907753a01fda1bb9bb163b39e573e` |
| NCBI SRA file | https://sra-downloadb.be-md.ncbi.nlm.nih.gov/sos7/sra-pub-run-38/SRR031/31302/SRR31302084/SRR31302084.1 (size_MB 426) |

Coverage check: 487.5 Mb / 4.584 Mb ≈ 106× against CP017100.1 (my calculation).

---

## Part C: References

All metadata come from Crossref (`api.crossref.org/works/<doi>`) unless stated otherwise. PubMed was used for some cross-checks.

| # | Manuscript citation | Verdict | Source data | Corrected full citation |
|---|---|---|---|---|
| 1 | Vaser & Šikić, Raven, Nat Comput Sci 1(5):332–336 (2021) | OK | Crossref: vol 1, iss 5, pp 332–336, 2021 | Vaser R, Šikić M. Time- and memory-efficient genome assembly with Raven. *Nat Comput Sci*. 2021;1(5):332–336. doi:10.1038/s43588-021-00073-4 |
| 2 | Vaser et al., Racon, Genome Res 27:737–746 (2017) | INCOMPLETE (issue missing) | vol 27, iss 5 | Vaser R, Sović I, Nagarajan N, Šikić M. Fast and accurate de novo genome assembly from long uncorrected reads. *Genome Res*. 2017;27(5):737–746. doi:10.1101/gr.214270.116 |
| 3 | GNNome | OK | vol 35, iss 4, pp 839–849; print April 2025 (online 2024-10-29) | Vrček L, Bresson X, Laurent T, Schmitz M, Kawaguchi K, Šikić M. Geometric deep learning framework for de novo genome assembly. *Genome Res*. 2025;35(4):839–849. doi:10.1101/gr.279307.124 |
| 4 | Cheng et al., hifiasm, Nat Methods 18:170–175 (2021) | INCOMPLETE (title, issue, DOI) | vol 18, iss 2 | Cheng H, Concepcion GT, Feng X, Zhang H, Li H. Haplotype-resolved de novo assembly using phased assembly graphs with hifiasm. *Nat Methods*. 2021;18(2):170–175. doi:10.1038/s41592-020-01056-5 |
| 5 | Kumar MS et al., Biotechnology Reports e00931 (2025) | INCOMPLETE: **volume 48** | Crossref: vol 48, art e00931, Dec 2025 | Kumar MS, Krishna MB, Soman K, Stanley J, Pourmand N, Suravajhala P, Babu T. Benchmarking long-read assembly tools and preprocessing strategies for bacterial genomes: A case study on E. coli DH5α. *Biotechnol Rep*. 2025;48:e00931. doi:10.1016/j.btre.2025.e00931 |
| 6 | Vrček, Veličković, Šikić, NeurIPS 2020 LMCA, arXiv:2011.05013 | OK | arXiv API: title "A step towards neural genome assembly"; comment "NeurIPS 2020 Learning Meets Combinatorial Algorithms Workshop. 5 pages, 1 figure"; posted 2020-11-10 | Vrček L, Veličković P, Šikić M. A step towards neural genome assembly. NeurIPS 2020 Learning Meets Combinatorial Algorithms Workshop; 2020. arXiv:2011.05013 |
| 7 | Luo J et al., GTasm, Front Genet 15 (2024) | INCOMPLETE: article no. **1495657** | vol 15, art 1495657, 2024-10-25 | Luo J, Zhang Z, Ma X, Yan C, Luo H. GTasm: a genome assembly method using graph transformers and HiFi reads. *Front Genet*. 2024;15:1495657. doi:10.3389/fgene.2024.1495657 |
| 8 | Schmitz et al., DipGNNome, RECOMB-CG 2026, LNCS 16569, pp 317–338 | OK | Crossref: pp 317–338, book "Comparative Genomics", ed. Lafond M, ISBN 978-3-032-26890-7. Volume 16569 confirmed via a retailer listing (bookswagon.ae: "16569 Lecture Notes in Computer Science"; "23rd RECOMB International Workshop, RECOMB-CG 2026, Thessaloniki, Greece, May 24–25, 2026, Proceedings"). The Springer page was blocked by a login redirect. | Schmitz M, Vrček L, Kawaguchi K, Šikić M. DipGNNome: Diploid de novo genome assembly with geometric deep learning and beam-search. In: Lafond M, ed. *Comparative Genomics. RECOMB-CG 2026*. Lecture Notes in Computer Science, vol 16569. Springer, Cham; 2026:317–338. doi:10.1007/978-3-032-26891-4_15 (preprint: bioRxiv doi:10.1101/2025.09.16.676474) |
| 9 | Edlund & Normark, Nature 292:269–271 (1981) | OK (add issue). **Content caution** | vol 292, iss 5820. Abstract: tandem duplications of *ampC* arising from "recombination between randomly occurring short homologies (12-13-bp long)". **Not about rRNA operons.** | Edlund T, Normark S. Recombination between short DNA homologies causes tandem duplication. *Nature*. 1981;292(5820):269–271. doi:10.1038/292269a0 |
| 10a | Hill CW et al., J Mol Biol 116(3):407–428 (1977) | OK | PubMed 338920 | Hill CW, Grafstrom RH, Harnish BW, Hillman BS. Tandem duplications resulting from recombination between ribosomal RNA genes in Escherichia coli. *J Mol Biol*. 1977;116(3):407–428. doi:10.1016/0022-2836(77)90077-8 |
| 10b | Hill & Harnish 1981, PNAS 78(11):7069–7072, as the inversion citation | OK; suitable | PubMed 6273909 abstract: "we have constructed mutants that have an inversion of the segment between rrnD and either rrnB or rrnE ... A major line of laboratory E. coli, W3110 and its derivatives, also has an inversion between rrnD and rrnE, probably created directly by a recombinational event between these highly homologous genes." | Hill CW, Harnish BW. Inversions between ribosomal RNA genes of Escherichia coli. *Proc Natl Acad Sci USA*. 1981;78(11):7069–7072. doi:10.1073/pnas.78.11.7069 |
| 11 | Maharjan et al., BMC Genomics 14:441 (2013) | OK. **Content caution** | Title: "A case of adaptation through a mutation in a tandem duplication during experimental evolution in Escherichia coli". It describes a 180 kb duplication of the 46′ region; **not an rRNA inversion paper**. | Maharjan RP, Gaffé J, Plucain J, Schliep M, Wang L, Feng L, Tenaillon O, Ferenci T, Schneider D. A case of adaptation through a mutation in a tandem duplication during experimental evolution in Escherichia coli. *BMC Genomics*. 2013;14:441. doi:10.1186/1471-2164-14-441 |
| 12 | Tørresen et al., NAR 47 (2019) | INCOMPLETE: **47(21):10994–11006** | Crossref | Tørresen OK, Star B, Mier P, Andrade-Navarro MA, Bateman A, Jarnot P, Gruca A, Grynberg M, Kajava AV, Promponas VJ, Anisimova M, Jakobsen KS, Linke D. Tandem repeats lead to sequence assembly errors and impose multi-level challenges for genome and protein databases. *Nucleic Acids Res*. 2019;47(21):10994–11006. doi:10.1093/nar/gkz841 |
| 13 | Fertin et al., DExTaR, IEEE BIBM 2014, pp 90–93 | OK | Crossref | Fertin G, Jean G, Radulescu A, Rusu I. DExTaR: Detection of exact tandem repeats based on the de Bruijn graph. In: *2014 IEEE International Conference on Bioinformatics and Biomedicine (BIBM)*; 2014:90–93. doi:10.1109/BIBM.2014.6999134 |
| 14 | Azizpour et al., GraSSRep, Genome Res 34(9):1468–1476 (2024) | Title needs correcting | The Genome Research title has no "GraSSRep" in it: "Graph-based self-supervised learning for repeat detection in metagenomic assembly". The title "GraSSRep: Graph-Based Self-supervised Learning for Repeat Detection in Metagenomic Assembly" belongs to the RECOMB 2024 LNCS short paper (pp 372–376, doi:10.1007/978-1-0716-3989-4_34). | Azizpour A, Balaji A, Treangen TJ, Segarra S. Graph-based self-supervised learning for repeat detection in metagenomic assembly. *Genome Res*. 2024;34(9):1468–1476. doi:10.1101/gr.279136.124 |
| 15 | Kelley & Salzberg, Genome Biol 11(3):R28 (2010) | OK | Crossref | Kelley DR, Salzberg SL. Detection and correction of false segmental duplications caused by genome mis-assembly. *Genome Biol*. 2010;11(3):R28. doi:10.1186/gb-2010-11-3-r28 |
| 16 | LaPierre N et al., BMC Bioinformatics 20:552 (2019) | Exact title supplied | Crossref | LaPierre N, Egan R, Wang W, Wang Z. De novo Nanopore read quality improvement using deep learning. *BMC Bioinformatics*. 2019;20:552. doi:10.1186/s12859-019-3103-z (this is MiniScrub; preprint bioRxiv doi:10.1101/433573) |
| 17 | Zhang JY et al., FEDRANN, bioRxiv 2025 + GigaScience giag048 | INCOMPLETE: **GigaScience 2026; vol 15** | Crossref: vol 15, art giag048, issued 2026 (published 2026-01-21). The author list differs from the preprint. | Zhang JY, Miao C, Qiu T, He J, Cao W, Lin W, Xia X, He L, Yang C, Sun Y, Zeng T, Li Y, Xu X, Ruan Y, Dong Y. FEDRANN: effective long-read overlap detection based on dimensionality reduction and approximate nearest neighbors. *GigaScience*. 2026;15:giag048. doi:10.1093/gigascience/giag048. Cite the journal version and drop the preprint, or cite the preprint as bioRxiv 2025, doi:10.1101/2025.05.30.656979. |
| 18 | Ono, Hamada, Asai, PBSIM3, NAR Genom Bioinform 4(4):lqac092 (2022) | OK | Crossref | Ono Y, Hamada M, Asai K. PBSIM3: a simulator for all types of PacBio and ONT long reads. *NAR Genom Bioinform*. 2022;4(4):lqac092. doi:10.1093/nargab/lqac092 |
| 19 | Gurevich et al., QUAST, Bioinformatics 29(8):1072–1075 (2013) | OK | Crossref | Gurevich A, Saveliev V, Vyahhi N, Tesler G. QUAST: quality assessment tool for genome assemblies. *Bioinformatics*. 2013;29(8):1072–1075. doi:10.1093/bioinformatics/btt086 |
| 20 | Li H, minimap2, Bioinformatics 34(18):3094–3100 (2018) | OK | Crossref | Li H. Minimap2: pairwise alignment for nucleotide sequences. *Bioinformatics*. 2018;34(18):3094–3100. doi:10.1093/bioinformatics/bty191 |
| 21 | Kurtz et al., MUMmer, Genome Biol 5(2):R12 (2004) | OK | Crossref | Kurtz S, Phillippy A, Delcher AL, Smoot M, Shumway M, Antonescu C, Salzberg SL. Versatile and open software for comparing large genomes. *Genome Biol*. 2004;5(2):R12. doi:10.1186/gb-2004-5-2-r12 |
| 22 | Šošić & Šikić, Edlib, Bioinformatics 33(9):1394–1395 (2017) | OK | Crossref | Šošić M, Šikić M. Edlib: a C/C++ library for fast, exact sequence alignment using edit distance. *Bioinformatics*. 2017;33(9):1394–1395. doi:10.1093/bioinformatics/btw753 |

Note: the GNNome paper's own reference list cites Raven as "Nat Comput Sci 1: 332–336" and Racon as "Genome Res 27: 737–746". These agree with the entries above.

---

## Part D: PBSIM3 and the CPU

### D1. HiFi simulation in PBSIM3

README (https://github.com/yukiteruono/pbsim3, `README.md`): "PBSIM does not directly simulate HiFi reads, but only simulate generation of CLR by multi-pass sequencing; the output of PBSIM simulation is input into ccs software (https://github.com/PacificBiosciences/ccs), which generates HiFi reads." Example: `pbsim --strategy wgs --method qshmm --qshmm data/QSHMM-RSII.model --depth 20 --genome sample/sample.fasta --pass-num 10`. The README adds: "If the number of passes (--pass-num) is two or more, multi-pass sequencing is performed", and the output is BAM ("sd_0001.bam") with "Note: sampling-based simulation cannot be done with multi-pass sequencing."

PBSIM3 paper (PMC9713900): "Multi-pass sequencing of subreads was simulated using PBSIM3. Using the PacBio BAM format data generated by PBSIM3 as an input, ccs (version 6.0.0 ...) was executed with default parameters to generate consensus reads (HiFi reads)." The paper also says: "when the number of passes is 10, CLR error rates of 10–15% can be used to simulate HiFi reads with an error rate similar to that of real HiFi reads." With 5 passes, "the error rate was high (0.99% for H. sapiens CHM13); notably, the yield rate of the consensus sequence from ccs was very low". Multi-pass mode uses a constant read length; single-pass mode uses a gamma distribution.

Developer, issue #46: "PBSIM was designed as a simulator of reads that are prone to sequencing errors. To directly simulate HiFi reads, which have fewer errors, would require a new design." https://github.com/yukiteruono/pbsim3/issues/46

### D2. Does QSHMM-RSII cap accuracy at about 96%?

**The README does not document a cap.** The ~96% ceiling does exist in practice. It comes from the code, not from any rule specific to the RSII model:
- `src/pbsim.cpp` builds the per-read accuracy distribution as `accuracy_max = floor(mean*1.05); accuracy_min = floor(mean*0.75); if (accuracy_max > 100) accuracy_max = 100;`, with weights `exp(0.22*i)` (lines ~2030–2045 of master). With `--accuracy-mean 1.0` the range is 75–100%. My numerical calculation of that distribution gives a **realised mean of 96.0%**; the same holds for `--accuracy-mean 0.99`. For means of 0.95 or below, the realised mean matches the requested value.
- In `data/QSHMM-RSII.model`, the HMMs only cover accuracy bins **75–90%**. The README says: "For read accuracy with insufficient training data, constant quality scores that match the accuracy were used." Other models cover these ranges: ERRHMM-RSII 73–95, ERRHMM-SEQUEL 72–94, QSHMM-ONT 51–90, and QSHMM-ONT-HQ / ERRHMM-ONT-HQ 71–99.
- User report in issue #32 (not from the developer): "I tried the QS model with accuracy set to 1. The final accuracy reported is around 96%." Developer, same thread: "it cannot generate 'error-free' reads even if you specify the option --accuracy-mean 1." https://github.com/yukiteruono/pbsim3/issues/32
- Default `--accuracy-mean` is 0.85, and the default `--accuracy-min` is 0.75.

Suggested wording: "In single-pass mode, PBSIM3's model-based simulation draws per-read accuracy from a distribution truncated at 100%, so the realised mean accuracy saturates at about 96% even with --accuracy-mean 1.0. HiFi-like reads therefore require multi-pass simulation (--pass-num) followed by PacBio ccs, as recommended by the PBSIM3 authors." Do not describe the 96% as a documented property of QSHMM-RSII. It is a property of the code's accuracy sampler, and it also applies to other models.

Note for the manuscript: GNNome used PBSIM3 v3.0.0 to simulate HG002 training reads. The GNNome paper does not state which PBSIM3 options were used. They may be in its Supplemental Note S6, which I did not check.

### D3. Intel Core i5-12450HX

Intel ARK (https://www.intel.com/content/www/us/en/products/sku/228794/intel-core-i512450hx-processor-12m-cache-up-to-4-40-ghz/specifications.html):
- Total Cores "8"; Performance-cores "4"; Efficient-cores "4"; Total Threads "12"
- Max Turbo "4.40 GHz"; P-core Max Turbo "4.40 GHz"; E-core Max Turbo "3.10 GHz"
- Cache "12 MB Intel® Smart Cache"; Base Power "55 W"; Max Turbo Power "157 W"; launched Q2'22

The base clocks were **not shown in the Intel page as fetched**. Most third-party spec sites list P-core base 2.4 GHz and E-core base 1.8 GHz, but pchardware.org lists 2.5 GHz. **UNVERIFIED from Intel.** Suggested wording: "Intel Core i5-12450HX (8 cores: 4P + 4E, 12 threads; up to 4.4 GHz)". This avoids quoting a base clock.
