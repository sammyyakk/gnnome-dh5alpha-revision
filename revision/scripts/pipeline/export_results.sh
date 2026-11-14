#!/usr/bin/env bash
# Copy small result files (QUAST reports, collect/trace JSON/TSV, logs, hashes) from work/runs into revision/results.
set -uo pipefail
W=$HOME/projects/gnnome-revision/work; O=$HOME/projects/gnnome-revision/revision/results
exp(){ # <run_dir> <dest>
  local d=$1 o=$2; [ -d "$d" ] || return 0; mkdir -p $o
  for f in reads.sha256 outputs.sha256 guard1.txt pipeline.log params.txt; do [ -f $d/$f ] && cp $d/$f $o/; done
  for q in $d/quast/*/; do [ -f $q/report.tsv ] && { mkdir -p $o/quast/$(basename $q); cp $q/report.tsv $o/quast/$(basename $q)/; }; done
  for g in $d/gn_*/guard2.txt; do [ -f $g ] && cp $g $o/$(basename $(dirname $g)).guard2.txt; done
  if [ -d $d/trace ]; then mkdir -p $o/trace
    find $d/trace -maxdepth 1 -type f \( -name '*.json' -o -name '*.tsv' -o -name '*.txt' -o -name '*.log' \) -size -3M -exec cp {} $o/trace/ \;
  fi
}
exp $W/runs/run2_full $O/run2
exp $W/runs/real $O/real
exp $W/runs/run1r $O/run1r
[ -f $W/runs/run1r/00_reads/command.log ] && cp $W/runs/run1r/00_reads/command.log $O/run1r/ 2>/dev/null
for d in $W/runs/reps/*_s*/; do d=${d%/}; [ -f $d/DONE ] && exp $d $O/replicates/$(basename $d); done
for d in $W/runs/stale_k12; do mkdir -p $O/stale_k12; for q in $d/quast_*/; do [ -d $q ] && for r in $(find $q -name report.tsv); do rel=${r#$d/}; mkdir -p $O/stale_k12/$(dirname $rel); cp $r $O/stale_k12/$rel; done; done; done
true
