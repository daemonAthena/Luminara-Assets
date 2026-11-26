#!/usr/bin/env python3
"""
_emit.py — shared analytics emitter for the Chronicler pipeline.

Every main-sequence stage (ground/route/scribe/drift/dedupe/commit) can emit a
structured "analytics event" describing what it decided (A: the decision) plus
light ops telemetry (B: model calls, timing, counts). Events are one JSON
object per line in an append-friendly .analytics.jsonl file, so a crash mid-run
never corrupts prior events.

NAMING CONVENTION (project-wide, per Cecìl's instruction):
    Meta/analytics/<stage>_<runid>.analytics.jsonl
  - <stage>  : ground | route | scribe | drift | dedupe  (the script name)
  - <runid>  : caller-supplied --run-id (recommended) OR a timestamp fallback.
               A shared run-id lets a checker JOIN a full pipeline pass
               (ground -> route -> scribe -> drift) for one lore batch.
  - .analytics.jsonl : unmistakably machine data, one event per line.

Emissions are OPT-IN: emit() is a no-op when run_id is falsy (i.e. the caller
did not pass --emit-analytics/--run-id). Normal runs are completely unaffected.
"""
import json
import os
import time

# Meta/analytics lives next to this file: Meta/analytics/_emit.py -> ../analytics
ANALYTICS_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "analytics"))


def emit(stage, run_id, payload):
    """Append one analytics event as a JSON line. No-op if run_id is falsy.

    Args:
        stage:   str, the script/stage name (e.g. "route")
        run_id:  str|None, the run identifier; falsy => do nothing
        payload: dict, stage-specific fields (merged into the event)
    """
    if not run_id:
        return
    os.makedirs(ANALYTICS_DIR, exist_ok=True)
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    event = {"run_id": run_id, "stage": stage, "ts": ts}
    event.update(payload)
    path = os.path.join(ANALYTICS_DIR, f"{stage}_{run_id}.analytics.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    return path


def new_run_id():
    """Default run-id when the caller does not supply one (UTC timestamp)."""
    return time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
