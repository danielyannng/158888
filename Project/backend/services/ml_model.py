from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import joblib

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "nlp_model.joblib"


@lru_cache(maxsize=1)
def load_model() -> dict | None:
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


def predict_with_model(text: str) -> dict | None:
    model = load_model()
    if not model:
        return None

    category_model = model["category_model"]
    sentiment_model = model["sentiment_model"]

    category = str(category_model.predict([text])[0])
    sentiment = str(sentiment_model.predict([text])[0])

    category_confidence = _max_probability(category_model, text)
    sentiment_confidence = _max_probability(sentiment_model, text)

    return {
        "category": category,
        "sentiment": sentiment,
        "model_confidence": round((category_confidence + sentiment_confidence) / 2, 3),
        "model_version": model.get("version", "unknown"),
    }


def _max_probability(model, text: str) -> float:
    if not hasattr(model, "predict_proba"):
        return 0.65
    probabilities = model.predict_proba([text])[0]
    return float(max(probabilities))
