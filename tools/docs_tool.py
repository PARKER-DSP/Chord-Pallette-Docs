#!/usr/bin/env python3
from __future__ import annotations
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / 'docs'
MKDOCS_FILE = ROOT / 'mkdocs.yml'

CANONICAL_MKDOCS = '''site_name: ChordPallette Docs
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
  - Changelog: 07-changelog/changelog.md
  - Archive:
      - Archive Index: archive/index.md
      - Migration Summary: archive/migration-summary.md
'''


def find_duplicate_top_level_keys(text: str):
    keys=[]
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith('#') or line.startswith((' ','\t')):
            continue
        m=re.match(r'^([A-Za-z0-9_-]+):', line)
        if m: keys.append(m.group(1))
    return sorted({k for k in keys if keys.count(k)>1})

def cmd_generate_nav(_):
    MKDOCS_FILE.write_text(CANONICAL_MKDOCS, encoding='utf-8')
    print('mkdocs.yml nav synchronized to canonical structure')
    return 0

def cmd_check_yaml(_):
    raw=MKDOCS_FILE.read_text(encoding='utf-8')
    d=find_duplicate_top_level_keys(raw)
    if d:
        print('Duplicate top-level YAML keys found: '+', '.join(d))
        return 1
    print('mkdocs.yml top-level key uniqueness check passed')
    return 0

def cmd_check_brand(_):
    bad=[re.compile(r'\bChord Palette\b', re.I), re.compile(r'\bChord-Palette\b', re.I)]
    fails=[]
    for p in DOCS_DIR.rglob('*.md'):
        t=p.read_text(encoding='utf-8', errors='ignore')
        for b in bad:
            if b.search(t): fails.append(f"{p.relative_to(ROOT)} -> {b.pattern}")
    if fails:
        print('Brand check failed\n'+'\n'.join(fails)); return 1
    print('Brand check passed'); return 0

def cmd_check_links(_):
    fails=[]
    link_re=re.compile(r'\[[^\]]+\]\(([^)]+)\)')
    for p in DOCS_DIR.rglob('*.md'):
        txt=p.read_text(encoding='utf-8', errors='ignore')
        for raw in link_re.findall(txt):
            tgt=raw.strip()
            if tgt.startswith(('http://','https://','mailto:','#')): continue
            tgt=tgt.split('#',1)[0]
            if not tgt: continue
            if not (p.parent / tgt).resolve().exists():
                fails.append(f"{p.relative_to(ROOT)} -> {raw}")
    if fails:
        print('Broken links found:\n'+'\n'.join(fails)); return 1
    print('Internal link check passed'); return 0

def main():
    ap=argparse.ArgumentParser()
    sp=ap.add_subparsers(dest='cmd',required=True)
    sp.add_parser('generate-nav').set_defaults(func=cmd_generate_nav)
    sp.add_parser('check-yaml').set_defaults(func=cmd_check_yaml)
    sp.add_parser('check-brand').set_defaults(func=cmd_check_brand)
    sp.add_parser('check-links').set_defaults(func=cmd_check_links)
    a=ap.parse_args(); raise SystemExit(a.func(a))

if __name__=='__main__':
    main()
