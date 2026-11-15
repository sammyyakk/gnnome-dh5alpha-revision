#!/usr/bin/env bash
# For every finished replicate: backfill the greedy_sim_twin variant if missing, then per-read truth + collect.json.
W=$HOME/projects/gnnome-revision/work; cd $W
A=$HOME/projects/gnnome-revision/revision/scripts/analysis
PY=$W/envs/gnnome/bin/python; export DGLBACKEND=pytorch
log(){ echo "[$(date -u +%FT%TZ)] $*" >> logs/reps_collect.log; }
for D in runs/reps/*_s??; do
  [ -f $D/DONE ] || continue
  if [ ! -s $D/asm/greedy_sim_twin.fasta ]; then
    log "backfill greedy_sim_twin $D"
    SKIP_DEF=1 bash bin/assemble_all.sh $D/sim/sim_0001.fq.gz $D 4 "greedy_sim_twin" >> $D/assemble.log 2>&1 || log "backfill FAILED $D"
  fi
  mkdir -p $D/trace
  if [ ! -s $D/trace/collect.json ] || [ $D/asm/greedy_sim_twin.fasta -nt $D/trace/collect.json ]; then
    log "collect $D"
    (cd $D/trace && [ -s truth.reads.tsv ] || $PY -I $A/read_truth.py ../sim/sim_0001.maf.gz ../sim/sim_0001.fq.gz 4583637 truth > /dev/null 2>&1)
    (cd $D/trace && $PY -I $A/collect.py .. truth.reads.tsv collect.json >> ../collect.log 2>&1) || log "collect FAILED $D"
  fi
done
log "ALL DONE"; touch runs/reps/COLLECT_DONE
