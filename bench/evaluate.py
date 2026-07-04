"""Accuracy evaluation vs planted ground truth."""

from __future__ import annotations

import json

from geoshift import synth
from geoshift.change import detect_new_activity
from geoshift.patternoflife import anomalies, build_profile
from geoshift.smalltarget import detect_small_targets

from .metrics import prf


def evaluate() -> dict:
    base, cur, planted_cells = synth.change_scenario()
    hotspots = detect_new_activity(base, cur, origin=synth.ORIGIN, cell_deg=synth.CELL)
    pred_cells = {tuple(h["cell"]) for h in hotspots}
    change_prf = prf(pred_cells, planted_cells)

    obs, planted_anoms = synth.pol_scenario()
    prof = build_profile(obs, origin=synth.ORIGIN, cell_deg=synth.CELL)
    an = anomalies(obs, prof, origin=synth.ORIGIN, cell_deg=synth.CELL)
    pred_anoms = {a["id"] for a in an}
    anomaly_prf = prf(pred_anoms, planted_anoms)

    determinism = ({tuple(h["cell"]) for h in
                    detect_new_activity(base, cur, origin=synth.ORIGIN, cell_deg=synth.CELL)}
                   == pred_cells)

    # wide-area small-target (lost hiker/object) detection vs planted pixels
    img, tpix = synth.landscape_with_people()
    blobs = detect_small_targets(img, k=5.0)
    tp = sum(1 for (r, c) in tpix
             if any(abs(b["row"] - r) <= 1.5 and abs(b["col"] - c) <= 1.5 for b in blobs))
    small_target = {"planted": len(tpix), "detected": len(blobs),
                    "recall": round(tp / len(tpix), 4) if tpix else 0.0,
                    "false_alarms": max(0, len(blobs) - tp)}

    return {"change_detection": change_prf, "pattern_of_life": anomaly_prf,
            "small_target": small_target,
            "hotspots": len(hotspots), "determinism": determinism}


def main():
    print(json.dumps(evaluate(), indent=2))


if __name__ == "__main__":
    main()
