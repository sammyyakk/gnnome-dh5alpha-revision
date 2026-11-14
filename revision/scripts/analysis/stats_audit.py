"""Re-test replicate claims with explicit tests and setting-level units.
usage: stats_audit.py <collected.tsv> <out.json>
Columns used: cond, raven_p0_identity, gnnome_p0_identity, raven_racon2_mm/indel, gnnome_racon2_mm/indel,
raven_source_read_error, gnnome_source_read_error. Rows with cond starting 'run1reads' are excluded (n=2 subsamples).
Tests (all two-sided):
  replicate level (n=21; pseudo-replicated, reported for comparison only): exact sign test; Wilcoxon signed-rank
     (scipy: exact when n<=50 without zeros/ties, else normal approximation; zero_method='wilcox')
  setting level (n=7 condition means): exact sign test; exact Wilcoxon signed-rank
  mixed model: diff ~ 1 + (1|cond), REML; intercept = mean GNNome-Raven difference with condition random effect
  slope: diff ~ read identity, OLS on 4 condition means (accuracy series, 30x, 9 kb) and mixed model on 12 replicates
"""
import json, sys, csv, math
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
df = pd.read_csv(sys.argv[1], sep="\t"); df = df[~df.cond.str.startswith("run1reads")].copy()
df["d_id"] = 100 * (df.gnnome_p0_identity - df.raven_p0_identity)            # pp, + = GNNome better
df["d_pol"] = (df.gnnome_racon2_mm + df.gnnome_racon2_indel) - (df.raven_racon2_mm + df.raven_racon2_indel)  # errors/100kbp, - = GNNome better
df["d_src"] = 100 * (df.gnnome_source_read_error - df.raven_source_read_error)  # pp, - = GNNome cleaner
def sign(x):
    x = np.asarray(x); k = int((x > 0).sum()); n = int((x != 0).sum())
    return dict(pos=k, neg=int((x < 0).sum()), zero=int((x == 0).sum()), p=float(stats.binomtest(k, n, 0.5).pvalue) if n else None)
def wil(x, mode):
    x = np.asarray(x)
    if np.all(x == 0): return None
    r = stats.wilcoxon(x, zero_method="wilcox", alternative="two-sided", mode=mode)
    return dict(stat=float(r.statistic), p=float(r.pvalue), mode=mode)
def mixed(col):
    m = smf.mixedlm(f"{col} ~ 1", df, groups=df["cond"]).fit(reml=True)
    ci = m.conf_int().loc["Intercept"].tolist()
    return dict(mean=float(m.params["Intercept"]), ci95=[float(ci[0]), float(ci[1])], p=float(m.pvalues["Intercept"]),
                group_var=float(m.cov_re.iloc[0, 0]), resid_var=float(m.scale))
out = {}
for col, better in (("d_id", "positive"), ("d_pol", "negative"), ("d_src", "negative")):
    cm = df.groupby("cond")[col].mean()
    out[col] = dict(direction_gnnome_better=better,
        replicate_n=len(df), replicate_sign=sign(df[col]), replicate_wilcoxon_auto=wil(df[col], "auto"),
        replicate_wilcoxon_approx=wil(df[col], "approx"),
        setting_n=len(cm), setting_means={k: round(float(v), 4) for k, v in cm.items()},
        setting_sign=sign(cm), setting_wilcoxon_exact=wil(cm, "exact"), mixed_model=mixed(col))
acc = df[df.cond.isin(["acc085_d30_L9k", "acc090_d30_L9k", "acc095_d30_L9k", "acc099_d30_L9k"])].copy()
acc["read_id_pp"] = 100 * acc.read_identity
cm = acc.groupby("cond")[["read_id_pp", "d_id"]].mean()
ols = stats.linregress(cm.read_id_pp, cm.d_id)
mm = smf.mixedlm("d_id ~ read_id_pp", acc, groups=acc["cond"]).fit(reml=True)
rep = stats.linregress(acc.read_id_pp, acc.d_id)
out["slope"] = dict(setting_level_ols=dict(n=4, slope=ols.slope, r=ols.rvalue, p=ols.pvalue),
                    replicate_level_ols_pseudoreplicated=dict(n=len(acc), slope=rep.slope, r=rep.rvalue, p=rep.pvalue),
                    mixed_model=dict(slope=float(mm.params["read_id_pp"]), p=float(mm.pvalues["read_id_pp"])))
json.dump(out, open(sys.argv[2], "w"), indent=1, default=float)
for c in ("d_id", "d_pol", "d_src"):
    o = out[c]; print(c, "rep sign", o["replicate_sign"], "rep wil", o["replicate_wilcoxon_auto"], "| setting sign", o["setting_sign"], "setting wil", o["setting_wilcoxon_exact"], "| mixed", {k: o["mixed_model"][k] for k in ("mean", "ci95", "p")})
print("slope", out["slope"])
