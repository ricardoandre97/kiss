#!/usr/bin/env python3
"""Rewrite counters.js from WHO and DELTA environment variables."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COUNTERS_PATH = ROOT / "counters.js"
PATTERN = re.compile(r"window\.COUNTERS\s*=\s*(\{[^;]*\})\s*;", re.DOTALL)


def main() -> int:
    who = os.environ.get("WHO", "").strip().lower()
    delta_raw = os.environ.get("DELTA", "").strip()

    if who not in {"cat", "duck"}:
        print(f"WHO must be cat or duck, got {who!r}", file=sys.stderr)
        return 1

    try:
        delta = int(delta_raw)
    except ValueError:
        print(f"DELTA must be an integer, got {delta_raw!r}", file=sys.stderr)
        return 1

    text = COUNTERS_PATH.read_text(encoding="utf-8")
    match = PATTERN.search(text)
    if not match:
        print("Could not find window.COUNTERS in counters.js", file=sys.stderr)
        return 1

    data = json.loads(match.group(1))
    cat = int(data.get("cat", 0))
    duck = int(data.get("duck", 0))
    current = cat if who == "cat" else duck
    updated = max(0, current + delta)

    if who == "cat":
        cat = updated
    else:
        duck = updated

    COUNTERS_PATH.write_text(
        "// Managed by CI. Keep this object valid JSON (quoted keys).\n"
        "window.COUNTERS = "
        + json.dumps({"cat": cat, "duck": duck}, separators=(", ", ": "))
        + ";\n",
        encoding="utf-8",
    )
    print(f"{who}: {current} + ({delta}) -> {updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
