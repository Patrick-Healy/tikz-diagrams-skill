#!/usr/bin/env python3
"""Collect GitHub repo traffic (views + clones) and accumulate history.

The GitHub traffic API only retains ~14 days. This script merges each daily
snapshot into CSVs under traffic/, deduping by date so history grows without
bound, then renders a cumulative line plot.

Env:
  GITHUB_REPOSITORY  owner/name (provided automatically in Actions)
  GH_TOKEN           token with push access to the repo (traffic API requires it)
"""
import csv
import json
import os
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = os.environ["GITHUB_REPOSITORY"]


def api(path):
    r = subprocess.run(
        ["gh", "api", f"repos/{REPO}/traffic/{path}"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise SystemExit(
            f"gh api traffic/{path} failed (exit {r.returncode}).\n{r.stderr}\n"
            "Traffic endpoints require a token with push access — set a classic "
            "PAT (repo scope) as the TRAFFIC_TOKEN secret."
        )
    return json.loads(r.stdout)


def merge(csv_path, rows):
    """Merge new {date: (count, uniques)} rows into csv_path, keeping the max
    seen for each date (guards against partial-day snapshots undercounting)."""
    data = {}
    if csv_path.exists():
        with open(csv_path) as f:
            for r in csv.DictReader(f):
                data[r["date"]] = [int(r["count"]), int(r["uniques"])]
    for date, (count, uniques) in rows.items():
        cur = data.get(date, [0, 0])
        data[date] = [max(cur[0], count), max(cur[1], uniques)]
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "count", "uniques"])
        for date in sorted(data):
            w.writerow([date, data[date][0], data[date][1]])
    return data


def snapshot(kind, key):
    payload = api(kind)
    rows = {
        item["timestamp"][:10]: (item["count"], item["uniques"])
        for item in payload[key]
    }
    return merge(HERE / f"{kind}.csv", rows)


def load_cumulative(data):
    dates = sorted(data)
    cum, running = [], 0
    for d in dates:
        running += data[d][0]
        cum.append(running)
    return dates, cum


def main():
    views = snapshot("views", "views")
    clones = snapshot("clones", "clones")

    vd, vc = load_cumulative(views)
    cd, cc = load_cumulative(clones)

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(vd, vc, marker="o", label="Cumulative views", color="#1f77b4")
        ax.plot(cd, cc, marker="s", label="Cumulative clones", color="#d62728")
        ax.set_title(f"{REPO} — cumulative traffic")
        ax.set_xlabel("Date")
        ax.set_ylabel("Cumulative count")
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.autofmt_xdate()
        fig.tight_layout()
        fig.savefig(HERE / "cumulative.png", dpi=120)
        print("Wrote cumulative.png")
    except ImportError:
        print("matplotlib unavailable; skipping plot")

    print(f"views: {len(views)} days, {vc[-1] if vc else 0} cumulative")
    print(f"clones: {len(clones)} days, {cc[-1] if cc else 0} cumulative")


if __name__ == "__main__":
    main()
