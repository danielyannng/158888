"""
Weibo Senti 100k loader  (zwn/weibo_senti_100k on HuggingFace, fallback local CSV)
====================================================================================
Labels:  0 = negative, 1 = positive
Returns {"train": DataFrame, "test": DataFrame} with columns [text, sentiment, source]

This dataset is used as a large-scale (100k) backup when ChnSentiCorp (12k) is insufficient,
e.g. for augmenting the sentiment training head.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "weibo_senti"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# HuggingFace dataset id.  The zwn/weibo_senti_100k repo may require a token; if
# it fails we fall back to the older lucadiliello/weibo-senti-100k split.
# Known-working HuggingFace IDs (may change as repos come/go).
# If all fail, place a local weibo_senti.csv with columns [text, label] under RAW_DIR.
_HF_IDS: list[str] = []          # add HF ids here if a new mirror appears
_LOCAL_CSV = RAW_DIR / "weibo_senti.csv"


def load(
    cache_dir: Path = RAW_DIR,
    max_per_class: int | None = 10_000,
) -> dict[str, pd.DataFrame]:
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise RuntimeError("Run: pip install datasets") from exc

    # 1. Try HuggingFace
    ds = None
    last_exc: Exception | None = None
    for hf_id in _HF_IDS:
        try:
            ds = load_dataset(hf_id, cache_dir=str(cache_dir))
            break
        except Exception as exc:  # noqa: BLE001
            last_exc = exc

    # 2. Fallback: local CSV  (columns: text, label where 0=neg 1=pos)
    if ds is None and _LOCAL_CSV.exists():
        import pandas as _pd  # local import to keep top-level clean

        raw = _pd.read_csv(_LOCAL_CSV)
        if "review" in raw.columns:
            raw = raw.rename(columns={"review": "text"})
        raw["sentiment"] = raw["label"].map({0: "negative", 1: "positive"})
        raw["source"] = "weibo_senti_100k_local"
        raw = raw[["text", "sentiment", "source"]]
        from sklearn.model_selection import train_test_split as _tts

        tr, te = _tts(raw, test_size=0.1, random_state=42, stratify=raw["sentiment"])
        return {"train": tr.reset_index(drop=True), "test": te.reset_index(drop=True)}

    if ds is None:
        raise RuntimeError(
            "weibo_senti_100k unavailable via HuggingFace and no local CSV found.\n"
            f"Place a CSV at {_LOCAL_CSV} (columns: text, label) or use ChnSentiCorp alone."
        )

    splits: dict[str, pd.DataFrame] = {}
    for split_name in ds:
        df = ds[split_name].to_pandas()
        # normalise column names across variants
        if "review" in df.columns:
            df = df.rename(columns={"review": "text"})
        if "label" in df.columns:
            df = df.rename(columns={"label": "sentiment_int"})

        df = df[["text", "sentiment_int"]].copy()
        df["sentiment"] = df["sentiment_int"].map({0: "negative", 1: "positive"})
        df = df.drop(columns=["sentiment_int"]).dropna(subset=["text"])
        df["text"] = df["text"].str.strip()
        df = df[df["text"].str.len() > 2]

        if max_per_class is not None:
            df = (
                df.groupby("sentiment", group_keys=False)
                .apply(lambda g: g.sample(min(len(g), max_per_class), random_state=42))
                .reset_index(drop=True)
            )
        else:
            df = df.reset_index(drop=True)

        df["source"] = "weibo_senti_100k"
        splits[split_name] = df

    return splits


def stats(splits: dict[str, pd.DataFrame]) -> None:
    for name, df in splits.items():
        counts = df["sentiment"].value_counts().to_dict()
        print(f"  {name:12s}: {len(df):6d} rows | {counts}")


if __name__ == "__main__":
    print("Downloading weibo_senti_100k …")
    splits = load()
    print(f"Cached to: {RAW_DIR}")
    stats(splits)
    sys.exit(0)
