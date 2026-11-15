#!/usr/bin/env bash
# Run 1R: truth MAF from CCS reads, full same-graph assembly, ground-truth trace.
W=$HOME/projects/gnnome-revision/work; cd $W
A=$HOME/projects/gnnome-revision/revision/scripts
R=runs/run1r/00_reads
log(){ echo "[$(date -u +%FT%TZ)] $*" >> logs/run1r_chain.log; }
[ -s $R/run1r.ccs.fastq.gz ] || { log "ABORT no ccs output"; exit 1; }
log "run1r truth (paf2maf map-hifi)"
[ -s $R/run1r.genome.maf.gz ] || envs/gnnome/bin/python -I $A/analysis/paf2maf.py $R/run1r.ccs.fastq.gz data/CP017100.fasta 12 map-hifi $R/run1r.genome.maf.gz >> logs/run1r_chain.log 2>&1
log "run1r assemble_all"
bash bin/assemble_all.sh $R/run1r.ccs.fastq.gz runs/run1r 12 > logs/run1r.log 2>&1 || { log "ABORT run1r assemble rc=$?"; exit 1; }
log "run1r trace"
bash $A/pipeline/trace_run.sh runs/run1r $R/run1r.ccs.fastq.gz $R/run1r.genome.maf.gz run1r 10 > logs/trace_run1r.log 2>&1
log "run1r DONE"
touch runs/run1r/CHAIN_DONE
