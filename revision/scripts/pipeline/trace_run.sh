#!/usr/bin/env bash
# Ground-truth tracing for one assemble_all.sh run directory.
# usage: trace_run.sh <run_dir> <reads> <maf.gz> <label> [threads]
#   maf.gz: PBSIM3 genome-coordinate MAF, or one made by paf2maf.py
set -euo pipefail
D=$(realpath "$1"); reads=$(realpath "$2"); maf=$(realpath "$3"); L=$4; T=${5:-8}
W=$HOME/projects/gnnome-revision/work; A=$HOME/projects/gnnome-revision/revision/scripts/analysis
PY="$W/envs/gnnome/bin/python"; export DGLBACKEND=pytorch REF=$W/data/CP017100.fasta MM=$W/envs/tools/bin/minimap2
export PATH=$W/envs/tools/bin:$PATH NUCMER=1
O=$D/trace; mkdir -p $O; cd $O
G=4583637
$PY -I $A/read_truth.py $maf $reads $G truth > /dev/null
$PY -I $A/collect.py $D truth.reads.tsv collect.json
for v in $(ls $D/asm | sed 's/.fasta//'); do
  q=$D/quast/p0_m80_$v
  $PY -I $A/breakpoints.py ${L}_$v $D/asm/$v.fasta $q bp_$v.tsv > /dev/null 2>&1 || echo "breakpoints failed $v"
  snps=$(ls $q/contigs_reports/minimap_output/*.used_snps* 2>/dev/null | head -1)
  if [ "$v" = raven ]; then
    $PY -I $A/repeat_errors.py ${L}_$v $D/asm/$v.fasta "$snps" bp_$v.tsv truth.reads.tsv $reads - - - 1 . > /dev/null 2>&1 || echo "repeat_errors failed $v"
  else
    $PY -I $A/graph_truth.py $D/raven/graph_1.gfa $D/gn_$v/raven truth.reads.tsv edges_$v > /dev/null 2>&1 || echo "graph_truth failed $v"
    $PY -I $A/repeat_errors.py ${L}_$v $D/asm/$v.fasta "$snps" bp_$v.tsv truth.reads.tsv $reads $D/raven/graph_1.gfa $D/gn_$v/raven edges_$v.edges.tsv 1 . > /dev/null 2>&1 || echo "repeat_errors failed $v"
  fi
done
# junction cut errors and twin-edge statistics (original parser lengths), why-cleaner chain, ablation
$PY -I $A/junction_check.py $D/raven/graph_1.gfa $D/gn_gnnome/raven $maf $reads "$(ls $D/quast/p0_m80_gnnome/contigs_reports/minimap_output/*.used_snps* | head -1)" ${L}_gnnome.junctions > /dev/null 2>&1 || echo "junction_check failed"
$PY -I $A/edge_discrepancy.py $D/raven/graph_1.gfa edges_gnnome.edges.tsv $maf $reads $D/gn_gnnome/raven ${L}_edge_cut_error > /dev/null 2>&1 || echo "edge_discrepancy failed"
$PY -I $A/why_cleaner.py $D/gn_gnnome/raven/processed/0.dgl edges_gnnome.edges.tsv truth.reads.tsv why_cleaner.json > /dev/null 2>&1 || echo "why_cleaner failed"
(cd $W/src/GNNome && $PY $A/why_cleaner_ablation.py $D/gn_gnnome/raven/processed/0.dgl $O/edges_gnnome.edges.tsv $O/truth.reads.tsv $O/why_cleaner_ablation.json > /dev/null 2>&1) || echo "ablation failed"
echo TRACE_DONE > TRACE_DONE
