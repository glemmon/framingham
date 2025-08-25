from __future__ import annotations
from typing import Dict, Any, List
import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt

def plot_km(km_result: Dict[str, Any], title: str = "Kaplan–Meier"):
    fig = plt.figure(figsize=(7, 4.5))
    times = [pt["t"] for pt in km_result["survival"]]
    surv = [pt["s"] for pt in km_result["survival"]]
    lcl = [pt["lcl"] for pt in km_result["survival"]]
    ucl = [pt["ucl"] for pt in km_result["survival"]]
    ax = plt.gca()
    ax.step(times, surv, where="post", linewidth=2, label="KM")
    ax.fill_between(times, lcl, ucl, step="post", alpha=0.2, label="95% CI")
    ax.set_title(title)
    ax.set_xlabel("Time (days)")
    ax.set_ylabel("Survival probability")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.4)
    fig.tight_layout()
    return fig

def plot_cox_forest(cox_result: Dict[str, Any], title: str = "Cox PH (HR with 95% CI)"):
    rows: List[Dict[str, Any]] = cox_result["rows"]
    if not rows:
        fig = plt.figure(figsize=(6, 3))
        ax = plt.gca()
        ax.text(0.5, 0.5, "No results (model did not converge or no predictors)", ha="center", va="center")
        ax.axis("off")
        fig.tight_layout()
        return fig
    labels = []
    hrs = []
    lows = []
    highs = []
    for r in rows:
        label = r["var"] if r.get("level") in (None, "",) else f'{r["var"]}={r["level"]}'
        labels.append(label)
        hrs.append(r["hr"])
        lows.append(r["lcl"])
        highs.append(r["ucl"])
    # Order by HR
    order = sorted(range(len(rows)), key=lambda i: hrs[i])
    labels = [labels[i] for i in order]
    hrs = [hrs[i] for i in order]
    lows = [lows[i] for i in order]
    highs = [highs[i] for i in order]

    y = list(range(len(labels)))
    fig = plt.figure(figsize=(8, 0.4*len(labels) + 2.5))
    ax = plt.gca()
    ax.errorbar(hrs, y, xerr=[ [hr - lo for hr, lo in zip(hrs, lows)],
                                [hi - hr for hr, hi in zip(hrs, highs)] ],
                fmt='o', capsize=3)
    ax.axvline(1.0, linestyle="--", linewidth=1)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xscale("log")
    ax.set_xlabel("Hazard Ratio (log scale)")
    ax.set_title(title)
    fig.tight_layout()
    return fig
