from __future__ import annotations

import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INTRO_TEXT = PROJECT_ROOT / "docs" / "1_Introduction_extracted_plain.txt"
OUT_MD = PROJECT_ROOT / "docs" / "FINAL_REPORT.md"


TITLE_BLOCK = """# Geo-located NLP Feedback System for Public Transport: A Shanghai Case Study

**Course:** 158.888 Information Technology Research Project  
**Group:** G8  
**System name:** Shanghai Transit Intelligence  
**Case study:** Shanghai metro and bus services  
**Main technologies:** Natural Language Processing, Geographic Information Systems, FastAPI, Streamlit, SQLite, Folium, QGIS, DBSCAN, Moran's I  

---

"""


def clean_intro_text(raw: str) -> str:
    raw = raw.replace("\f", "\n")
    raw = raw.split("\nReferences\n", 1)[0]
    replacements = {
        "1.1 Background\n1.1 Background": "1.1 Background",
        "1.2 Problem Statement\n1.2 Problem Statement": "1.2 Problem Statement",
        "1.3 Research Motivation 1.3 Research Motivation": "1.3 Research Motivation",
        "2.1 Public Transport Service Quality and Passenger\nSatisfaction": (
            "2.1 Public Transport Service Quality and Passenger Satisfaction"
        ),
        "2 literature Review": "2 Literature Review",
        "2.1 Public Transport Service Quality and Passenger\nFeedback": (
            "2.1 Public Transport Service Quality and Passenger Feedback"
        ),
        "transportrelated": "transport-related",
        "usergenerated": "user-generated",
        "usercentred": "user-centred",
        "large-\nscale": "large-scale",
        "largescale": "large-scale",
        "GISbased": "GIS-based",
        "near realtime": "near real-time",
        "decisionmaking": "decision-making",
        "geolocated": "geo-located",
    }
    for old, new in replacements.items():
        raw = raw.replace(old, new)

    lines = [line.strip() for line in raw.splitlines()]
    cleaned_lines: list[str] = []
    previous = ""
    for line in lines:
        if line == previous and re.match(r"^\d", line):
            continue
        cleaned_lines.append(line)
        previous = line

    output: list[str] = []
    para: list[str] = []

    def flush() -> None:
        nonlocal para
        if not para:
            return
        text = " ".join(para)
        text = re.sub(r"\s+", " ", text).strip()
        text = text.replace("large- scale", "large-scale")
        text = text.replace("transport- related", "transport-related")
        output.append(text)
        output.append("")
        para = []

    for line in cleaned_lines:
        if not line:
            flush()
            continue

        if re.match(r"^\d+\s+[A-Z]", line):
            flush()
            output.append(f"## {line}")
            output.append("")
            continue

        if re.match(r"^\d+\.\d+\.\d+\s+", line):
            flush()
            output.append(f"#### {line}")
            output.append("")
            continue

        if re.match(r"^\d+\.\d+\s+", line):
            flush()
            output.append(f"### {line}")
            output.append("")
            continue

        if re.match(r"^RQ\d+:", line):
            flush()
            output.append(line)
            output.append("")
            continue

        if re.match(r"^\d+\.\s+", line):
            flush()
            output.append(line)
            output.append("")
            continue

        if para and para[-1].endswith("-"):
            para[-1] = para[-1][:-1] + line
        else:
            para.append(line)

    flush()
    text = "\n".join(output)
    text = text.replace("## 3 Methodology\n\n### 3.1 Research Design and Overall Approach", "## 3 Methodology\n\n### 3.1 Research Design and Overall Approach")
    return text.strip() + "\n\n"


CONTINUATION = r"""
### 3.2 System Architecture

The system architecture was designed to connect textual feedback processing, geospatial data preparation, backend data services, and web-based visualisation in a single workflow. Instead of treating these components as separate tasks, the project organises them as a pipeline in which each layer produces data that can be used by the next layer. This design was selected because the research problem itself is not only about classifying text or drawing maps, but about linking passenger comments with transport locations in a way that can be explored through an interactive system.

The implemented system contains four main layers. The first layer is the data and model preparation layer. This layer includes the synthetic public transport feedback templates, the hand-labelled out-of-distribution test set, the ChnSentiCorp sentiment dataset, and the QGIS spatial data prepared by the group. It also includes the training scripts used to build the sentiment and category classification models. The second layer is the backend service layer, implemented with FastAPI. The backend receives text from the frontend, applies station matching and NLP analysis, stores processed records in SQLite, and provides API endpoints for feedback records, sentiment aggregation, hotspot data, GIS layers, and spatial statistics. The third layer is the spatial processing layer. It reads QGIS outputs, converts spatial data to GeoJSON, transforms coordinates for AMap compatibility, and calculates DBSCAN clusters, Moran's I, LISA labels, and district comparison results. The fourth layer is the frontend dashboard layer, implemented with Streamlit and Folium. This layer allows users to submit feedback, initialise demonstration data, filter maps, inspect sentiment results, and explore spatial patterns.

In the current implementation, the backend is located in `Project/backend/`, the frontend is located in `Project/frontend/`, model training scripts are located in `Project/training/`, evaluation scripts are stored in `Project/evaluation/`, and QGIS outputs are stored in `Project/qgis/QGIS/`. This structure was useful for the project because it separated responsibilities clearly. Backend services can be tested independently from the dashboard, while the dashboard can be modified without changing the model code. The model contract is also kept stable, which means that a future model can replace the current lightweight classifier without changing the frontend interface.

The system architecture is shown conceptually in Figure 3.1. Passenger feedback is first submitted through the dashboard or generated through the seed endpoint. The backend analyses the text and stores the structured result. Aggregation services then calculate station-level sentiment summaries and hotspot weights. Spatial services use station coordinates to calculate cluster and autocorrelation results. Finally, the Streamlit dashboard displays these results through charts, maps, tables, and model evaluation panels.

### 3.3 Data Processing Workflow

The data processing workflow begins with raw or generated passenger feedback. In the prototype, feedback can be provided through the Streamlit text input form or generated through the `/api/seed` endpoint. The seed function creates a repeatable set of synthetic commuter comments that cover different station names, transport issue categories, and sentiment labels. This repeatable data generation is important because it allows the system to be demonstrated and tested even when live passenger data is not available.

After feedback text is received, the backend applies station matching. The current station matching method checks whether the feedback contains a known Chinese or English station name from the key Shanghai station list. If a station is found, the system attaches the station name, English name, latitude, and longitude to the result. If no station is found, the system still returns an NLP result, but the record is not used for map heatmap generation because it does not contain a reliable geographic point.

The next step is issue classification and sentiment analysis. The system first applies rule-based keyword matching to identify possible categories and sentiment words. These matched keywords are retained because they help explain the classification result. The system then checks whether the trained machine learning model is available. If the model is available, it predicts the category and sentiment. If the model file is missing, the rule result is used as a fallback. This design avoids system failure and keeps the dashboard usable during model development.

The processed feedback record is then saved in SQLite. Each record contains the original text, station information, coordinates, category, sentiment, confidence, matched keywords, and timestamp. Once stored, the record becomes available to the analytics services. The sentiment aggregation service groups feedback by station and category, counting positive, neutral, and negative records. The hotspot service filters negative records with valid coordinates and calculates a relative weight based on the negative-feedback count at each station.

The spatial analysis workflow uses the same stored records but aggregates them at station level. DBSCAN uses station coordinates and negative feedback counts to identify possible clusters. Moran's I calculates whether station-level negative-feedback rates show global spatial autocorrelation. District comparison assigns stations to the supported districts and compares negative rates. This workflow makes the system dynamic: if new feedback is submitted, the database changes, and the dashboard can refresh the analytical outputs.

### 3.4 NLP Processing Methodology

The NLP processing methodology combines a transparent rule baseline with a lightweight machine learning model. This combination was chosen because the project needed a working prototype that could run reliably while still showing a realistic model development process. A pure machine learning approach would require a larger labelled transport feedback dataset, while a pure rule-based system would not demonstrate model evaluation. The hybrid approach therefore provides a practical balance between reliability and research value.

The rule baseline uses keyword dictionaries for the major transport categories. For example, delay-related feedback is identified through words such as "晚点", "延误", "delay", "late", and "waiting". Crowding feedback is associated with words such as "拥挤", "人多", "挤不上", "crowded", and "packed". Similar keyword groups are defined for cleanliness, safety, noise, and accessibility. The sentiment baseline uses negative and positive keyword lists. Negative keywords are checked first because complaints often contain explicit negative service descriptions. If no negative keyword is found but a positive keyword is present, the sentiment is classified as positive. If neither type of keyword is found, the text is treated as neutral.

The machine learning model is implemented as a split-head model. One head predicts the issue category, and the other predicts sentiment. Both heads use TF-IDF character n-gram features and Logistic Regression. Character n-grams were selected because the feedback data contains Chinese text, English text, mixed-language text, station names, and short informal expressions. Character n-grams can represent local text patterns without relying heavily on word segmentation. Logistic Regression was selected because it is efficient, interpretable at a baseline level, and easy to deploy through a local joblib model file.

The model is assembled into `backend/models/nlp_model.joblib`, and the backend loads it through `services/ml_model.py`. The output of the model is kept compatible with the model contract used by the backend. This contract includes category, sentiment, confidence, station information, and matched keywords. The stability of this contract is important because the frontend depends on these fields. If a future model is introduced, it only needs to provide the same output structure.

### 3.5 Spatial Analysis Methodology

The spatial analysis methodology is based on the idea that passenger feedback becomes more useful when it is linked to locations. A negative comment about crowding becomes more meaningful if it can be placed at a specific station or district. For this reason, the system performs spatial analysis only on feedback records that contain a matched station and valid coordinates.

Three spatial techniques are used. The first technique is heatmap visualisation. Negative feedback points are passed to the frontend with a relative weight. This allows the dashboard to show areas where negative records are more concentrated. The second technique is DBSCAN clustering. DBSCAN identifies groups of nearby stations with negative feedback without requiring the number of clusters to be known in advance. It uses the Haversine metric because the station data is represented as longitude and latitude. The third technique is Moran's I, which is used to test whether negative-feedback rates are spatially autocorrelated across stations. The system also generates LISA labels to support local interpretation.

District comparison is included as an additional spatial method. The current implementation uses approximate bounding boxes to assign stations to Huangpu, Hongkou, or Pudong. This is sufficient for demonstrating the workflow, although a more accurate version should use polygon containment based on official district boundaries. The comparison uses a chi-square test to examine whether negative and non-negative feedback rates differ across districts.

### 3.6 Web-based System Development Methodology

The web-based system was developed as a Streamlit dashboard because Streamlit supports rapid development of research prototypes and integrates well with Python-based data analysis. This was suitable for the project because the main goal was to demonstrate a complete analytical workflow rather than build a production front-end framework. Folium and streamlit-folium were used for map rendering because they support interactive map layers, marker popups, heatmaps, layer controls, and integration with GeoJSON data.

The dashboard was designed around the main tasks that a user may need to perform. These tasks include submitting feedback, checking backend connection status, seeding demonstration records, selecting map layers, viewing metro network data, analysing sentiment distribution, identifying hotspots, exploring spatial clusters, and reviewing model evaluation results. The interface is organised into five main tabs: Metro Network, Sentiment Analysis, Hotspot Detection, Spatial Insights, and Methods & Evaluation.

The dashboard also includes a sidebar for configuration. Users can switch between light and dark themes, select district focus, choose the map tile style, toggle key station markers, toggle QGIS bus stops, and filter metro lines. The sidebar also shows model status and backend connection status. This allows the user to understand whether the system is functioning before interpreting the results.

### 3.7 Evaluation Strategy

The evaluation strategy was designed to assess both the individual components and the integrated system. For the NLP component, three evaluation levels were used. The first was a small hand-labelled baseline evaluation containing 27 public transport cases. The second was the training and testing evaluation of the sentiment and category heads. The third was the out-of-distribution evaluation based on 120 hand-labelled transport feedback texts. The OOD evaluation is treated as the most important result because it tests whether the model can handle expressions outside the training templates.

For the spatial analysis component, evaluation was performed on 420 seeded feedback records. The results include DBSCAN cluster counts, noise station counts, Moran's I statistics, and district comparison outputs. These results do not claim to represent real Shanghai passenger behaviour. Instead, they demonstrate that the spatial methods are implemented correctly and can produce interpretable outputs when feedback data is available.

The integrated system was evaluated by checking whether the backend API, SQLite database, NLP analysis, GIS layer conversion, map rendering, and dashboard interaction work together. This included testing the `/api/health`, `/api/feedback`, `/api/sentiments`, `/api/hotspots`, `/api/spatial/clusters`, `/api/spatial/moran`, and GIS endpoints. The dashboard was also tested by submitting sample feedback, initialising synthetic data, viewing sentiment charts, rendering heatmaps, and checking the sidebar behaviour.

### 3.8 Chapter Summary

This chapter described the methodology used in the project. The project follows a design-oriented approach and develops a working prototype that integrates NLP, GIS, spatial analysis, backend APIs, database storage, and web visualisation. The methodology is structured as a pipeline from feedback text to geographic analysis. The following chapter explains the data sources and preparation steps used to support this workflow.

## 4 Data Collection and Preparation

### 4.1 Overview of Data Used in the Project

The project uses several types of data because the system needs to combine textual feedback with transport geography. The main data sources include synthetic public transport feedback, a hand-labelled out-of-distribution test set, the ChnSentiCorp sentiment dataset, key Shanghai metro station data, metro route data, and QGIS spatial files. Each data source serves a different purpose in the project.

The feedback data is used for NLP processing and system demonstration. The station and route data provide the geographic reference needed to locate feedback on the map. The QGIS files provide additional spatial layers for district boundaries, subway lines, subway stops, and bus stops. The evaluation data is used to measure model performance and spatial analysis outputs. Together, these data sources allow the system to move from text analysis to spatial interpretation.

### 4.2 Public Transport Network Data

The transport network data used by the dashboard is stored in `frontend/shanghai_metro_data.py`. This file contains metro route coordinates, metro line information, and key station metadata. Each key station includes its Chinese name, English name, longitude, latitude, line information, and station type. The station list includes important interchange and landmark stations such as People's Square, Lujiazui, Century Avenue, Xujiahui, Jing'an Temple, Zhongshan Park, Hongqiao Railway Station, and Shanghai Railway Station.

This station dataset is important because it connects text to geography. When the backend identifies a station name in a feedback comment, it uses this station list to attach coordinates. Without this step, the system could still classify the text, but it would not be able to display the feedback on a map or include it in spatial analysis.

Metro route data is used to draw the network on the Folium map. The route coordinates are stored as lists of longitude and latitude pairs, and each metro line is associated with its display colour. The dashboard allows users to filter which lines are visible. This provides context for the feedback points and makes it easier to interpret whether issues are located near important interchange areas.

### 4.3 Feedback Data Preparation

The project currently uses synthetic feedback for the working dashboard. This choice was made because collecting real passenger feedback from online platforms may involve ethical, privacy, and data-access concerns. Synthetic feedback allows the system to be developed and tested in a controlled way while still representing common transport issues.

The synthetic generator is implemented in `backend/services/nlp_baseline.py`. It produces feedback records using templates for negative, positive, and neutral comments. The negative templates cover six issue categories: Delay, Crowding, Cleanliness, Safety, Noise, and Accessibility. Positive templates describe improved or satisfactory service conditions, such as clean stations, punctual trains, safe management, and convenient accessibility. Neutral templates describe normal passenger flow or ordinary station use.

The default seed endpoint generates 420 feedback records. The generation process is deterministic because it uses a fixed random seed. This means the same demonstration data can be reproduced, which is useful for testing and reporting. After the seed data is generated, each text is analysed by the backend and stored in SQLite.

Examples of generated feedback include comments such as "人民广场站今天晚点太严重了", "陆家嘴站很干净", and "Century Avenue is packed during rush hour". These examples are not intended to represent real-world data, but they are useful for testing whether station matching, category classification, sentiment analysis, database storage, and map rendering work as expected.

### 4.4 Out-of-distribution Test Set

To avoid relying only on template-based data, the project also uses a hand-labelled out-of-distribution test set. The file is stored at `data/evaluation/ood_test_set.jsonl` and contains 120 feedback records. Each record includes text, category, sentiment, source, and perturbation type. The data includes Chinese, English, and mixed examples. It also includes typos, synonyms, emojis, hard neutral examples, and expressions that do not exactly match the training templates.

This test set is important because it provides a more realistic measure of model generalisation. In-domain synthetic test results can be misleading because the model may learn template structures. The OOD set makes the task harder by using different wording. For example, instead of saying directly that a train was "delayed", a comment may say that passengers waited for half an hour. Instead of using a standard cleanliness keyword, a comment may describe smell, liquid, or rubbish indirectly.

The OOD set contains examples such as "今早人民广场那边出了点问题，等了半个多小时一辆车都没来，气死人了", labelled as Delay and negative. Another example is "陆家嘴站人太塞了😤，早高峰根本挤不上去", labelled as Crowding and negative with emoji perturbation. These examples help reveal whether the model can handle more natural and less template-like feedback.

### 4.5 Sentiment Training Data

The sentiment model uses ChnSentiCorp together with synthetic transit examples. ChnSentiCorp provides Chinese sentiment data with positive and negative labels. It is not a public transport dataset, but it helps expose the sentiment model to natural Chinese opinion expressions. However, it does not contain a neutral label, which creates a limitation for three-class sentiment analysis. For this reason, neutral transit examples are introduced through synthetic templates.

The sentiment head was trained on 10,217 rows and tested on 1,927 rows. The use of GroupShuffleSplit by template ID helps reduce template-level leakage in the synthetic portion of the data. Even so, the sentiment task remains challenging because positive and negative expressions in general review datasets do not always map perfectly to transport feedback.

### 4.6 QGIS Spatial Data

The GIS component uses QGIS outputs stored in `qgis/QGIS/`. The supported districts are Huangpu, Hongkou, and Pudong. The spatial files include district boundaries, subway line layers, subway stop layers, and bus stop layers. These files were prepared in QGIS and then integrated into the backend through `backend/services/geo_layers.py`.

The backend reads these files using GeoPandas. If the file has a coordinate reference system, it is converted to EPSG:4326. If no coordinate reference system is detected, it is treated as EPSG:4326. After the layer is cleaned, the geometry is transformed to GCJ-02. This transformation is necessary because the dashboard uses AMap tiles, and AMap uses GCJ-02 coordinates. Without the transformation, QGIS points and lines would not align correctly with the map background.

The dashboard can display QGIS district boundaries, subway lines, subway stops, and bus stops. This makes the feedback analysis more spatially meaningful because the user can view passenger concerns together with transport infrastructure.

### 4.7 Data Preparation Limitations

The main limitation of the data preparation process is that the feedback records are not real passenger comments collected from live platforms. This limits the ability to make claims about actual service problems in Shanghai. The purpose of the dataset is therefore system demonstration and methodological validation rather than real operational analysis.

A second limitation is that the QGIS data covers only three districts. Although Huangpu, Hongkou, and Pudong are important urban areas, they do not represent the complete Shanghai transport system. Future work should extend the spatial data coverage and include more station and route layers.

Finally, the station matching approach depends on known station names. If a passenger refers to a location indirectly, uses a nickname, or makes a spelling mistake, the system may fail to attach coordinates. This is an important limitation for future location extraction work.

### 4.8 Chapter Summary

This chapter described the data used in the project and explained how it was prepared for the NLP, GIS, and dashboard components. The project uses synthetic feedback for demonstration, a hand-labelled OOD set for evaluation, ChnSentiCorp for sentiment training, station data for geolocation, and QGIS layers for spatial context. The next chapter discusses the NLP implementation and evaluation results in detail.

## 5 NLP Model Implementation and Evaluation

### 5.1 Implementation Overview

The NLP component is responsible for transforming raw feedback text into structured information. In the implemented system, each feedback record is processed to identify the station, issue category, sentiment label, confidence score, and matched keywords. This output is then stored in the database and used by the dashboard.

The main NLP files are `backend/services/nlp_baseline.py`, `backend/services/ml_model.py`, `training/train_sentiment.py`, `training/train_category.py`, and `training/train_nlp_model.py`. The baseline file contains station matching, keyword rules, sentiment rules, and synthetic feedback generation. The model loader file loads the trained joblib model. The training files build the sentiment head, category head, and assembled model artifact.

### 5.2 Station Matching

Station matching is performed before category and sentiment interpretation. The system checks the feedback text against the key station list. Both Chinese station names and English station names are considered. The stations are sorted by name length so that longer station names are checked first. This helps reduce incorrect partial matching when station names overlap.

If a station is matched, the system attaches the station's Chinese name, English name, latitude, and longitude. If no station is matched, the station fields are returned as null. This is an important design choice because the system should not invent a location when it cannot identify one. Records without matched coordinates can still be stored and analysed textually, but they are excluded from heatmap and spatial clustering outputs.

### 5.3 Category Classification

The category classification task uses seven labels: Delay, Crowding, Cleanliness, Safety, Noise, Accessibility, and Other. These categories were selected because they reflect common public transport issues and can be interpreted by planners or operators. Delay and crowding relate to service reliability and passenger capacity. Cleanliness relates to station and carriage conditions. Safety relates to perceived risk and crowd management. Noise relates to the travel environment. Accessibility relates to elevators, escalators, ramps, wheelchairs, and other facilities.

The rule baseline uses keyword lists for each category. For example, Delay includes words such as "晚点", "延误", "delay", and "late". Crowding includes "拥挤", "人多", "crowded", and "packed". Accessibility includes "电梯", "扶梯", "无障碍", "wheelchair", and "elevator". The classifier counts matched keywords and selects the category with the highest number of matches. If no category keyword is found, the result is Other.

The machine learning category head uses TF-IDF character n-grams and Logistic Regression. The category training data contains 4,365 training rows and 1,170 test rows. In the training evaluation, the category model achieved 1.0000 accuracy and 1.0000 macro-F1. This result needs careful interpretation. It shows that the model fits the synthetic template dataset very well, but it does not prove that the model generalises to real-world feedback. This is why the OOD evaluation is more important.

### 5.4 Sentiment Analysis

The sentiment task uses three labels: positive, neutral, and negative. The rule baseline checks negative keywords first, then positive keywords. If neither is found, the text is treated as neutral. This simple method is easy to explain, but it can make mistakes when keywords appear in a negated or neutral context. For example, a sentence saying that a station is "not crowded" contains a crowding keyword but expresses a positive or neutral experience.

The sentiment model is trained using ChnSentiCorp and synthetic transit examples. The sentiment training set contains 10,217 rows, and the test set contains 1,927 rows. The sentiment model achieved 0.8085 accuracy and 0.5653 macro-F1. The macro-F1 is lower than the accuracy because the neutral class is difficult. The ChnSentiCorp dataset is binary, so neutral examples mainly come from synthetic transit data. This affects the model's ability to recognise subtle neutral feedback.

### 5.5 Model Assembly and Backend Deployment

The project uses `training/train_nlp_model.py` to train and assemble the model. The assembled file is saved as `backend/models/nlp_model.joblib`. This file contains both the category model and the sentiment model. The backend loads the model through `services/ml_model.py`. If the model file is missing, the backend returns to the rule baseline.

This design makes the system robust. The dashboard does not depend on the training process being repeated every time. Once the model artifact exists, the backend can load it and use it for prediction. If future work introduces a BERT-based model or another classifier, the replacement can be made inside the model service while keeping the API fields unchanged.

### 5.6 Baseline Evaluation Results

The rule baseline was first evaluated on a small hand-labelled set of 27 public transport feedback cases. This evaluation is stored in `data/evaluation/baseline_metrics.json`. The category task achieved 0.8889 accuracy and 0.8912 macro-F1. The sentiment task achieved 0.7778 accuracy and 0.7493 macro-F1.

These results show that the rule baseline works reasonably well on simple examples. It performs especially well when issue keywords are explicit. However, the evaluation set is small, and the result should not be treated as a complete measure of real-world performance. The baseline is more useful as a reference point for system integration and interpretability.

<!-- pagebreak -->

### 5.7 Out-of-distribution Evaluation

The main NLP evaluation uses the 120-case OOD test set. Three model variants were compared: the rule baseline, TF-IDF with Logistic Regression, and TF-IDF with LinearSVC. The results are shown in Table 5.1.

| Model | OOD Cat. Acc. | OOD Cat. F1 | OOD Sent. Acc. | OOD Sent. F1 | ChnSent. Acc. | ChnSent. F1 |
|---|---:|---:|---:|---:|---:|---:|
| Rule baseline | 0.5833 | 0.5883 | 0.5417 | 0.4410 | 0.9108 | 0.9108 |
| TF-IDF + LR | 0.5833 | 0.5883 | 0.5417 | 0.4410 | 0.9108 | 0.9108 |
| TF-IDF + SVC | 0.5917 | 0.5929 | 0.5500 | 0.4513 | 0.9342 | 0.9342 |

The OOD results show that the current model has limited generalisation. TF-IDF with Logistic Regression performs the same as the rule baseline on the OOD set. TF-IDF with LinearSVC performs slightly better, but the improvement is small. This suggests that the current machine learning model is still strongly dependent on surface-level patterns and keywords. It has not learned a deep semantic understanding of transport feedback.

This result is not necessarily negative for the project. In fact, it provides an honest finding. It shows that template-generated data can support system development but is not enough for robust NLP generalisation. It also supports the argument that future work should use real labelled public transport comments or stronger language models.

### 5.8 Confusion Matrix Evidence

The evaluation script outputs confusion matrices for the OOD test set. The sentiment confusion matrix is stored at `data/evaluation/ood_confusion_sentiment.png`, and the category confusion matrix is stored at `data/evaluation/ood_confusion_category.png`. These figures are included in the Word version of the report.

The confusion matrices help show where the model makes mistakes. In particular, neutral sentiment is difficult because neutral comments may still contain words related to problems, such as delay, crowding, or construction. Category confusion also occurs when one text contains multiple issues. For example, a station may be crowded because a train was delayed, or an accessibility issue may also create a safety concern. A single-label classifier cannot fully represent this complexity.

### 5.9 NLP Evaluation Discussion

The NLP implementation meets the system requirement because it can classify feedback, return structured outputs, support explanation through matched keywords, and provide evaluation evidence. At the same time, the evaluation shows clear limitations. The strongest evidence is the difference between in-domain category performance and OOD performance. The in-domain category model achieved perfect scores, but the OOD macro-F1 was around 0.59. This indicates that the model fits synthetic templates but does not generalise strongly to new expressions.

For the purposes of this project, the model should therefore be described as a baseline. Its value lies in proving that the system can connect NLP outputs to GIS and dashboard components. The model is good enough for prototype integration, but it should not be used for real operational decision-making without further training and validation.

### 5.10 Chapter Summary

This chapter presented the NLP component of the project. The system uses station matching, rule-based classification, a lightweight machine learning model, and a stable output contract. Evaluation results show that the current model provides a useful baseline but has limited OOD generalisation. The next chapter discusses how the structured NLP outputs are used in spatial analysis.

## 6 Spatial Analysis Implementation

### 6.1 Spatial Processing Overview

The spatial analysis component transforms station-level feedback records into geographic outputs. Once feedback records are linked to station coordinates, they can be mapped, clustered, and compared across areas. This is the main reason the project combines NLP with GIS. NLP provides the meaning of the feedback, while GIS provides the geographic context.

The spatial analysis service is implemented in `backend/services/spatial_analysis.py`. It reads records from SQLite and aggregates them by station. For each station, it counts positive, neutral, and negative feedback. It then calculates negative-feedback intensity and applies spatial analysis methods.

### 6.2 Hotspot Heatmap Generation

The hotspot heatmap is generated from negative feedback records that have matched stations and valid coordinates. The backend calculates the number of negative records for each station and normalises the value by the maximum negative count across stations. This produces a weight between 0 and 1. The frontend passes these weighted points into a Folium HeatMap layer.

The heatmap is useful for visual exploration. It allows users to quickly identify areas with more negative feedback in the demonstration data. However, heatmap results should be interpreted carefully. A station with more feedback may appear more intense not because it is worse, but because it is busier or more frequently mentioned. A future version should normalise by station passenger volume or total feedback volume.

### 6.3 DBSCAN Clustering

DBSCAN is used to identify geographic clusters of negative-feedback stations. The method is suitable because the number of clusters does not need to be specified in advance. The backend uses Haversine distance because the input coordinates are geographic coordinates.

The spatial evaluation was conducted on 420 seeded feedback records. With the default parameters of 1.5 km radius and two minimum samples, DBSCAN identified four clusters and eleven noise stations. The cluster output is stored in `data/evaluation/spatial_clusters.geojson`, and the static cluster map is stored in `data/evaluation/spatial_cluster_map.png`.

The DBSCAN output includes the cluster ID, whether the point is noise, station count, station names, total negative records, total feedback, negative rate, and category filter. These properties allow the dashboard to display cluster information in popups and summary indicators.

The result demonstrates that negative feedback can be grouped spatially. However, because the seeded records are synthetic, the cluster locations are not evidence of real Shanghai transport problems. They should be understood as evidence that the method and system integration work.

### 6.4 Moran's I and Local Spatial Association

Moran's I is used to test whether station-level negative-feedback rates are spatially autocorrelated. The negative-feedback rate is calculated as the number of negative records divided by the total number of records at the station. The system builds a K-nearest-neighbour spatial weights matrix and calculates global Moran's I.

The evaluation result was:

| Metric | Value |
|---|---:|
| Moran's I | -0.1030 |
| Expected I | -0.0370 |
| z-score | -0.2001 |
| p-value | 0.8414 |
| Interpretation | No significant spatial autocorrelation detected |

The result indicates that the seeded feedback data does not show significant global spatial clustering of negative-feedback intensity. This is an important result because it shows that the system is not simply forcing a hotspot interpretation. The method can also report when there is no significant spatial pattern.

The system also calculates LISA labels for local interpretation. In the current output, most stations are labelled as not significant. This is consistent with the global Moran's I result. If future real data produces stronger local patterns, the LISA layer could help identify High-High hotspots or local outliers.

### 6.5 District Comparison

The district comparison function compares negative-feedback rates across Huangpu, Hongkou, and Pudong. The current implementation assigns stations to districts using approximate bounding boxes. It then creates a contingency table for negative and non-negative feedback and applies a chi-square test.

The evaluation result is shown in Table 6.1.

| District | Station Count | Total Feedback | Positive | Neutral | Negative | Negative Rate | Chi-square p-value | Significant |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Huangpu | 6 | 90 | 17 | 13 | 60 | 0.667 | 0.3667 | False |
| Hongkou | 2 | 30 | 6 | 4 | 20 | 0.667 | 0.3667 | False |
| Pudong | 2 | 30 | 2 | 4 | 24 | 0.800 | 0.3667 | False |

Pudong has the highest negative rate in the seeded data, but the chi-square result is not significant. Again, this result should not be interpreted as evidence about actual passenger experiences. It demonstrates the method and shows how district-level comparison could be performed when real feedback data is available.

### 6.6 Spatial Analysis Limitations

The spatial analysis has several limitations. First, the dataset is synthetic, so spatial patterns are artificial. Second, district assignment uses bounding boxes rather than polygon containment. This can cause errors near district boundaries. Third, feedback counts are not normalised by station passenger flow. Busy stations may naturally generate more feedback. Fourth, the analysis is not time-aware. Real transport issues often vary by time of day, weekday, weather, and service disruption events.

Despite these limitations, the spatial analysis component is valuable because it completes the NLP-GIS pipeline. It shows that classified feedback can be transformed into maps, clusters, spatial statistics, and district comparison outputs.

### 6.7 Chapter Summary

This chapter described the spatial analysis implementation. The system generates heatmap points, DBSCAN clusters, Moran's I statistics, LISA labels, and district comparison outputs. The evaluation results show that the methods run successfully, although the seeded data does not support strong real-world spatial conclusions. The next chapter describes the web-based system implementation.

## 7 System Implementation

### 7.1 Backend Implementation

The backend is implemented using FastAPI. The main file is `backend/app.py`. FastAPI was selected because it is lightweight, supports clear endpoint definitions, and works well with Python data processing services. The backend is responsible for receiving feedback, running NLP analysis, saving results, returning aggregation outputs, and serving spatial data.

The backend initialises the SQLite database on startup. It also enables CORS so that the Streamlit frontend can call the API locally. The backend service is normally started with the command `uvicorn app:app --reload --port 8000` from the `Project/backend` directory.

The key endpoints include `/api/health`, `/api/model/status`, `/api/stations`, `/api/feedback`, `/api/sentiments`, `/api/hotspots`, `/api/seed`, `/api/analyse`, `/api/gis/districts`, and the spatial endpoints. These endpoints make the backend the central connection point between the NLP model, database, GIS files, and frontend.

### 7.2 SQLite Storage

The feedback database is stored at `backend/db/feedback.db`. The table contains the original text, station name, English station name, latitude, longitude, category, sentiment, confidence, matched keywords, and timestamp. SQLite was selected because it is simple and reliable for a local prototype. It does not require a separate database server, and it is easy to reset through the seed endpoint.

The database design is intentionally minimal. It is not intended to be a full production database schema. However, it supports the main needs of the project: saving processed feedback, retrieving records, building aggregates, and running spatial analysis on current records.

### 7.3 Frontend Dashboard Implementation

The frontend is implemented in `frontend/app.py` using Streamlit. The dashboard uses `requests` to communicate with the backend. It uses Pandas for local table and chart preparation, Folium for maps, and streamlit-folium to display Folium maps inside Streamlit.

The dashboard has a top navigation area with five tabs. The Metro Network tab shows the metro network, station markers, QGIS layers, and key station table. The Sentiment Analysis tab shows sentiment breakdown charts and station-level negative feedback. The Hotspot Detection tab displays the heatmap and hotspot ranking. The Spatial Insights tab shows DBSCAN, Moran's I, LISA, and district comparison outputs. The Methods & Evaluation tab shows model comparison results, confusion matrices, OOD examples, and live inference.

The dashboard also includes a feedback input form. Users can type a comment such as "人民广场站今天晚点太严重了", submit it, and receive a structured NLP result. The result is saved in the database, and the dashboard can be refreshed to update the maps and charts.

### 7.4 Sidebar Controls

The sidebar provides system controls. It displays the backend connection status and backend URL. It includes buttons for refreshing data and initialising synthetic feedback. It also includes map controls such as district focus, QGIS bus stop toggle, key station toggle, station label toggle, map style selector, and metro line filter.

The model card in the sidebar shows whether the model is available. If the model file exists, the sidebar displays the model version and available metrics. This helps the user understand whether the dashboard is using the trained model or fallback rules.

### 7.5 GIS Layer Rendering

GIS layers are rendered through Folium GeoJson and marker layers. When a user selects a district, the frontend requests district boundary, subway line, subway stop, and bus stop data from the backend. The backend reads QGIS files and returns GeoJSON. The frontend then adds these layers to the map.

This is important because it connects the dashboard to the group's QGIS work. The dashboard is not only showing station points from a Python file. It is also able to display QGIS-prepared spatial layers from the project folder. This makes the system more complete from a GIS perspective.

### 7.6 User Interface Design

The interface was refined to look more professional and simpler. The visual style uses a dark theme, clear spacing, compact cards, and restrained colour. The aim was not to make a decorative landing page, but to make an analytical dashboard that is easy to read during demonstration. The cards show key metrics, while the maps and tables provide detailed exploration.

One practical UI issue was fixed during implementation. In Streamlit, collapsing the sidebar can hide the built-in button used to open it again if custom CSS hides the header or toolbar. The final implementation keeps the sidebar expand and collapse button visible. This improves usability because the user can close and reopen the sidebar without losing access to controls.

### 7.7 Methods and Evaluation Page

The Methods & Evaluation tab is included because the project needs to show evidence, not only visual outputs. This tab displays the model comparison CSV, OOD confusion matrices, live inference, OOD test set samples, and training metrics. It allows the report discussion to be supported by visible outputs in the system itself.

This page also helps demonstrate that the project is not simply a mock dashboard. It shows that there is a model evaluation pipeline behind the interface. During presentation, this page can be used to explain the difference between in-domain results and OOD results.

### 7.8 Running the System

The system can be run locally. The dependencies are installed through `requirements.txt`. The backend is started from `Project/backend` using uvicorn, and the frontend is started from the project root using Streamlit. After opening the dashboard, the user can initialise data from the sidebar and then explore all tabs.

The backend health endpoint returns `{"status": "ok"}` when the API is running. The frontend uses this endpoint to display connection status. If the backend is offline, the frontend shows an error instead of crashing.

### 7.9 System Verification

The system was verified through multiple checks. The frontend Python file was compiled to confirm syntax validity. The backend and frontend were run locally. Browser testing confirmed that the dashboard rendered, the backend connection status appeared, the sidebar could be collapsed and reopened, and the main UI remained usable in dark mode. API outputs were also checked through the dashboard and command-line requests.

These checks do not replace formal automated testing, but they confirm that the prototype is functional and suitable for demonstration.

### 7.10 Chapter Summary

This chapter described the implementation of the backend, database, frontend dashboard, GIS layers, and user interface. The system is a complete working prototype that connects NLP processing, spatial analysis, and web visualisation. The following chapter discusses the main findings and limitations of the project.

## 8 Discussion

### 8.1 Achievement of Project Aim

The project achieved its main aim of developing a geo-located NLP feedback system for public transport. The final system is able to process feedback text, identify transport issue categories, predict sentiment, match station names, store records, generate hotspot data, integrate GIS layers, perform spatial analysis, and present results through a web dashboard. This means the project successfully moved beyond a theoretical proposal and produced a working prototype.

The most important achievement is the integration of different technologies. NLP, GIS, backend APIs, database storage, and dashboard visualisation often appear as separate components in transport analysis projects. In this project, they are connected through a shared workflow. A user can submit text in the frontend and see its effect on the database, maps, charts, and spatial analysis outputs.

### 8.2 Interpretation of NLP Findings

The NLP results show that the system works as a baseline but requires stronger data and models for real-world deployment. The in-domain category result is perfect, but this should not be overemphasised. Since the category data is generated from templates, the model can learn patterns that are very close to the test data. The OOD result is more realistic. On the OOD set, the best category macro-F1 is about 0.5929, and the best sentiment macro-F1 is about 0.4513.

These results suggest that the current classifier is useful for demonstrating the system pipeline but not strong enough for operational decision-making. The fact that TF-IDF with Logistic Regression performs the same as the rule baseline shows that the model has not learned much beyond keyword-based patterns. This is an important finding because it shows the limitation of using synthetic templates for NLP training.

At the same time, the model contract and backend design are useful. They allow a future model to replace the current baseline without changing the frontend. Therefore, the project creates a platform for model improvement even if the current model is limited.

### 8.3 Interpretation of Spatial Findings

The spatial analysis results show that the system can produce meaningful spatial outputs, but the current data does not show significant real-world patterns. DBSCAN found four clusters in the seeded data, which demonstrates that the clustering function works. However, Moran's I was -0.1030 with a p-value of 0.8414, indicating no significant global spatial autocorrelation. District comparison also did not show significant differences.

This outcome is reasonable because the data is synthetic. The seeded records were designed to fill the dashboard with examples, not to reproduce real passenger complaint geography. Therefore, the spatial results should be interpreted as method validation rather than transport evidence. The system can calculate and display spatial statistics, but real conclusions would require real feedback data and more careful normalisation.

### 8.4 Strengths of the Project

One strength of the project is that it produces a complete system rather than an isolated model. The user can interact with the dashboard, submit feedback, view maps, inspect model results, and explore spatial analysis. This improves the practical value of the project.

Another strength is the clear separation between frontend and backend. The Streamlit dashboard calls FastAPI endpoints instead of generating all data locally. This makes the architecture more realistic and easier to extend.

A third strength is the integration of QGIS outputs. The system reads the spatial files prepared by the group and converts them into web map layers. This links the GIS work directly with the dashboard.

A fourth strength is that the evaluation is honest. The report does not only show high in-domain metrics. It also includes OOD results that reveal limitations. This makes the project more credible as a research artefact.

### 8.5 Limitations

The project has several important limitations. The first limitation is the lack of real passenger feedback data. The current feedback records are synthetic or hand-labelled test examples. They are useful for demonstration, but they cannot support real operational conclusions about Shanghai Metro or bus services.

The second limitation is model generalisation. The NLP model is trained mainly on synthetic transport templates and external sentiment data. It struggles with varied expressions, subtle neutral cases, and comments that contain multiple issues.

The third limitation is station matching. Exact string matching can fail when users refer to a station indirectly or use informal names. Real user feedback often contains incomplete location references.

The fourth limitation is spatial precision. District assignment currently uses approximate bounding boxes, and station feedback is not normalised by passenger flow. A real system would need better spatial assignment and exposure correction.

The fifth limitation is interface and deployment scale. Streamlit is suitable for the prototype, but a production dashboard may require stronger frontend engineering, authentication, automated tests, and deployment infrastructure.

### 8.6 Practical Implications

Even with these limitations, the project has practical implications. It shows that user feedback can be converted into a form that is easier for planners to inspect. Instead of reading raw comments manually, the system can group them by station, category, sentiment, and district. This could help transport operators identify where more detailed investigation is needed.

The dashboard also shows how feedback analysis can be communicated visually. Maps, heatmaps, cluster layers, and district cards are easier to interpret than raw text files. This is useful for decision-making contexts where different stakeholders need to understand the same information.

The project also shows that evaluation needs to be realistic. If only in-domain synthetic results are reported, the model may appear stronger than it is. The OOD test set gives a more honest view of performance and helps guide future improvement.

### 8.7 Future Work

Future work should first focus on collecting and labelling real public transport feedback. Real feedback would allow the model to learn more natural expressions and would make spatial results more meaningful. The dataset should include different districts, time periods, transport modes, and issue types.

Second, the NLP model should be improved. A transformer-based model such as BERT or RoBERTa could be tested. Multi-label classification should also be considered because many feedback comments mention more than one issue. A future model should also handle typos, synonyms, emojis, and mixed Chinese-English comments more effectively.

Third, the spatial analysis should be improved. District assignment should use polygon containment rather than bounding boxes. Feedback should be normalised by passenger volume or total station feedback. Time-based analysis could be added to identify peak-hour issues or temporary disruptions.

Fourth, the system could be improved as a software product. Docker Compose could make deployment easier. Automated tests could check API behaviour and dashboard outputs. Authentication could be added if the system were used with sensitive feedback data. A more advanced frontend could be developed if more complex user interaction is required.

### 8.8 Research Questions Revisited

The research questions introduced in Chapter 1 can be revisited based on the completed prototype and the evaluation results. The first research question asked what transport-related issues are most frequently discussed by metro and bus users in Shanghai. Because the implemented dataset is mainly synthetic rather than a real online feedback corpus, the project cannot provide a reliable empirical answer about actual Shanghai passengers. However, the system demonstrates how this question could be answered once real comments are available. The classification framework is able to organise comments into delay, crowding, cleanliness, safety, noise, accessibility, and other categories. In the current prototype, these categories are represented in the seeded data so that the dashboard can show how issue frequencies would be calculated and visualised. Therefore, the project answers the question methodologically rather than empirically. It provides the tool and workflow needed to analyse issue frequency, but it does not claim that the synthetic frequencies represent real passenger behaviour.

The second research question asked where these issues are geographically concentrated across the public transport network. The project addresses this question through station matching, coordinate attachment, heatmap visualisation, DBSCAN clustering, Moran's I, and district comparison. The system can identify where negative feedback records are located when a station is matched. The dashboard can display complaint intensity through heatmaps and station bubbles. DBSCAN can group nearby stations with negative feedback, while Moran's I can test whether negative-feedback rates are spatially autocorrelated. In the seeded evaluation, DBSCAN produced four clusters, but Moran's I was not statistically significant. This means that the demonstration data did not show a strong global spatial pattern. The answer to the research question is therefore cautious: the system is capable of identifying geographic concentration, but the current synthetic data does not support a claim about real concentrations.

The third research question asked how NLP and GIS technologies can be integrated to improve the interpretation and visualisation of transport-related user feedback. This question is the strongest part of the project. The implemented architecture shows a clear integration path. NLP extracts structured meaning from text, including station, category, sentiment, confidence, and matched keywords. GIS provides the spatial context through station coordinates, QGIS layers, district boundaries, subway stops, subway lines, and bus stops. The backend connects these layers through API endpoints, and the frontend presents the outputs in interactive maps and charts. This integration improves interpretation because users can see both what kind of issue is being discussed and where it appears in the transport network.

The fourth research question asked to what extent an interactive web-based system can support the exploration and understanding of public transport issues. The dashboard provides evidence that an interactive system can make the analysis more accessible. Users can submit feedback, initialise data, filter metro lines, select district layers, view heatmaps, inspect sentiment distributions, and examine model evaluation results. This is more useful than a static table because it allows users to move between text-level results, station-level results, and spatial-level results. However, the current system remains a research prototype. It supports exploration and demonstration, but it is not yet a professional transport management platform. Its usefulness would increase if connected to real feedback streams, passenger volume data, and a larger GIS database.

### 8.9 Lessons Learned from Prototype Implementation

The implementation process revealed several lessons that are relevant to future projects combining NLP and GIS. The first lesson is that system integration is often as difficult as model development. Building a classifier is only one part of the project. The model output must be stored, aggregated, converted into map-ready formats, and displayed in a way that users can understand. A model that produces category and sentiment labels is not very useful unless those labels can be connected with stations, coordinates, and dashboard components. This is why the project placed emphasis on the API contract and backend services.

The second lesson is that simple baselines are valuable. The rule baseline is not sophisticated, but it helped make the system reliable. It allowed the backend to analyse feedback even before the machine learning model was fully trained. It also provided matched keywords, which helped explain classification decisions. In a research project with limited time, this kind of baseline is useful because it provides a functioning reference point. It also makes it easier to identify whether a machine learning model is genuinely improving on simple keyword logic.

The third lesson is that synthetic data is useful but risky. Synthetic templates made it possible to build and test the dashboard without collecting real passenger comments. They also ensured that all categories were represented. However, the OOD evaluation showed that template data can make a model appear stronger than it actually is. This is an important methodological issue. If the project only reported in-domain scores, it would give an overly positive impression. The OOD test set made the evaluation more realistic and revealed the need for better training data.

The fourth lesson is that spatial analysis needs careful interpretation. A heatmap can look convincing even when the underlying data is synthetic or biased. A cluster can be produced by an algorithm, but that does not automatically mean the cluster represents a real transport problem. For this reason, the report interprets spatial outputs carefully. DBSCAN, Moran's I, and district comparison are presented as implemented methods and demonstration results rather than evidence of actual service conditions.

The fifth lesson is that dashboard usability affects the credibility of the prototype. A system may have correct backend logic, but if the interface is confusing or visually broken, it becomes harder to demonstrate. The sidebar issue in Streamlit was a good example. When the sidebar could not be reopened after being collapsed, the interface became less reliable. Fixing this problem improved the practical quality of the artefact. Small user interface details therefore matter, especially in a project that must be demonstrated to an audience.

### 8.10 Implications for the Final Project Demonstration

The final system can be demonstrated in a structured sequence. First, the presenter can explain the research gap: transport feedback is textual, while transport planning often needs spatial evidence. Second, the dashboard can be opened to show the backend connection and model status. Third, the presenter can submit a sample comment, such as "人民广场站今天晚点太严重了", and show that the system identifies the station, category, sentiment, confidence score, and matched keywords. This provides a direct example of the NLP pipeline.

After the live inference example, the presenter can initialise the seeded data and move to the Sentiment Analysis tab. This tab can be used to explain how individual feedback records become aggregated station and category statistics. The Hotspot Detection tab can then be used to show how negative feedback becomes a heatmap. This helps the audience understand the link between sentiment analysis and spatial visualisation.

The Spatial Insights tab should be used to explain the GIS contribution. The presenter can show DBSCAN clusters, Moran's I values, and district comparison cards. It is important to state clearly that the data is synthetic and that the spatial results demonstrate the method rather than real passenger patterns. This honest interpretation is likely to be stronger than overstating the results.

The Methods & Evaluation tab should be used near the end of the demonstration. It shows that the project includes evaluation evidence, not only a visual interface. The model comparison table and confusion matrices can be used to explain that the current model is a baseline. The presenter can highlight that OOD performance is modest and that this motivates future work with real labelled data and stronger models. This makes the project appear more research-aware and less like a simple dashboard exercise.

### 8.11 Chapter Summary

This chapter discussed the findings, strengths, limitations, and future work of the project. The system successfully demonstrates the integration of NLP and GIS for public transport feedback analysis. However, the results also show that stronger data and models are needed before the system can support real operational decisions.

## 9 Conclusion

This project developed a Geo-located NLP Feedback System for Public Transport using Shanghai as a case-study city. The system integrates passenger feedback analysis, station matching, NLP classification, sentiment analysis, GIS layer processing, spatial analysis, backend APIs, database storage, and web-based visualisation. The final prototype is implemented as a Streamlit dashboard connected to a FastAPI backend.

The project demonstrates that unstructured transport feedback can be transformed into structured information. A feedback text can be analysed to identify a station, category, sentiment, confidence score, and matched keywords. Once stored in the database, these outputs can be aggregated into station-level statistics, heatmaps, hotspot rankings, spatial clusters, Moran's I results, and district comparison tables.

The NLP evaluation shows that the current model is useful as a baseline but limited in real-world generalisation. The OOD results are modest, especially for sentiment macro-F1. This reflects the limitations of synthetic training data and keyword-dependent approaches. However, the system design allows future models to replace the current baseline through the same API contract.

The spatial analysis evaluation shows that the system can perform DBSCAN clustering, Moran's I analysis, LISA labelling, and district comparison. The seeded data did not show significant spatial autocorrelation, but this is an honest and expected result for demonstration data. The value of the spatial component is that it proves the feedback-to-map pipeline works.

Overall, the project provides a practical research prototype that connects NLP and GIS in the context of public transport service analysis. It contributes a working system architecture, an interpretable baseline, a replaceable model interface, QGIS integration, spatial analytics, and dashboard-based visualisation. With real passenger feedback data, stronger NLP models, and expanded GIS coverage, the system could be developed further into a more robust decision-support tool for public transport planning and smart-city applications.

## References

Aggarwal, C. C., & Zhai, C. (2012). Mining Text Data. Springer. https://doi.org/10.1007/978-1-4614-3223-4

Anselin, L. (1995). Local indicators of spatial association: LISA. Geographical Analysis, 27(2), 93-115.

Batty, M., Axhausen, K. W., Giannotti, F., Pozdnoukhov, A., Bazzani, A., Wachowicz, M., Ouzounis, G., & Portugali, Y. (2012). Smart cities of the future. The European Physical Journal Special Topics, 214, 481-518. https://doi.org/10.1140/epjst/e2012-01703-3

Cheung, C. M. K., & Thadani, D. R. (2012). The impact of electronic word-of-mouth communication: A literature analysis and integrative model. Decision Support Systems, 54(1), 461-470. https://doi.org/10.1016/j.dss.2012.06.008

de Oña, J., & de Oña, R. (2015). Quality of service in public transport based on customer satisfaction surveys: A review and assessment of methodological approaches. Transportation Science, 49(3), 605-622. https://doi.org/10.1287/trsc.2014.0544

Dou, M., Gu, Y., & Gong, J. (2024). How do people perceive the quality of urban transport service? New insights from online reviews of Shanghai metro system. Journal of Urban Management, 13(4), 705-719. https://doi.org/10.1016/j.jum.2024.07.008

Eboli, L., & Mazzulla, G. (2007). Service quality attributes affecting customer satisfaction for bus transit. Journal of Public Transportation, 10(3), 21-34. https://doi.org/10.5038/2375-0901.10.3.2

Ester, M., Kriegel, H.-P., Sander, J., & Xu, X. (1996). A density-based algorithm for discovering clusters in large spatial databases with noise. Proceedings of the Second International Conference on Knowledge Discovery and Data Mining, 226-231.

Few, S. (2006). Information Dashboard Design: The Effective Visual Communication of Data. O'Reilly Media.

Goodchild, M. F. (2007). Citizens as sensors: The world of volunteered geography. GeoJournal, 69, 211-221.

Jurafsky, D., & Martin, J. H. (2024). Speech and Language Processing: An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition (3rd ed. draft). Stanford University. https://web.stanford.edu/~jurafsky/slp3/

Kaplan, A. M., & Haenlein, M. (2010). Users of the world, unite! The challenges and opportunities of social media. Business Horizons, 53(1), 59-68. https://doi.org/10.1016/j.bushor.2009.09.003

Liu, B. (2012). Sentiment Analysis and Opinion Mining. Morgan & Claypool Publishers. https://doi.org/10.2200/S00416ED1V01Y201204HLT016

Longley, P. A., Goodchild, M. F., Maguire, D. J., & Rhind, D. W. (2015). Geographic Information Science and Systems (4th ed.). Wiley.

Moran, P. A. P. (1950). Notes on continuous stochastic phenomena. Biometrika, 37(1/2), 17-23.

Nathanail, E. (2008). Measuring the quality of service for passengers on the Hellenic railways. Transportation Research Part A: Policy and Practice, 42(1), 48-66. https://doi.org/10.1016/j.tra.2007.06.006

Pang, B., & Lee, L. (2008). Opinion mining and sentiment analysis. Foundations and Trends in Information Retrieval, 2(1-2), 1-135. https://doi.org/10.1561/1500000011

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, E. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825-2830.

Sobral, T., Galvão, T., & Borges, J. (2019). Visualization of urban mobility data from intelligent transportation systems. Sensors, 19(2), 332. https://doi.org/10.3390/s19020332

Zheng, Y., Capra, L., Wolfson, O., & Yang, H. (2014). Urban computing: Concepts, methodologies, and applications. ACM Transactions on Intelligent Systems and Technology, 5(3), Article 38. https://doi.org/10.1145/2629592

## Appendix A Project Evidence Files

The following files are used as evidence for the implementation and evaluation of the project.

| Evidence Area | File |
|---|---|
| Frontend dashboard | `Project/frontend/app.py` |
| Backend API | `Project/backend/app.py` |
| API schemas | `Project/backend/schemas.py` |
| NLP baseline | `Project/backend/services/nlp_baseline.py` |
| Model loading | `Project/backend/services/ml_model.py` |
| SQLite storage | `Project/backend/services/feedback_store.py` |
| Analytics service | `Project/backend/services/analytics.py` |
| GIS layer conversion | `Project/backend/services/geo_layers.py` |
| Spatial analysis | `Project/backend/services/spatial_analysis.py` |
| Model training | `Project/training/train_nlp_model.py` |
| Model comparison | `Project/data/evaluation/model_comparison.csv` |
| OOD sentiment matrix | `Project/data/evaluation/ood_confusion_sentiment.png` |
| OOD category matrix | `Project/data/evaluation/ood_confusion_category.png` |
| Spatial cluster map | `Project/data/evaluation/spatial_cluster_map.png` |

## Appendix B Main Run Commands

The backend can be started using:

```bash
cd /Users/danielyang/Study/158888/Project/backend
uvicorn app:app --reload --port 8000
```

The frontend can be started using:

```bash
cd /Users/danielyang/Study/158888
streamlit run Project/frontend/app.py --server.port 8502
```

The NLP model can be trained using:

```bash
cd /Users/danielyang/Study/158888/Project
python3 training/train_nlp_model.py
```

The model and spatial evaluations can be run using:

```bash
cd /Users/danielyang/Study/158888/Project
python3 evaluation/evaluate_models.py
python3 evaluation/evaluate_spatial.py
```
"""


def main() -> None:
    front = clean_intro_text(INTRO_TEXT.read_text(encoding="utf-8"))
    OUT_MD.write_text(TITLE_BLOCK + front + CONTINUATION.strip() + "\n", encoding="utf-8")
    print(OUT_MD)


if __name__ == "__main__":
    main()
