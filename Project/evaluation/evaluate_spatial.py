"""
Spatial analysis evaluation  (evaluate_spatial.py)
====================================================
Seeds the SQLite database with synthetic feedback, then runs all three
spatial analyses and writes report-ready artefacts to data/evaluation/:

  spatial_clusters.geojson   — DBSCAN cluster centroids + hull coords
  spatial_moran.json         — Global Moran's I + LISA per station
  district_comparison.csv    — Chi-square test across three districts
  spatial_cluster_map.png    — Static map of cluster centroids

Run:
  python3 evaluation/evaluate_spatial.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
for _p in (PROJECT_ROOT, BACKEND_DIR, FRONTEND_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from services.feedback_store import clear_feedback, init_db, save_feedback  # noqa: E402
from services.nlp_baseline import analyse_feedback, generate_synthetic_feedback  # noqa: E402
from services.spatial_analysis import (  # noqa: E402
    dbscan_negative_clusters,
    district_compare,
    morans_i_by_category,
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "evaluation"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CATEGORIES = ["Delay", "Crowding", "Cleanliness", "Safety", "Noise", "Accessibility"]


def seed_database(n: int = 420) -> int:
    init_db()
    clear_feedback()
    texts = generate_synthetic_feedback(count=n, seed=42)
    for text in texts:
        save_feedback(analyse_feedback(text))
    return n


def run_and_save() -> dict:
    print("  Seeding database …")
    n = seed_database(420)
    print(f"  {n} synthetic feedback records created")

    # ── DBSCAN clusters ──
    print("  Running DBSCAN clustering …")
    clusters = dbscan_negative_clusters(eps_km=1.5, min_samples=2)
    (OUTPUT_DIR / "spatial_clusters.geojson").write_text(
        json.dumps(clusters, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    n_clusters = clusters["summary"]["n_clusters"]
    n_noise = clusters["summary"]["n_noise"]
    print(f"  → {n_clusters} clusters, {n_noise} noise stations")

    # Per-category DBSCAN
    per_category_clusters: dict[str, dict] = {}
    for cat in CATEGORIES:
        per_category_clusters[cat] = dbscan_negative_clusters(eps_km=1.5, min_samples=2, category=cat)
    (OUTPUT_DIR / "spatial_clusters_by_category.json").write_text(
        json.dumps(per_category_clusters, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # ── Moran's I ──
    print("  Computing Moran's I …")
    moran_all = morans_i_by_category()
    (OUTPUT_DIR / "spatial_moran.json").write_text(
        json.dumps(moran_all, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"  → Moran's I = {moran_all['moran_i']}  (p = {moran_all['p_value']})")
    print(f"  → {moran_all['interpretation']}")

    moran_by_cat: dict[str, dict] = {}
    for cat in CATEGORIES:
        moran_by_cat[cat] = morans_i_by_category(category=cat)
    (OUTPUT_DIR / "spatial_moran_by_category.json").write_text(
        json.dumps(moran_by_cat, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # ── District comparison ──
    print("  Running district chi-square comparison …")
    dist_results = district_compare()
    dist_df = pd.DataFrame(dist_results)
    dist_df.to_csv(OUTPUT_DIR / "district_comparison.csv", index=False)
    for row in dist_results:
        print(f"  → {row['label']:8s}  neg_rate={row['neg_rate']}  "
              f"n={row['total_feedback']}  chi2_p={row['chi2_p_value']}")

    # ── Static map ──
    print("  Generating cluster map …")
    _plot_cluster_map(clusters, moran_all)

    summary = {
        "database_records": n,
        "dbscan_summary": clusters["summary"],
        "moran": {
            "i": moran_all["moran_i"],
            "p": moran_all["p_value"],
            "z": moran_all["z_score"],
            "interpretation": moran_all["interpretation"],
        },
        "district_comparison": dist_results,
        "outputs": {
            "clusters_geojson": str(OUTPUT_DIR / "spatial_clusters.geojson"),
            "clusters_by_category": str(OUTPUT_DIR / "spatial_clusters_by_category.json"),
            "moran_json": str(OUTPUT_DIR / "spatial_moran.json"),
            "moran_by_category": str(OUTPUT_DIR / "spatial_moran_by_category.json"),
            "district_comparison_csv": str(OUTPUT_DIR / "district_comparison.csv"),
            "cluster_map_png": str(OUTPUT_DIR / "spatial_cluster_map.png"),
        },
    }
    (OUTPUT_DIR / "spatial_evaluation_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


def _plot_cluster_map(clusters: dict, moran_result: dict) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left: DBSCAN cluster centroids
    ax = axes[0]
    noise_lons, noise_lats = [], []
    cluster_groups: dict[int, list] = {}

    for feat in clusters.get("features", []):
        props = feat["properties"]
        lon, lat = feat["geometry"]["coordinates"]
        cid = props["cluster_id"]
        if props["is_noise"]:
            noise_lons.append(lon)
            noise_lats.append(lat)
        else:
            if cid not in cluster_groups:
                cluster_groups[cid] = []
            cluster_groups[cid].append((lon, lat, props["neg_rate"]))

    if noise_lons:
        ax.scatter(noise_lons, noise_lats, c="lightgray", s=30, label="Noise", zorder=2)

    colors = plt.cm.tab10.colors  # type: ignore[attr-defined]
    for i, (cid, pts) in enumerate(sorted(cluster_groups.items())):
        lons_c = [p[0] for p in pts]
        lats_c = [p[1] for p in pts]
        ax.scatter(lons_c, lats_c, c=[colors[i % 10]], s=80,
                   label=f"Cluster {cid}", zorder=3)

    ax.set_title(
        f"DBSCAN Negative-Feedback Clusters\n"
        f"({clusters['summary']['n_clusters']} clusters, "
        f"eps={clusters['summary']['eps_km']} km)"
    )
    ax.set_xlabel("Longitude (GCJ-02)")
    ax.set_ylabel("Latitude (GCJ-02)")
    if cluster_groups or noise_lons:
        ax.legend(loc="upper left", fontsize=8, ncol=2)

    # Right: LISA heatmap
    ax2 = axes[1]
    lisa_colors = {"HH": "red", "LL": "blue", "HL": "orange", "LH": "lightblue", "NS": "lightgray"}
    lisa_counts: dict[str, int] = {"HH": 0, "LL": 0, "HL": 0, "LH": 0, "NS": 0}

    for s in moran_result.get("stations", []):
        lbl = s["lisa"]
        color = lisa_colors.get(lbl, "gray")
        ax2.scatter(s["lon"], s["lat"], c=color, s=60, zorder=3)
        lisa_counts[lbl] = lisa_counts.get(lbl, 0) + 1

    # Legend
    from matplotlib.patches import Patch
    legend_elems = [Patch(facecolor=c, label=f"{k} (n={lisa_counts[k]})")
                    for k, c in lisa_colors.items()]
    ax2.legend(handles=legend_elems, loc="upper left", fontsize=8)
    mi = moran_result.get("moran_i")
    pv = moran_result.get("p_value")
    ax2.set_title(
        f"LISA Spatial Autocorrelation\n"
        f"Moran's I = {mi}  (p = {pv})"
    )
    ax2.set_xlabel("Longitude (GCJ-02)")
    ax2.set_ylabel("Latitude (GCJ-02)")

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "spatial_cluster_map.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    print("Running spatial evaluation …")
    result = run_and_save()
    print("\nSummary:")
    print(f"  DBSCAN: {result['dbscan_summary']['n_clusters']} clusters")
    print(f"  Moran's I: {result['moran']['i']}  p={result['moran']['p']}")
    print(f"  Outputs: {OUTPUT_DIR}")
