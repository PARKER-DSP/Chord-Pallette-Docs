#!/usr/bin/env python3
"""Watch docs/ for markdown changes and regenerate mkdocs nav."""

import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
NAV_SCRIPT = ROOT / "scripts" / "generate_nav.py"
POLL_SECONDS = 1.0


def latest_mtime() -> float:
    newest = 0.0
    for root, _, files in os.walk(DOCS_DIR):
        for name in files:
            if not name.lower().endswith(".md"):
                continue
            path = Path(root) / name
            newest = max(newest, path.stat().st_mtime)
    return newest


def rebuild_nav() -> int:
    proc = subprocess.run([sys.executable, str(NAV_SCRIPT)], cwd=ROOT)
    return proc.returncode


def main() -> int:
    if not DOCS_DIR.exists():
        print(f"docs directory missing: {DOCS_DIR}", file=sys.stderr)
        return 1
    if not NAV_SCRIPT.exists():
        print(f"nav script missing: {NAV_SCRIPT}", file=sys.stderr)
        return 1

    print("Watching docs/ for markdown changes. Press Ctrl+C to stop.")
    last = latest_mtime()
    while True:
        try:
            time.sleep(POLL_SECONDS)
            current = latest_mtime()
            if current > last:
                print("Change detected. Rebuilding nav...")
                code = rebuild_nav()
                if code != 0:
                    print(f"Nav generation failed with exit code {code}", file=sys.stderr)
                else:
                    print("Nav rebuilt.")
                last = current
        except KeyboardInterrupt:
            print("\nStopped nav watcher.")
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
