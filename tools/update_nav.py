#!/usr/bin/env python3
"""
update_nav.py

Scan the `docs` folder for Markdown files and append an "All Pages (auto-generated)"
section to the `nav` in `mkdocs.yml` so every document is reachable from the site nav.

Usage:
  .\.venv\Scripts\python tools\update_nav.py

This script will preserve the existing `nav` entries and add a single new
top-level entry named "All Pages (auto-generated)" that mirrors the current
`docs` folder structure.
"""
import os
import sys
from pathlib import Path

try:
    import yaml
except Exception:
    print("PyYAML is required. Install in your venv: python -m pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
MKDOCS_YML = ROOT / "mkdocs.yml"


def title_from_name(name: str) -> str:
    name = name.replace('_', ' ').replace('-', ' ')
    return name.rstrip('.md')


def insert_nested(mapping: dict, parts: list, title: str, relpath: str):
    if not parts:
        # add file entry to mapping list
        mapping.setdefault('__files__', []).append({title: relpath})
        return
    head = parts[0]
    rest = parts[1:]
    mapping = mapping.setdefault(head, {})
    insert_nested(mapping, rest, title, relpath)


def build_structure():
    tree = {}
    for root, dirs, files in os.walk(DOCS_DIR):
        rel_root = Path(root).relative_to(DOCS_DIR)
        for f in sorted(files):
            if not f.lower().endswith('.md'):
                continue
            relpath = (rel_root / f).as_posix() if str(rel_root) != '.' else f
            parts = rel_root.parts if rel_root.parts != () else []
            title = title_from_name(f)
            insert_nested(tree, list(parts), title, relpath)
    return tree


def fancy_list_from_tree(tree: dict):
    result = []

    # files at root
    for k, v in sorted(tree.items()):
        if k == '__files__':
            for ent in v:
                result.append(ent)
    # directories
    for k in sorted(tree.keys()):
        if k == '__files__':
            continue
        subtree = tree[k]
        children = fancy_list_from_tree(subtree)
        result.append({k: children})
    return result


def main():
    if not MKDOCS_YML.exists():
        print(f"mkdocs.yml not found at {MKDOCS_YML}", file=sys.stderr)
        sys.exit(1)

    with open(MKDOCS_YML, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f)

    existing_nav = cfg.get('nav', []) or []

    tree = build_structure()
    generated = fancy_list_from_tree(tree)

    # create final nav: preserve existing, but append generated section
    # remove any previous generated section to avoid duplicates
    filtered = [n for n in existing_nav if not isinstance(n, dict) or 'All Pages (auto-generated)' not in n]
    filtered.append({'All Pages (auto-generated)': generated})

    cfg['nav'] = filtered

    with open(MKDOCS_YML, 'w', encoding='utf-8') as f:
        yaml.safe_dump(cfg, f, sort_keys=False, allow_unicode=True)

    print('mkdocs.yml nav updated with auto-generated "All Pages (auto-generated)" section')


if __name__ == '__main__':
    main()
