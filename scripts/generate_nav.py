#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
print("Deprecated: use tools/docs_tool.py generate-nav")
raise SystemExit(subprocess.call([sys.executable, str(ROOT / 'tools' / 'docs_tool.py'), 'generate-nav']))
