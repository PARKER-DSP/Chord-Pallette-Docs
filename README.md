# ChordPallette — Documentation Repository

This repository is the canonical, human-readable source for ChordPallette product, feature, engineering, UX, and go-to-market documentation.

## Information architecture

Primary documentation is organized into:
- Home
- Start Here
- Product Foundation
- Feature Guide
- Developer Guide
- UX & Design
- Go-to-Market
- Changelog
- Archive (non-authoritative)

## Local setup

1. Install dependencies:
   ```bash
   pip install mkdocs mkdocs-material pymdown-extensions pyyaml
   ```
2. Synchronize canonical navigation:
   ```bash
   python tools/docs_tool.py generate-nav
   ```
3. Run docs quality checks:
   ```bash
   python tools/docs_tool.py check-yaml
   python tools/docs_tool.py check-brand
   python tools/docs_tool.py check-links
   python tools/check_mermaid_syntax.py
   ```
4. Build docs:
   ```bash
   mkdocs build
   ```

## Contribution guidance

- Add or update canonical docs in existing topic domains instead of creating duplicate trees.
- Use relative links to canonical pages.
- Move superseded material to `docs/archive/legacy/` and mark as non-authoritative.
- Include frontmatter metadata: `audience`, `status`, `owner`, `last_reviewed`.
