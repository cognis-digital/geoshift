"""Geofence entry/dwell detection over bounding-box areas of interest."""

from __future__ import annotations


def _inside(o, fence) -> bool:
    return (fence["min_lat"] <= o["lat"] <= fence["max_lat"]
            and fence["min_lon"] <= o["lon"] <= fence["max_lon"])


def check(observations, fences: list) -> list:
    events = []
    for fence in fences:
        hits = [o for o in observations if _inside(o, fence)]
        if hits:
            events.append({"fence": fence.get("name", "aoi"), "entries": len(hits),
                           "observation_ids": [h.get("id") for h in hits]})
    return events
