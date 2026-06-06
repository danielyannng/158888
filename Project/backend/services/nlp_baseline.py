from __future__ import annotations

import random
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIR = PROJECT_ROOT / "frontend"
if str(FRONTEND_DIR) not in sys.path:
    sys.path.insert(0, str(FRONTEND_DIR))

from shanghai_metro_data import KEY_STATIONS  # noqa: E402

try:
    from services.ml_model import predict_with_model
except ImportError:  # Allows direct script execution without package context.
    from ml_model import predict_with_model


CATEGORY_KEYWORDS = {
    "Delay": [
        "晚点",
        "延误",
        "延迟",
        "等很久",
        "等了很久",
        "不准时",
        "delay",
        "delayed",
        "late",
        "waiting",
    ],
    "Crowding": [
        "拥挤",
        "太挤",
        "人多",
        "挤不上",
        "排队",
        "满员",
        "crowded",
        "crowding",
        "packed",
        "full",
    ],
    "Cleanliness": [
        "干净",
        "卫生",
        "垃圾",
        "脏",
        "异味",
        "clean",
        "dirty",
        "smell",
        "trash",
        "hygiene",
    ],
    "Safety": [
        "安全",
        "危险",
        "摔倒",
        "推搡",
        "拥堵危险",
        "security",
        "safe",
        "unsafe",
        "danger",
        "accident",
    ],
    "Noise": [
        "噪音",
        "太吵",
        "吵",
        "广播太响",
        "noise",
        "noisy",
        "loud",
    ],
    "Accessibility": [
        "无障碍",
        "电梯",
        "扶梯",
        "轮椅",
        "坡道",
        "accessible",
        "accessibility",
        "elevator",
        "escalator",
        "wheelchair",
    ],
}

NEGATIVE_KEYWORDS = [
    "严重",
    "糟糕",
    "不好",
    "不方便",
    "太差",
    "投诉",
    "问题",
    "坏了",
    "没有",
    "无法",
    "危险",
    "脏",
    "晚点",
    "延误",
    "拥挤",
    "太挤",
    "吵",
    "negative",
    "bad",
    "poor",
    "terrible",
    "broken",
    "unsafe",
    "dirty",
    "delayed",
    "crowded",
]

POSITIVE_KEYWORDS = [
    "很好",
    "不错",
    "方便",
    "干净",
    "准时",
    "安全",
    "满意",
    "顺畅",
    "positive",
    "good",
    "great",
    "clean",
    "convenient",
    "safe",
    "on time",
]


def _normalise(text: str) -> str:
    return text.strip().lower()


def match_station(text: str) -> dict | None:
    normalised = _normalise(text)
    candidates = sorted(
        KEY_STATIONS,
        key=lambda station: max(len(station["name"]), len(station["name_en"])),
        reverse=True,
    )
    for station in candidates:
        if station["name"] in text or station["name_en"].lower() in normalised:
            return station
    return None


def classify_category(text: str) -> tuple[str, list[str]]:
    normalised = _normalise(text)
    best_category = "Other"
    best_matches: list[str] = []

    for category, keywords in CATEGORY_KEYWORDS.items():
        matches = [kw for kw in keywords if kw.lower() in normalised]
        if len(matches) > len(best_matches):
            best_category = category
            best_matches = matches

    return best_category, best_matches


def classify_sentiment(text: str) -> tuple[str, list[str]]:
    normalised = _normalise(text)
    negative_matches = [kw for kw in NEGATIVE_KEYWORDS if kw.lower() in normalised]
    positive_matches = [kw for kw in POSITIVE_KEYWORDS if kw.lower() in normalised]

    if negative_matches:
        return "negative", negative_matches
    if positive_matches:
        return "positive", positive_matches
    return "neutral", []


def analyse_feedback(text: str) -> dict:
    clean_text = text.strip()
    station = match_station(clean_text)
    rule_category, category_matches = classify_category(clean_text)
    rule_sentiment, sentiment_matches = classify_sentiment(clean_text)
    model_prediction = predict_with_model(clean_text)
    if model_prediction:
        category = model_prediction["category"]
        sentiment = model_prediction["sentiment"]
    else:
        category = rule_category
        sentiment = rule_sentiment
    matched_keywords = sorted(set(category_matches + sentiment_matches))

    if model_prediction:
        confidence = model_prediction["model_confidence"]
        if station:
            confidence = min(confidence + 0.05, 0.99)
    else:
        confidence = 0.45
        if station:
            confidence += 0.2
        if category != "Other":
            confidence += 0.2
        if sentiment != "neutral":
            confidence += 0.1
        confidence += min(len(matched_keywords), 3) * 0.015

    return {
        "text": clean_text,
        "station": station["name"] if station else None,
        "station_en": station["name_en"] if station else None,
        "lat": station["lat"] if station else None,
        "lon": station["lon"] if station else None,
        "category": category,
        "sentiment": sentiment,
        "confidence": round(min(confidence, 0.99), 3),
        "matched_keywords": matched_keywords,
    }


NEGATIVE_TEMPLATES = {
    "Delay": [
        "{station}站今天晚点太严重了",
        "{station}站等了很久还是没有车",
        "{station_en} had a serious delay this morning",
    ],
    "Crowding": [
        "{station}站早高峰太挤了",
        "{station}站人多到挤不上车",
        "{station_en} is packed during rush hour",
    ],
    "Cleanliness": [
        "{station}站地面有垃圾，卫生不好",
        "{station}站有异味，环境太差",
        "{station_en} feels dirty today",
    ],
    "Safety": [
        "{station}站扶梯口推搡很危险",
        "{station}站人流组织不好，存在安全问题",
        "{station_en} feels unsafe at the platform",
    ],
    "Noise": [
        "{station}站广播太响，噪音很大",
        "{station}站施工声音太吵",
        "{station_en} is too noisy today",
    ],
    "Accessibility": [
        "{station}站电梯坏了，很不方便",
        "{station}站无障碍通道不好找",
        "{station_en} elevator is broken and not accessible",
    ],
}

POSITIVE_TEMPLATES = {
    "Delay": [
        "{station}站今天很准时",
        "{station_en} was on time today",
    ],
    "Crowding": [
        "{station}站今天人流顺畅",
        "{station_en} was not crowded today",
    ],
    "Cleanliness": [
        "{station}站很干净",
        "{station_en} is clean and comfortable",
    ],
    "Safety": [
        "{station}站秩序很好，很安全",
        "{station_en} feels safe and well managed",
    ],
    "Noise": [
        "{station}站今天很安静",
        "{station_en} was quiet today",
    ],
    "Accessibility": [
        "{station}站电梯方便，无障碍体验很好",
        "{station_en} has convenient accessibility",
    ],
}

NEUTRAL_TEMPLATES = [
    "{station}站今天客流正常",
    "{station}站有一些乘客排队",
    "{station_en} has normal passenger flow today",
]


def generate_synthetic_feedback(count: int = 420, seed: int = 42) -> list[str]:
    rng = random.Random(seed)
    texts: list[str] = []
    categories = list(CATEGORY_KEYWORDS.keys())

    for i in range(count):
        station = KEY_STATIONS[i % len(KEY_STATIONS)]
        category = categories[i % len(categories)]
        sentiment_roll = rng.random()
        if sentiment_roll < 0.62:
            template = rng.choice(NEGATIVE_TEMPLATES[category])
        elif sentiment_roll < 0.84:
            template = rng.choice(POSITIVE_TEMPLATES[category])
        else:
            template = rng.choice(NEUTRAL_TEMPLATES)

        texts.append(
            template.format(station=station["name"], station_en=station["name_en"])
        )

    rng.shuffle(texts)
    return texts


def generate_real_feedback() -> list[str]:
    """Return real Shanghai Metro passenger feedback collected from public sources.

    Data collected from:
      - 人民网领导留言板 (liuyan.people.com.cn)
      - 上海市交通委公开回复 (jtw.sh.gov.cn)
      - 澎湃新闻/新民晚报 (thepaper.cn)
      - 新浪财经 (finance.sina.com.cn)
      - 静安区政协提案 (jazx.gov.cn)
      - 新闻晨报 (shxwcb.com)
      - 上海地铁官方微博 (@上海地铁shmetro)

    All texts are real, publicly reported passenger feedback.
    """
    from services.real_data import get_real_feedback_texts

    return get_real_feedback_texts()
