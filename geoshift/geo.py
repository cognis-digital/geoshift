"""Geospatial helpers."""

from __future__ import annotations

import math

EARTH_KM = 6371.0088


def haversine_km(a_lat, a_lon, b_lat, b_lon) -> float:
    p1, p2 = math.radians(a_lat), math.radians(b_lat)
    dphi = math.radians(b_lat - a_lat)
    dl = math.radians(b_lon - a_lon)
    h = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_KM * math.asin(min(1.0, math.sqrt(h)))


def cell_of(lat, lon, origin=(0.0, 0.0), cell_deg=0.05):
    return (int(math.floor((lat - origin[0]) / cell_deg)),
            int(math.floor((lon - origin[1]) / cell_deg)))
