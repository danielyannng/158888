# Methods and Evidence Notes

## Research Alignment

This project implements a geo-located NLP feedback system for public transport (158.888 Brief D.3). It supports the research requirement by connecting:

- unstructured commuter feedback text,
- NLP-based issue category and sentiment classification,
- station-level geolocation,
- spatial hotspot and clustering analysis,
- dashboard evidence for transport planning decisions.

## System Architecture

```
[Public datasets + Synthetic templates]
         │
         ▼
[NLP Training (train_sentiment.py, train_category.py)]
         │
         ▼
[nlp_model.joblib]  ←── loaded by backend/services/ml_model.py
         │
[QGIS shapefile outputs] ──► geo_layers.py ──► GeoJSON (WGS84 → GCJ-02)
         │
         ▼
[FastAPI Backend]  ←── /api/feedback, /api/sentiments, /api/hotspots
                        /api/spatial/clusters, /api/spatial/moran
         │
         ▼
[Streamlit Dashboard]
```

Backend: `backend/`  |  Frontend: `frontend/`  |  GIS sources: `qgis/QGIS/`

## Datasets

### Training data

| Dataset | Size | Labels | Use |
|---|---|---|---|
| lansinuote/ChnSentiCorp | 9 600 train / 1 200 val / 1 200 test | positive / negative | Sentiment head training (real-world Chinese hotel/product reviews) |
| Synthetic transit templates | ≈ 4 600 rows | 6 categories + neutral sentiment | Category head training + sentiment head augmentation |

ChnSentiCorp is a standard benchmark dataset (Tan & Zhang, 2008) for Chinese sentiment analysis. Using it for the sentiment head ensures the model is exposed to natural Chinese sentiment expressions beyond transit-specific templates.

### Evaluation data

| Dataset | Size | Use |
|---|---|---|
| In-domain synthetic held-out | 15% of training templates (GroupShuffleSplit by station) | Shows template-domain fit |
| **OOD hand-labelled set** | **120 rows** | **Primary research evaluation — real-world generalisation** |
| ChnSentiCorp test split | 1 200 rows | External sentiment benchmark |

The OOD set (`data/evaluation/ood_test_set.jsonl`) contains:
- 60 new-template texts (never seen in training; varied sentence structures)
- 30 perturbation samples (typos, synonyms, emoji)
- 30 hard negatives (neutral texts containing emotion-trigger words)

All 120 rows were hand-labelled, then reviewed and corrected.

## NLP Model

### Architecture

Two independently trained heads, assembled into a single `.joblib` artifact:

| Head | Task | Training data | Algorithm |
|---|---|---|---|
| Sentiment | positive / neutral / negative | ChnSentiCorp + synthetic transit | TF-IDF char 2–5 gram + Logistic Regression |
| Category | Delay / Crowding / Cleanliness / Safety / Noise / Accessibility / Other | Synthetic transit templates | TF-IDF char 2–5 gram + Logistic Regression |

GroupShuffleSplit by station name is used for category training — ensures the model is tested on stations it has never seen, while keyword patterns remain in both splits.

### Training commands

```bash
# Train and assemble the full model (runs in ~2 min)
python3 training/train_nlp_model.py

# Train individual heads
python3 training/train_sentiment.py
python3 training/train_category.py
```

### Previous data-leakage issue (resolved)

The earlier version of the pipeline (`tfidf-logreg-v1`) used `train_test_split` on a flat dataframe where training texts and test texts came from the same templates, differing only in station name. This caused perfect accuracy/F1 (1.0) on the test set because the model simply memorised template patterns. This is a known data-leakage pitfall and does not reflect real-world generalisation.

The current version (`split-head-v1`) uses:
1. ChnSentiCorp (external real-world data) for the sentiment head
2. GroupShuffleSplit by station for the category head
3. A separately-constructed OOD test set as the primary evaluation metric

## Evaluation Results

Evaluated across three model variants on the OOD test set:

| Model | OOD Category Accuracy | OOD Category Macro-F1 | OOD Sentiment Accuracy | OOD Sentiment Macro-F1 | ChnSentiCorp Acc |
|---|---|---|---|---|---|
| Rule baseline | 0.583 | 0.588 | 0.542 | 0.441 | 0.911 |
| TF-IDF + LR | 0.583 | 0.588 | 0.542 | 0.441 | 0.911 |
| TF-IDF + LinearSVC | **0.592** | **0.593** | **0.550** | **0.451** | **0.934** |

**Key finding**: TF-IDF + LR produces identical results to the rule baseline. This indicates the ML model has not learned representations beyond keyword-level patterns present in the rule system — a direct consequence of training on template-generated synthetic data. This motivates future use of BERT/RoBERTa models and/or more diverse training corpora.

**OOD category F1 ≈ 0.59** (vs prior in-domain 1.0) is the honest measure of model performance and should be cited in the report.

### Confusion matrices

- `data/evaluation/ood_confusion_category.png` — 7-class category confusion (TF-IDF + LR, OOD)
- `data/evaluation/ood_confusion_sentiment.png` — 3-class sentiment confusion (TF-IDF + LR, OOD)
- `data/evaluation/model_comparison.csv` — full comparison table

### Running all evaluations

```bash
# Full multi-model comparison (primary)
python3 evaluation/evaluate_models.py

# Rule baseline only (legacy 27-case set)
python3 evaluation/evaluate_baseline.py
```

Outputs: `data/evaluation/`

## GIS Data Integration

Backend reads QGIS outputs from `qgis/QGIS/`:

- District boundaries: `huangpu.gpkg`, `hongkou.gpkg`, `pudong.gpkg`
- Subway lines/stops per district: `HP/HK/PD subway line.gpkg`, `HP/HK/PD subway stop.gpkg`
- Bus stops: `huangpu_bus_stop.shp`, `hongkou_bus_stops_.shp`, `pudong_bus_stop.shp`

All files are read as WGS-84 and converted to GCJ-02 for alignment with AMap tile providers in the dashboard.

QGIS preparation workflow:

1. Import the district boundary, subway line, subway stop, and bus stop layers in QGIS.
2. Clip or export the study districts: Huangpu, Hongkou, and Pudong.
3. Save district boundaries and subway layers as `.gpkg`, and bus stops as `.shp`.
4. Store exported files under `qgis/QGIS/`.
5. `backend/services/geo_layers.py` reads the files with GeoPandas, normalises the CRS to WGS-84, keeps useful attributes, adds `district`, `district_label`, and `layer_kind`, converts geometries to GCJ-02, and returns GeoJSON.
6. The Streamlit dashboard renders the resulting GeoJSON in the Metro, Sentiment, Hotspot, and Spatial Insights maps.

Current loaded feature counts:

| District | Boundary | Bus Stops | Subway Stops | Subway Lines |
|---|---:|---:|---:|---:|
| Huangpu | 1 | 330 | 63 | 50 |
| Hongkou | 1 | 332 | 31 | 38 |
| Pudong | 1 | 7251 | 940 | 734 |

## Spatial Analysis

The backend includes a spatial analysis service (`backend/services/spatial_analysis.py`) that applies:

- **DBSCAN clustering** — identifies geographic concentrations of negative feedback using Haversine metric (eps in km)
- **Moran's I** — tests for spatial autocorrelation in negative-feedback intensity across stations; LISA classification (HH/LL/HL/LH)
- **District comparison** — chi-square test of negative-feedback rates across Huangpu, Hongkou, and Pudong, assigning stations to districts with QGIS boundary polygons

API endpoints: `/api/spatial/clusters`, `/api/spatial/moran`, `/api/spatial/districts/compare`

## Current Limitations

1. **Synthetic training data**: Category head trained on template-generated text → limited OOD generalisation (macro-F1 ≈ 0.59). Real commuter feedback would require either crowd-sourced labelling or a domain-specific pre-trained model.
2. **No real commuter data**: Due to ethical/legal constraints on scraping social media, all inference is performed on synthetic transit texts. Findings should be interpreted as a proof-of-concept, not as empirical evidence of real Shanghai metro patterns.
3. **Binary ChnSentiCorp**: The public dataset has no "neutral" label. Neutral detection is trained only on synthetic transit templates and is expected to underperform on ambiguous real-world texts.
4. **Small spatial footprint**: QGIS data covers only three districts (Huangpu, Hongkou, Pudong). Full-network spatial analysis would require data for all Shanghai districts.
