#!/usr/bin/env bash
# Full same-graph comparison on one read set, with provenance guards.
#   Raven fork (twin-export build; graph_1.gfa byte-identical to the original fork) -p0
#   -> GUARD 1: GFA segments are substrings of THESE reads (200/200), else abort
#   -> GNNome (original parser) / GNNome (twin-length fix)
#   -> greedy raw-feature baselines (sim, simlen) on both parsers
#   -> GUARD 2: every GNNome run consumed exactly this GFA (nodes, edges, sequences), else abort
#   -> Racon x2 for every assembly (same command for all) -> QUAST (--min-identity 80 unpolished; default polished)
# usage: assemble_all.sh <reads> <rundir> [threads] [variants]
set -euo pipefail
W=$HOME/projects/gnnome-revision/work
reads=$(realpath "$1"); D=$(realpath -m "$2"); T=${3:-10}
VARIANTS=${4:-"gnnome gnnome_twin greedy_sim greedy_simlen greedy_sim_twin greedy_simlen_twin"}
PY=$W/envs/gnnome/bin/python; TB=$W/envs/tools/bin; Q=$W/envs/quast/bin/quast.py
REF=$W/data/CP017100.fasta; RAVEN=$W/src/raven_twin/build/bin/raven
mkdir -p "$D"/{raven,asm,polish,quast}; cd "$D"
log(){ echo "[$(date -u +%FT%TZ)] $*" | tee -a "$D/pipeline.log"; }
sha256sum "$reads" > reads.sha256

if [ ! -s raven/graph_1.gfa ]; then
  log "raven -p0"; (cd raven && "$RAVEN" -t "$T" -p0 "$reads" > raven_p0.fasta 2> raven.log)
fi
cp raven/raven_p0.fasta asm/raven.fasta
log "GUARD 1 graph<->reads"
$PY -I $W/bin/check_gfa_reads.py raven/graph_1.gfa "$reads" | tee guard1.txt
grep -q "identical sequence 200/200" guard1.txt || { log "ABORT: graph not built from these reads"; exit 3; }

for v in $VARIANTS; do
  [ -s asm/$v.fasta ] && continue
  src=$W/src/GNNome; [[ $v == *twin ]] && src=$W/src/GNNome_twin
  case $v in greedy_simlen*) scorer=simlen ;; greedy_sim*) scorer=sim ;; greedy_len*) scorer=len ;; *) scorer="" ;; esac
  log "assemble $v (src=$(basename $src) scorer=${scorer:-model})"
  SCORER=$scorer T=$T $W/bin/gnnome_run.sh "$reads" raven/graph_1.gfa gn_$v "$src"
  DGLBACKEND=pytorch $PY -I $W/bin/prove_graph_consumed.py raven/graph_1.gfa gn_$v/raven > gn_$v/guard2.txt 2>&1
  grep -q "VERDICT        : MATCH" gn_$v/guard2.txt || { log "ABORT: $v did not consume this graph"; exit 4; }
  cp gn_$v/raven/assembly/0_assembly.fasta asm/$v.fasta
  rm -f gn_$v/raven/info/0_reads.pkl
done

for a in asm/*.fasta; do
  n=$(basename $a .fasta); o=polish/$n; [ -s $o/round2.fasta ] && continue
  log "racon x2 $n"; mkdir -p $o; cp $a $o/round0.fasta
  for i in 1 2; do
    $TB/minimap2 -t $T -x map-pb $o/round$((i-1)).fasta "$reads" > $o/round$i.paf 2>> $o/polish.log
    $TB/racon -t $T -m 3 -x -5 -g -4 -w 500 "$reads" $o/round$i.paf $o/round$((i-1)).fasta > $o/round$i.fasta 2>> $o/polish.log
    rm -f $o/round$i.paf
  done
done

for a in asm/*.fasta; do
  n=$(basename $a .fasta)
  [ -s quast/p0_m80_$n/report.tsv ] || $Q -t $T --min-identity 80 $a -r $REF -o quast/p0_m80_$n > /dev/null 2>&1
  [ -n "${SKIP_DEF:-}" ] || [ -s quast/p0_def_$n/report.tsv ] || $Q -t $T $a -r $REF -o quast/p0_def_$n > /dev/null 2>&1
  [ -s quast/racon2_$n/report.tsv ] || $Q -t $T polish/$n/round2.fasta -r $REF -o quast/racon2_$n > /dev/null 2>&1
done
sha256sum raven/graph_1.gfa asm/*.fasta polish/*/round2.fasta > outputs.sha256
log "DONE"; touch DONE
