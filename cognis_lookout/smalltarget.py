"""Small / faint-target detection for wide-area search (lost hiker/object as a
pixel or two against terrain), with CA-CFAR, Pfa-controlled thresholding,
multi-pass SNR stacking, and a georeferenced confidence heatmap.

CA-CFAR flags pixels whose local contrast exceeds k sigma over a ring of training
cells (a guard band excludes the target). The threshold can be derived from a
target probability of false alarm. Non-kinetic search leads. See docs/COMPLIANCE.md.
An image is a 2-D list of intensity values (rows x cols).
"""

from __future__ import annotations

import statistics
from statistics import NormalDist


def pfa_to_k(pfa: float) -> float:
    """Target probability of false alarm -> CFAR threshold in sigma (Gaussian)."""
    pfa = min(max(pfa, 1e-12), 0.5)
    return round(NormalDist().inv_cdf(1.0 - pfa), 4)


def snr_map(image, guard: int = 1, train: int = 4) -> list:
    H = len(image)
    W = len(image[0]) if H else 0
    out = [[0.0] * W for _ in range(H)]
    span = guard + train
    for r in range(H):
        for c in range(W):
            vals = []
            for dr in range(-span, span + 1):
                for dc in range(-span, span + 1):
                    if abs(dr) <= guard and abs(dc) <= guard:
                        continue
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < H and 0 <= cc < W:
                        vals.append(image[rr][cc])
            if len(vals) < 8:
                continue
            mean = sum(vals) / len(vals)
            std = statistics.pstdev(vals)
            if std > 0:
                out[r][c] = (image[r][c] - mean) / std
    return out


def detect_small_targets(image, k: float = 5.0, guard: int = 1, train: int = 4,
                         max_size: int = 8, pfa: float = None) -> list:
    if not image or not image[0]:
        return []
    if pfa is not None:
        k = pfa_to_k(pfa)
    snr = snr_map(image, guard, train)
    H, W = len(snr), len(snr[0])
    hit = {(r, c): snr[r][c] for r in range(H) for c in range(W) if snr[r][c] >= k}
    seen, blobs = set(), []
    for start in hit:
        if start in seen:
            continue
        stack, comp = [start], []
        while stack:
            p = stack.pop()
            if p in seen or p not in hit:
                continue
            seen.add(p)
            comp.append(p)
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    q = (p[0] + dr, p[1] + dc)
                    if q in hit and q not in seen:
                        stack.append(q)
        if len(comp) > max_size:
            continue
        rows = [p[0] for p in comp]
        cols = [p[1] for p in comp]
        peak = max(hit[p] for p in comp)
        blobs.append({"row": round(sum(rows) / len(rows), 2),
                      "col": round(sum(cols) / len(cols), 2),
                      "size": len(comp), "peak_snr": round(peak, 2),
                      "confidence": round(min(0.99, (peak / (k * 2)) *
                                              (1.0 / (1 + 0.15 * (len(comp) - 1)))), 4)})
    blobs.sort(key=lambda b: -b["confidence"])
    return blobs


def stack_frames(frames) -> list:
    n = len(frames)
    H = len(frames[0])
    W = len(frames[0][0])
    return [[sum(frames[i][r][c] for i in range(n)) / n for c in range(W)] for r in range(H)]


def detect_with_stacking(frames, k: float = 5.0, **kw) -> list:
    """Recover a faint static target by SNR-stacking multiple imagery passes."""
    return detect_small_targets(stack_frames(frames), k=k, **kw)


def to_geojson(blobs, geotransform) -> dict:
    gt = geotransform
    feats = []
    for b in blobs:
        lat = gt["origin_lat"] + b["row"] * gt["dlat"]
        lon = gt["origin_lon"] + b["col"] * gt["dlon"]
        feats.append({"type": "Feature",
                      "geometry": {"type": "Point", "coordinates": [round(lon, 6), round(lat, 6)]},
                      "properties": {"kind": "possible-person-or-object",
                                     "peak_snr": b["peak_snr"], "confidence": b["confidence"],
                                     "size_px": b["size"]}})
    return {"type": "FeatureCollection", "features": feats}


def heatmap(image, cell: int = 8, guard: int = 1, train: int = 4) -> list:
    """Downsample the dense CA-CFAR SNR surface into a search-priority grid."""
    snr = snr_map(image, guard, train)
    H, W = len(snr), len(snr[0])
    rows, cols = (H + cell - 1) // cell, (W + cell - 1) // cell
    grid = [[0.0] * cols for _ in range(rows)]
    for r in range(H):
        for c in range(W):
            v = snr[r][c]
            if v > grid[r // cell][c // cell]:
                grid[r // cell][c // cell] = round(v, 3)
    return grid


def heatmap_geojson(grid, geotransform, cell: int = 8, snr_floor: float = 3.0) -> dict:
    gt = geotransform
    feats = []
    for gr, row in enumerate(grid):
        for gc, v in enumerate(row):
            if v < snr_floor:
                continue
            def ll(rr, cc):
                return [round(gt["origin_lon"] + cc * gt["dlon"], 6),
                        round(gt["origin_lat"] + rr * gt["dlat"], 6)]
            poly = [[ll(gr * cell, gc * cell), ll(gr * cell, (gc + 1) * cell),
                     ll((gr + 1) * cell, (gc + 1) * cell), ll((gr + 1) * cell, gc * cell),
                     ll(gr * cell, gc * cell)]]
            feats.append({"type": "Feature",
                          "geometry": {"type": "Polygon", "coordinates": poly},
                          "properties": {"snr": v, "priority":
                                         "high" if v >= 8 else "medium" if v >= 5 else "low"}})
    return {"type": "FeatureCollection", "features": feats}
