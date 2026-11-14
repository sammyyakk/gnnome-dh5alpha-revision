#!/usr/bin/env bash
# usage: gnnome_run.sh <reads> <gfa> <outdir> [gnnome_src_dir]
set -euo pipefail
W=$HOME/projects/gnnome-revision/work; PY=$W/envs/gnnome/bin/python
reads=$(realpath $1); gfa=$(realpath $2); out=$(realpath -m $3); src=${4:-$W/src/GNNome}
mkdir -p $out; cd $src
export OMP_NUM_THREADS=${T:-8} DGLBACKEND=pytorch
$PY create_inference_graphs.py --reads $reads --gfa $gfa --asm raven --out $out > $out/preprocess.log 2>&1
if [ -n "${SCORES:-}" ]; then mkdir -p $out/raven/decode; cp $SCORES $out/raven/decode/0_predicts.pt; fi
if [ -n "${SCORER:-}" ]; then mkdir -p $out/raven/decode; $PY -I $W/bin/raw_scores.py $out/raven/processed/0.dgl $SCORER $out/raven/decode/0_predicts.pt; fi
$PY inference.py --data $out --asm raven --out $out/raven --model weights/weights.pt > $out/inference.log 2>&1
sha256sum $gfa $out/raven/processed/0.dgl $out/raven/decode/0_predicts.pt $out/raven/assembly/0_assembly.fasta > $out/hashes.sha256
