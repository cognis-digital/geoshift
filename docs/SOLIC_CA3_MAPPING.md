# SOLIC Challenge Area 3 — Capability Mapping

| Desired capability | Geoshift | Module |
|---|---|---|
| Near-real-time reporting on trafficking corridors | AOI-grid activity + change detection between windows | `grid`, `change` |
| AI-enabled change detection & anomaly alerting | New-activity hotspots + pattern-of-life anomalies (confidence-scored) | `change`, `patternoflife` |
| HVT pattern-of-life surveillance | Entity anchor/hour profiling + off-pattern flags | `patternoflife` |
| Go-fast / remote-area monitoring | Grid + geofence over maritime/land AOIs | `geofence` |
| Unclassified partner-shareable products | JSON products (GeoJSON export roadmap) | `report` |

## Non-kinetic
Detection/monitoring only, per counternarcotics ISR scope. Leads for lawful
interdiction; no targeting.

## TRL posture (honest)
- **Change/pattern-of-life/geofence (working, measured):** reproducible metrics
  in `RESULTS.md` — change-detection F1 = 1.00; pattern-of-life recall 1.00 with
  honest precision (0.60).
- **Prototype scope (post-award):** ingest real commercial-imagery/AIS feeds,
  add multi-phenomenology (EO/SAR) change detection and calibrated thresholds,
  validate against a Government reference AOI.
