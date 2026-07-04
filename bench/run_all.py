"""Run verification; write bench/results.json and RESULTS.md."""

from __future__ import annotations

import json
import os
import platform
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bench import evaluate  # noqa: E402
from geoshift import synth  # noqa: E402
from geoshift.change import detect_new_activity  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def _perf():
    rows = []
    for n in (2000, 10000, 40000):
        base = [{"id": f"b{i}", "lat": (i % 200) * 0.05, "lon": (i % 137) * 0.05,
                 "ts": "2026-01-01T10:00:00Z"} for i in range(n)]
        cur = base + base[: n // 5]
        t0 = time.perf_counter()
        detect_new_activity(base, cur)
        dt = time.perf_counter() - t0
        rows.append({"observations": len(cur), "detect_s": round(dt, 4),
                     "obs_per_s": int(len(cur) / dt) if dt > 0 else None})
    return rows


def render_md(a, perf, env) -> str:
    c, pol = a["change_detection"], a["pattern_of_life"]
    L = []
    L.append("# Geoshift — Verification Results\n")
    L.append("Reproduce with: `python bench/run_all.py`.\n")
    L.append(f"Environment: {env['implementation']} {env['python']} on {env['system']}/{env['machine']}. "
             "Deterministic synthetic data; detection/monitoring only.\n")
    L.append("| Metric | Value |")
    L.append("|---|---|")
    L.append(f"| Change detection (new activity) | P={c['precision']:.3f} / R={c['recall']:.3f} / F1={c['f1']:.3f} |")
    L.append(f"| Pattern-of-life anomaly | P={pol['precision']:.3f} / R={pol['recall']:.3f} / F1={pol['f1']:.3f} |")
    L.append(f"| Determinism | {a['determinism']} |")
    L.append("")
    L.append("## Performance (single-thread, stdlib only)\n")
    L.append("| Observations | Detect (s) | Obs/s |")
    L.append("|---:|---:|---:|")
    for r in perf:
        L.append(f"| {r['observations']:,} | {r['detect_s']} | {r['obs_per_s']:,} |")
    L.append("")
    L.append("Gated in CI by `tests/test_bench.py`. See `docs/LIMITATIONS.md`.\n")
    return "\n".join(L)


def main():
    a = evaluate.evaluate()
    perf = _perf()
    env = {"python": platform.python_version(), "implementation": platform.python_implementation(),
           "system": platform.system(), "machine": platform.machine()}
    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as f:
        json.dump({"accuracy": a, "performance": perf, "environment": env}, f, indent=2)
    with open(os.path.join(ROOT, "RESULTS.md"), "w", encoding="utf-8") as f:
        f.write(render_md(a, perf, env))
    print("[+] wrote bench/results.json and RESULTS.md")
    print(render_md(a, perf, env))


if __name__ == "__main__":
    main()
