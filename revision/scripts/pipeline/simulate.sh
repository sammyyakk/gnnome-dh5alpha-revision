#!/usr/bin/env bash
# Run 1R: logged regeneration of the accurate (HiFi-like) Run 1 reads.
# PBSIM3 35ce0de multi-pass CLR (QSHMM-RSII, 10 passes) -> samtools BAM -> pbccs. Seed fixed.
set -euo pipefail
W=$HOME/projects/gnnome-revision/work; T=$W/envs/tools/bin; P=$W/src/pbsim3
cd $W/runs/run1r/00_reads
export PATH=$T:$PATH   # PBSIM3 multi-pass pipes SAM through samtools
echo "date_utc: $(date -u)" > command.log
python3 -I make_templates.py $W/data/CP017100.fasta run1r.template 20261115 60 >> command.log
CMD="$P/src/pbsim_fixed --strategy templ --method qshmm --qshmm $P/data/QSHMM-RSII.model --template run1r.template --pass-num 10 --prefix run1r --seed 20261115"
echo "pbsim: $CMD" >> command.log; $CMD > pbsim.log 2>&1
if [ -s run1r.sam ]; then samtools view -@ 10 -b -o run1r.bam run1r.sam && rm run1r.sam; fi
ls -la >> command.log
CCS="$T/ccs -j 11 --min-passes 3 --min-rq 0.99 run1r.bam run1r.ccs.fastq.gz"
echo "ccs: $CCS" >> command.log; $CCS > ccs.log 2>&1
sha256sum run1r.ccs.fastq.gz run1r.maf.gz $P/src/pbsim_fixed >> command.log
echo SIM_DONE >> command.log
