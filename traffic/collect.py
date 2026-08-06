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


def series(data):
    """Return (dates, counts, uniques, cumulative_counts). Uniques are per-day
    and are NOT cumulated — GitHub dedupes them per window, so summing across
    days would double-count returning visitors."""
    dates = sorted(data)
    counts = [data[d][0] for d in dates]
    uniques = [data[d][1] for d in dates]
    cum, running = [], 0
    for c in counts:
        running += c
        cum.append(running)
    return dates, counts, uniques, cum


def write_table(vd, vcount, vuni, vcum, cd, ccount, cuni, ccum):
    lines = [
        "# Traffic — by date",
        "",
        "Cumulative columns are running sums of daily counts. Unique columns are",
        "**per-day** and intentionally not summed (GitHub dedupes uniques within a",
        "window, so cross-day sums would double-count returning visitors).",
        "",
        "| Date | Views | Cum. Views | Unique Viewers | Clones | Cum. Clones | Unique Cloners |",
        "|------|------:|-----------:|---------------:|-------:|------------:|---------------:|",
    ]
    vmap = {d: (vcount[i], vcum[i], vuni[i]) for i, d in enumerate(vd)}
    cmap = {d: (ccount[i], ccum[i], cuni[i]) for i, d in enumerate(cd)}
    for d in sorted(set(vd) | set(cd)):
        v = vmap.get(d, (0, 0, 0))
        c = cmap.get(d, (0, 0, 0))
        lines.append(
            f"| {d} | {v[0]} | {v[1]} | {v[2]} | {c[0]} | {c[1]} | {c[2]} |"
        )
    lines += [
        "",
        f"**Totals:** {vcum[-1] if vcum else 0} cumulative views · "
        f"{ccum[-1] if ccum else 0} cumulative clones",
        "",
        "![cumulative traffic](cumulative.png)",
        "",
    ]
    (HERE / "TRAFFIC.md").write_text("\n".join(lines))
    print("Wrote TRAFFIC.md")


def main():
    views = snapshot("views", "views")
    clones = snapshot("clones", "clones")

    vd, vcount, vuni, vcum = series(views)
    cd, ccount, cuni, ccum = series(clones)

    write_table(vd, vcount, vuni, vcum, cd, ccount, cuni, ccum)

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, (ax1, ax2) = plt.subplots(
            2, 1, figsize=(10, 8), sharex=True,
            gridspec_kw={"height_ratios": [2, 1]},
        )
        # Top: cumulative counts
        ax1.plot(vd, vcum, marker="o", label="Cumulative views", color="#1f77b4")
        ax1.plot(cd, ccum, marker="s", label="Cumulative clones", color="#d62728")
        ax1.set_ylabel("Cumulative count")
        ax1.set_title(f"{REPO} — traffic")
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        # Bottom: daily uniques
        ax2.plot(vd, vuni, marker="o", label="Unique viewers/day", color="#1f77b4",
                 linestyle="--", alpha=0.8)
        ax2.plot(cd, cuni, marker="s", label="Unique cloners/day", color="#d62728",
                 linestyle="--", alpha=0.8)
        ax2.set_ylabel("Unique / day")
        ax2.set_xlabel("Date")
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        fig.autofmt_xdate()
        fig.tight_layout()
        fig.savefig(HERE / "cumulative.png", dpi=120)
        print("Wrote cumulative.png")
    except ImportError:
        print("matplotlib unavailable; skipping plot")

    print(f"views: {len(views)} days, {vcum[-1] if vcum else 0} cumulative")
    print(f"clones: {len(clones)} days, {ccum[-1] if ccum else 0} cumulative")


if __name__ == "__main__":
    main()
