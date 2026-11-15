"""Replicate analysis for the revision (27 replicates = 9 settings x 3 seeds).

1. Builds results/replicates/replicates.tsv: one row per replicate, columns <variant>_<metric> from each
   runs/reps/<setting>_s<seed>/trace/collect.json (unpolished identity = minimap2 asm20; QUAST m80 unpolished and
   default after Racon x2; source-read selection).
2. Paired comparisons A - B for several pairs and three metrics:
     d_id  = 100*(A_p0_identity - B_p0_identity)          pp, positive = A better
     d_pol = (A_racon2 mm+indel) - (B_racon2 mm+indel)     errors/100 kbp, negative = A better
     d_src = 100*(A_source_err - B_source_err)            pp, negative = A copies cleaner reads
   Units: settings (exact sign test, exact Wilcoxon on setting means) and replicates (mixed model diff ~ 1 + (1|setting),
   REML). Replicate-level sign counts are descriptive only.
   Done for the original 7-setting design (21 replicates, manuscript audit) and the full 9-setting design (27).
3. Slope of d_id(GNNome - Raven) on read identity: OLS on the 4 accuracy-series setting means (30x, 9 kb).
4. Depth vs length: 99%-target settings 30x/9k, 60x/9k, 30x/18.5k, 60x/18.5k (2x2, setting means).
5. Reproduction check against the original repository's collected.tsv (same settings and seeds).
usage: rep_stats.py <reps_dir> <original collected.tsv> <out_dir>
"""
import glob, json, os, sys
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

reps, orig, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
ORIGINAL = ["acc085_d30_L9k", "acc090_d30_L9k", "acc095_d30_L9k", "acc099_d30_L9k",
            "acc085_d60_L9k", "acc085_d30_L18k", "acc099_d60_L18k"]
rows = []
for f in sorted(glob.glob(f"{reps}/*_s??/trace/collect.json")):
    d = json.load(open(f)); name = f.split("/")[-3]
    r = dict(replicate=name, setting=name.rsplit("_s", 1)[0], seed=int(name.rsplit("_s", 1)[1]),
             read_identity_mean=d["read_identity_mean"], read_identity_p90=d["read_identity_p90"])
    for v, a in d["assemblies"].items():
        for k in ("p0_identity", "racon2_mm", "racon2_indel", "racon2_localmis", "racon2_mis", "p0m80_mis", "p0m80_localmis",
                  "p0m80_mm", "p0m80_indel", "p0m80_gf", "source_read_error_weighted", "source_reads", "source_contrib_median",
                  "source_reads_in_worst_decile", "source_read_identity_mean"):
            r[f"{v}_{k}"] = a.get(k)
    rows.append(r)
df = pd.DataFrame(rows)
df.to_csv(f"{out}/replicates.tsv", sep="\t", index=False)


def sign(x):
    # round first: QUAST values have 2 decimals, so float residue (e.g. 0.46+0.48+0.46 vs 0.44+0.59+0.37) is a tie
    x = np.round(np.asarray(x, float), 9); k = int((x > 0).sum()); n = int((x != 0).sum())
    return dict(pos=k, neg=int((x < 0).sum()), zero=int((x == 0).sum()), p=float(stats.binomtest(k, n, 0.5).pvalue) if n else None)


def wil(x):
    x = np.round(np.asarray(x, float), 9)
    x = x[x != 0]  # Wilcoxon's zero handling, done here so scipy keeps the exact distribution
    if len(x) < 2:
        return None
    r = stats.wilcoxon(x, alternative="two-sided", mode="exact")
    return dict(stat=float(r.statistic), p=float(r.pvalue), n_nonzero=int(len(x)))


def mixed(d, col):
    try:
        m = smf.mixedlm(f"{col} ~ 1", d, groups=d["setting"]).fit(reml=True)
        ci = m.conf_int().loc["Intercept"].tolist()
        return dict(mean=float(m.params["Intercept"]), ci95=[float(ci[0]), float(ci[1])], p=float(m.pvalues["Intercept"]))
    except Exception as e:
        return dict(error=str(e))


PAIRS = [("gnnome", "raven"), ("gnnome_twin", "raven"), ("greedy_sim", "raven"), ("greedy_sim_twin", "raven"),
         ("greedy_simlen", "raven"), ("greedy_sim", "gnnome"), ("greedy_sim_twin", "gnnome_twin"),
         ("gnnome_twin", "gnnome"), ("greedy_simlen", "gnnome")]
res = dict(n_replicates=len(df), settings=sorted(df.setting.unique()), comparisons={})
for design, sub in (("original_7x3", df[df.setting.isin(ORIGINAL)]), ("full_9x3", df)):
    for a, b in PAIRS:
        if f"{a}_p0_identity" not in sub or sub[f"{a}_p0_identity"].isna().any():
            continue
        d = sub[["setting", "seed"]].copy()
        d["d_id"] = 100 * (sub[f"{a}_p0_identity"] - sub[f"{b}_p0_identity"])
        d["d_pol"] = (sub[f"{a}_racon2_mm"] + sub[f"{a}_racon2_indel"]) - (sub[f"{b}_racon2_mm"] + sub[f"{b}_racon2_indel"])
        d["d_src"] = 100 * (sub[f"{a}_source_read_error_weighted"] - sub[f"{b}_source_read_error_weighted"])
        key = f"{design}:{a}-{b}"
        res["comparisons"][key] = {}
        for col in ("d_id", "d_pol", "d_src"):
            cm = d.groupby("setting")[col].mean()
            res["comparisons"][key][col] = dict(replicate_n=len(d), replicate_sign=sign(d[col]),
                                                setting_n=len(cm), setting_means={k: round(float(v), 4) for k, v in cm.items()},
                                                setting_sign=sign(cm), setting_wilcoxon_exact=wil(cm), mixed_model=mixed(d, col))
# slope: GNNome - Raven unpolished identity vs read identity, accuracy series
acc = df[df.setting.isin(ORIGINAL[:4])].copy()
for a in ("gnnome", "greedy_sim", "gnnome_twin"):
    acc["d"] = 100 * (acc[f"{a}_p0_identity"] - acc["raven_p0_identity"])
    m = acc.groupby("setting")[["d", "read_identity_mean"]].mean()
    lr = stats.linregress(100 * m.read_identity_mean, m.d)
    res[f"slope_{a}_minus_raven"] = dict(n_settings=len(m), slope_pp_per_pp=lr.slope, r=lr.rvalue, p=lr.pvalue,
                                         setting_means=m.round(5).to_dict())
# depth vs length (99% target)
dl = {}
for s in ("acc099_d30_L9k", "acc099_d60_L9k", "acc099_d30_L18k", "acc099_d60_L18k"):
    x = df[df.setting == s]
    if len(x):
        dl[s] = {f"{a}_minus_raven_pp": round(float((100 * (x[f"{a}_p0_identity"] - x.raven_p0_identity)).mean()), 3)
                 for a in ("gnnome", "gnnome_twin", "greedy_sim")}
        dl[s]["raven_p0_identity"] = round(float(x.raven_p0_identity.mean()), 5)
        dl[s]["gnnome_p0_identity"] = round(float(x.gnnome_p0_identity.mean()), 5)
        dl[s]["read_identity_mean"] = round(float(x.read_identity_mean.mean()), 5)
res["depth_vs_length_99target"] = dl
# reproduction check vs original collected.tsv
try:
    o = pd.read_csv(orig, sep="\t")
    o = o[~o.cond.str.startswith("run1reads")]
    chk = []
    for _, r in o.iterrows():
        seed = int(r.get("seed", 0)) if "seed" in o.columns else None
        name = f"{r.cond}_s{seed}" if seed else None
        m = df[df.replicate == name] if name else pd.DataFrame()
        if len(m):
            m = m.iloc[0]
            chk.append(dict(replicate=name,
                            raven_id_orig=r.raven_p0_identity, raven_id_new=m.raven_p0_identity,
                            gnnome_id_orig=r.gnnome_p0_identity, gnnome_id_new=m.gnnome_p0_identity))
    res["reproduction_vs_original"] = dict(matched=len(chk), rows=chk,
                                           max_abs_diff_pp=float(max((100 * max(abs(c["raven_id_orig"] - c["raven_id_new"]), abs(c["gnnome_id_orig"] - c["gnnome_id_new"])) for c in chk), default=float("nan"))))
except Exception as e:
    res["reproduction_vs_original"] = dict(error=str(e))
json.dump(res, open(f"{out}/rep_stats.json", "w"), indent=1, default=float)
for k, v in res["comparisons"].items():
    s = v["d_id"]; p = v["d_pol"]
    print(f"{k:45s} unpol: settings {s['setting_sign']['pos']}/{s['setting_n']} p={s['setting_sign']['p']:.3g} mixed={s['mixed_model'].get('mean', float('nan')):+.3f}pp "
          f"| polished A better {p['setting_sign']['neg']}/{p['setting_n']} p={p['setting_sign']['p']:.3g} mixed={p['mixed_model'].get('mean', float('nan')):+.3f}")
