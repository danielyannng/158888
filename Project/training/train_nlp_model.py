"""
NLP model assembler  (train_nlp_model.py)
==========================================
Trains both heads (sentiment + category) if their artifacts are absent,
then assembles them into a single nlp_model.joblib expected by
backend/services/ml_model.py.

Usage
-----
  python3 training/train_nlp_model.py          # train both heads then assemble
  python3 training/train_nlp_model.py --assemble-only  # just (re)assemble existing heads

The assembled artifact format is unchanged from the previous version so that
backend/services/ml_model.py requires zero edits.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import joblib

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
OUTPUT_DIR = PROJECT_ROOT / "data" / "evaluation"
MODEL_DIR = BACKEND_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SENTIMENT_MODEL_PATH = MODEL_DIR / "sentiment_model.joblib"
CATEGORY_MODEL_PATH = MODEL_DIR / "category_model.joblib"
ASSEMBLED_PATH = MODEL_DIR / "nlp_model.joblib"

# Add project root + backend/frontend to path so all imports resolve
for _p in (PROJECT_ROOT, BACKEND_DIR, PROJECT_ROOT / "frontend"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))


def train_sentiment_head() -> dict:
    from training.train_sentiment import train
    return train()


def train_category_head() -> dict:
    from training.train_category import train
    return train()


def assemble(sentiment_metrics: dict | None = None, category_metrics: dict | None = None) -> dict:
    """Load individual head models and pack into the shared artifact format."""
    if not SENTIMENT_MODEL_PATH.exists():
        raise FileNotFoundError(f"Sentiment model not found: {SENTIMENT_MODEL_PATH}")
    if not CATEGORY_MODEL_PATH.exists():
        raise FileNotFoundError(f"Category model not found: {CATEGORY_MODEL_PATH}")

    sentiment_model = joblib.load(SENTIMENT_MODEL_PATH)
    category_model = joblib.load(CATEGORY_MODEL_PATH)

    # Reload metrics from disk if not passed in
    if sentiment_metrics is None and (OUTPUT_DIR / "sentiment_train_metrics.json").exists():
        sentiment_metrics = json.loads((OUTPUT_DIR / "sentiment_train_metrics.json").read_text())
    if category_metrics is None and (OUTPUT_DIR / "category_train_metrics.json").exists():
        category_metrics = json.loads((OUTPUT_DIR / "category_train_metrics.json").read_text())

    combined_metrics = {
        "sentiment": sentiment_metrics or {},
        "category": category_metrics or {},
    }

    artifact = {
        "version": "split-head-v1",
        "category_model": category_model,
        "sentiment_model": sentiment_model,
        "metrics": combined_metrics,
    }
    joblib.dump(artifact, ASSEMBLED_PATH)

    summary = {
        "assembled_path": str(ASSEMBLED_PATH),
        "sentiment_accuracy": (sentiment_metrics or {}).get("accuracy", "n/a"),
        "sentiment_macro_f1": (sentiment_metrics or {}).get("macro_f1", "n/a"),
        "category_accuracy": (category_metrics or {}).get("accuracy", "n/a"),
        "category_macro_f1": (category_metrics or {}).get("macro_f1", "n/a"),
        "note": "Separate heads trained independently; assembled for ml_model.py compatibility.",
    }
    (OUTPUT_DIR / "ml_model_metrics.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--assemble-only", action="store_true",
                        help="Skip training; just (re-)assemble existing head artifacts")
    args = parser.parse_args()

    if args.assemble_only:
        print("Assembling existing head models …")
        summary = assemble()
    else:
        print("Step 1/3  Training sentiment head …")
        sm = train_sentiment_head()
        print(f"          accuracy={sm['accuracy']}  macro_f1={sm['macro_f1']}")

        print("Step 2/3  Training category head …")
        cm = train_category_head()
        print(f"          accuracy={cm['accuracy']}  macro_f1={cm['macro_f1']}")

        print("Step 3/3  Assembling combined artifact …")
        summary = assemble(sm, cm)

    print(f"\nDone.  Artifact → {summary['assembled_path']}")
    print(f"  sentiment: accuracy={summary['sentiment_accuracy']}  macro_f1={summary['sentiment_macro_f1']}")
    print(f"  category:  accuracy={summary['category_accuracy']}   macro_f1={summary['category_macro_f1']}")


if __name__ == "__main__":
    main()
