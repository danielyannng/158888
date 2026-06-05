from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from services.nlp_baseline import analyse_feedback  # noqa: E402

OUTPUT_DIR = PROJECT_ROOT / "data" / "evaluation"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CATEGORIES = ["Delay", "Crowding", "Cleanliness", "Safety", "Noise", "Accessibility", "Other"]
SENTIMENTS = ["positive", "neutral", "negative"]

EVAL_CASES = [
    ("人民广场站今天晚点太严重了", "Delay", "negative"),
    ("徐家汇站等了很久还是没有车", "Delay", "negative"),
    ("Century Avenue had a serious delay this morning", "Delay", "negative"),
    ("陆家嘴站今天很准时", "Delay", "positive"),
    ("静安寺站早高峰太挤了", "Crowding", "negative"),
    ("虹桥火车站人多到挤不上车", "Crowding", "negative"),
    ("Lujiazui is packed during rush hour", "Crowding", "negative"),
    ("中山公园站今天人流顺畅", "Crowding", "positive"),
    ("南京东路站地面有垃圾，卫生不好", "Cleanliness", "negative"),
    ("海伦路站有异味，环境太差", "Cleanliness", "negative"),
    ("Hailun Road feels dirty today", "Cleanliness", "negative"),
    ("陆家嘴站很干净", "Cleanliness", "positive"),
    ("豫园站扶梯口推搡很危险", "Safety", "negative"),
    ("曹杨路站人流组织不好，存在安全问题", "Safety", "negative"),
    ("People's Square feels unsafe at the platform", "Safety", "negative"),
    ("世纪大道站秩序很好，很安全", "Safety", "positive"),
    ("四平路站广播太响，噪音很大", "Noise", "negative"),
    ("龙阳路站施工声音太吵", "Noise", "negative"),
    ("Longyang Road is too noisy today", "Noise", "negative"),
    ("徐家汇站今天很安静", "Noise", "positive"),
    ("上海火车站电梯坏了，很不方便", "Accessibility", "negative"),
    ("南京西路站无障碍通道不好找", "Accessibility", "negative"),
    ("Pudong Intl Airport elevator is broken and not accessible", "Accessibility", "negative"),
    ("陆家嘴站电梯方便，无障碍体验很好", "Accessibility", "positive"),
    ("这个地方今天体验一般", "Other", "neutral"),
    ("乘客反馈已经收到", "Other", "neutral"),
    ("No clear station issue in this text", "Other", "neutral"),
]


def evaluate() -> dict:
    rows = []
    for text, expected_category, expected_sentiment in EVAL_CASES:
        prediction = analyse_feedback(text)
        rows.append(
            {
                "text": text,
                "expected_category": expected_category,
                "predicted_category": prediction["category"],
                "expected_sentiment": expected_sentiment,
                "predicted_sentiment": prediction["sentiment"],
                "station": prediction["station"],
                "confidence": prediction["confidence"],
                "matched_keywords": ", ".join(prediction["matched_keywords"]),
            }
        )

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_DIR / "baseline_predictions.csv", index=False)

    category_summary = _classification_summary(
        df["expected_category"],
        df["predicted_category"],
        CATEGORIES,
        "category",
    )
    sentiment_summary = _classification_summary(
        df["expected_sentiment"],
        df["predicted_sentiment"],
        SENTIMENTS,
        "sentiment",
    )

    summary = {
        "dataset": "hand-labelled synthetic public transport feedback cases",
        "case_count": len(df),
        "category": category_summary,
        "sentiment": sentiment_summary,
        "outputs": {
            "predictions_csv": str(OUTPUT_DIR / "baseline_predictions.csv"),
            "category_confusion_csv": str(OUTPUT_DIR / "category_confusion_matrix.csv"),
            "sentiment_confusion_csv": str(OUTPUT_DIR / "sentiment_confusion_matrix.csv"),
            "category_confusion_png": str(OUTPUT_DIR / "category_confusion_matrix.png"),
            "sentiment_confusion_png": str(OUTPUT_DIR / "sentiment_confusion_matrix.png"),
        },
    }
    (OUTPUT_DIR / "baseline_metrics.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return summary


def _classification_summary(expected, predicted, labels: list[str], prefix: str) -> dict:
    cm = confusion_matrix(expected, predicted, labels=labels)
    pd.DataFrame(cm, index=labels, columns=labels).to_csv(
        OUTPUT_DIR / f"{prefix}_confusion_matrix.csv"
    )
    _plot_confusion_matrix(cm, labels, OUTPUT_DIR / f"{prefix}_confusion_matrix.png")
    return {
        "accuracy": round(float(accuracy_score(expected, predicted)), 4),
        "macro_f1": round(float(f1_score(expected, predicted, labels=labels, average="macro")), 4),
        "classification_report": classification_report(
            expected,
            predicted,
            labels=labels,
            zero_division=0,
            output_dict=True,
        ),
    }


def _plot_confusion_matrix(cm, labels: list[str], output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 6))
    image = ax.imshow(cm, interpolation="nearest", cmap="Blues")
    ax.figure.colorbar(image, ax=ax)
    ax.set(
        xticks=range(len(labels)),
        yticks=range(len(labels)),
        xticklabels=labels,
        yticklabels=labels,
        ylabel="Expected",
        xlabel="Predicted",
    )
    plt.setp(ax.get_xticklabels(), rotation=35, ha="right", rotation_mode="anchor")

    threshold = cm.max() / 2 if cm.max() else 0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(
                j,
                i,
                format(cm[i, j], "d"),
                ha="center",
                va="center",
                color="white" if cm[i, j] > threshold else "black",
            )
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, ensure_ascii=False))
