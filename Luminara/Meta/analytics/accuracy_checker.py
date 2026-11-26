#!/usr/bin/env python3
"""
accuracy_checker.py — standalone verifier for route.py PRIMARY-target accuracy.

Design (per plan):
  - Reads Meta/analytics/bench/corpus.jsonl (gold: id, subset, source, gold, lore).
  - For each subset dir Meta/analytics/bench/subset_N/, loads its articles as the
    known-entity menu, then evaluates every corpus case tagged with that subset by
    calling the REAL route.py logic (DET = Layer-1 only, MOD = model-only,
    HYB = actual route_sentence).
  - Reports PER-SUBSET and AGGREGATE accuracy for DET/MOD/HYB, plus a human-vs-ai
    breakdown, and lists every failing id (predicted vs gold).

GATE (OPT-IN, three ways — matches Cecìl's approved toggle):
  - built-in GATE_ENABLED = False  (default OFF: always exits 0)
  - --strict flag
  - ROUTE_BENCH_GATE=1 env var
  When on and AGGREGATE HYB < 0.9 -> sys.exit(1). Otherwise always 0.

No script emits the gate; this checker is the only thing that enforces it, and
only when you opt in. Normal usage just prints the scoreboard and exits 0.

Usage:
  python3 accuracy_checker.py                # all 6 subsets, gate off
  python3 accuracy_checker.py --subset 3     # only subset 3
  ROUTE_BENCH_GATE=1 python3 accuracy_checker.py   # enforce >=0.9 aggregate
"""
import argparse
import json
import os
import re
import sys

# Allow importing route.py / scribe from the project root.
ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "Meta", "analytics"))

import scribe
import route as R

BENCH = os.path.join(ROOT, "Meta", "analytics", "bench")
CORPUS = os.path.join(BENCH, "corpus.jsonl")

GATE_ENABLED = False  # default OFF — safe. Flip to True, or use --strict / env.

# Pacing between model calls. The local W6600 server degrades (intermittent
# [Errno -2] DNS drops) when hammered with rapid sequential requests, which
# made batch HYB runs artificially low. A short sleep between calls lets the
# server breathe and makes the HYB number reproducible. Set --pace 0 to disable.
PACE = 1.5


def load_corpus():
    rows = []
    with open(CORPUS, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def norm(t):
    """Normalize a predicted/gold target for comparison (case + NEW: insensitive)."""
    if t is None:
        return ""
    t = t.strip()
    if t.startswith("NEW:"):
        t = t[4:]
    return t.strip().lower()


def correct(pred, gold):
    return norm(pred) == norm(gold)


def evaluate_case(row):
    """Return (det_pred, mod_pred, hyb_pred) for one corpus row.

    HYB is measured by invoking the REAL route.py as a subprocess with the
    subset dir as --vault (exactly how web.py / harness.py use it), then
    parsing the PRIMARY line from stdout. This is the faithful hybrid measure
    and avoids inline-import model-call quirks.
    """
    import subprocess as _sp
    subset_dir = os.path.join(BENCH, f"subset_{row['subset']}")
    ents = scribe.load_entities(subset_dir)
    aliases = scribe.load_aliases(subset_dir)
    nlp = R.get_nlp()
    s = row["lore"]

    # --- DET: Layer-1 only (no model). Inline call with a dummy URL so the
    # model is never contacted; mimics a --no-model run. Reliable, no network.
    det = R.route_sentence(s, 1, "", ents, aliases, nlp,
                           "http://x", "m", None)
    det_primary = det[0]

    # --- HYB: the real pipeline. Shell out to route.py exactly as the
    # production callers do (run("route.py", "--lore", ...)) and parse the
    # PRIMARY target. Pace it so the local GPU server isn't hammered.
    import time as _time
    if PACE:
        _time.sleep(PACE)
    try:
        out = _sp.run(
            [sys.executable, os.path.join(ROOT, "route.py"),
             "--lore", s, "--vault", subset_dir],
            capture_output=True, text=True, timeout=180)
        primary = None
        for line in out.stdout.splitlines():
            if "-> PRIMARY:" in line:
                # format: "    -> PRIMARY: <target>  (<method>)"
                primary = line.split("-> PRIMARY:")[1].split("(")[0].strip()
                break
        hyb_primary = primary
    except Exception as e:
        print(f"(checker subprocess failed: {e})", file=sys.stderr)
        hyb_primary = None

    # MOD (model-only) is a diagnostic; reuse the HYB subprocess result is not
    # pure-model, so we approximate MOD as None here and rely on HYB/DET.
    mod_primary = None
    return det_primary, mod_primary, hyb_primary


def main():
    ap = argparse.ArgumentParser(description="Route accuracy checker (opt-in gate).")
    ap.add_argument("--bench", default=BENCH)
    ap.add_argument("--subset", type=int, default=0, help="0 = all six")
    ap.add_argument("--pace", type=float, default=PACE,
                    help=f"seconds to sleep between model calls (default {PACE}); "
                         "0 disables. Prevents W6600 overload during batch runs.")
    ap.add_argument("--strict", action="store_true", help="exit 1 if aggregate HYB < 0.9")
    args = ap.parse_args()

    gate = GATE_ENABLED or args.strict or os.environ.get("ROUTE_BENCH_GATE") == "1"
    if args.pace is not None:
        globals()["PACE"] = args.pace
    corpus = load_corpus()
    subsets = [args.subset] if args.subset else sorted({r["subset"] for r in corpus})

    agg = {"det": [0, 0], "hyb": [0, 0]}  # [correct, total]
    by_src = {"human": [0, 0], "ai": [0, 0]}

    print("=" * 70)
    for sn in subsets:
        rows = [r for r in corpus if r["subset"] == sn]
        if not rows:
            continue
        sc = {"det": [0, 0], "hyb": [0, 0]}
        fails = []
        for r in rows:
            d, m, h = evaluate_case(r)
            for key, pred in (("det", d), ("hyb", h)):
                if pred is None:
                    pred = "(unrouted)"
                ok = correct(pred, r["gold"])
                sc[key][0] += int(ok)
                sc[key][1] += 1
                agg[key][0] += int(ok)
                agg[key][1] += 1
            by_src[r["source"]][0] += int(correct(h, r["gold"]))
            by_src[r["source"]][1] += 1
            if not correct(h, r["gold"]):
                fails.append((r["id"], r["source"], d, h, r["gold"]))
        pct = lambda c, t: f"{c}/{t} ({100*c/t:.0f}%)" if t else "n/a"
        print(f"SUBSET {sn}  (n={len(rows)})")
        print(f"  DET: {pct(sc['det'][0], sc['det'][1])}   "
              f"HYB: {pct(sc['hyb'][0], sc['hyb'][1])}")
        for fid, src, d, h, g in fails:
            print(f"    FAIL {fid} [{src}] det={d} hyb={h} gold={g}")
        print()

    def pct(c, t):
        return f"{c}/{t} ({100*c/t:.0f}%)" if t else "n/a"
    print("-" * 70)
    print(f"AGGREGATE  DET: {pct(agg['det'][0], agg['det'][1])}   "
          f"HYB: {pct(agg['hyb'][0], agg['hyb'][1])}")
    print(f"  BY SOURCE (HYB): human {pct(by_src['human'][0], by_src['human'][1])}   "
          f"ai {pct(by_src['ai'][0], by_src['ai'][1])}")
    print("(MOD/model-only dropped as a measured column; HYB is the pipeline target.)")
    print("=" * 70)

    # Gate
    if gate:
        t = agg["hyb"][1]
        acc = agg["hyb"][0] / t if t else 0
        if acc < 0.9:
            print(f"GATE FAIL: aggregate HYB {acc:.2f} < 0.9")
            sys.exit(1)
        print(f"GATE PASS: aggregate HYB {acc:.2f} >= 0.9")
    sys.exit(0)


if __name__ == "__main__":
    main()
