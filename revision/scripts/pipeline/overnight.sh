#!/usr/bin/env bash
# Overnight driver: Run 1R assembly + trace, second replicate runner after CCS frees the CPU.
W=$HOME/projects/gnnome-revision/work; cd $W
A=$HOME/projects/gnnome-revision/revision/scripts
log(){ echo "[$(date -u +%FT%TZ)] $*" >> logs/overnight.log; }
while pgrep -f "ccs -j 11" > /dev/null; do sleep 60; done
log "ccs finished"
R=runs/run1r/00_reads
[ -s $R/run1r.ccs.fastq.gz ] || { log "ABORT no ccs output"; exit 1; }
log "second replicate runner (reverse order) started"
setsid nohup bash -c "tac runs/jobs_rev.txt | xargs -P 2 -L 1 bin/replicate.sh" > logs/reps_rev.log 2>&1 < /dev/null &
log "run1r truth (paf2maf map-hifi)"
envs/gnnome/bin/python -I $A/analysis/paf2maf.py $R/run1r.ccs.fastq.gz data/CP017100.fasta 4 map-hifi $R/run1r.genome.maf.gz >> logs/overnight.log 2>&1
log "run1r assemble_all"
bash bin/assemble_all.sh $R/run1r.ccs.fastq.gz runs/run1r 6 > logs/run1r.log 2>&1 || { log "ABORT run1r assemble rc=$?"; exit 1; }
log "run1r trace"
bash $A/pipeline/trace_run.sh runs/run1r $R/run1r.ccs.fastq.gz $R/run1r.genome.maf.gz run1r 6 > logs/trace_run1r.log 2>&1
log "overnight DONE"
