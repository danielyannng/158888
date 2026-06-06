"""
ChnSentiCorp loader  (lansinuote/ChnSentiCorp on HuggingFace)
=========================================================
Labels:  0 = negative, 1 = positive
Returns a dict  {"train": DataFrame, "test": DataFrame, "validation": DataFrame}
each with columns  [text, sentiment]  where sentiment ∈ {"positive","negative"}
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "chnsenticorp"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def load(cache_dir: Path = RAW_DIR) -> dict[str, pd.DataFrame]:
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise RuntimeError("Run: pip install datasets") from exc

    # lansinuote/ChnSentiCorp is a parquet-native mirror (works with datasets >= 2.18)
    ds = load_dataset("lansinuote/ChnSentiCorp", cache_dir=str(cache_dir))

    splits: dict[str, pd.DataFrame] = {}
    for split_name in ds:
        df = ds[split_name].to_pandas()
        # 'label' col: 0=negative, 1=positive
        df = df.rename(columns={"label": "sentiment_int"})[["text", "sentiment_int"]].copy()
        df["sentiment"] = df["sentiment_int"].map({0: "negative", 1: "positive"})
        df = df.drop(columns=["sentiment_int"]).dropna(subset=["text"])
        df["text"] = df["text"].str.strip()
        df = df[df["text"].str.len() > 2].reset_index(drop=True)
        df["source"] = "chnsenticorp"
        splits[split_name] = df

    return splits


def stats(splits: dict[str, pd.DataFrame]) -> None:
    for name, df in splits.items():
        counts = df["sentiment"].value_counts().to_dict()
        print(f"  {name:12s}: {len(df):6d} rows | {counts}")


if __name__ == "__main__":
    print("Downloading ChnSentiCorp …")
    splits = load()
    print(f"Cached to: {RAW_DIR}")
    stats(splits)
    sys.exit(0)
