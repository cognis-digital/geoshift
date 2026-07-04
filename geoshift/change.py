"""Change detection between two time-window activity grids.

Flags cells that became newly active (low/absent baseline -> high current) and,
optionally, cells with a large relative surge. Confidence rises with the surge.
"""

from __future__ import annotations

from .grid import activity_grid


def detect_new_activity(baseline_obs, current_obs, origin=(0.0, 0.0), cell_deg=0.05,
                        max_baseline=1, min_current=4) -> list:
    base = activity_grid(baseline_obs, origin, cell_deg)
    cur = activity_grid(current_obs, origin, cell_deg)
    out = []
    for cell, count in cur.items():
        b = base.get(cell, 0)
        if b <= max_baseline and count >= min_current:
            surge = count / (b + 1)
            conf = min(0.95, 0.5 + 0.05 * count + 0.02 * surge)
            out.append({"cell": list(cell), "baseline": b, "current": count,
                        "surge": round(surge, 2), "confidence": round(conf, 4)})
    out.sort(key=lambda x: -x["confidence"])
    return out
