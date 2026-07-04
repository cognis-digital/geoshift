"""Pattern-of-life: learn an entity's normal cells and active hours, then flag
observations that fall outside that pattern (anomalies)."""

from __future__ import annotations

from collections import Counter

from .geo import cell_of


def _hour(ts) -> int:
    if isinstance(ts, str) and "T" in ts:
        try:
            return int(ts.split("T", 1)[1][:2])
        except ValueError:
            return -1
    if isinstance(ts, (int, float)):
        return int((ts // 3600) % 24)
    return -1


def build_profile(observations, origin=(0.0, 0.0), cell_deg=0.05, anchor_min=3):
    cells = Counter(cell_of(o["lat"], o["lon"], origin, cell_deg) for o in observations)
    hours = Counter(_hour(o.get("ts")) for o in observations)
    anchors = {c for c, n in cells.items() if n >= anchor_min}
    typical_hours = {h for h, n in hours.items() if n >= max(1, anchor_min - 1) and h >= 0}
    return {"anchors": anchors, "typical_hours": typical_hours}


def anomalies(observations, profile, origin=(0.0, 0.0), cell_deg=0.05) -> list:
    out = []
    for o in observations:
        cell = cell_of(o["lat"], o["lon"], origin, cell_deg)
        hour = _hour(o.get("ts"))
        off_place = cell not in profile["anchors"]
        off_time = profile["typical_hours"] and hour not in profile["typical_hours"]
        if off_place or off_time:
            reasons = []
            if off_place:
                reasons.append("off-pattern-location")
            if off_time:
                reasons.append("off-pattern-hour")
            conf = 0.5 + (0.3 if off_place else 0) + (0.2 if off_time else 0)
            out.append({"id": o.get("id"), "cell": list(cell), "hour": hour,
                        "reasons": reasons, "confidence": round(min(0.95, conf), 4)})
    return out
