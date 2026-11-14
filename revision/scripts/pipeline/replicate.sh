#!/usr/bin/env bash
# usage: replicate.sh <cond> <accuracy> <depth> <len_mean> <len_sd> <seed> <threads>
set -euo pipefail
cond=$1 acc=$2 depth=$3 lm=$4 lsd=$5 seed=$6 T=$7
W=$HOME/projects/gnnome-revision/work; P=$W/src/pbsim3
D=$W/runs/reps/${cond}_s${seed}; mkdir -p $D/sim; cd $D
[ -f DONE ] && exit 0
echo "cond=$cond acc=$acc depth=$depth len_mean=$lm len_sd=$lsd seed=$seed" > params.txt
if [ ! -s sim/sim_0001.fq.gz ]; then
  $P/src/pbsim --strategy wgs --method qshmm --qshmm $P/data/QSHMM-RSII.model --depth $depth --accuracy-mean $acc \
    --length-mean $lm --length-sd $lsd --genome $W/data/CP017100.fasta --prefix sim/sim --seed $seed > sim/pbsim.log 2>&1
fi
SKIP_DEF=1 $W/bin/assemble_all.sh sim/sim_0001.fq.gz $D $T "gnnome gnnome_twin greedy_sim greedy_simlen greedy_simlen_twin" > assemble.log 2>&1
touch DONE
