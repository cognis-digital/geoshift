from bench import evaluate
from geoshift import synth
from geoshift.change import detect_new_activity
from geoshift.geo import cell_of, haversine_km
from geoshift.geofence import check
from geoshift.patternoflife import anomalies, build_profile


def test_cell_and_haversine():
    assert cell_of(0.07, 0.12, (0.0, 0.0), 0.05) == (1, 2)
    assert 110 < haversine_km(0, 0, 1, 0) < 112


def test_change_detects_planted_hotspots():
    base, cur, planted = synth.change_scenario()
    hot = detect_new_activity(base, cur, origin=synth.ORIGIN, cell_deg=synth.CELL)
    pred = {tuple(h["cell"]) for h in hot}
    assert planted <= pred


def test_pol_flags_planted_anomalies():
    obs, planted = synth.pol_scenario()
    prof = build_profile(obs, origin=synth.ORIGIN, cell_deg=synth.CELL)
    an = {a["id"] for a in anomalies(obs, prof, origin=synth.ORIGIN, cell_deg=synth.CELL)}
    assert planted <= an


def test_geofence():
    obs = [{"id": "a", "lat": 1.0, "lon": 1.0}, {"id": "b", "lat": 9.0, "lon": 9.0}]
    fence = {"name": "aoi", "min_lat": 0.5, "max_lat": 2.0, "min_lon": 0.5, "max_lon": 2.0}
    ev = check(obs, [fence])
    assert ev[0]["entries"] == 1 and ev[0]["observation_ids"] == ["a"]


def test_bench_gates():
    r = evaluate.evaluate()
    assert r["change_detection"]["recall"] == 1.0
    assert r["pattern_of_life"]["recall"] == 1.0
    assert r["determinism"] is True
