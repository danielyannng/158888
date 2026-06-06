"""
Sentiment head trainer
======================
Trains pos/neg/neutral classifier on:
  - ChnSentiCorp train split  (9 600 rows, real-world hotel/product reviews)
  - Synthetic neutral samples generated from transit templates

GroupShuffleSplit groups by sentence-template-id so no in-distribution leakage.

Outputs
-------
  backend/models/sentiment_model.joblib   — sklearn Pipeline (tfidf + classifier)
  data/evaluation/sentiment_train_metrics.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
for _p in (BACKEND_DIR, FRONTEND_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from training.data_loaders.chnsenti_loader import load as load_chnsenti  # noqa: E402
from services.nlp_baseline import (  # noqa: E402
    NEGATIVE_TEMPLATES,
    NEUTRAL_TEMPLATES,
    POSITIVE_TEMPLATES,
)
from shanghai_metro_data import KEY_STATIONS  # noqa: E402

MODEL_DIR = BACKEND_DIR / "models"
OUTPUT_DIR = PROJECT_ROOT / "data" / "evaluation"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SENTIMENT_MODEL_PATH = MODEL_DIR / "sentiment_model.joblib"


def _build_transit_neutral(seed: int = 158888) -> pd.DataFrame:
    """Generate neutral transit texts from templates (no positive/negative keywords)."""
    import random
    rng = random.Random(seed)
    rows: list[dict] = []
    for station in KEY_STATIONS:
        for template in NEUTRAL_TEMPLATES:
            for _ in range(6):
                text = template.format(station=station["name"], station_en=station["name_en"])
                rows.append({"text": text, "sentiment": "neutral", "template_id": f"neutral_{template[:20]}"})
    rng.shuffle(rows)
    return pd.DataFrame(rows)


def build_training_data() -> pd.DataFrame:
    # ChnSentiCorp (binary: pos / neg)
    splits = load_chnsenti()
    chn_df = pd.concat([splits["train"], splits["validation"]], ignore_index=True)
    chn_df = chn_df[["text", "sentiment"]].copy()
    chn_df["template_id"] = "chnsenti_" + chn_df.index.astype(str)

    # Transit neutral augmentation
    neutral_df = _build_transit_neutral()

    # Add some positive/negative transit samples to expose transit-domain vocab
    transit_rows: list[dict] = []
    for station in KEY_STATIONS:
        for category, templates in NEGATIVE_TEMPLATES.items():
            for tmpl in templates:
                transit_rows.append({
                    "text": tmpl.format(station=station["name"], station_en=station["name_en"]),
                    "sentiment": "negative",
                    "template_id": f"neg_{category}_{tmpl[:15]}",
                })
        for category, templates in POSITIVE_TEMPLATES.items():
            for tmpl in templates:
                transit_rows.append({
                    "text": tmpl.format(station=station["name"], station_en=station["name_en"]),
                    "sentiment": "positive",
                    "template_id": f"pos_{category}_{tmpl[:15]}",
                })
    transit_df = pd.DataFrame(transit_rows)

    df = pd.concat([chn_df, neutral_df, transit_df], ignore_index=True)
    df = df.dropna(subset=["text"]).reset_index(drop=True)
    return df


def train(seed: int = 42) -> dict:
    df = build_training_data()

    # Template-group-aware split: rows with same template_id go into same split
    unique_templates = df["template_id"].unique()
    rng_templates = list(unique_templates)
    from sklearn.model_selection import GroupShuffleSplit
    gss = GroupShuffleSplit(n_splits=1, test_size=0.15, random_state=seed)
    train_idx, test_idx = next(gss.split(df, df["sentiment"], groups=df["template_id"]))
    train_df = df.iloc[train_idx]
    test_df = df.iloc[test_idx]

    model = _pipeline()
    model.fit(train_df["text"], train_df["sentiment"])
    pred = model.predict(test_df["text"])

    labels = ["positive", "neutral", "negative"]
    metrics = {
        "model": "tfidf-logreg-sentiment-v1",
        "train_rows": int(len(train_df)),
        "test_rows": int(len(test_df)),
        "accuracy": round(float(accuracy_score(test_df["sentiment"], pred)), 4),
        "macro_f1": round(float(f1_score(test_df["sentiment"], pred, average="macro", labels=labels, zero_division=0)), 4),
        "classification_report": classification_report(
            test_df["sentiment"], pred, labels=labels, zero_division=0, output_dict=True
        ),
        "note": "GroupShuffleSplit by template_id — no template-level leakage",
    }

    joblib.dump(model, SENTIMENT_MODEL_PATH)
    (OUTPUT_DIR / "sentiment_train_metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    return metrics


def _pipeline() -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(2, 5),
            min_df=2,
            sublinear_tf=True,
            max_features=80_000,
        )),
        ("clf", LogisticRegression(
            C=1.0,
            max_iter=1000,
            class_weight="balanced",
            random_state=42,
            solver="lbfgs",
        )),
    ])


if __name__ == "__main__":
    print("Training sentiment head …")
    m = train()
    print(f"  accuracy={m['accuracy']}  macro_f1={m['macro_f1']}")
    print(f"  Saved → {SENTIMENT_MODEL_PATH}")
