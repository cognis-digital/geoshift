"""Bin observations into an AOI grid of activity counts."""

from __future__ import annotations

import json
from collections import Counter

from .geo import cell_of


def load_observations(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def activity_grid(observations, origin=(0.0, 0.0), cell_deg=0.05) -> Counter:
    grid = Counter()
    for o in observations:
        grid[cell_of(o["lat"], o["lon"], origin, cell_deg)] += 1
    return grid
