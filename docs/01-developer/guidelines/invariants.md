---
audience: contributors
status: canonical
owner: docs
last_reviewed: 2026-02-16
---

# Documentation Invariants

These are non-negotiable repository rules for docs structure and consistency.

## Canonical Source Rules

1. Pages referenced by `mkdocs.yml` navigation are canonical.
2. Canonical pages must include frontmatter:
   - `audience`
   - `status`
   - `owner`
   - `last_reviewed`
3. Canonical content must not depend on non-canonical files for core definitions.

## Structure Rules

1. Keep concerns separated by domain folders:
   - `00-foundation`
   - `01-developer`
   - `02-features`
   - `03-go-to-market`
   - `04-ux-design`
   - `05-vision-lab`
   - `07-changelog`
   - `archive`
2. Raw intake and superseded material belong in archive/intake paths, not canonical trees.
3. Avoid duplicate pages that define the same concept with different wording.

## Linking Rules

1. Use relative internal links for canonical page references.
2. Prefer linking to the canonical page instead of restating full content.
3. Do not leave broken internal links.

## Navigation Rules

1. `mkdocs.yml` and `tools/docs_tool.py` canonical nav must stay synchronized.
2. If nav changes, run `python tools/docs_tool.py generate-nav`.

## Brand and Tone Rules

1. Use `ChordPallette` consistently in canonical docs.
2. Maintain professional, concise, evidence-oriented tone.
3. Separate factual specification from speculative ideas.

## High-Risk Pages

Use extra care when editing:

- `docs/01-developer/architecture/ChordPallette_Core_Object_Models.md`
- `docs/01-developer/architecture/ChordPallette_Migration_Serialization_UndoRedo.md`
- `docs/03-go-to-market/market-analysis.md`

These pages influence multiple linked sections and should stay internally consistent.
