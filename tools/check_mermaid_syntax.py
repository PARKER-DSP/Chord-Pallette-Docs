#!/usr/bin/env python3
"""Static Mermaid guardrails for docs.

This check intentionally avoids external dependencies and focuses on common
Mermaid parse pitfalls we can catch cheaply during review/CI.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"

MERMAID_FENCE_RE = re.compile(r"```mermaid\n(.*?)\n```", re.DOTALL)
SUBGRAPH_RE = re.compile(r"^\s*subgraph\s+(.+?)\s*$")
EXPLICIT_SUBGRAPH_ID_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\s*\[")


def iter_mermaid_blocks(text: str):
    for match in MERMAID_FENCE_RE.finditer(text):
        yield match.group(1), text.count("\n", 0, match.start()) + 1


def validate_block(block: str, start_line: int, file_path: Path) -> list[str]:
    errors: list[str] = []
    seen_bare_subgraph_names: set[str] = set()

    for i, line in enumerate(block.splitlines(), start=start_line + 1):
        sub_match = SUBGRAPH_RE.match(line)
        if not sub_match:
            continue

        sub_decl = sub_match.group(1).strip()
        # If there is an explicit Mermaid subgraph identifier (e.g.,
        # "subgraph INTEG_OUT[Integration - Output]"), it is stable.
        if EXPLICIT_SUBGRAPH_ID_RE.match(sub_decl):
            continue

        # Bare labels (e.g., "subgraph Integration") can collide if repeated
        # in the same diagram and trigger Mermaid parser issues.
        bare = sub_decl
        if bare in seen_bare_subgraph_names:
            errors.append(
                f"{file_path}:{i}: duplicate bare subgraph name '{bare}'. "
                "Use an explicit ID form like `subgraph NAME[Label]`."
            )
        else:
            seen_bare_subgraph_names.add(bare)

    return errors


def main() -> int:
    if not DOCS_DIR.exists():
        print(f"docs directory not found: {DOCS_DIR}", file=sys.stderr)
        return 2

    errors: list[str] = []
    for path in DOCS_DIR.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for block, start_line in iter_mermaid_blocks(text):
            errors.extend(validate_block(block, start_line, path.relative_to(ROOT)))

    if errors:
        print("Mermaid guardrail check failed:\n")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Mermaid guardrail check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
