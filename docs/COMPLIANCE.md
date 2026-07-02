# Standards & Compliance Posture — an honest statement

Cognis Lookout is engineered *toward* defense-grade GEOINT needs. This states
plainly what is implemented versus what formal military acceptance requires. We do
**not** claim the software "meets all military requirements" — that is a
determination made by a sponsoring authority through a formal process.

## Implemented (verifiable in-repo)
- **Controllable false-alarm rate** — CA-CFAR threshold set directly or from a
  target probability of false alarm (`pfa_to_k`).
- **ROC characterization** — `bench/` sweeps threshold and reports detection
  probability vs false alarms; monotonicity checked.
- **Sensitivity management** — multi-pass SNR stacking recovers faint targets
  below single-pass detectability.
- **Reproducibility** — deterministic algorithms, fixed-seed synthetic ground
  truth, identical outputs for identical inputs.
- **Supply-chain minimalism** — zero third-party dependencies; runs offline.
- **Interoperability** — GeoJSON detections and georeferenced heatmap polygons.
- **Ethical scope** — detection/monitoring only; non-kinetic; analyst-corroborated.

## NOT yet done — required for formal military acceptance
- Independent Test & Evaluation against government reference imagery and a defined
  operational requirement.
- ATO / RMF accreditation (NIST 800-53) for any deployment enclave.
- Conformance to applicable geospatial standards with real commercial-imagery/SAR
  feeds (this repo is characterized on synthetic ground truth).
- Human-factors, safety, and cyber-hardening reviews per the sponsoring program.

## Summary
Robust, tested, characterized, reproducible — a credible TRL-5/6 prototype.
Formal compliance is achieved *with* a sponsor through the processes above.
