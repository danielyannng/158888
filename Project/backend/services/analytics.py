from __future__ import annotations

from collections import defaultdict

from schemas import Category
from services.feedback_store import list_feedback

CATEGORIES: list[Category] = [
    "Delay",
    "Crowding",
    "Cleanliness",
    "Safety",
    "Noise",
    "Accessibility",
    "Other",
]


def build_sentiment_aggregates() -> list[dict]:
    records = list_feedback()
    grouped: dict[tuple, dict] = {}

    for record in records:
        if not record["station"]:
            continue
        key = (record["station"], record["category"])
        if key not in grouped:
            grouped[key] = {
                "station": record["station"],
                "station_en": record["station_en"],
                "lat": record["lat"],
                "lon": record["lon"],
                "category": record["category"],
                "positive": 0,
                "neutral": 0,
                "negative": 0,
            }
        grouped[key][record["sentiment"]] += 1

    return sorted(
        grouped.values(),
        key=lambda row: (row["station"] or "", row["category"]),
    )


def build_hotspot_points() -> list[dict]:
    records = list_feedback()
    station_negative_counts: defaultdict[str, int] = defaultdict(int)
    for record in records:
        if record["station"] and record["lat"] is not None and record["sentiment"] == "negative":
            station_negative_counts[record["station"]] += 1

    max_count = max(station_negative_counts.values(), default=1)
    points: list[dict] = []
    for record in records:
        if (
            record["sentiment"] != "negative"
            or not record["station"]
            or record["lat"] is None
            or record["lon"] is None
        ):
            continue
        points.append(
            {
                "station": record["station"],
                "lat": record["lat"],
                "lon": record["lon"],
                "weight": round(station_negative_counts[record["station"]] / max_count, 3),
                "category": record["category"],
                "text": record["text"],
            }
        )
    return points
