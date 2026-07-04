"""Geoshift CLI."""

from __future__ import annotations

import argparse
import json
import sys

from . import __version__, synth
from .change import detect_new_activity
from .grid import load_observations
from .patternoflife import anomalies, build_profile
from .report import render_json, render_text


def cmd_demo(args):
    base, cur, _ = synth.change_scenario()
    obs, _ = synth.pol_scenario()
    prof = build_profile(obs)
    product = {"new_activity": detect_new_activity(base, cur),
               "anomalies": anomalies(obs, prof)}
    print(render_text(product))
    return 0


def cmd_change(args):
    base = load_observations(args.baseline)
    cur = load_observations(args.current)
    out = detect_new_activity(base, cur)
    print(json.dumps(out, indent=2))
    return 0


def cmd_pol(args):
    obs = load_observations(args.observations)
    prof = build_profile(obs)
    print(json.dumps(anomalies(obs, prof), indent=2))
    return 0


def cmd_search(args):
    """Wide-area small-target search — e.g. a lost hiker as a pixel in terrain."""
    from . import synth
    from .smalltarget import detect_small_targets, detect_with_stacking, pfa_to_k
    k = pfa_to_k(args.pfa) if args.pfa else args.k
    if args.stack:
        frames, tpt = synth.landscape_passes()
        single = detect_small_targets(frames[0], k=k)
        blobs = detect_with_stacking(frames, k=k)
        truth = {tpt}
        print(f"COGNIS LOOKOUT | {len(frames)}-pass SNR stack over terrain "
              f"(single-pass found {len(single)})")
    else:
        img, truth = synth.landscape_with_people()
        blobs = detect_small_targets(img, k=k)
        print(f"COGNIS LOOKOUT | wide-area search over {len(img)}x{len(img[0])} terrain scene (CA-CFAR)")
    print(f"planted targets: {len(truth)}   detections: {len(blobs)}   (k={round(k,2)} sigma)")
    for i, b in enumerate(blobs[:10], 1):
        print(f"  [{i}] pixel ({b['row']},{b['col']}) size={b['size']}px "
              f"SNR={b['peak_snr']} conf={b['confidence']:.2f}")
    print("NOTE: non-kinetic search leads (possible person/object); corroborate before tasking.")
    return 0


def cmd_heatmap(args):
    from . import synth
    from .smalltarget import heatmap, heatmap_geojson
    img, _ = synth.landscape_with_people()
    grid = heatmap(img, cell=8)
    hi = max((max(r) for r in grid if r), default=1.0) or 1.0
    ramp = " .:-=+*#%@"
    print(f"COGNIS LOOKOUT | georeferenced search-priority heatmap ({len(grid)}x{len(grid[0])} cells)")
    for row in grid:
        print("".join(ramp[min(len(ramp) - 1, int((v / hi) * (len(ramp) - 1)))] for v in row))
    if args.geojson:
        gt = {"origin_lat": 40.0, "origin_lon": -105.0, "dlat": -0.0005, "dlon": 0.0005}
        with open(args.geojson, "w", encoding="utf-8") as f:
            f.write(json.dumps(heatmap_geojson(grid, gt, cell=8), indent=2))
        print(f"[+] heatmap GeoJSON -> {args.geojson}")
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog="geoshift",
                                description="Geoshift — geospatial change & pattern-of-life (non-kinetic)")
    p.add_argument("--version", action="version", version=f"geoshift {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    d = sub.add_parser("demo", help="end-to-end demo on synthetic data")
    d.set_defaults(func=cmd_demo)

    c = sub.add_parser("change", help="new-activity change detection between two windows")
    c.add_argument("--baseline", required=True)
    c.add_argument("--current", required=True)
    c.set_defaults(func=cmd_change)

    pol = sub.add_parser("pol", help="pattern-of-life anomaly detection")
    pol.add_argument("--observations", required=True)
    pol.set_defaults(func=cmd_pol)

    s = sub.add_parser("search", help="wide-area small-target search (lost hiker/object)")
    s.add_argument("--k", type=float, default=5.0, help="CFAR threshold (sigma)")
    s.add_argument("--pfa", type=float, help="target probability of false alarm (overrides --k)")
    s.add_argument("--stack", action="store_true", help="SNR-stack multiple passes for a faint target")
    s.set_defaults(func=cmd_search)

    h = sub.add_parser("heatmap", help="georeferenced search-priority heatmap")
    h.add_argument("--geojson")
    h.set_defaults(func=cmd_heatmap)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
