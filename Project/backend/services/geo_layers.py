from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Callable

import geopandas as gpd
from shapely.ops import transform

PROJECT_ROOT = Path(__file__).resolve().parents[2]
QGIS_DIR = PROJECT_ROOT / "qgis" / "QGIS"

DISTRICTS = {
    "Huangpu": {
        "label": "黄浦区",
        "boundary": "huangpu.gpkg",
        "subway_lines": "HP subway line.gpkg",
        "subway_stops": "HP subway stop.gpkg",
        "bus_stops": "huangpu_bus_stop.shp",
    },
    "Hongkou": {
        "label": "虹口区",
        "boundary": "hongkou.gpkg",
        "subway_lines": "HK subway line.gpkg",
        "subway_stops": "HK subway stop.gpkg",
        "bus_stops": "hongkou_bus_stops_.shp",
    },
    "Pudong": {
        "label": "浦东新区",
        "boundary": "pudong.gpkg",
        "subway_lines": "PD subway line.gpkg",
        "subway_stops": "PD subway stop.gpkg",
        "bus_stops": "pudong_bus_stop.shp",
    },
}


def out_of_china(lon: float, lat: float) -> bool:
    return lon < 72.004 or lon > 137.8347 or lat < 0.8293 or lat > 55.8271


def _transform_lat(x: float, y: float) -> float:
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y
    ret += 0.2 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
    return ret


def _transform_lon(x: float, y: float) -> float:
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y
    ret += 0.1 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x / 30.0 * math.pi)) * 2.0 / 3.0
    return ret


def wgs84_to_gcj02(lon: float, lat: float) -> tuple[float, float]:
    if out_of_china(lon, lat):
        return lon, lat
    a = 6378245.0
    ee = 0.00669342162296594323
    dlat = _transform_lat(lon - 105.0, lat - 35.0)
    dlon = _transform_lon(lon - 105.0, lat - 35.0)
    radlat = lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrt_magic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrt_magic) * math.pi)
    dlon = (dlon * 180.0) / (a / sqrt_magic * math.cos(radlat) * math.pi)
    return lon + dlon, lat + dlat


def _gcj_transformer() -> Callable:
    def convert(x, y, z=None):
        return wgs84_to_gcj02(x, y)

    return convert


def _read_layer(path: Path) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(path)
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
    else:
        gdf = gdf.to_crs("EPSG:4326")
    return gdf


def _clean_columns(gdf: gpd.GeoDataFrame, district: str, kind: str) -> gpd.GeoDataFrame:
    useful = [
        "full_id",
        "osm_id",
        "name",
        "name_en",
        "name_zh",
        "railway",
        "highway",
        "colour",
        "adcode",
        "center",
        "centroid",
    ]
    keep = [col for col in useful if col in gdf.columns]
    cleaned = gdf[keep + ["geometry"]].copy()
    cleaned["district"] = district
    cleaned["district_label"] = DISTRICTS[district]["label"]
    cleaned["layer_kind"] = kind
    for col in cleaned.columns:
        if col != "geometry":
            cleaned[col] = cleaned[col].fillna("").astype(str)
    cleaned["geometry"] = cleaned.geometry.apply(lambda geom: transform(_gcj_transformer(), geom))
    return cleaned


def _feature_collection(gdf: gpd.GeoDataFrame) -> dict:
    return json.loads(gdf.to_json())


@lru_cache(maxsize=32)
def district_options() -> list[dict]:
    return [
        {"key": key, "label": value["label"]}
        for key, value in DISTRICTS.items()
    ]


@lru_cache(maxsize=16)
def district_boundary(district: str) -> dict:
    _validate_district(district)
    gdf = _read_layer(QGIS_DIR / DISTRICTS[district]["boundary"])
    return _feature_collection(_clean_columns(gdf, district, "district_boundary"))


@lru_cache(maxsize=16)
def bus_stops(district: str) -> dict:
    _validate_district(district)
    gdf = _read_layer(QGIS_DIR / DISTRICTS[district]["bus_stops"])
    return _feature_collection(_clean_columns(gdf, district, "bus_stop"))


@lru_cache(maxsize=16)
def subway_stops(district: str) -> dict:
    _validate_district(district)
    gdf = _read_layer(QGIS_DIR / DISTRICTS[district]["subway_stops"])
    return _feature_collection(_clean_columns(gdf, district, "subway_stop"))


@lru_cache(maxsize=16)
def subway_lines(district: str) -> dict:
    _validate_district(district)
    gdf = _read_layer(QGIS_DIR / DISTRICTS[district]["subway_lines"])
    return _feature_collection(_clean_columns(gdf, district, "subway_line"))


def _validate_district(district: str) -> None:
    if district not in DISTRICTS:
        allowed = ", ".join(DISTRICTS)
        raise ValueError(f"Unknown district '{district}'. Allowed: {allowed}")
