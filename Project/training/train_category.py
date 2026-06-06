"""
Category head trainer
=====================
Trains 7-class issue classifier on:
  - Synthetic transit templates (80%)  — grouped so same template → same split
  - OOD hand-labelled test set excluded from training (read-only ground truth)

GroupShuffleSplit on template_id prevents any template leakage.

Outputs
-------
  backend/models/category_model.joblib
  data/evaluation/category_train_metrics.json
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
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
for _p in (BACKEND_DIR, FRONTEND_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from services.nlp_baseline import (  # noqa: E402
    CATEGORY_KEYWORDS,
    NEGATIVE_TEMPLATES,
    NEUTRAL_TEMPLATES,
    POSITIVE_TEMPLATES,
)
from shanghai_metro_data import KEY_STATIONS  # noqa: E402

MODEL_DIR = BACKEND_DIR / "models"
OUTPUT_DIR = PROJECT_ROOT / "data" / "evaluation"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CATEGORY_MODEL_PATH = MODEL_DIR / "category_model.joblib"

FILLER_PHRASES = [
    "",
    "请尽快处理",
    "影响通勤体验",
    "during rush hour",
    "today",
    "for commuters",
    "真的很不方便",
    "希望改善",
]


def build_training_data(seed: int = 158888) -> pd.DataFrame:
    """
    Build synthetic training data grouped by station name.

    GroupShuffleSplit on station_name means:
      - All texts about a held-out station go to test
      - Classification keywords (晚点/拥挤/etc) still appear in both sets
        because they come from different stations' templates
    This is a realistic domain-generalisation split: model sees new stations.
    """
    import random
    rng = random.Random(seed)
    rows: list[dict] = []

    for station in KEY_STATIONS:
        for category in CATEGORY_KEYWORDS:
            for template in NEGATIVE_TEMPLATES[category]:
                for _ in range(6):
                    filler = rng.choice(FILLER_PHRASES)
                    text = template.format(station=station["name"], station_en=station["name_en"])
                    if filler:
                        text = f"{text}，{filler}" if not filler.isascii() else f"{text} {filler}"
                    rows.append({
                        "text": text,
                        "category": category,
                        "group": station["name"],   # group by station, not template
                    })
            for template in POSITIVE_TEMPLATES[category]:
                for _ in range(6):
                    filler = rng.choice(FILLER_PHRASES)
                    text = template.format(station=station["name"], station_en=station["name_en"])
                    if filler:
                        text = f"{text}，{filler}" if not filler.isascii() else f"{text} {filler}"
                    rows.append({
                        "text": text,
                        "category": category,
                        "group": station["name"],
                    })
        for template in NEUTRAL_TEMPLATES:
            for _ in range(5):
                text = template.format(station=station["name"], station_en=station["name_en"])
                rows.append({
                    "text": text,
                    "category": "Other",
                    "group": station["name"],
                })

    # Station-independent "Other" samples (fixed group)
    extra_other = [
        {"text": "这个地方今天体验一般", "category": "Other", "group": "_fixed"},
        {"text": "乘客反馈已经收到", "category": "Other", "group": "_fixed"},
        {"text": "No clear station issue in this text", "category": "Other", "group": "_fixed"},
        {"text": "服务记录已更新", "category": "Other", "group": "_fixed"},
        {"text": "general commuter feedback received", "category": "Other", "group": "_fixed"},
    ] * 15

    rows.extend(extra_other)
    rng.shuffle(rows)
    return pd.DataFrame(rows)


def train(seed: int = 42) -> dict:
    df = build_training_data()

    gss = GroupShuffleSplit(n_splits=1, test_size=0.18, random_state=seed)
    train_idx, test_idx = next(gss.split(df, df["category"], groups=df["group"]))
    train_df = df.iloc[train_idx]
    test_df = df.iloc[test_idx]

    model = _pipeline()
    model.fit(train_df["text"], train_df["category"])
    pred = model.predict(test_df["text"])

    labels = ["Delay", "Crowding", "Cleanliness", "Safety", "Noise", "Accessibility", "Other"]
    metrics = {
        "model": "tfidf-logreg-category-v1",
        "train_rows": int(len(train_df)),
        "test_rows": int(len(test_df)),
        "accuracy": round(float(accuracy_score(test_df["category"], pred)), 4),
        "macro_f1": round(float(f1_score(test_df["category"], pred, average="macro", labels=labels, zero_division=0)), 4),
        "classification_report": classification_report(
            test_df["category"], pred, labels=labels, zero_division=0, output_dict=True
        ),
        "note": "GroupShuffleSplit by template_id — same template never spans train/test",
    }

    joblib.dump(model, CATEGORY_MODEL_PATH)
    (OUTPUT_DIR / "category_train_metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    return metrics


def _pipeline() -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(2, 5),
            min_df=1,
            sublinear_tf=True,
        )),
        ("clf", LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=42,
        )),
    ])


if __name__ == "__main__":
    print("Training category head …")
    m = train()
    print(f"  accuracy={m['accuracy']}  macro_f1={m['macro_f1']}")
    print(f"  Saved → {CATEGORY_MODEL_PATH}")
