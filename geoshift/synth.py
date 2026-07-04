"""Deterministic synthetic geospatial data with planted ground truth."""

from __future__ import annotations

import random

ORIGIN = (0.0, 0.0)
CELL = 0.05


def _cell_center(row, col):
    return (row * CELL + CELL / 2, col * CELL + CELL / 2)


def change_scenario(seed=30, baseline_cells=6, new_cells=4, per_cell=6):
    """Baseline activity in some cells; current window adds NEW hotspot cells.
    Returns (baseline_obs, current_obs, planted_new_cells)."""
    rng = random.Random(seed)
    baseline, current = [], []
    oid = 0

    def emit(dst, row, col, n):
        nonlocal oid
        for _ in range(n):
            oid += 1
            lat, lon = _cell_center(row, col)
            dst.append({"id": f"o{oid}", "lat": round(lat + rng.uniform(-0.01, 0.01), 5),
                        "lon": round(lon + rng.uniform(-0.01, 0.01), 5),
                        "ts": f"2026-01-01T{rng.randint(0,23):02d}:00:00Z"})

    base_cells = [(10 + i, 20 + i) for i in range(baseline_cells)]
    for (r, c) in base_cells:
        emit(baseline, r, c, per_cell)
        emit(current, r, c, per_cell)  # persists
    planted = [(40 + i, 50 + i) for i in range(new_cells)]
    for (r, c) in planted:
        emit(current, r, c, per_cell)  # appears only in current
    rng.shuffle(baseline)
    rng.shuffle(current)
    return baseline, current, {tuple(c) for c in planted}


def pol_scenario(seed=31, home_obs=20, anomalies=3):
    """Entity mostly at home cell during working hours + planted anomalies
    (far cell and/or odd hour). Returns (observations, planted_anomaly_ids)."""
    rng = random.Random(seed)
    obs = []
    oid = 0
    home = _cell_center(100, 100)
    for _ in range(home_obs):
        oid += 1
        obs.append({"id": f"o{oid}", "lat": round(home[0] + rng.uniform(-0.01, 0.01), 5),
                    "lon": round(home[1] + rng.uniform(-0.01, 0.01), 5),
                    "ts": f"2026-01-{rng.randint(1,28):02d}T{rng.randint(9,17):02d}:00:00Z"})
    planted = set()
    for k in range(anomalies):
        oid += 1
        far = _cell_center(500 + k * 25, 500 + k * 25)  # distinct far off-pattern cells
        hour = (2 + k) % 6  # distinct odd/early hours, outside the 9-17 pattern
        obs.append({"id": f"o{oid}", "lat": round(far[0], 5), "lon": round(far[1], 5),
                    "ts": f"2026-01-15T{hour:02d}:00:00Z"})
        planted.add(f"o{oid}")
    rng.shuffle(obs)
    return obs, planted


def landscape_with_people(seed=32, H=80, W=80, n_people=4, clutter=0.05, amp=0.42):
    """A wide, textured terrain scene with a few planted 1-pixel 'people/objects'
    (~8 sigma over terrain clutter). Returns (image, planted_pixels)."""
    import random as _r
    rng = _r.Random(seed)
    img = [[max(0.0, rng.gauss(0.25, clutter)) for _ in range(W)] for _ in range(H)]
    truth = set()
    for _ in range(n_people):
        r, c = rng.randint(6, H - 7), rng.randint(6, W - 7)
        img[r][c] += amp
        truth.add((r, c))
    return img, truth


def landscape_passes(seed=33, H=64, W=64, passes=12, clutter=0.06, amp=0.16):
    """Multiple overhead passes of the same terrain with one faint static target
    (~2.7 sigma single-pass, below detection) — recoverable only by SNR stacking.
    Returns (frames, (row, col))."""
    rng = random.Random(seed)
    r0, c0 = H // 2, W // 2
    frames = []
    for _ in range(passes):
        img = [[max(0.0, rng.gauss(0.25, clutter)) for _ in range(W)] for _ in range(H)]
        img[r0][c0] += amp
        frames.append(img)
    return frames, (r0, c0)
