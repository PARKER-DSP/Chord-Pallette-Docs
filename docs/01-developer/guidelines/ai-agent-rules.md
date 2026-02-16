---
audience: ai_agents
status: canonical
owner: docs
last_reviewed: 2026-02-16
---

# AI Agent Rules

These rules are for autonomous contributors working in this documentation repository.

## Human-First Standard

- Optimize for reader understanding before optimization for token count.
- Prefer plain language over abstract phrasing.
- Keep pages scannable and actionable for humans.
- If a concept is already documented canonically, link to it instead of rewriting it.

## Primary Objective

Maintain one coherent source of truth across canonical docs while preserving archival context in non-authoritative locations.

## Explicit Agentic Execution Flow

1. Read context pages:
   - [Start Here](../../start-here.md)
   - [Architecture Index](../architecture/index.md)
   - [Guidelines Overview](overview.md)
2. Classify input material as one of:
   - canonical update candidate
   - experimental concept (Vision Lab)
   - archive/intake reference
3. Create a destination map before editing.
4. Edit canonical pages with minimal scope and no duplicate trees.
5. Ensure every edited canonical page has frontmatter metadata.
6. Add internal links to related canonical docs.
7. If navigation changed, regenerate `mkdocs.yml` with:
   - `python tools/docs_tool.py generate-nav`
8. Run validation:
   - `python tools/docs_tool.py check-all`
9. Build docs:
   - `python tools/docs_tool.py build`
10. Report exactly what changed, what was validated, and any remaining gaps.

## Hard Constraints

- Do not treat `docs/archive/legacy/` or intake folders as canonical truth.
- Do not introduce duplicate canonical pages for the same concept.
- Do not leave unresolved internal links.
- Do not change brand spelling (`ChordPallette`) in canonical docs.
- Do not silently remove historical docs without updating archive indexes.

## Preferred Change Shape

- One focused objective per change.
- Small, reviewable edits with explicit rationale.
- Keep future agent handoff clear through updated links and metadata.

## Related Docs

- [Invariants](invariants.md)
- [Documentation Creation Guide](ChordPallette_Documentation_Creation_Guide.md)
- [Pro Commit Guidelines](pro-commit-guidelines.md)
