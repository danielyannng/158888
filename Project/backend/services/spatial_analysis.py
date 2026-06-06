"""
Spatial analysis service
========================
Provides three analysis functions consumed by /api/spatial/* endpoints:

  dbscan_negative_clusters(eps_km, min_samples)
      → DBSCAN clusters of negative-feedback stations (Haversine metric)

  morans_i_by_category(category)
      → Global Moran's I + LISA classification per station

  district_compare()
      → Chi-square test of negative-feedback rates across Huangpu / Hongkou / Pudong

All functions operate on the live SQLite feedback table via feedback_store.list_feedback().
"""
from __future__ import annotations

import math
from collections import defaultdict
from functools import lru_cache
from typing import Any

import numpy as np
from shapely.geometry import Point, shape

try:
    from services.feedback_store import list_feedback
    from services.geo_layers import district_boundary, district_options
except ImportError:
    from feedback_store import list_feedback  # direct execution
    from geo_layers import district_boundary, district_options

# ─── District fallback bounding boxes (GCJ-02, approximate) ─────────────────
# Used only if QGIS polygon loading fails.
DISTRICT_BOUNDS = {
    "Huangpu": {"lat_min": 31.215, "lat_max": 31.240, "lon_min": 121.470, "lon_max": 121.510},
    "Hongkou": {"lat_min": 31.240, "lat_max": 31.280, "lon_min": 121.480, "lon_max": 121.520},
    "Pudong":  {"lat_min": 31.170, "lat_max": 31.280, "lon_min": 121.510, "lon_max": 121.620},
}


@lru_cache(maxsize=1)
def _district_polygon_index() -> list[dict]:
    """Load QGIS district boundary polygons transformed to GCJ-02 by geo_layers."""
    polygons: list[dict] = []
    for district in district_options():
        key = district["key"]
        boundary = district_boundary(key)
        geometries = [
            shape(feature["geometry"])
            for feature in boundary.get("features", [])
            if feature.get("geometry")
        ]
        if geometries:
            polygons.append({"district": key, "label": district["label"], "geometries": geometries})
    return polygons


# ─── Haversine helpers ───────────────────────────────────────────────────────

def _haversine_rad(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Return great-circle distance in km (inputs in radians)."""
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 6371.0 * 2 * math.asin(math.sqrt(a))


# ─── Internal: build station-level aggregates ────────────────────────────────

def _aggregate_by_station(category: str | None = None) -> dict[str, dict]:
    """
    Return dict keyed by station name with counts + coords.
    If category is given, filter records to that category.
    """
    records = list_feedback()
    agg: dict[str, dict] = {}
    for rec in records:
        if not rec["station"] or rec["lat"] is None:
            continue
        if category and rec["category"] != category:
            continue
        s = rec["station"]
        if s not in agg:
            agg[s] = {
                "station": s,
                "station_en": rec["station_en"],
                "lat": rec["lat"],
                "lon": rec["lon"],
                "positive": 0,
                "neutral": 0,
                "negative": 0,
            }
        agg[s][rec["sentiment"]] += 1
    return agg


def _station_list(category: str | None = None) -> list[dict]:
    agg = _aggregate_by_station(category)
    return list(agg.values())


# ─── DBSCAN clustering ───────────────────────────────────────────────────────

def dbscan_negative_clusters(
    eps_km: float = 1.5,
    min_samples: int = 2,
    category: str | None = None,
) -> dict:
    """
    Cluster stations with negative feedback using DBSCAN + Haversine metric.

    Returns GeoJSON FeatureCollection where each Feature is a cluster centroid
    (or a noise point labelled cluster_id=-1) plus summary stats per cluster.
    """
    from sklearn.cluster import DBSCAN

    stations = _station_list(category)
    stations = [s for s in stations if s["negative"] > 0]

    if len(stations) < 2:
        return {
            "type": "FeatureCollection",
            "features": [],
            "summary": {"n_clusters": 0, "n_noise": len(stations), "message": "Insufficient negative-feedback stations"},
        }

    coords = np.array([[s["lat"], s["lon"]] for s in stations])
    coords_rad = np.radians(coords)

    eps_rad = eps_km / 6371.0
    db = DBSCAN(eps=eps_rad, min_samples=min_samples, metric="haversine")
    labels = db.fit_predict(coords_rad)

    clusters: dict[int, list[int]] = defaultdict(list)
    for i, lbl in enumerate(labels):
        clusters[int(lbl)].append(i)

    n_clusters = len([k for k in clusters if k != -1])
    features: list[dict] = []

    for cluster_id, indices in sorted(clusters.items()):
        cluster_stations = [stations[i] for i in indices]
        lats = [s["lat"] for s in cluster_stations]
        lons = [s["lon"] for s in cluster_stations]
        total_neg = sum(s["negative"] for s in cluster_stations)
        total_all = sum(s["positive"] + s["neutral"] + s["negative"] for s in cluster_stations)
        neg_rate = round(total_neg / total_all, 3) if total_all else 0.0
        centroid = [sum(lons) / len(lons), sum(lats) / len(lats)]  # [lon, lat] for GeoJSON

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": centroid,
            },
            "properties": {
                "cluster_id": cluster_id,
                "is_noise": cluster_id == -1,
                "station_count": len(cluster_stations),
                "stations": [s["station"] for s in cluster_stations],
                "total_negative": total_neg,
                "total_feedback": total_all,
                "neg_rate": neg_rate,
                "category_filter": category or "all",
                "hull_coords": [[s["lon"], s["lat"]] for s in cluster_stations],
            },
        })

    return {
        "type": "FeatureCollection",
        "features": features,
        "summary": {
            "n_clusters": n_clusters,
            "n_noise": len(clusters.get(-1, [])),
            "eps_km": eps_km,
            "min_samples": min_samples,
            "category_filter": category or "all",
        },
    }


# ─── Moran's I ───────────────────────────────────────────────────────────────

def _knn_weights(coords: np.ndarray, k: int = 5) -> np.ndarray:
    """
    Build row-standardised KNN spatial weights matrix (numpy, no pysal required).
    coords shape: (n, 2) as [lat, lon] degrees.
    Returns dense W matrix (n × n).
    """
    n = len(coords)
    coords_rad = np.radians(coords)
    W = np.zeros((n, n))

    for i in range(n):
        dists = np.array([
            _haversine_rad(coords_rad[i, 0], coords_rad[i, 1],
                           coords_rad[j, 0], coords_rad[j, 1])
            for j in range(n)
        ])
        dists[i] = np.inf
        k_actual = min(k, n - 1)
        nbrs = np.argsort(dists)[:k_actual]
        W[i, nbrs] = 1.0

    # Row-standardise
    row_sums = W.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1.0
    return W / row_sums


def morans_i_by_category(category: str | None = None, k_neighbours: int = 5) -> dict:
    """
    Compute global Moran's I on negative-feedback intensity (neg / total) per station.
    Also returns LISA classification: HH / LL / HL / LH / NS (not significant).
    """
    stations = _station_list(category)
    stations = [s for s in stations if (s["positive"] + s["neutral"] + s["negative"]) > 0]

    if len(stations) < 4:
        return {
            "moran_i": None,
            "expected_i": None,
            "z_score": None,
            "p_value": None,
            "interpretation": "Insufficient stations for spatial autocorrelation analysis",
            "category_filter": category or "all",
            "k_neighbours": k_neighbours,
            "stations": [],
        }

    coords = np.array([[s["lat"], s["lon"]] for s in stations])
    totals = np.array([s["positive"] + s["neutral"] + s["negative"] for s in stations], dtype=float)
    neg_counts = np.array([s["negative"] for s in stations], dtype=float)
    x = np.where(totals > 0, neg_counts / totals, 0.0)

    W = _knn_weights(coords, k=min(k_neighbours, len(stations) - 1))

    # Global Moran's I
    n = len(x)
    x_mean = x.mean()
    z = x - x_mean
    S0 = W.sum()

    numerator = n * float(z @ W @ z)
    denominator = S0 * float(z @ z)
    moran_i = numerator / denominator if denominator != 0 else 0.0

    # Expected value and variance under randomisation
    e_i = -1.0 / (n - 1)
    # Simplified p-value via standard normal approximation
    s1 = 0.5 * np.sum((W + W.T) ** 2)
    s2 = np.sum((W.sum(axis=1) + W.sum(axis=0)) ** 2)
    n2 = n * n
    s12 = s1 / s2 if s2 else 0
    var_i = (
        (n * ((n2 - 3 * n + 3) * s1 - n * s2 + 3 * S0 ** 2))
        / ((n - 1) * (n - 2) * (n - 3) * S0 ** 2)
        - (x ** 4).sum() / (((x - x_mean) ** 2).sum() ** 2 + 1e-12)
        * (n2 * s1 - n * s2 + 3 * S0 ** 2)
        / ((n - 1) * (n - 2) * (n - 3) * S0 ** 2)
        - e_i ** 2
    )

    z_score = (moran_i - e_i) / (math.sqrt(abs(var_i)) + 1e-12)
    # Two-tailed p-value approximation (normal)
    from scipy.special import erfc  # noqa: PLC0415  (lazy import keeps scipy optional)
    p_value = float(erfc(abs(z_score) / math.sqrt(2)))

    # LISA: local indicator
    lz = W @ z  # spatially lagged z
    lisa_scores = z * lz

    lisa_labels: list[str] = []
    sig_threshold = 0.05
    for i in range(n):
        if abs(z_score) < 1.96:  # global not significant — still compute local
            local_sig = False
        else:
            local_sig = True
        if not local_sig:
            lisa_labels.append("NS")
        elif z[i] > 0 and lz[i] > 0:
            lisa_labels.append("HH")  # hot spot
        elif z[i] < 0 and lz[i] < 0:
            lisa_labels.append("LL")  # cold spot
        elif z[i] > 0 and lz[i] < 0:
            lisa_labels.append("HL")  # spatial outlier (high surrounded by low)
        else:
            lisa_labels.append("LH")  # spatial outlier (low surrounded by high)

    station_results = []
    for i, s in enumerate(stations):
        station_results.append({
            "station": s["station"],
            "station_en": s["station_en"],
            "lat": s["lat"],
            "lon": s["lon"],
            "neg_rate": round(float(x[i]), 3),
            "lisa": lisa_labels[i],
            "lisa_score": round(float(lisa_scores[i]), 4),
        })

    interpretation = (
        "positive spatial autocorrelation (negative feedback clusters geographically)"
        if moran_i > 0.1 and p_value < 0.05
        else (
            "negative spatial autocorrelation (negative feedback dispersed)"
            if moran_i < -0.1 and p_value < 0.05
            else "no significant spatial autocorrelation detected"
        )
    )

    return {
        "moran_i": round(float(moran_i), 4),
        "expected_i": round(float(e_i), 4),
        "z_score": round(float(z_score), 4),
        "p_value": round(float(p_value), 4),
        "interpretation": interpretation,
        "category_filter": category or "all",
        "k_neighbours": k_neighbours,
        "stations": station_results,
    }


# ─── District comparison ─────────────────────────────────────────────────────

def _assign_district(lat: float, lon: float) -> str | None:
    point = Point(lon, lat)
    try:
        for district in _district_polygon_index():
            for geom in district["geometries"]:
                if geom.contains(point) or geom.touches(point):
                    return district["district"]
    except Exception:  # noqa: BLE001 - keep spatial API available if local QGIS files fail
        pass

    for name, bounds in DISTRICT_BOUNDS.items():
        if (bounds["lat_min"] <= lat <= bounds["lat_max"] and
                bounds["lon_min"] <= lon <= bounds["lon_max"]):
            return name
    return None


def district_compare() -> list[dict]:
    """
    Chi-square test of negative-feedback rates across the three QGIS districts.
    Station-to-district assignment uses QGIS boundary polygons, with approximate
    bounding boxes only as a fallback if local QGIS files cannot be loaded.
    Returns one dict per district with counts, neg_rate, and per-district chi-square
    p-value (1-vs-rest: this district vs all others combined).
    """
    from scipy.stats import chi2_contingency  # noqa: PLC0415

    stations = _station_list()
    district_counts: dict[str, dict[str, int]] = {
        d: {"positive": 0, "neutral": 0, "negative": 0, "stations": 0}
        for d in DISTRICT_BOUNDS
    }

    for s in stations:
        dist = _assign_district(s["lat"], s["lon"])
        if dist:
            district_counts[dist]["positive"] += s["positive"]
            district_counts[dist]["neutral"] += s["neutral"]
            district_counts[dist]["negative"] += s["negative"]
            district_counts[dist]["stations"] += 1

    # Collect districts that have data
    valid_districts = [
        name for name, counts in district_counts.items()
        if (counts["positive"] + counts["neutral"] + counts["negative"]) > 0
    ]

    results: list[dict] = []
    for name in valid_districts:
        counts = district_counts[name]
        total = counts["positive"] + counts["neutral"] + counts["negative"]
        neg_rate = round(counts["negative"] / total, 3) if total else 0.0

        # Per-district 1-vs-rest chi-square: this district vs all others combined
        other_neg = sum(
            district_counts[d]["negative"] for d in valid_districts if d != name
        )
        other_non_neg = sum(
            district_counts[d]["positive"] + district_counts[d]["neutral"]
            for d in valid_districts if d != name
        )
        this_non_neg = counts["positive"] + counts["neutral"]
        chi2_stat = p_val = None
        if other_neg + other_non_neg > 0:
            try:
                chi2_stat, p_val, _, _ = chi2_contingency(
                    [[counts["negative"], this_non_neg], [other_neg, other_non_neg]]
                )
            except Exception:  # noqa: BLE001
                pass

        results.append({
            "district": name,
            "label": {"Huangpu": "黄浦区", "Hongkou": "虹口区", "Pudong": "浦东新区"}.get(name, name),
            "assignment_method": "qgis_polygon",
            "station_count": counts["stations"],
            "total_feedback": total,
            "positive": counts["positive"],
            "neutral": counts["neutral"],
            "negative": counts["negative"],
            "neg_rate": neg_rate,
            "chi2_statistic": round(float(chi2_stat), 4) if chi2_stat is not None else None,
            "chi2_p_value": round(float(p_val), 4) if p_val is not None else None,
            "chi2_significant": bool(p_val < 0.05) if p_val is not None else None,
        })

    return results
