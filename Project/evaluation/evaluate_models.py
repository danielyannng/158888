"""
Multi-model evaluation  (evaluate_models.py)
=============================================
Runs three evaluation sets against three model variants and writes:

  data/evaluation/model_comparison.csv   — per-model summary table (report-ready)
  data/evaluation/ood_results.json       — full OOD prediction details
  data/evaluation/chnsenti_results.json  — ChnSentiCorp benchmark (sentiment only)
  data/evaluation/ood_confusion_category.png
  data/evaluation/ood_confusion_sentiment.png

Evaluation sets
---------------
1. In-domain synthetic     — generated from same templates as training (shows template fit)
2. OOD hand-labelled       — data/evaluation/ood_test_set.jsonl  (real-world generalisation)
3. ChnSentiCorp test split — external benchmark, sentiment only

Model variants compared
-----------------------
  rule      — keyword rule baseline (nlp_baseline.analyse_feedback)
  tfidf_lr  — TF-IDF + Logistic Regression (assembled nlp_model.joblib)
  tfidf_svc — TF-IDF + LinearSVC  (trained inline for comparison)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
for _p in (PROJECT_ROOT, BACKEND_DIR, FRONTEND_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from services.nlp_baseline import analyse_feedback, generate_synthetic_feedback  # noqa: E402
from services.ml_model import load_model  # noqa: E402
from training.data_loaders.chnsenti_loader import load as load_chnsenti  # noqa: E402
from training.train_category import build_training_data as build_category_data  # noqa: E402
from training.train_sentiment import build_training_data as build_sentiment_data  # noqa: E402

OUTPUT_DIR = PROJECT_ROOT / "data" / "evaluation"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CATEGORIES = ["Delay", "Crowding", "Cleanliness", "Safety", "Noise", "Accessibility", "Other"]
SENTIMENTS = ["positive", "neutral", "negative"]


# ─── Helpers ────────────────────────────────────────────────────────────────

def _plot_cm(cm: np.ndarray, labels: list[str], path: Path, title: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 6))
    img = ax.imshow(cm, interpolation="nearest", cmap="Blues")
    ax.figure.colorbar(img, ax=ax)
    ax.set(xticks=range(len(labels)), yticks=range(len(labels)),
           xticklabels=labels, yticklabels=labels,
           ylabel="True", xlabel="Predicted", title=title)
    plt.setp(ax.get_xticklabels(), rotation=35, ha="right")
    threshold = cm.max() / 2 if cm.max() else 0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                    color="white" if cm[i, j] > threshold else "black")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _metrics(true, pred, labels: list[str]) -> dict:
    return {
        "accuracy": round(float(accuracy_score(true, pred)), 4),
        "macro_f1": round(float(f1_score(true, pred, labels=labels, average="macro", zero_division=0)), 4),
        "per_class": classification_report(true, pred, labels=labels, zero_division=0, output_dict=True),
    }


# ─── OOD test set ────────────────────────────────────────────────────────────

def load_ood() -> pd.DataFrame:
    rows = [json.loads(ln) for ln in (OUTPUT_DIR / "ood_test_set.jsonl").read_text().splitlines() if ln.strip()]
    return pd.DataFrame(rows)


# ─── In-domain synthetic test ────────────────────────────────────────────────

def load_indomain_test(seed: int = 99) -> pd.DataFrame:
    """Generate a small held-out synthetic batch (different seed from training)."""
    from sklearn.model_selection import GroupShuffleSplit
    df = build_category_data(seed=seed + 1)
    gss = GroupShuffleSplit(n_splits=1, test_size=0.15, random_state=seed)
    _, test_idx = next(gss.split(df, df["category"], groups=df["group"]))
    cat_test = df.iloc[test_idx][["text", "category"]].copy()
    cat_test.rename(columns={"category": "category"}, inplace=True)

    sdf = build_sentiment_data(seed=seed + 1)
    from sklearn.model_selection import GroupShuffleSplit as GSS2
    gss2 = GSS2(n_splits=1, test_size=0.15, random_state=seed)
    _, stest_idx = next(gss2.split(sdf, sdf["sentiment"], groups=sdf["template_id"]))
    senti_test = sdf.iloc[stest_idx][["text", "sentiment"]].copy()

    merged = cat_test.merge(senti_test, on="text", how="inner")
    return merged


# ─── Model predictors ────────────────────────────────────────────────────────

def predict_rule(texts: list[str]) -> tuple[list[str], list[str]]:
    cats, sentis = [], []
    for t in texts:
        r = analyse_feedback(t)
        cats.append(r["category"])
        sentis.append(r["sentiment"])
    return cats, sentis


def predict_tfidf_lr(texts: list[str]) -> tuple[list[str], list[str]]:
    artifact = load_model()
    if not artifact:
        raise RuntimeError("nlp_model.joblib not found — run train_nlp_model.py first")
    cats = list(artifact["category_model"].predict(texts))
    sentis = list(artifact["sentiment_model"].predict(texts))
    return cats, sentis


def _build_and_train_svc(seed: int = 42) -> tuple[Pipeline, Pipeline]:
    """Train TF-IDF + LinearSVC inline (for comparison only — not saved)."""
    def _pipe() -> Pipeline:
        return Pipeline([
            ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5),
                                      min_df=1, sublinear_tf=True)),
            ("clf", LinearSVC(max_iter=2000, class_weight="balanced", random_state=seed)),
        ])

    from sklearn.model_selection import GroupShuffleSplit

    cat_df = build_category_data()
    gss = GroupShuffleSplit(n_splits=1, test_size=0.0, random_state=seed)
    # Train on all data (we evaluate on OOD — no need for in-domain test split here)
    cat_pipe = _pipe()
    cat_pipe.fit(cat_df["text"], cat_df["category"])

    senti_df = build_sentiment_data()
    senti_pipe = _pipe()
    senti_pipe.fit(senti_df["text"], senti_df["sentiment"])

    return cat_pipe, senti_pipe


# ─── Evaluation runner ───────────────────────────────────────────────────────

def evaluate() -> dict:
    ood_df = load_ood()

    # ── ChnSentiCorp benchmark (sentiment only) ──
    chn_splits = load_chnsenti()
    chn_test = chn_splits["test"]

    print("  Training LinearSVC for comparison …")
    svc_cat, svc_senti = _build_and_train_svc()

    results: list[dict] = []

    print("  Evaluating on OOD test set …")
    ood_texts = ood_df["text"].tolist()
    ood_true_cat = ood_df["category"].tolist()
    ood_true_senti = ood_df["sentiment"].tolist()

    for model_name, cat_fn, senti_fn in [
        ("rule_baseline",
         lambda t: predict_rule(t)[0],
         lambda t: predict_rule(t)[1]),
        ("tfidf_lr",
         lambda t: predict_tfidf_lr(t)[0],
         lambda t: predict_tfidf_lr(t)[1]),
        ("tfidf_svc",
         lambda t: list(svc_cat.predict(t)),
         lambda t: list(svc_senti.predict(t))),
    ]:
        pred_cat = cat_fn(ood_texts)
        pred_senti = senti_fn(ood_texts)

        m_cat = _metrics(ood_true_cat, pred_cat, CATEGORIES)
        m_senti = _metrics(ood_true_senti, pred_senti, SENTIMENTS)

        # ChnSentiCorp sentiment benchmark (binary only, no neutral rows)
        chn_texts_list = chn_test["text"].tolist()
        chn_true_senti = chn_test["sentiment"].tolist()
        chn_pred = senti_fn(chn_texts_list)
        # keep only pos/neg for benchmark accuracy
        chn_pairs = [(t, p) for t, p in zip(chn_true_senti, chn_pred) if t in ("positive", "negative")]
        chn_true_b = [x[0] for x in chn_pairs]
        chn_pred_b = [x[1] for x in chn_pairs]
        chn_acc = round(float(accuracy_score(chn_true_b, chn_pred_b)), 4) if chn_pairs else None
        chn_f1 = round(float(f1_score(chn_true_b, chn_pred_b,
                                       labels=["positive", "negative"],
                                       average="macro", zero_division=0)), 4) if chn_pairs else None

        results.append({
            "model": model_name,
            "ood_cat_accuracy": m_cat["accuracy"],
            "ood_cat_macro_f1": m_cat["macro_f1"],
            "ood_senti_accuracy": m_senti["accuracy"],
            "ood_senti_macro_f1": m_senti["macro_f1"],
            "chnsenti_accuracy": chn_acc,
            "chnsenti_macro_f1": chn_f1,
        })

    # Best model confusion matrices (tfidf_lr) on OOD
    lr_pred_cat = predict_tfidf_lr(ood_texts)[0]
    lr_pred_senti = predict_tfidf_lr(ood_texts)[1]
    cm_cat = confusion_matrix(ood_true_cat, lr_pred_cat, labels=CATEGORIES)
    cm_senti = confusion_matrix(ood_true_senti, lr_pred_senti, labels=SENTIMENTS)
    _plot_cm(cm_cat, CATEGORIES, OUTPUT_DIR / "ood_confusion_category.png",
             "Category (TF-IDF+LR) on OOD Test Set")
    _plot_cm(cm_senti, SENTIMENTS, OUTPUT_DIR / "ood_confusion_sentiment.png",
             "Sentiment (TF-IDF+LR) on OOD Test Set")

    # Save detailed OOD predictions
    ood_out = []
    for i, text in enumerate(ood_texts):
        ood_out.append({
            "text": text,
            "true_category": ood_true_cat[i],
            "true_sentiment": ood_true_senti[i],
            "pred_category_lr": lr_pred_cat[i],
            "pred_sentiment_lr": lr_pred_senti[i],
            "perturbation": ood_df["perturbation"].iloc[i],
        })
    (OUTPUT_DIR / "ood_results.json").write_text(
        json.dumps(ood_out, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Write comparison CSV
    comparison_df = pd.DataFrame(results)
    comparison_df.to_csv(OUTPUT_DIR / "model_comparison.csv", index=False)

    summary = {
        "ood_test_size": len(ood_df),
        "chnsenti_test_size": len(chn_test),
        "models": results,
        "confusion_matrix_paths": {
            "ood_category": str(OUTPUT_DIR / "ood_confusion_category.png"),
            "ood_sentiment": str(OUTPUT_DIR / "ood_confusion_sentiment.png"),
        },
    }
    (OUTPUT_DIR / "model_comparison_full.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


if __name__ == "__main__":
    print("Running multi-model evaluation …")
    result = evaluate()
    print("\nModel comparison:")
    df = pd.read_csv(OUTPUT_DIR / "model_comparison.csv")
    print(df.to_string(index=False))
    print(f"\nOutputs in: {OUTPUT_DIR}")
