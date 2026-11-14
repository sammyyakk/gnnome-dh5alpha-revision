"""Greedy raw-feature baseline: replace GNNome's model edge scores by a monotone
function of the raw edge features (no GNN). GNNome's inference.py loads
decode/0_predicts.pt if present and skips the model, so the decoder (seed-edge
sampling, greedy walk both ways, contig selection) is otherwise unchanged.

usage: raw_scores.py <processed/0.dgl> <sim|len|simlen> <out 0_predicts.pt>
  sim    : score = logit(overlap_similarity)          -> greedy picks most similar overlap
  len    : score = z(overlap_length)                  -> greedy picks longest overlap
  simlen : score = z(overlap_similarity) + z(overlap_length)
"""
import os
import sys

os.environ.setdefault("DGLBACKEND", "pytorch")
import dgl  # noqa: E402
import torch  # noqa: E402

dgl_path, mode, out = sys.argv[1:4]
g = dgl.load_graphs(dgl_path)[0][0]
sim = g.edata["overlap_similarity"].double()
ol = g.edata["overlap_length"].double()


def z(x):
    return (x - x.mean()) / x.std()


if mode == "sim":
    s = sim.clamp(1e-6, 1 - 1e-6)
    score = torch.log(s / (1 - s))
elif mode == "len":
    score = z(ol)
elif mode == "simlen":
    score = z(sim) + z(ol)
else:
    raise SystemExit(f"unknown mode {mode}")
torch.save(score.float(), out)
print(f"[raw_scores] mode={mode} edges={score.shape[0]} -> {out}")
