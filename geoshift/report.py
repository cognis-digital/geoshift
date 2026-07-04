"""Human-readable / JSON GEOINT products."""

from __future__ import annotations

import json


def render_json(product) -> str:
    return json.dumps(product, indent=2)


def render_text(product) -> str:
    L = []
    L.append("=" * 70)
    L.append("  COGNIS LOOKOUT  |  Geospatial Change & Pattern-of-Life")
    L.append("  Cognis Digital LLC - detection & monitoring, non-kinetic")
    L.append("=" * 70)
    na = product.get("new_activity", [])
    L.append(f"New-activity hotspots: {len(na)}")
    for h in na[:8]:
        L.append(f"   cell {h['cell']} current={h['current']} surge={h['surge']}x conf={h['confidence']:.2f}")
    an = product.get("anomalies", [])
    if an:
        L.append(f"Pattern-of-life anomalies: {len(an)}")
        for a in an[:8]:
            L.append(f"   {a['id']} cell={a['cell']} hour={a['hour']} {','.join(a['reasons'])} conf={a['confidence']:.2f}")
    L.append("")
    L.append("NOTE: Confidence-scored leads for analysis; corroborate before acting.")
    return "\n".join(L)
