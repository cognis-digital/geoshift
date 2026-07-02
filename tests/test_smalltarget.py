from bench import evaluate
from cognis_lookout import synth
from cognis_lookout.smalltarget import (
    detect_small_targets, detect_with_stacking, heatmap, heatmap_geojson,
    pfa_to_k, to_geojson,
)


def _matched(blobs, truth, tol=1.5):
    return sum(1 for (tr, tc) in truth
               if any(abs(b["row"] - tr) <= tol and abs(b["col"] - tc) <= tol for b in blobs))


def test_finds_faint_people_in_terrain():
    img, truth = synth.landscape_with_people()
    blobs = detect_small_targets(img, k=5.0)
    assert _matched(blobs, truth) == len(truth)      # recall = 1.0
    assert len(blobs) <= len(truth) + 2


def test_geojson_export():
    img, truth = synth.landscape_with_people(n_people=3)
    gt = {"origin_lat": 40.0, "origin_lon": -105.0, "dlat": -0.0005, "dlon": 0.0005}
    fc = to_geojson(detect_small_targets(img, k=5.0), gt)
    assert fc["type"] == "FeatureCollection" and fc["features"]
    assert fc["features"][0]["properties"]["kind"] == "possible-person-or-object"


def test_pfa_to_k_monotonic():
    assert pfa_to_k(1e-6) > pfa_to_k(1e-4) > pfa_to_k(1e-2)


def test_stacking_recovers_faint_target():
    frames, (tr, tc) = synth.landscape_passes()
    single = detect_small_targets(frames[0], k=5.0)
    stacked = detect_with_stacking(frames, k=5.0)
    single_hit = any(abs(b["row"] - tr) <= 1.5 and abs(b["col"] - tc) <= 1.5 for b in single)
    stacked_hit = any(abs(b["row"] - tr) <= 1.5 and abs(b["col"] - tc) <= 1.5 for b in stacked)
    assert not single_hit and stacked_hit


def test_heatmap_geojson_priority():
    img, _ = synth.landscape_with_people()
    grid = heatmap(img, cell=8)
    gt = {"origin_lat": 40.0, "origin_lon": -105.0, "dlat": -0.0005, "dlon": 0.0005}
    fc = heatmap_geojson(grid, gt, cell=8, snr_floor=3.0)
    assert fc["features"] and fc["features"][0]["geometry"]["type"] == "Polygon"
    assert fc["features"][0]["properties"]["priority"] in ("low", "medium", "high")


def test_bench_small_target_recall():
    assert evaluate.evaluate()["small_target"]["recall"] >= 0.9
