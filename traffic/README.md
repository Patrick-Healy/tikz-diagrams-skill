# Traffic stats

Accumulated GitHub traffic history. The traffic API only retains ~14 days, so
[`.github/workflows/traffic.yml`](../.github/workflows/traffic.yml) snapshots it
daily (06:00 UTC) and merges into the CSVs here, keeping the max count per date.

- `views.csv` / `clones.csv` — one row per date: `date, count, uniques`
- `cumulative.png` — cumulative views + clones line plot, regenerated each run

Run manually from the **Actions** tab → *Collect traffic stats* → *Run workflow*,
or locally: `GITHUB_REPOSITORY=Patrick-Healy/tikz-diagrams-skill python traffic/collect.py`

![cumulative traffic](cumulative.png)

> Note: traffic endpoints require push access. If the workflow 403s on the
> default `GITHUB_TOKEN`, add a classic PAT (`repo` scope) as the `TRAFFIC_TOKEN`
> repository secret — it's preferred automatically.
