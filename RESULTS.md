# Geoshift — Verification Results

Reproduce with: `python bench/run_all.py`.

Environment: CPython 3.14.0 on Windows/AMD64. Deterministic synthetic data; detection/monitoring only.

| Metric | Value |
|---|---|
| Change detection (new activity) | P=1.000 / R=1.000 / F1=1.000 |
| Pattern-of-life anomaly | P=0.600 / R=1.000 / F1=0.750 |
| Determinism | True |

## Performance (single-thread, stdlib only)

| Observations | Detect (s) | Obs/s |
|---:|---:|---:|
| 2,400 | 0.0026 | 917,115 |
| 12,000 | 0.0137 | 872,771 |
| 48,000 | 0.0517 | 928,641 |

Gated in CI by `tests/test_bench.py`. See `docs/LIMITATIONS.md`.
