from typing import Literal

from pydantic import BaseModel, Field, field_validator


Category = Literal[
    "Delay",
    "Crowding",
    "Cleanliness",
    "Safety",
    "Noise",
    "Accessibility",
    "Other",
]
Sentiment = Literal["positive", "neutral", "negative"]


class Station(BaseModel):
    name: str
    name_en: str
    lon: float
    lat: float
    lines: str
    type: str


class FeedbackCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)

    @field_validator("text")
    @classmethod
    def text_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must not be blank or whitespace only")
        return v


class NLPResult(BaseModel):
    text: str
    station: str | None
    station_en: str | None
    lat: float | None
    lon: float | None
    category: Category
    sentiment: Sentiment
    confidence: float = Field(..., ge=0, le=1)
    matched_keywords: list[str]


class FeedbackRecord(NLPResult):
    id: int
    created_at: str


class SeedRequest(BaseModel):
    count: int = Field(default=420, ge=1, le=5000)
    reset: bool = True
    use_real: bool = False


class SentimentAggregate(BaseModel):
    station: str
    station_en: str | None
    lat: float | None
    lon: float | None
    category: Category
    positive: int = 0
    neutral: int = 0
    negative: int = 0


class HotspotPoint(BaseModel):
    station: str
    lat: float
    lon: float
    weight: float
    category: Category
    text: str


class HealthResponse(BaseModel):
    status: str


# ─── Spatial analysis schemas ────────────────────────────────────────────────

class ClusterFeatureProperties(BaseModel):
    cluster_id: int
    is_noise: bool
    station_count: int
    stations: list[str]
    total_negative: int
    total_feedback: int
    neg_rate: float
    category_filter: str
    hull_coords: list[list[float]]


class ClusterSummary(BaseModel):
    n_clusters: int
    n_noise: int
    eps_km: float
    min_samples: int
    category_filter: str


class ClusterResult(BaseModel):
    type: str
    features: list[dict]
    summary: ClusterSummary


class LISAStation(BaseModel):
    station: str
    station_en: str | None
    lat: float
    lon: float
    neg_rate: float
    lisa: str
    lisa_score: float


class MoranResult(BaseModel):
    moran_i: float | None
    expected_i: float | None
    z_score: float | None
    p_value: float | None
    interpretation: str
    category_filter: str
    k_neighbours: int
    stations: list[LISAStation]


class DistrictCompare(BaseModel):
    district: str
    label: str
    station_count: int
    total_feedback: int
    positive: int
    neutral: int
    negative: int
    neg_rate: float
    chi2_statistic: float | None
    chi2_p_value: float | None
    chi2_significant: bool | None
