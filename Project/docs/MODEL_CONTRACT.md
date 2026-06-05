# NLP Model Contract

The backend currently uses a trained lightweight model saved at `backend/models/nlp_model.joblib`, with rule fallback in `backend/services/nlp_baseline.py`. A future teammate model can replace the internal implementation as long as it returns the same fields.

## Input

```python
predict(text: str) -> dict
```

## Required Output

```json
{
  "text": "人民广场站今天晚点太严重了",
  "station": "人民广场",
  "station_en": "People's Square",
  "lat": 31.232687,
  "lon": 121.475108,
  "category": "Delay",
  "sentiment": "negative",
  "confidence": 0.98,
  "matched_keywords": ["晚点", "严重"]
}
```

## Allowed Labels

Categories:

- `Delay`
- `Crowding`
- `Cleanliness`
- `Safety`
- `Noise`
- `Accessibility`
- `Other`

Sentiment:

- `positive`
- `neutral`
- `negative`

## Station Matching

If the model only predicts category and sentiment, keep station matching in the backend using `KEY_STATIONS`. If the model also extracts stations, it must use station names compatible with `frontend/shanghai_metro_data.py`.

## Replacement Rule

Do not change frontend API response fields. Replace only the internals of:

```text
backend/services/nlp_baseline.py::analyse_feedback()
```

This keeps `/api/feedback`, `/api/sentiments`, and `/api/hotspots` stable.

## Current Training Command

```bash
cd /Users/danielyang/Study/158888/Project
python3 training/train_nlp_model.py
```

The current artifact is a TF-IDF + Logistic Regression model trained from synthetic public-transport feedback templates. Treat it as a model-interface baseline until real labelled data is available.
