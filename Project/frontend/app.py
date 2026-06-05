import streamlit as st
import folium
from folium.plugins import HeatMap, Fullscreen, LocateControl, MiniMap
from streamlit_folium import st_folium
import os
from pathlib import Path
import json
import pandas as pd
import requests
from shanghai_metro_data import METRO_LINES_INFO, METRO_ROUTES, KEY_STATIONS

# ─────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="Shanghai Transit Intelligence",
    page_icon="🚇",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────────
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "metro"
if "ui_theme_mode" not in st.session_state:
    st.session_state.ui_theme_mode = "Dark"

# ─────────────────────────────────────────────────────────────────
#  BACKEND API CLIENT
# ─────────────────────────────────────────────────────────────────
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000").rstrip("/")
SENTIMENT_CATEGORIES = ["Delay", "Crowding", "Cleanliness", "Safety", "Noise", "Accessibility", "Other"]


def _api_url(endpoint: str) -> str:
    return f"{BACKEND_URL}{endpoint}"


@st.cache_data(ttl=10)
def fetch_health():
    try:
        response = requests.get(_api_url("/api/health"), timeout=2)
        response.raise_for_status()
        return True, response.json()
    except requests.RequestException as exc:
        return False, {"error": str(exc)}


@st.cache_data(ttl=60)
def fetch_sentiments():
    try:
        response = requests.get(_api_url("/api/sentiments"), timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return []


@st.cache_data(ttl=60)
def fetch_hotspots():
    try:
        response = requests.get(_api_url("/api/hotspots"), timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return []


@st.cache_data(ttl=60)
def fetch_feedback(limit=25):
    try:
        response = requests.get(_api_url(f"/api/feedback?limit={limit}"), timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return []


@st.cache_data(ttl=3600)
def fetch_districts():
    try:
        response = requests.get(_api_url("/api/gis/districts"), timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return []


@st.cache_data(ttl=3600)
def fetch_gis_layer(district, layer):
    try:
        response = requests.get(_api_url(f"/api/gis/districts/{district}/{layer}"), timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {"type": "FeatureCollection", "features": []}


def post_feedback(text):
    response = requests.post(_api_url("/api/feedback"), json={"text": text}, timeout=8)
    response.raise_for_status()
    st.cache_data.clear()
    return response.json()


def seed_feedback(count=420):
    response = requests.post(_api_url("/api/seed"), json={"count": count, "reset": True}, timeout=20)
    response.raise_for_status()
    st.cache_data.clear()
    return response.json()


@st.cache_data(ttl=120)
def fetch_spatial_clusters(eps_km=1.5, min_samples=2):
    try:
        r = requests.get(_api_url(f"/api/spatial/clusters?eps_km={eps_km}&min_samples={min_samples}"), timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        return {"type": "FeatureCollection", "features": [], "summary": {"n_clusters": 0, "n_noise": 0}}


@st.cache_data(ttl=120)
def fetch_moran(category=None):
    url = _api_url("/api/spatial/moran") + (f"?category={category}" if category else "")
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        return {"moran_i": None, "p_value": None, "interpretation": "Unavailable", "stations": []}


@st.cache_data(ttl=120)
def fetch_district_compare():
    try:
        r = requests.get(_api_url("/api/spatial/districts/compare"), timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        return []


@st.cache_data(ttl=300)
def fetch_model_status():
    try:
        r = requests.get(_api_url("/api/model/status"), timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        return {"available": False}


def sentiments_df():
    columns = ["station", "station_en", "lat", "lon", "category", "positive", "neutral", "negative"]
    df = pd.DataFrame(fetch_sentiments())
    if df.empty:
        return pd.DataFrame(columns=columns)
    return df.reindex(columns=columns, fill_value=0)


def hotspots_df():
    columns = ["station", "lat", "lon", "weight", "category", "text"]
    df = pd.DataFrame(fetch_hotspots())
    if df.empty:
        return pd.DataFrame(columns=columns)
    return df.reindex(columns=columns, fill_value=0)


SENTIMENT_DF = sentiments_df()
HOTSPOT_DF = hotspots_df()
FEEDBACK_DF = pd.DataFrame(fetch_feedback(limit=5000))
DISTRICT_OPTIONS = fetch_districts()

# ─────────────────────────────────────────────────────────────────
#  AMAP TILE DEFINITIONS
# ─────────────────────────────────────────────────────────────────
AMAP_TILES = {
    "AMap Standard": {
        "url": "https://webrd01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}",
        "attr": "AMap",
    },
    "AMap Satellite": {
        "url": "https://webst01.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}",
        "attr": "AMap Satellite",
    },
    "AMap Dark": {
        "url": "https://webrd01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}",
        "attr": "AMap Dark",
    },
}

# Station marker colors
STATION_MARKER_COLORS = {
    "Interchange": "#0071E3",
    "Terminal": "#FF3B30",
    "Landmark": "#34C759",
    "Regular": "#8E8E93",
}

DISTRICT_DISPLAY_NAMES = {
    "Huangpu": "Huangpu District",
    "Hongkou": "Hongkou District",
    "Pudong": "Pudong New Area",
}

STATION_EN_BY_NAME = {station["name"]: station["name_en"] for station in KEY_STATIONS}


def station_display_name(station_name):
    return STATION_EN_BY_NAME.get(station_name, station_name)


def metro_line_display_name(line_name):
    if line_name == "10号线支线":
        return "Line 10 Branch"
    if line_name.endswith("号线"):
        return f"Line {line_name.replace('号线', '')}"
    return line_name


with st.sidebar:
    st.radio(
        "Interface Theme",
        ["Auto", "Light", "Dark"],
        key="ui_theme_mode",
        horizontal=True,
    )


def use_dark_interface():
    if st.session_state.ui_theme_mode == "Dark":
        return True
    if st.session_state.ui_theme_mode == "Light":
        return False
    return st.context.theme.get("type") == "dark"


THEME_VARS = {
    "dark": {
        "app_bg_start": "#0B0D12",
        "app_bg_end": "#151922",
        "surface": "rgba(31,35,45,0.86)",
        "surface_strong": "rgba(38,43,54,0.96)",
        "surface_muted": "rgba(42,47,58,0.74)",
        "text_primary": "#F5F7FA",
        "text_secondary": "#D2D8E2",
        "text_muted": "#A7B0BE",
        "border_subtle": "rgba(255,255,255,0.10)",
        "border_strong": "rgba(255,255,255,0.18)",
        "shadow_soft": "0 1px 2px rgba(0,0,0,0.28), 0 10px 24px rgba(0,0,0,0.34)",
        "shadow_hover": "0 8px 30px rgba(0,0,0,0.46)",
        "map_border": "rgba(255,255,255,0.14)",
        "sidebar_bg": "rgba(16,19,27,0.96)",
        "input_bg": "rgba(34,39,50,0.98)",
        "input_text": "#F5F7FA",
        "chip_bg": "rgba(38,43,54,0.82)",
        "nav_secondary_bg": "rgba(38,43,54,0.86)",
        "nav_secondary_hover": "rgba(48,54,68,0.96)",
    },
    "light": {
        "app_bg_start": "#FBFBFD",
        "app_bg_end": "#F3F4F8",
        "surface": "rgba(255,255,255,0.84)",
        "surface_strong": "rgba(255,255,255,0.94)",
        "surface_muted": "rgba(255,255,255,0.68)",
        "text_primary": "#1D1D1F",
        "text_secondary": "#6E6E73",
        "text_muted": "#86868B",
        "border_subtle": "rgba(0,0,0,0.08)",
        "border_strong": "rgba(0,0,0,0.14)",
        "shadow_soft": "0 1px 2px rgba(0,0,0,0.04), 0 6px 16px rgba(0,0,0,0.05)",
        "shadow_hover": "0 4px 24px rgba(0,0,0,0.10)",
        "map_border": "rgba(0,0,0,0.08)",
        "sidebar_bg": "rgba(251,251,253,0.94)",
        "input_bg": "rgba(255,255,255,0.96)",
        "input_text": "#1D1D1F",
        "chip_bg": "rgba(255,255,255,0.72)",
        "nav_secondary_bg": "rgba(255,255,255,0.66)",
        "nav_secondary_hover": "rgba(255,255,255,0.94)",
    },
}


theme_vars = THEME_VARS["dark" if use_dark_interface() else "light"]


# ─────────────────────────────────────────────────────────────────
#  APPLE-STYLE CSS
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --app-bg-start: #FBFBFD;
    --app-bg-end: #F3F4F8;
    --surface: rgba(255,255,255,0.84);
    --surface-strong: rgba(255,255,255,0.94);
    --surface-muted: rgba(255,255,255,0.68);
    --text-primary: #1D1D1F;
    --text-secondary: #6E6E73;
    --text-muted: #86868B;
    --border-subtle: rgba(0,0,0,0.08);
    --border-strong: rgba(0,0,0,0.14);
    --shadow-soft: 0 1px 2px rgba(0,0,0,0.04), 0 6px 16px rgba(0,0,0,0.05);
    --shadow-hover: 0 4px 24px rgba(0,0,0,0.10);
    --map-border: rgba(0,0,0,0.08);
    --sidebar-bg: rgba(251,251,253,0.94);
    --input-bg: rgba(255,255,255,0.96);
    --input-text: #1D1D1F;
    --chip-bg: rgba(255,255,255,0.72);
    --nav-secondary-bg: rgba(255,255,255,0.66);
    --nav-secondary-hover: rgba(255,255,255,0.94);
}

@media (prefers-color-scheme: dark) {
    :root {
        --app-bg-start: #0B0D12;
        --app-bg-end: #151922;
        --surface: rgba(31,35,45,0.86);
        --surface-strong: rgba(38,43,54,0.96);
        --surface-muted: rgba(42,47,58,0.74);
        --text-primary: #F5F7FA;
        --text-secondary: #D2D8E2;
        --text-muted: #A7B0BE;
        --border-subtle: rgba(255,255,255,0.10);
        --border-strong: rgba(255,255,255,0.18);
        --shadow-soft: 0 1px 2px rgba(0,0,0,0.28), 0 10px 24px rgba(0,0,0,0.34);
        --shadow-hover: 0 8px 30px rgba(0,0,0,0.46);
        --map-border: rgba(255,255,255,0.14);
        --sidebar-bg: rgba(16,19,27,0.96);
        --input-bg: rgba(34,39,50,0.98);
        --input-text: #F5F7FA;
        --chip-bg: rgba(38,43,54,0.82);
        --nav-secondary-bg: rgba(38,43,54,0.86);
        --nav-secondary-hover: rgba(48,54,68,0.96);
    }
}

html[data-theme="dark"], body[data-theme="dark"], [data-baseweb-theme="dark"] {
    --app-bg-start: #0B0D12;
    --app-bg-end: #151922;
    --surface: rgba(31,35,45,0.86);
    --surface-strong: rgba(38,43,54,0.96);
    --surface-muted: rgba(42,47,58,0.74);
    --text-primary: #F5F7FA;
    --text-secondary: #D2D8E2;
    --text-muted: #A7B0BE;
    --border-subtle: rgba(255,255,255,0.10);
    --border-strong: rgba(255,255,255,0.18);
    --shadow-soft: 0 1px 2px rgba(0,0,0,0.28), 0 10px 24px rgba(0,0,0,0.34);
    --shadow-hover: 0 8px 30px rgba(0,0,0,0.46);
    --map-border: rgba(255,255,255,0.14);
    --sidebar-bg: rgba(16,19,27,0.96);
    --input-bg: rgba(34,39,50,0.98);
    --input-text: #F5F7FA;
    --chip-bg: rgba(38,43,54,0.82);
    --nav-secondary-bg: rgba(38,43,54,0.86);
    --nav-secondary-hover: rgba(48,54,68,0.96);
}

.stApp {
    background: linear-gradient(180deg, var(--app-bg-start) 0%, var(--app-bg-end) 100%);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-primary);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {
    visibility: visible;
    background: transparent;
    height: 44px;
    pointer-events: none;
}

[data-testid="stToolbar"] {
    visibility: visible !important;
    display: flex !important;
    background: transparent !important;
    pointer-events: auto !important;
}

[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
    display: none !important;
}

#MainMenu, [data-testid="stMainMenuButton"], [data-testid="stDeployButton"] {
    display: none !important;
}

button[data-testid="stBaseButton-header"] {
    display: none !important;
}

div:has(> button[data-testid="stExpandSidebarButton"]),
div:has(> button[data-testid="stCollapseSidebarButton"]),
div:has(> button[data-testid="stBaseButton-headerNoPadding"]) {
    position: fixed !important;
    top: 14px !important;
    left: 14px !important;
    width: 42px !important;
    height: 42px !important;
    min-width: 42px !important;
    min-height: 42px !important;
    overflow: visible !important;
    z-index: 2147483647 !important;
    pointer-events: auto !important;
}

button[data-testid="stExpandSidebarButton"],
button[data-testid="stCollapseSidebarButton"],
button[data-testid="stBaseButton-headerNoPadding"] {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    visibility: visible !important;
    opacity: 1 !important;
    width: 38px !important;
    height: 38px !important;
    min-width: 38px !important;
    min-height: 38px !important;
    padding: 0 !important;
    margin: 0 !important;
    color: var(--text-primary) !important;
    background: var(--surface-strong) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 999px !important;
    box-shadow: var(--shadow-soft) !important;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    position: fixed !important;
    top: 14px !important;
    left: 14px !important;
    z-index: 2147483647 !important;
    transform: none !important;
    pointer-events: auto !important;
}

button[data-testid="stExpandSidebarButton"] *,
button[data-testid="stCollapseSidebarButton"] *,
button[data-testid="stBaseButton-headerNoPadding"] * {
    visibility: visible !important;
    opacity: 1 !important;
    color: var(--text-primary) !important;
}

.block-container {
    max-width: 1180px;
    padding-top: 3.4rem;
    padding-left: 2.2rem;
    padding-right: 2.2rem;
}

.stMarkdown, .stText, p, label, span, div {
    color: inherit;
}

h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
}

.hero {
    text-align: center;
    padding: 54px 20px 26px 20px;
}
.hero .eyebrow {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 7px 12px;
    margin-bottom: 16px;
    border-radius: 999px;
    background: var(--surface-muted);
    border: 1px solid var(--border-subtle);
    color: var(--text-secondary);
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}
.hero h1 {
    font-size: 52px;
    font-weight: 700;
    letter-spacing: 0;
    color: var(--text-primary);
    margin-bottom: 8px;
    line-height: 1.05;
}
.hero .gradient-text {
    background: linear-gradient(135deg, #0071E3, #34C759, #30D5C8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero p {
    font-size: 17px;
    color: var(--text-muted);
    font-weight: 400;
    max-width: 720px;
    margin: 0 auto;
    line-height: 1.5;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    padding: 0 16px;
    margin: 10px auto 36px auto;
    max-width: 980px;
}
@media (max-width: 900px) {
    .metric-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 500px) {
    .metric-grid { grid-template-columns: 1fr; padding: 0 16px; }
}

.metric-card {
    position: relative;
    overflow: hidden;
    background: var(--surface);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    padding: 25px 22px;
    box-shadow: var(--shadow-soft);
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}
.metric-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, #0071E3, #34C759, #30D5C8);
    opacity: 0;
    transition: opacity 0.3s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-hover);
    border-color: rgba(0,113,227,0.15);
}
.metric-card:hover::before {
    opacity: 1;
}
.metric-label {
    font-size: 12px;
    color: var(--text-muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 6px;
}
.metric-value {
    font-size: 30px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: 0;
    line-height: 1.1;
}
.metric-delta {
    font-size: 12px;
    font-weight: 500;
    margin-top: 5px;
    opacity: 0.8;
}
.delta-up { color: #34C759; }
.delta-down { color: #FF3B30; }

.section-header {
    text-align: center;
    margin: 42px 0 20px 0;
}
.section-header h2 {
    font-size: 30px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.5px;
    margin: 0;
}
.section-header p {
    font-size: 14px;
    color: var(--text-muted);
    font-weight: 300;
    margin-top: 6px;
}

.map-container {
    border-radius: 16px;
    overflow: hidden;
    box-shadow: var(--shadow-soft);
    margin: 0 12px 34px 12px;
    border: 1px solid var(--map-border);
}

.legend-grid {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 6px;
    margin: 8px auto 30px auto;
    max-width: 980px;
}
.legend-item {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 14px;
    border-radius: 980px;
    background: var(--chip-bg);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid var(--border-subtle);
    font-size: 11px;
    font-weight: 500;
    color: var(--text-primary);
    white-space: nowrap;
    transition: transform 0.15s ease;
}
.legend-item:hover {
    transform: scale(1.04);
}
.legend-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
    box-shadow: 0 0 0 1px var(--border-strong);
}

.footer {
    text-align: center;
    padding: 30px 20px 24px 20px;
    border-top: 1px solid var(--border-subtle);
    margin-top: 40px;
}
.footer p {
    font-size: 12px;
    color: var(--text-muted);
    font-weight: 400;
    margin: 2px 0;
}

[data-testid="stSidebar"] {
    background-color: var(--sidebar-bg);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border-right: 1px solid var(--border-subtle);
    box-shadow: 18px 0 42px rgba(0,0,0,0.10);
}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0.8rem;
}

[data-testid="stSidebar"] * {
    color: var(--text-primary);
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: var(--text-secondary);
}

input, textarea, [data-baseweb="select"] > div, [data-baseweb="input"] > div {
    background-color: var(--input-bg) !important;
    color: var(--input-text) !important;
    border-color: var(--border-subtle) !important;
}

input::placeholder, textarea::placeholder {
    color: var(--text-muted) !important;
}

[data-testid="stDataFrame"], [data-testid="stTable"] {
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    overflow: hidden;
    background: var(--surface-strong);
}

[data-testid="stForm"] {
    max-width: 860px;
    margin: 8px auto 18px auto;
    padding: 18px 18px 16px 18px;
    background: var(--surface);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    box-shadow: var(--shadow-soft);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
}

[data-testid="stForm"] label p {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

/* ── Nav Pill Buttons ── */
[data-testid="stHorizontalBlock"]:has(button[kind="primary"]),
[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) {
    max-width: 820px;
    margin: 0 auto;
}

div[data-testid="stHorizontalBlock"] button {
    border-radius: 14px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 12px 18px !important;
    transition: all 0.25s ease !important;
    border: 1px solid var(--border-subtle) !important;
    min-height: 54px !important;
    box-shadow: none !important;
}
div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
    background: var(--nav-secondary-bg) !important;
    color: var(--text-secondary) !important;
    border-color: var(--border-subtle) !important;
}
div[data-testid="stHorizontalBlock"] button[kind="secondary"]:hover {
    background: var(--nav-secondary-hover) !important;
    color: var(--text-primary) !important;
    border-color: rgba(0,113,227,0.25) !important;
}
div[data-testid="stHorizontalBlock"] button[kind="primary"] {
    background: linear-gradient(135deg, #0071E3, #005BB5) !important;
    color: white !important;
    border-color: transparent !important;
    box-shadow: 0 8px 20px rgba(0,113,227,0.24) !important;
}

div[data-testid="stHorizontalBlock"] button p {
    color: inherit !important;
}

.stAlert {
    color: var(--text-primary);
}

.vega-embed, canvas, svg {
    max-width: 100%;
}

@media (max-width: 700px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .hero {
        padding-top: 42px;
    }
    .hero h1 {
        font-size: 38px;
        line-height: 1.08;
    }
    .hero p {
        font-size: 15px;
    }
    div[data-testid="stHorizontalBlock"] button {
        min-height: 48px !important;
        padding: 10px 12px !important;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    f"""
    <style>
    :root {{
        --app-bg-start: {theme_vars["app_bg_start"]};
        --app-bg-end: {theme_vars["app_bg_end"]};
        --surface: {theme_vars["surface"]};
        --surface-strong: {theme_vars["surface_strong"]};
        --surface-muted: {theme_vars["surface_muted"]};
        --text-primary: {theme_vars["text_primary"]};
        --text-secondary: {theme_vars["text_secondary"]};
        --text-muted: {theme_vars["text_muted"]};
        --border-subtle: {theme_vars["border_subtle"]};
        --border-strong: {theme_vars["border_strong"]};
        --shadow-soft: {theme_vars["shadow_soft"]};
        --shadow-hover: {theme_vars["shadow_hover"]};
        --map-border: {theme_vars["map_border"]};
        --sidebar-bg: {theme_vars["sidebar_bg"]};
        --input-bg: {theme_vars["input_bg"]};
        --input-text: {theme_vars["input_text"]};
        --chip-bg: {theme_vars["chip_bg"]};
        --nav-secondary-bg: {theme_vars["nav_secondary_bg"]};
        --nav-secondary-hover: {theme_vars["nav_secondary_hover"]};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("""
<style>
/* Critical Streamlit chrome fixes kept in a short style block to avoid truncation. */
header[data-testid="stHeader"] {
    visibility: visible !important;
    background: transparent !important;
    pointer-events: none !important;
}

[data-testid="stToolbar"] {
    visibility: visible !important;
    display: flex !important;
    background: transparent !important;
    pointer-events: auto !important;
}

[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stMainMenuButton"],
[data-testid="stDeployButton"],
button[data-testid="stBaseButton-header"] {
    display: none !important;
}

div:has(> button[data-testid="stExpandSidebarButton"]),
div:has(> button[data-testid="stCollapseSidebarButton"]),
div[data-testid="stSidebarCollapseButton"] {
    position: fixed !important;
    top: 14px !important;
    left: 14px !important;
    width: 42px !important;
    height: 42px !important;
    min-width: 42px !important;
    min-height: 42px !important;
    overflow: visible !important;
    z-index: 2147483647 !important;
    pointer-events: auto !important;
}

button[data-testid="stExpandSidebarButton"],
button[data-testid="stCollapseSidebarButton"],
div[data-testid="stSidebarCollapseButton"] > button {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    visibility: visible !important;
    opacity: 1 !important;
    width: 38px !important;
    height: 38px !important;
    min-width: 38px !important;
    min-height: 38px !important;
    padding: 0 !important;
    margin: 0 !important;
    color: var(--text-primary) !important;
    background: var(--surface-strong) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 999px !important;
    box-shadow: var(--shadow-soft) !important;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    position: fixed !important;
    top: 14px !important;
    left: 14px !important;
    z-index: 2147483647 !important;
    transform: none !important;
    pointer-events: auto !important;
}

button[data-testid="stExpandSidebarButton"] *,
button[data-testid="stCollapseSidebarButton"] *,
div[data-testid="stSidebarCollapseButton"] > button * {
    visibility: visible !important;
    opacity: 1 !important;
    color: var(--text-primary) !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
#  HERO SECTION
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="eyebrow">158.888 Research Prototype · NLP × GIS</div>
    <h1>Shanghai <span class="gradient-text">Transit Intelligence</span></h1>
    <p>NLP-powered commuter feedback · real-time spatial analysis · Shanghai Metro Network</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
#  FUNCTIONAL NAV PILLS
# ─────────────────────────────────────────────────────────────────
tabs = {
    "metro": "🚇 Metro Network",
    "sentiment": "📊 Sentiment Analysis",
    "hotspot": "🔥 Hotspot Detection",
    "spatial": "🗺️ Spatial Insights",
    "evaluation": "🔬 Methods & Evaluation",
}

nav_cols = st.columns(len(tabs))
for i, (key, label) in enumerate(tabs.items()):
    with nav_cols[i]:
        if st.button(label, key=f"nav_{key}", use_container_width=True,
                     type="primary" if st.session_state.active_tab == key else "secondary"):
            st.session_state.active_tab = key
            st.rerun()

active_tab = st.session_state.active_tab

# ─────────────────────────────────────────────────────────────────
#  SIDEBAR CONTROLS
# ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎛️ Map Controls")
    backend_ok, backend_info = fetch_health()
    if backend_ok:
        st.success("Backend connected")
    else:
        st.error("Backend offline")
        st.caption(backend_info.get("error", "Unable to reach API"))
    st.caption(f"API: {BACKEND_URL}")
    refresh_col, seed_col = st.columns(2)
    with refresh_col:
        if st.button("Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    with seed_col:
        if st.button("Seed Demo Data", use_container_width=True, disabled=not backend_ok):
            try:
                seed_feedback()
                st.success("Seeded synthetic feedback")
                st.rerun()
            except requests.RequestException as exc:
                st.error(f"Seed failed: {exc}")
    st.markdown("---")
    district_labels = ["All districts"] + [
        DISTRICT_DISPLAY_NAMES.get(d["key"], d["key"])
        for d in DISTRICT_OPTIONS
    ]
    selected_district_label = st.selectbox("District Focus", district_labels)
    selected_district = None
    for district in DISTRICT_OPTIONS:
        if DISTRICT_DISPLAY_NAMES.get(district["key"], district["key"]) == selected_district_label:
            selected_district = district["key"]
            break
    show_qgis_bus_stops = st.toggle(
        "Show QGIS Bus Stops",
        value=selected_district is not None,
        disabled=selected_district is None,
        help="Select a district to display bus stops processed from the team's QGIS data.",
    )
    st.markdown("---")
    show_stations = st.toggle("Show Key Stations", value=True)
    show_labels = st.toggle("Show Station Labels", value=True)
    st.markdown("---")

    map_style_name = st.selectbox("Base Map Style", list(AMAP_TILES.keys()))
    st.markdown("---")

    all_lines = [name for name, coords in METRO_ROUTES.items() if len(coords) >= 2]
    selected_lines = st.multiselect(
        "Metro Line Filter",
        options=all_lines,
        default=all_lines,
        format_func=metro_line_display_name,
        help="Choose which metro lines are displayed on the map.",
    )
    st.markdown("---")
    st.markdown(
        "<p style='font-size:12px;color:#86868B;'>Base map source: AMap<br/>"
        "Station coordinates: GCJ-02 coordinate system</p>",
        unsafe_allow_html=True,
    )

    # ── Model Card ──────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🤖 Model Card")
    _ms = fetch_model_status()
    if _ms.get("available"):
        _metrics = _ms.get("metrics", {})
        st.success(f"v{_ms.get('version', '?')}")
        _ood_f1 = _metrics.get("ood_sentiment_f1") or _metrics.get("sentiment_macro_f1")
        if _ood_f1:
            st.metric("OOD Sentiment F1", f"{_ood_f1:.3f}")
        _cat_f1 = _metrics.get("ood_category_f1") or _metrics.get("category_macro_f1")
        if _cat_f1:
            st.metric("OOD Category F1", f"{_cat_f1:.3f}")
        with st.expander("Limitations & Notes"):
            st.markdown(
                "- Trained on **synthetic transit text** → in-domain accuracy overstated\n"
                "- OOD sentiment F1 ≈ 0.44 (limited generalisation beyond keywords)\n"
                "- Category head may conflate semantically similar issues\n"
                "- Spatial data uses GCJ-02 (AMap); WGS-84 offsets possible near boundaries\n"
                "- Data: ChnSentiCorp (12k hotel/product reviews) + 420 synthetic transit texts"
            )
    else:
        st.warning("Model unavailable")
        st.caption("Run training/train_nlp_model.py to build the artifact.")


# ─────────────────────────────────────────────────────────────────
#  FEEDBACK SUBMISSION
# ─────────────────────────────────────────────────────────────────
with st.form("feedback_form", clear_on_submit=True):
    feedback_text = st.text_input(
        "Submit commuter feedback",
        placeholder="Example: People's Square station had serious delays today",
        disabled=not backend_ok,
    )
    submitted = st.form_submit_button("Run NLP Analysis", disabled=not backend_ok)
    if submitted and feedback_text.strip():
        try:
            result = post_feedback(feedback_text)
            st.session_state["last_nlp_result"] = result
            st.rerun()
        except requests.RequestException as exc:
            st.error(f"Failed to submit feedback: {exc}")

if st.session_state.get("last_nlp_result"):
    result = st.session_state["last_nlp_result"]
    st.success(
        f"NLP result: {result.get('station_en') or result.get('station') or 'No station matched'} · "
        f"{result.get('category')} · {result.get('sentiment')} · "
        f"confidence {result.get('confidence')}"
    )
    if result.get("matched_keywords"):
        st.caption("Matched keywords: " + ", ".join(result["matched_keywords"]))


# ─────────────────────────────────────────────────────────────────
#  SHARED FOLIUM MAP BUILDER
# ─────────────────────────────────────────────────────────────────
def create_base_map(zoom=11):
    """Create a folium map with AMap as default + OSM fallback."""
    tile_info = AMAP_TILES[map_style_name]
    m = folium.Map(
        location=[31.2304, 121.4737],
        zoom_start=zoom,
        tiles=None,
        control_scale=True,
    )
    # AMap as primary tile layer
    folium.TileLayer(
        tiles=tile_info["url"],
        attr=tile_info["attr"],
        name=map_style_name,
        overlay=False,
        control=False,
    ).add_to(m)
    # OpenStreetMap as fallback
    folium.TileLayer(
        tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr="© OpenStreetMap contributors",
        name="OpenStreetMap",
        overlay=False,
    ).add_to(m)
    Fullscreen(
        position="topright",
        title="Fullscreen",
        title_cancel="Exit fullscreen",
    ).add_to(m)
    LocateControl(
        position="topright",
        strings={"title": "Locate current position"},
        auto_start=False,
    ).add_to(m)
    return m


def add_metro_lines(m):
    """Add metro lines as a FeatureGroup layer."""
    fg = folium.FeatureGroup(name="🚇 Metro Lines", show=True, overlay=True)
    for name, coords in METRO_ROUTES.items():
        if len(coords) < 2:
            continue
        if name not in selected_lines:
            continue
        display_name = name.replace("支线", "")
        info = METRO_LINES_INFO.get(name, METRO_LINES_INFO.get(display_name, {}))
        color = info.get("hex", "#888888")
        line_label = metro_line_display_name(name)
        folium_coords = [[c[1], c[0]] for c in coords]
        folium.PolyLine(
            folium_coords,
            color=color,
            weight=4,
            opacity=0.9,
            popup=folium.Popup(f"<b>{line_label}</b>", parse_html=True),
            tooltip=line_label,
        ).add_to(fg)
    fg.add_to(m)
    return m


def add_station_markers(m):
    """Add station markers as a FeatureGroup layer with enhanced popups."""
    fg = folium.FeatureGroup(name="📍 Key Stations", show=True, overlay=True)
    if not show_stations:
        return m
    for s in KEY_STATIONS:
        color = STATION_MARKER_COLORS.get(s["type"], "#8E8E93")
        radius = {"Interchange": 7, "Terminal": 6, "Landmark": 6, "Regular": 4}.get(s["type"], 4)
        # Fetch sentiment summary for this station (mock for now)
        station_data = SENTIMENT_DF[SENTIMENT_DF["station"] == s["name"]]
        total_neg = int(station_data["negative"].sum()) if not station_data.empty else 0
        top_cat = station_data.groupby("category")["negative"].sum().idxmax() if not station_data.empty else "N/A"

        tooltip_text = s["name_en"] if show_labels else ""
        popup_html = (
            f"<div style='font-family:Inter,-apple-system,sans-serif;min-width:200px'>"
            f"<b style='font-size:14px;color:#1D1D1F'>{s['name_en']}</b><br/>"
            f"<div style='height:1px;background:#E8E8ED;margin:6px 0'></div>"
            f"<span style='font-size:12px;color:#666'>Lines: <b>{s['lines']}</b></span><br/>"
            f"<span style='font-size:12px;color:#666'>Type: <b>{s['type']}</b></span><br/>"
            f"<div style='height:1px;background:#E8E8ED;margin:6px 0'></div>"
            f"<span style='font-size:12px;color:#666'>Negative Reports: <b style='color:#FF3B30'>{total_neg}</b></span><br/>"
            f"<span style='font-size:12px;color:#666'>Top Issue: <b>{top_cat}</b></span>"
            f"</div>"
        )

        folium.CircleMarker(
            location=[s["lat"], s["lon"]],
            radius=radius,
            color="white",
            weight=2.5,
            fill=True,
            fill_color=color,
            fill_opacity=0.92,
            tooltip=tooltip_text,
            popup=folium.Popup(popup_html, max_width=280),
        ).add_to(fg)
    fg.add_to(m)
    return m


def add_qgis_layers(m):
    """Add district-level QGIS outputs provided by the GIS teammate."""
    if not selected_district:
        return m

    boundary = fetch_gis_layer(selected_district, "boundary")
    subway_lines = fetch_gis_layer(selected_district, "subway-lines")
    subway_stops = fetch_gis_layer(selected_district, "subway-stops")

    folium.GeoJson(
        boundary,
        name=f"🗺️ {selected_district_label} Boundary",
        style_function=lambda _: {
            "color": "#1D1D1F",
            "weight": 2,
            "fillColor": "#0071E3",
            "fillOpacity": 0.06,
        },
        tooltip=folium.GeoJsonTooltip(fields=["district"], aliases=["District"]),
    ).add_to(m)

    folium.GeoJson(
        subway_lines,
        name=f"🚇 QGIS Subway Lines ({selected_district_label})",
        style_function=lambda feature: {
            "color": feature["properties"].get("colour") or "#5A5A5F",
            "weight": 3,
            "opacity": 0.78,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["name_en"],
            aliases=["Line"],
            labels=True,
        ),
    ).add_to(m)

    subway_stop_fg = folium.FeatureGroup(
        name=f"Ⓜ️ QGIS Subway Stops ({selected_district_label})",
        show=False,
    )
    for feature in subway_stops.get("features", []):
        coords = feature.get("geometry", {}).get("coordinates")
        props = feature.get("properties", {})
        if not coords:
            continue
        name_en = props.get("name_en") or props.get("name") or "Subway stop"
        folium.CircleMarker(
            location=[coords[1], coords[0]],
            radius=4,
            color="#FFFFFF",
            weight=1.5,
            fill=True,
            fill_color="#AF52DE",
            fill_opacity=0.9,
            tooltip=name_en,
            popup=folium.Popup(
                f"<b>{name_en}</b><br/>"
                f"<span style='font-size:12px'>OSM: {props.get('osm_id', '')}</span>",
                max_width=240,
            ),
        ).add_to(subway_stop_fg)
    subway_stop_fg.add_to(m)

    if show_qgis_bus_stops:
        bus_stops = fetch_gis_layer(selected_district, "bus-stops")
        bus_stop_fg = folium.FeatureGroup(
            name=f"🚌 QGIS Bus Stops ({selected_district_label})",
            show=True,
        )
        for feature in bus_stops.get("features", []):
            coords = feature.get("geometry", {}).get("coordinates")
            props = feature.get("properties", {})
            if not coords:
                continue
            name_en = props.get("name_en") or props.get("name") or "Bus stop"
            folium.CircleMarker(
                location=[coords[1], coords[0]],
                radius=2.5,
                color="#FFFFFF",
                weight=0.7,
                fill=True,
                fill_color="#FF9F0A",
                fill_opacity=0.72,
                tooltip=name_en,
                popup=folium.Popup(
                    f"<b>{name_en}</b><br/>"
                    f"<span style='font-size:12px'>{selected_district_label} · OSM {props.get('osm_id', '')}</span>",
                    max_width=260,
                ),
            ).add_to(bus_stop_fg)
        bus_stop_fg.add_to(m)

    return m


# =================================================================
#  TAB: METRO NETWORK
# =================================================================
if active_tab == "metro":
    total_stations = sum(len(v) for v in METRO_ROUTES.values() if len(v) >= 2)
    total_lines = sum(1 for v in METRO_ROUTES.values() if len(v) >= 2)
    feedback_count = len(FEEDBACK_DF)
    if feedback_count and "sentiment" in FEEDBACK_DF:
        negative_feedback = int((FEEDBACK_DF["sentiment"] == "negative").sum())
        negative_delta = f"{round(negative_feedback / feedback_count * 100, 1)}% negative sentiment"
    else:
        negative_delta = "Seed or submit feedback"

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-label">Metro Lines</div>
            <div class="metric-value">{total_lines}</div>
            <div class="metric-delta delta-up">AMap tile source</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Mapped Stations</div>
            <div class="metric-value">{total_stations}</div>
            <div class="metric-delta delta-up">GCJ-02 coordinates</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Daily Ridership</div>
            <div class="metric-value">13.5M</div>
            <div class="metric-delta delta-up">↑ 5.2% vs last month</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Feedback Collected</div>
            <div class="metric-value">{feedback_count:,}</div>
            <div class="metric-delta delta-down">{negative_delta}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header">
        <h2>Network Overview</h2>
        <p>Shanghai metro network · Base map by AMap</p>
    </div>
    """, unsafe_allow_html=True)

    m = create_base_map()
    add_metro_lines(m)
    add_qgis_layers(m)
    add_station_markers(m)
    folium.LayerControl(collapsed=False, position="topright").add_to(m)

    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    st_folium(m, use_container_width=True, height=620, returned_objects=[])
    st.markdown('</div>', unsafe_allow_html=True)

    # Line legend — moved into a cleaner chip-style row
    legend_html = '<div class="legend-grid">'
    for name, info in METRO_LINES_INFO.items():
        if name in selected_lines:
            legend_html += (
                f'<span class="legend-item">'
                f'<span class="legend-dot" style="background:{info["hex"]}"></span>'
                f'{metro_line_display_name(name)}</span>'
            )
    legend_html += '</div>'
    st.markdown(legend_html, unsafe_allow_html=True)

    # Station table
    st.markdown("""
    <div class="section-header">
        <h2>Key Interchange Stations</h2>
        <p>Major interchange stations in the Shanghai Metro network</p>
    </div>
    """, unsafe_allow_html=True)

    display_df = pd.DataFrame(KEY_STATIONS)
    display_df = display_df[["name_en", "lines", "type", "lon", "lat"]]
    display_df.columns = ["Station", "Lines", "Type", "Longitude", "Latitude"]
    display_df["Longitude"] = display_df["Longitude"].round(4)
    display_df["Latitude"] = display_df["Latitude"].round(4)
    st.dataframe(display_df, use_container_width=True, hide_index=True)


# =================================================================
#  TAB: SENTIMENT ANALYSIS
# =================================================================
elif active_tab == "sentiment":
    total_feedback = int(SENTIMENT_DF[["positive", "neutral", "negative"]].sum().sum())
    total_neg = int(SENTIMENT_DF["negative"].sum())
    neg_pct = round(total_neg / total_feedback * 100, 1) if total_feedback else 0
    top_issue_cat = (
        SENTIMENT_DF.groupby("category")["negative"].sum().idxmax()
        if total_feedback
        else "N/A"
    )

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-label">Total Feedback</div>
            <div class="metric-value">{total_feedback:,}</div>
            <div class="metric-delta delta-up">NLP classified</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Negative Reports</div>
            <div class="metric-value">{total_neg:,}</div>
            <div class="metric-delta delta-down">{neg_pct}% of total</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Top Concern</div>
            <div class="metric-value">{top_issue_cat}</div>
            <div class="metric-delta delta-down">Highest negative count</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Stations Monitored</div>
            <div class="metric-value">{SENTIMENT_DF['station'].nunique()}</div>
            <div class="metric-delta delta-up">Key interchanges</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if SENTIMENT_DF.empty:
        st.info("No feedback data yet. Start the backend, use Seed Demo Data, or submit feedback above.")

    st.markdown("""
    <div class="section-header">
        <h2>Sentiment Breakdown</h2>
        <p>NLP-classified commuter feedback by issue category and station</p>
    </div>
    """, unsafe_allow_html=True)

    cat_summary = SENTIMENT_DF.groupby("category")[["positive", "neutral", "negative"]].sum().reset_index()
    cat_chart = cat_summary.melt(id_vars="category", var_name="Sentiment", value_name="Count")
    if not cat_chart.empty:
        st.bar_chart(cat_chart, x="category", y="Count", color="Sentiment", horizontal=False,
                     use_container_width=True, height=380)

    st.markdown("""
    <div class="section-header">
        <h2>Negative Feedback by Station</h2>
        <p>Stations ranked by negative-feedback count</p>
    </div>
    """, unsafe_allow_html=True)

    if not SENTIMENT_DF.empty:
        station_neg = (
            SENTIMENT_DF.groupby(["station", "station_en"])["negative"]
            .sum().reset_index().sort_values("negative", ascending=True)
        )
        station_neg["label"] = station_neg["station_en"].fillna(station_neg["station"])
        st.bar_chart(station_neg, x="label", y="negative", horizontal=True,
                     use_container_width=True, height=600, color="#FF3B30")

    # Sentiment map with circle markers sized by negative count — use FeatureGroup
    st.markdown("""
    <div class="section-header">
        <h2>Sentiment Map</h2>
        <p>Station-level negative sentiment intensity · Larger circles indicate more negative feedback</p>
    </div>
    """, unsafe_allow_html=True)

    station_agg = SENTIMENT_DF.groupby(["station", "station_en"]).agg(
        lon=("lon", "first"), lat=("lat", "first"),
        negative=("negative", "sum"), positive=("positive", "sum"),
    ).reset_index()

    m = create_base_map(zoom=11)
    add_metro_lines(m)
    add_qgis_layers(m)

    # Sentiment bubbles as a FeatureGroup on top of lines
    sentiment_fg = folium.FeatureGroup(name="📊 Sentiment Bubbles", show=True, overlay=True)
    max_neg = station_agg["negative"].max() if not station_agg.empty else 0
    if max_neg:
        for _, row in station_agg.iterrows():
            ratio = row["negative"] / max_neg
            radius = 8 + ratio * 24
            popup_html = (
                f"<div style='font-family:Inter,-apple-system,sans-serif;min-width:180px'>"
                f"<b style='font-size:14px'>{row['station_en'] or station_display_name(row['station'])}</b><br/>"
                f"<div style='height:1px;background:#E8E8ED;margin:6px 0'></div>"
                f"<span style='color:#FF3B30'>🔴 Negative: <b>{row['negative']}</b></span><br/>"
                f"<span style='color:#34C759'>🟢 Positive: <b>{row['positive']}</b></span>"
                f"</div>"
            )
            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=radius,
                color="#FF3B30",
                weight=1.5,
                fill=True,
                fill_color="#FF3B30",
                fill_opacity=0.25 + ratio * 0.45,
                tooltip=f"{row['station_en'] or station_display_name(row['station'])}: {row['negative']} negative reports",
                popup=folium.Popup(popup_html, max_width=260),
            ).add_to(sentiment_fg)
    sentiment_fg.add_to(m)

    folium.LayerControl(collapsed=False, position="topright").add_to(m)

    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    st_folium(m, use_container_width=True, height=620, returned_objects=[])
    st.markdown('</div>', unsafe_allow_html=True)


# =================================================================
#  TAB: HOTSPOT DETECTION
# =================================================================
elif active_tab == "hotspot":
    top_hotspot_station = HOTSPOT_DF.groupby("station")["weight"].sum().idxmax() if not HOTSPOT_DF.empty else "N/A"
    top_hotspot = station_display_name(top_hotspot_station)
    total_pts = len(HOTSPOT_DF)
    avg_severity = HOTSPOT_DF["weight"].mean() if total_pts else 0

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-label">Complaint Points</div>
            <div class="metric-value">{total_pts:,}</div>
            <div class="metric-delta delta-up">Geo-tagged reports</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Top Hotspot</div>
            <div class="metric-value">{top_hotspot}</div>
            <div class="metric-delta delta-down">Highest density</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Clusters Detected</div>
            <div class="metric-value">{HOTSPOT_DF['station'].nunique() if total_pts else 0}</div>
            <div class="metric-delta delta-up">Spatial clustering</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Avg Severity</div>
            <div class="metric-value">{avg_severity:.2f}</div>
            <div class="metric-delta delta-down">0-1 scale</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if HOTSPOT_DF.empty:
        st.info("No hotspot data yet. Negative feedback with a matched station will appear here.")

    st.markdown("""
    <div class="section-header">
        <h2>Complaint Heatmap</h2>
        <p>Spatial distribution of negative feedback · Layer controls enabled</p>
    </div>
    """, unsafe_allow_html=True)

    m = create_base_map(zoom=11)
    add_metro_lines(m)
    add_qgis_layers(m)

    # HeatMap as a FeatureGroup (renders BELOW station markers)
    heat_fg = folium.FeatureGroup(name="🔥 Complaint Heatmap", show=True, overlay=True)
    heat_data = HOTSPOT_DF[["lat", "lon", "weight"]].values.tolist()
    if heat_data:
        HeatMap(
            heat_data,
            radius=25,
            blur=15,
            max_zoom=13,
            gradient={0.2: "#ffffb2", 0.4: "#fecc5c", 0.6: "#fd8d3c", 0.8: "#f03b20", 1.0: "#bd0026"},
        ).add_to(heat_fg)
    heat_fg.add_to(m)

    # Station markers ON TOP of heatmap
    add_station_markers(m)

    folium.LayerControl(collapsed=False, position="topright").add_to(m)

    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    st_folium(m, use_container_width=True, height=620, returned_objects=[])
    st.markdown('</div>', unsafe_allow_html=True)

    # Hotspot ranking table
    st.markdown("""
    <div class="section-header">
        <h2>Hotspot Ranking</h2>
        <p>Stations ranked by complaint density</p>
    </div>
    """, unsafe_allow_html=True)

    if not HOTSPOT_DF.empty:
        hotspot_rank = (
            HOTSPOT_DF.groupby("station")
            .agg(complaints=("weight", "count"), severity=("weight", "mean"))
            .reset_index().sort_values("complaints", ascending=False)
        )
        hotspot_rank["station"] = hotspot_rank["station"].map(station_display_name)
        hotspot_rank["severity"] = hotspot_rank["severity"].round(3)
        hotspot_rank.columns = ["Station", "Complaints", "Avg Severity"]
        st.dataframe(hotspot_rank, use_container_width=True, hide_index=True)


# =================================================================
#  TAB: SPATIAL INSIGHTS
# =================================================================
elif active_tab == "spatial":
    _EVAL_DIR = Path(__file__).resolve().parents[1] / "data" / "evaluation"

    # ── Controls (top of tab) ────────────────────────────────────
    col_eps, col_min, col_cat = st.columns([1, 1, 2])
    with col_eps:
        eps_km = st.slider("Cluster radius (km)", min_value=0.5, max_value=5.0, value=1.5, step=0.25)
    with col_min:
        min_samp = st.slider("Min stations per cluster", min_value=2, max_value=8, value=2)
    with col_cat:
        spatial_cat = st.selectbox(
            "Category filter", ["All"] + ["Delay", "Crowding", "Cleanliness", "Safety", "Noise", "Accessibility"],
        )
    spatial_cat_arg = None if spatial_cat == "All" else spatial_cat

    cluster_data = fetch_spatial_clusters(eps_km=eps_km, min_samples=min_samp)
    moran_data = fetch_moran(category=spatial_cat_arg)
    district_data = fetch_district_compare()

    n_clusters = cluster_data.get("summary", {}).get("n_clusters", 0)
    n_noise = cluster_data.get("summary", {}).get("n_noise", 0)
    moran_i = moran_data.get("moran_i")
    moran_p = moran_data.get("p_value")

    # ── KPI row ──────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("DBSCAN Clusters", n_clusters)
    k2.metric("Noise Stations", n_noise)
    k3.metric("Moran's I", f"{moran_i:.4f}" if moran_i is not None else "N/A")
    k4.metric("p-value", f"{moran_p:.4f}" if moran_p is not None else "N/A",
              delta="significant" if (moran_p is not None and moran_p < 0.05) else "not significant",
              delta_color="normal" if (moran_p is not None and moran_p < 0.05) else "off")

    st.markdown("""
    <div class="section-header">
        <h2>DBSCAN Negative-Feedback Clusters + LISA Autocorrelation</h2>
        <p>Geographic clustering with DBSCAN Haversine distance and Moran's I local autocorrelation</p>
    </div>
    """, unsafe_allow_html=True)

    m = create_base_map(zoom=11)
    add_metro_lines(m)
    add_qgis_layers(m)

    # ── DBSCAN cluster polygons / centroids ──────────────────────
    cluster_fg = folium.FeatureGroup(name="🔵 DBSCAN Clusters", show=True, overlay=True)
    _CLUSTER_PALETTE = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    ]
    for feat in cluster_data.get("features", []):
        props = feat["properties"]
        lon, lat = feat["geometry"]["coordinates"]
        cid = props["cluster_id"]
        is_noise = props["is_noise"]
        if is_noise:
            folium.CircleMarker(
                location=[lat, lon],
                radius=5,
                color="#aaaaaa",
                fill=True,
                fill_color="#cccccc",
                fill_opacity=0.6,
                tooltip=f"{', '.join(station_display_name(s) for s in props['stations'])} — noise",
            ).add_to(cluster_fg)
        else:
            color = _CLUSTER_PALETTE[cid % len(_CLUSTER_PALETTE)]
            hull = props.get("hull_coords", [[lon, lat]])
            if len(hull) >= 3:
                folium.Polygon(
                    locations=[[h[1], h[0]] for h in hull],
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.15,
                    weight=2,
                    tooltip=f"Cluster {cid} — {props['station_count']} stations, negative rate={props['neg_rate']}",
                ).add_to(cluster_fg)
            folium.CircleMarker(
                location=[lat, lon],
                radius=8,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.8,
                tooltip=f"Cluster {cid}: {', '.join(station_display_name(s) for s in props['stations'])}",
                popup=folium.Popup(
                    f"<b>Cluster {cid}</b><br/>Stations: {props['station_count']}<br/>"
                    f"Neg rate: {props['neg_rate']}<br/>"
                    f"Total feedback: {props['total_feedback']}",
                    max_width=220,
                ),
            ).add_to(cluster_fg)
    cluster_fg.add_to(m)

    # ── LISA circles ─────────────────────────────────────────────
    _LISA_COLORS = {"HH": "#FF3B30", "LL": "#007AFF", "HL": "#FF9500", "LH": "#5AC8FA", "NS": "#C7C7CC"}
    lisa_fg = folium.FeatureGroup(name="🔴 LISA (local autocorrelation)", show=True, overlay=True)
    for s in moran_data.get("stations", []):
        lbl = s.get("lisa", "NS")
        folium.CircleMarker(
            location=[s["lat"], s["lon"]],
            radius=7,
            color=_LISA_COLORS.get(lbl, "#888"),
            fill=True,
            fill_color=_LISA_COLORS.get(lbl, "#888"),
            fill_opacity=0.75,
            tooltip=f"{s.get('station_en') or station_display_name(s['station'])} — LISA:{lbl}  negative rate:{s['neg_rate']}",
        ).add_to(lisa_fg)
    lisa_fg.add_to(m)

    folium.LayerControl(collapsed=False, position="topright").add_to(m)
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    st_folium(m, use_container_width=True, height=620, returned_objects=[])
    st.markdown('</div>', unsafe_allow_html=True)

    # ── LISA legend ───────────────────────────────────────────────
    st.markdown(
        "<small>🔴 **HH** High–High hotspot &nbsp;|&nbsp; 🔵 **LL** Low–Low coldspot &nbsp;|&nbsp; "
        "🟠 **HL** High surrounded by Low &nbsp;|&nbsp; 🩵 **LH** Low surrounded by High &nbsp;|&nbsp; "
        "⬜ **NS** Not significant</small>",
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div class="section-header">
        <h2>District Comparison (Chi-square)</h2>
        <p>Chi-square comparison of negative-feedback rates across QGIS districts</p>
    </div>
    """, unsafe_allow_html=True)

    if district_data:
        dist_cols = st.columns(len(district_data))
        for i, d in enumerate(district_data):
            with dist_cols[i]:
                sig_flag = "✅ Sig" if d.get("chi2_significant") else "— NS"
                st.markdown(
                    f"<div class='metric-card'>"
                    f"<div class='metric-label'>{DISTRICT_DISPLAY_NAMES.get(d['district'], d['district'])}</div>"
                    f"<div class='metric-value'>{d['neg_rate']:.1%}</div>"
                    f"<div class='metric-delta'>n={d['total_feedback']} · χ² p={d.get('chi2_p_value', '?')} {sig_flag}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
        dist_df = pd.DataFrame(district_data)[
            ["district", "station_count", "total_feedback", "negative", "neutral", "positive", "neg_rate",
             "chi2_statistic", "chi2_p_value", "chi2_significant"]
        ]
        st.dataframe(dist_df, use_container_width=True, hide_index=True)
    else:
        st.info("District data unavailable — ensure backend is running and feedback has been seeded.")

    # ── Static evaluation map (cached PNG) ────────────────────────
    _smap = _EVAL_DIR / "spatial_cluster_map.png"
    if _smap.exists():
        with st.expander("📊 Static evaluation cluster map (from evaluate_spatial.py)"):
            st.image(str(_smap), caption="DBSCAN clusters + LISA (synthetic data, 420 records)")

    # ── Moran interpretation ──────────────────────────────────────
    interp = moran_data.get("interpretation", "")
    if interp:
        st.info(f"**Moran's I interpretation:** {interp}")


# =================================================================
#  TAB: METHODS & EVALUATION
# =================================================================
elif active_tab == "evaluation":
    _EVAL_DIR = Path(__file__).resolve().parents[1] / "data" / "evaluation"

    st.markdown("""
    <div class="section-header">
        <h2>Model Performance</h2>
        <p>Out-of-distribution evaluation on 120 hand-labelled transit texts</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Model comparison table ─────────────────────────────────
    _comp_csv = _EVAL_DIR / "model_comparison.csv"
    if _comp_csv.exists():
        comp_df = pd.read_csv(_comp_csv)
        st.dataframe(comp_df, use_container_width=True, hide_index=True)
        st.caption(
            "InDomain: held-out synthetic templates · OOD: 120 hand-labelled texts · "
            "ChnSentiCorp: hotel/product review benchmark (sentiment head only)"
        )
    else:
        st.warning("model_comparison.csv not found — run evaluation/evaluate_models.py")

    # ── Confusion matrices ─────────────────────────────────────
    col_cm1, col_cm2 = st.columns(2)
    with col_cm1:
        _cm_s = _EVAL_DIR / "ood_confusion_sentiment.png"
        if _cm_s.exists():
            st.image(str(_cm_s), caption="OOD Sentiment confusion matrix")
    with col_cm2:
        _cm_c = _EVAL_DIR / "ood_confusion_category.png"
        if _cm_c.exists():
            st.image(str(_cm_c), caption="OOD Category confusion matrix")

    # ── Live inference ─────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
        <h2>Live Inference</h2>
        <p>Real-time inference · Enter a feedback text and inspect the NLP result</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("eval_inference_form", clear_on_submit=False):
        infer_text = st.text_area(
            "Enter transit feedback text",
            placeholder="Example: This morning People's Square was too crowded and I had to wait for four trains",
            height=100,
        )
        infer_submitted = st.form_submit_button("Analyse")

    if infer_submitted and infer_text.strip():
        try:
            r = requests.post(
                f"{BACKEND_URL}/api/analyse",
                json={"text": infer_text},
                timeout=8,
            )
            r.raise_for_status()
            _res = r.json()
            ri1, ri2, ri3, ri4 = st.columns(4)
            ri1.metric("Category", _res.get("category", "—"))
            ri2.metric("Sentiment", _res.get("sentiment", "—"))
            ri3.metric("Confidence", f"{_res.get('confidence', 0):.2f}")
            ri4.metric("Station", _res.get("station_en") or _res.get("station") or "none matched")
            if _res.get("matched_keywords"):
                st.caption("Matched keywords: " + "  ·  ".join(_res["matched_keywords"]))
        except requests.RequestException as exc:
            st.error(f"Inference failed: {exc}")

    # ── OOD dataset sample ─────────────────────────────────────
    st.markdown("""
    <div class="section-header">
        <h2>OOD Test Set Sample</h2>
        <p>120 hand-labelled texts covering new sentence styles and perturbations</p>
    </div>
    """, unsafe_allow_html=True)

    _ood_path = _EVAL_DIR / "ood_test_set.jsonl"
    if _ood_path.exists():
        ood_rows = [json.loads(l) for l in _ood_path.read_text(encoding="utf-8").splitlines() if l.strip()]
        ood_df = pd.DataFrame(ood_rows)[["text", "category", "sentiment", "perturbation", "source"]]
        st.dataframe(ood_df, use_container_width=True, hide_index=True, height=320)

        c1, c2 = st.columns(2)
        with c1:
            st.bar_chart(ood_df["sentiment"].value_counts(), height=200)
            st.caption("Sentiment distribution")
        with c2:
            st.bar_chart(ood_df["category"].value_counts(), height=200)
            st.caption("Category distribution")
    else:
        st.warning("ood_test_set.jsonl not found.")

    # ── Training dataset stats ─────────────────────────────────
    st.markdown("""
    <div class="section-header">
        <h2>Training Data Sources</h2>
        <p>Sentiment head: ChnSentiCorp + transit synthetic neutral · Category head: synthetic templates</p>
    </div>
    """, unsafe_allow_html=True)

    _senti_metrics = _EVAL_DIR / "sentiment_train_metrics.json"
    _cat_metrics = _EVAL_DIR / "category_train_metrics.json"
    if _senti_metrics.exists() and _cat_metrics.exists():
        sm = json.loads(_senti_metrics.read_text())
        cm = json.loads(_cat_metrics.read_text())
        tc1, tc2 = st.columns(2)
        with tc1:
            st.markdown("**Sentiment head**")
            st.json(sm)
        with tc2:
            st.markdown("**Category head**")
            st.json(cm)


# ─────────────────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <p>Shanghai Transit Intelligence · 158.888 IT Research Project · Massey University · G8</p>
    <p style="margin-top:4px;">Geo-located NLP Feedback System for Public Transport 🚇</p>
    <p style="margin-top:4px;font-size:11px;">Base map: AMap · Coordinate system: GCJ-02</p>
</div>
""", unsafe_allow_html=True)
