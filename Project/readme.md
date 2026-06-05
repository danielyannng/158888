# Geo-located NLP Feedback System for Public Transport 🚇

> **Course:** 158.888 Information Technology Research Project (Massey University)
> **Group:** G8
> **Target Case Study:** Shanghai Metro Network

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![NLP](https://img.shields.io/badge/NLP-HuggingFace-yellow)
![GIS](https://img.shields.io/badge/GIS-Spatial%20Analysis-green)

## 📌 Project Overview
This project processes unstructured commuter feedback from social media, classifying specific transit-related concerns (e.g., delays, cleanliness, safety) and detecting spatial trends. By integrating Natural Language Processing (NLP) with Geospatial Information Systems (GIS), the system maps classified text data to physical network nodes, delivering actionable intelligence for transport planners via a real-time visual dashboard.

## 👥 Team Members
* **Yifan Shi** - Lead NLP Engineer (Model training, fine-tuning, metric evaluation)
* **Junzhen Wang** - Geospatial Data Analyst (Data cleaning, geocoding, spatial clustering)
* **Hanwen Yang** - Full-Stack & Dashboard Developer (UI design, Map API integration, deployment)

## 🏗️ Repository Structure

```text
├── data/
│   ├── raw/                  # Scraped raw data (Do not commit large datasets)
│   ├── processed/            # Cleaned and geo-tagged data
├── notebooks/                # Jupyter notebooks for exploratory data analysis (EDA)
├── nlp_pipeline/
│   ├── scraper/              # Scripts to collect social media data
│   ├── preprocessing/        # Text cleaning and tokenization
│   └── models/               # BERT-based aspect & sentiment classification scripts
├── gis_pipeline/
│   ├── geocoding/            # Address-to-coordinate mapping
│   └── clustering/           # Spatial analysis algorithms
├── backend/                  # API server (e.g., FastAPI/Flask) to serve model inferences
├── frontend/                 # Interactive web dashboard (e.g., React/Vue + Mapbox)
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## Run the Prototype

Install dependencies:

```bash
cd /Users/danielyang/Study/158888
python3 -m pip install -r Project/requirements.txt
```

Start the FastAPI backend:

```bash
cd /Users/danielyang/Study/158888/Project/backend
uvicorn app:app --reload --port 8000
```

Start the Streamlit frontend in another terminal:

```bash
cd /Users/danielyang/Study/158888
streamlit run Project/frontend/app.py --server.port 8502
```

Open `http://localhost:8502`, then use **初始化数据** to seed synthetic NLP feedback.

## API Endpoints

- `GET /api/health` - backend status
- `GET /api/model/status` - current NLP model artifact and metrics
- `GET /api/stations` - key Shanghai metro stations
- `POST /api/feedback` - submit one feedback text for NLP analysis
- `GET /api/feedback` - processed feedback records
- `GET /api/sentiments` - station/category sentiment aggregation
- `GET /api/hotspots` - negative-feedback heatmap points
- `POST /api/seed` - reset and generate synthetic feedback
- `GET /api/gis/districts` - available QGIS districts
- `GET /api/gis/districts/{district}/boundary` - district boundary GeoJSON
- `GET /api/gis/districts/{district}/bus-stops` - QGIS bus stop GeoJSON
- `GET /api/gis/districts/{district}/subway-stops` - QGIS subway stop GeoJSON
- `GET /api/gis/districts/{district}/subway-lines` - QGIS subway line GeoJSON

## Evaluation

Run the rule baseline evaluation:

```bash
cd /Users/danielyang/Study/158888/Project
python3 evaluation/evaluate_baseline.py
```

Train or retrain the lightweight NLP model:

```bash
cd /Users/danielyang/Study/158888/Project
python3 training/train_nlp_model.py
```

Outputs are saved under `data/evaluation/` for report evidence.
