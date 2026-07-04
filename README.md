<h1 align="center">🟣 Geoshift</h1>
<p align="center"><b>Geospatial change detection &amp; pattern-of-life for counternarcotics</b><br>
<i>Surface newly-active areas, flag off-pattern activity, and geofence areas of interest — self-hosted, offline.</i></p>

<p align="center">
<img alt="license" src="https://img.shields.io/badge/license-COCL--1.0-6D28D9">
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-6D28D9">
<img alt="deps" src="https://img.shields.io/badge/dependencies-none%20(stdlib)-6D28D9">
<img alt="status" src="https://img.shields.io/badge/status-v0.1.0-6D28D9">
</p>

---

> **Built for:** SOLIC Accelerator / ONIX OTA — **Challenge Area 3: Advanced Geospatial Intelligence for Counternarcotics.**
> Near-real-time change detection, AI-style anomaly alerting on trafficking-relevant signatures, and pattern-of-life surveillance — at lower cost than legacy systems.

> 🛡️ **Detection & monitoring only — non-kinetic.** Confidence-scored leads for lawful analysis, not targeting.

## What it does

- 🗺️ **Change detection** — grids activity into AOI cells and flags cells that became newly active between two time windows (surge + confidence).
- 🔎 **Pattern-of-life** — learns an entity's normal cells/hours, flags off-pattern observations (location and/or time anomalies).
- 📍 **Geofencing** — entry/dwell detection over areas of interest.
- 🔬 **Wide-area small-target search** — CA-CFAR pulls a faint **1–2 pixel target** (lost hiker, small object) out of vast terrain in overhead imagery; exports GeoJSON search leads.
- 🔒 **Offline / zero-dependency** — pure Python stdlib.

## Quick start

```bash
git clone https://github.com/cognis-digital/geoshift
cd geoshift
python -m geoshift demo
```

## Verification & proof

Gated in CI (`python bench/run_all.py` → [`RESULTS.md`](RESULTS.md)):

| Metric | Value |
|---|---|
| Change detection (new activity) | P/R/F1 = **1.00** |
| Pattern-of-life anomaly | R = **1.00**, P = 0.60 (honest: anomaly detection has false positives) |
| Determinism | ✓ |

## License

Source-available under **COCL v1.0** (see [LICENSE](LICENSE)). Detection/monitoring
only — see [NOTICE](NOTICE).

<p align="center"><sub>© 2026 Cognis Digital LLC · <a href="https://cognis.digital">cognis.digital</a></sub></p>
