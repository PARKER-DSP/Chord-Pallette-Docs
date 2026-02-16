#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
MKDOCS_FILE = ROOT / "mkdocs.yml"
MERMAID_CHECK = ROOT / "tools" / "check_mermaid_syntax.py"

CANONICAL_MKDOCS = """site_name: ChordPallette Docs
site_description: Professional product, engineering, UX, and GTM documentation for ChordPallette.

watch:
  - docs
  - mkdocs.yml

theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - toc.follow
    - content.code.copy

markdown_extensions:
  - admonition
  - toc:
      permalink: true
  - tables
  - def_list
  - footnotes
  - attr_list
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format

extra_javascript:
  - https://unpkg.com/mermaid@10/dist/mermaid.min.js
  - javascripts/mermaid-init.js

nav:
  - Home: index.md
  - Start Here:
      - Start Here Overview: start-here.md
      - Product Overview: 00-foundation/product-overview.md
      - How to Use These Docs: 00-foundation/how-to-use-these-docs.md
  - Product Foundation:
      - Foundation Overview: 00-foundation/product-overview.md
      - Jobs To Be Done: 00-foundation/jtbd.md
      - Personas: 00-foundation/personas.md
      - Positioning: 00-foundation/positioning.md
      - Reading Paths: 00-foundation/reading-paths.md
  - Feature Guide:
      - Feature Guide Introduction: 02-features/overview.md
      - Voice Leading:
          - Voice Leading Overview: 02-features/voice-leading/overview.md
          - Voice Leading Operator Pack UX: 02-features/voice-leading/operator-pack-ux.md
      - Operators:
          - Operator Overview: 02-features/operators/overview.md
          - Operator System: 02-features/operators/operator-system.md
          - Operator Catalog: 02-features/operators/operator-catalog.md
  - Developer Guide:
      - Developer Onboarding Overview: 01-developer/onboarding.md
      - Developer Onboarding Hub: 01-developer/onboarding/index.md
      - Human Developer Path: 01-developer/onboarding/human-developer-path.md
      - AI Agent Path: 01-developer/onboarding/ai-agent-path.md
      - Architecture:
          - Architecture Index: 01-developer/architecture/index.md
          - Architecture Overview: 01-developer/architecture/architecture-overview.md
          - Architecture Principles: 01-developer/architecture/architecture-principles.md
          - Module Boundaries: 01-developer/architecture/module-boundaries.md
          - Realtime Safety: 01-developer/architecture/realtime-safety.md
          - Threading and Lifecycle: 01-developer/architecture/threading-and-lifecycle.md
          - Playability Overlays Spec: 01-developer/architecture/playability-overlays-spec.md
          - Current Baseline: 01-developer/architecture/current-baseline.md
          - Core Object Models: 01-developer/architecture/ChordPallette_Core_Object_Models.md
          - Extended Core Objects: 01-developer/architecture/ChordPallette_Extended_Core_Objects.md
          - Migration and Serialization: 01-developer/architecture/ChordPallette_Migration_Serialization_UndoRedo.md
      - Engineering Guidelines:
          - Guidelines Overview: 01-developer/guidelines/overview.md
          - AI Agent Rules: 01-developer/guidelines/ai-agent-rules.md
          - Invariants: 01-developer/guidelines/invariants.md
          - Code Style Guide: 01-developer/guidelines/ChordPallette_Code_Style_Guide.md
          - Documentation Creation Guide: 01-developer/guidelines/ChordPallette_Documentation_Creation_Guide.md
          - Documentation Style Guide: 01-developer/guidelines/documentation-style-guide.md
          - Pro Commit Guidelines: 01-developer/guidelines/pro-commit-guidelines.md
  - UX & Design:
      - UX and Design Overview: 04-ux-design/overview.md
      - UI Patterns: 04-ux-design/ui/ui-patterns.md
      - Voice Leading UX: 04-ux-design/ui/voice-leading-ux.md
      - Visual Style Guide: 04-ux-design/style-guide/style-guide.md
  - Go-to-Market:
      - GTM Index: 03-go-to-market/index.md
      - GTM Overview: 03-go-to-market/overview.md
      - Marketing Strategy: 03-go-to-market/marketing/marketing-strategy.md
      - Launch Plan: 03-go-to-market/marketing/launch-plan.md
      - Copy Vault: 03-go-to-market/marketing/copy-vault.md
      - Market Analysis: 03-go-to-market/market-analysis.md
      - Sales One Pager: 03-go-to-market/sales/one-pager.md
      - Investor Pitch Deck: 03-go-to-market/sales/investor-pitch.md
      - Press Kit: 03-go-to-market/sales/press-kit.md
  - Vision Lab:
      - Vision Lab Index: 05-vision-lab/index.md
      - Moonshots: 05-vision-lab/moonshots.md
      - Dream Feature Template: 05-vision-lab/dream-feature-template.md
      - Research Intake Summary: 05-vision-lab/research-intake-summary.md
  - Changelog: 07-changelog/changelog.md
  - Archive:
      - Archive Index: archive/index.md
      - Migration Summary: archive/migration-summary.md
"""


def find_duplicate_top_level_keys(text: str) -> list[str]:
    keys: list[str] = []
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or line.startswith((" ", "\t")):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):", line)
        if match:
            keys.append(match.group(1))
    return sorted({key for key in keys if keys.count(key) > 1})


def run_command(command: list[str], description: str) -> int:
    print(f"[docs-tool] {description}")
    return subprocess.call(command, cwd=ROOT)


def ensure_mkdocs_available() -> int:
    if importlib.util.find_spec("mkdocs") is None:
        print("mkdocs is not installed in the active Python environment.")
        print("Install dependencies with: python -m pip install -r requirements-dev.txt")
        return 1
    return 0


def cmd_generate_nav(_args: argparse.Namespace) -> int:
    MKDOCS_FILE.write_text(CANONICAL_MKDOCS, encoding="utf-8")
    print("mkdocs.yml nav synchronized to canonical structure")
    return 0


def cmd_check_yaml(_args: argparse.Namespace) -> int:
    raw = MKDOCS_FILE.read_text(encoding="utf-8")
    duplicates = find_duplicate_top_level_keys(raw)
    if duplicates:
        print("Duplicate top-level YAML keys found: " + ", ".join(duplicates))
        return 1
    print("mkdocs.yml top-level key uniqueness check passed")
    return 0


def cmd_check_brand(_args: argparse.Namespace) -> int:
    disallowed_patterns = [re.compile(r"\bChord Palette\b", re.I), re.compile(r"\bChord-Palette\b", re.I)]
    failures: list[str] = []
    for doc_path in DOCS_DIR.rglob("*.md"):
        text = doc_path.read_text(encoding="utf-8", errors="ignore")
        for pattern in disallowed_patterns:
            if pattern.search(text):
                failures.append(f"{doc_path.relative_to(ROOT)} -> {pattern.pattern}")
    if failures:
        print("Brand check failed\n" + "\n".join(failures))
        return 1
    print("Brand check passed")
    return 0


def cmd_check_links(_args: argparse.Namespace) -> int:
    failures: list[str] = []
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for doc_path in DOCS_DIR.rglob("*.md"):
        text = doc_path.read_text(encoding="utf-8", errors="ignore")
        for raw_target in link_pattern.findall(text):
            target = raw_target.strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            resolved_target = (doc_path.parent / target).resolve()
            if not resolved_target.exists():
                failures.append(f"{doc_path.relative_to(ROOT)} -> {raw_target}")
    if failures:
        print("Broken links found:\n" + "\n".join(failures))
        return 1
    print("Internal link check passed")
    return 0


def cmd_check_mermaid(_args: argparse.Namespace) -> int:
    return run_command([sys.executable, str(MERMAID_CHECK)], "Running Mermaid guardrail check")


def cmd_check_all(args: argparse.Namespace) -> int:
    for checker in (cmd_check_yaml, cmd_check_brand, cmd_check_links, cmd_check_mermaid):
        exit_code = checker(args)
        if exit_code != 0:
            return exit_code
    print("All docs checks passed")
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    availability_exit_code = ensure_mkdocs_available()
    if availability_exit_code != 0:
        return availability_exit_code

    command = [sys.executable, "-m", "mkdocs", "build"]
    if args.strict:
        command.append("--strict")
    return run_command(command, "Building docs")


def cmd_serve(args: argparse.Namespace) -> int:
    availability_exit_code = ensure_mkdocs_available()
    if availability_exit_code != 0:
        return availability_exit_code

    return run_command([sys.executable, "-m", "mkdocs", "serve", "--dev-addr", args.addr], "Starting docs server")


def cmd_ci(args: argparse.Namespace) -> int:
    exit_code = cmd_generate_nav(args)
    if exit_code != 0:
        return exit_code

    exit_code = cmd_check_all(args)
    if exit_code != 0:
        return exit_code

    return cmd_build(args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ChordPallette docs utility commands")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    subparsers.add_parser("generate-nav").set_defaults(func=cmd_generate_nav)
    subparsers.add_parser("check-yaml").set_defaults(func=cmd_check_yaml)
    subparsers.add_parser("check-brand").set_defaults(func=cmd_check_brand)
    subparsers.add_parser("check-links").set_defaults(func=cmd_check_links)
    subparsers.add_parser("check-mermaid").set_defaults(func=cmd_check_mermaid)
    subparsers.add_parser("check-all").set_defaults(func=cmd_check_all)

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--strict", action="store_true", help="Run mkdocs build --strict")
    build_parser.set_defaults(func=cmd_build)

    serve_parser = subparsers.add_parser("serve")
    serve_parser.add_argument("--addr", default="127.0.0.1:8000", help="mkdocs dev server address")
    serve_parser.set_defaults(func=cmd_serve)

    ci_parser = subparsers.add_parser("ci")
    ci_parser.add_argument("--strict", action="store_true", help="Run mkdocs build --strict")
    ci_parser.set_defaults(func=cmd_ci)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
