from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from schemas import (
    ClusterResult,
    DistrictCompare,
    FeedbackCreate,
    FeedbackRecord,
    HealthResponse,
    HotspotPoint,
    MoranResult,
    NLPResult,
    SeedRequest,
    SentimentAggregate,
    Station,
)
from services.analytics import build_hotspot_points, build_sentiment_aggregates
from services.feedback_store import clear_feedback, init_db, list_feedback, save_feedback
from services.geo_layers import (
    bus_stops,
    district_boundary,
    district_options,
    subway_lines,
    subway_stops,
)
from services.ml_model import MODEL_PATH, load_model
from services.nlp_baseline import analyse_feedback, generate_real_feedback, generate_synthetic_feedback
from services.spatial_analysis import (
    dbscan_negative_clusters,
    district_compare,
    morans_i_by_category,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = PROJECT_ROOT / "frontend"
if str(FRONTEND_DIR) not in sys.path:
    sys.path.insert(0, str(FRONTEND_DIR))

from shanghai_metro_data import KEY_STATIONS  # noqa: E402

app = FastAPI(
    title="Shanghai Transit Intelligence API",
    version="0.1.0",
    description="NLP baseline and feedback analytics API for the 158.888 project.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/api/health", response_model=HealthResponse)
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/model/status")
def model_status() -> dict:
    model = load_model()
    if not model:
        return {
            "available": False,
            "path": str(MODEL_PATH),
            "message": "Model artifact not found. Run Project/training/train_nlp_model.py.",
        }
    return {
        "available": True,
        "path": str(MODEL_PATH),
        "version": model.get("version", "unknown"),
        "metrics": model.get("metrics", {}),
    }


@app.get("/api/stations", response_model=list[Station])
def stations() -> list[dict]:
    return KEY_STATIONS


@app.post("/api/feedback", response_model=FeedbackRecord)
def create_feedback(payload: FeedbackCreate) -> dict:
    result = analyse_feedback(payload.text)
    return save_feedback(result)


@app.get("/api/feedback", response_model=list[FeedbackRecord])
def feedback(limit: int | None = Query(default=None, ge=1, le=5000)) -> list[dict]:
    return list_feedback(limit=limit)


@app.get("/api/sentiments", response_model=list[SentimentAggregate])
def sentiments() -> list[dict]:
    return build_sentiment_aggregates()


@app.get("/api/hotspots", response_model=list[HotspotPoint])
def hotspots() -> list[dict]:
    return build_hotspot_points()


@app.post("/api/seed", response_model=list[FeedbackRecord])
def seed(payload: SeedRequest) -> list[dict]:
    if payload.reset:
        clear_feedback()
    records: list[dict] = []
    if payload.use_real:
        texts = generate_real_feedback()
    else:
        texts = generate_synthetic_feedback(count=payload.count)
    for text in texts:
        records.append(save_feedback(analyse_feedback(text)))
    return records


@app.post("/api/seed/real", response_model=list[FeedbackRecord])
def seed_real(reset: bool = True) -> list[dict]:
    """Seed database with real Shanghai Metro passenger feedback from public sources."""
    if reset:
        clear_feedback()
    records: list[dict] = []
    for text in generate_real_feedback():
        records.append(save_feedback(analyse_feedback(text)))
    return records


@app.post("/api/analyse", response_model=NLPResult)
def analyse(payload: FeedbackCreate) -> dict:
    return analyse_feedback(payload.text)


@app.get("/api/gis/districts")
def gis_districts() -> list[dict]:
    return district_options()


@app.get("/api/gis/districts/{district}/boundary")
def gis_district_boundary(district: str) -> dict:
    return _geo_response(district_boundary, district)


@app.get("/api/gis/districts/{district}/bus-stops")
def gis_bus_stops(district: str) -> dict:
    return _geo_response(bus_stops, district)


@app.get("/api/gis/districts/{district}/subway-stops")
def gis_subway_stops(district: str) -> dict:
    return _geo_response(subway_stops, district)


@app.get("/api/gis/districts/{district}/subway-lines")
def gis_subway_lines(district: str) -> dict:
    return _geo_response(subway_lines, district)


@app.get("/api/spatial/clusters")
def spatial_clusters(
    eps_km: float = Query(default=1.5, ge=0.1, le=10.0),
    min_samples: int = Query(default=2, ge=2, le=20),
    category: str | None = Query(default=None),
) -> dict:
    return dbscan_negative_clusters(eps_km=eps_km, min_samples=min_samples, category=category or None)


@app.get("/api/spatial/moran")
def spatial_moran(
    category: str | None = Query(default=None),
    k: int = Query(default=5, ge=2, le=15),
) -> dict:
    return morans_i_by_category(category=category or None, k_neighbours=k)


@app.get("/api/spatial/districts/compare", response_model=list[DistrictCompare])
def spatial_district_compare() -> list[dict]:
    return district_compare()


def _geo_response(loader, district: str) -> dict:
    try:
        return loader(district)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
