# Changelog

Adheres to [Semantic Versioning](https://semver.org/).

## [0.3.0] — 2026-07-02

### Added
- **Multi-pass SNR stacking** (`detect_with_stacking`) to recover a faint target
  below single-pass detectability; **Pfa-controlled CFAR** (`pfa_to_k`).
- **Georeferenced search-priority heatmap** (`heatmap`, `heatmap_geojson`) — dense
  CA-CFAR SNR surface as graded GeoJSON polygons; CLI `heatmap`.
- **ROC characterization** in `bench/` + honest `docs/COMPLIANCE.md`.

## [0.2.0] — 2026-07-02

### Added
- **Wide-area small-target detection** (`smalltarget.py`): CA-CFAR point-target
  detection to find a faint 1–2 pixel target — a lost hiker or small object —
  against vast terrain in overhead imagery, with GeoJSON export ("possible
  person/object" leads). CLI `search`; small-target recall gated in CI.
- Verified: recovers all planted faint targets (recall 1.0) at ~8 sigma.

## [0.1.0] — 2026-07-01

Initial public release.

### Added
- AOI grid binning + geospatial helpers — `grid`, `geo`.
- Change detection (new-activity hotspots between two windows) — `change`.
- Pattern-of-life profiling + anomaly detection — `patternoflife`.
- Geofence entry/dwell detection — `geofence`.
- Deterministic synthetic generators with planted ground truth — `synth`.
- CLI (`cognis-lookout`): `demo`, `change`, `pol`.
- Verification harness: change + pattern-of-life metrics + performance;
  results in `RESULTS.md`. 5 tests. CI across Python 3.9–3.13.
