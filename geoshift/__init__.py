"""Geoshift — geospatial change detection & pattern-of-life for counternarcotics.

Grid-based change detection surfaces newly-active areas between two time windows;
pattern-of-life analysis flags observations outside an entity's normal
locations/hours; geofencing flags entries/dwell in areas of interest. Detection
and monitoring only — leads for lawful analysis, not targeting.

(c) 2026 Cognis Digital LLC (Wyoming, USA). Source-available under COCL-1.0.
"""

__version__ = "0.3.0"
__all__ = ["geo", "grid", "change", "patternoflife", "geofence",
           "smalltarget", "report", "synth"]
