---
audience: contributors
status: canonical
owner: docs
last_reviewed: 2026-02-16
---

# Documentation Creation Guide

Use this guide when creating or refactoring documentation in this repository.

## Human-First Authoring Rules

- Lead with user understanding, not implementation trivia.
- Explain why a behavior matters before listing mechanics.
- Keep pages scannable with clear sections and short paragraphs.
- Move speculative material to Vision Lab or archive, not canonical specs.

## Canonical Document Types

| Type | Purpose | Typical Location |
| --- | --- | --- |
| Foundation | product definitions and shared language | `docs/00-foundation` |
| Developer architecture | runtime contracts and implementation boundaries | `docs/01-developer/architecture` |
| Guidelines | contribution and workflow standards | `docs/01-developer/guidelines` |
| Feature docs | behavior, UX, and system intent per feature | `docs/02-features` |
| GTM docs | strategy, launch, and messaging artifacts | `docs/03-go-to-market` |
| Vision Lab | explicit experimental or moonshot concepts | `docs/05-vision-lab` |
| Archive | historical and non-authoritative context | `docs/archive` |

## Intake-to-Canonical Process

When source material arrives from folders like:

- `docs/stuff to consider`
- `docs to incorporate/2. OLD DOCUMENTS`

follow this sequence:

1. classify each file (`canonical`, `experimental`, `archive-only`)
2. extract durable concepts and constraints
3. map each concept to a single canonical destination page
4. rewrite content to match canonical tone and metadata
5. add internal links to related canonical pages
6. keep raw intake files as context unless explicitly archived/moved

## Explicit Agentic Flow

1. Build a destination map before editing.
2. Edit canonical docs first; archive or intake references second.
3. Avoid creating new top-level trees unless required by IA.
4. Add or update frontmatter metadata on touched canonical pages.
5. Add "Related Docs" links where concept boundaries cross pages.
6. Run navigation and validation commands before handoff.

## Required Metadata

Every canonical page must include:

- `audience`
- `status`
- `owner`
- `last_reviewed` (`YYYY-MM-DD`)

## Link Strategy

- Use relative links to canonical pages.
- Link to archive only for historical context.
- Remove duplicate definitions by replacing them with canonical links.

## Validation Commands

```bash
python tools/docs_tool.py check-all
python tools/docs_tool.py build
```

If nav changed:

```bash
python tools/docs_tool.py generate-nav
```

## Definition of Done

Documentation refactor work is done when:

1. concepts are separated into the right domain pages
2. canonical pages are internally linked and consistent
3. nav, links, and build checks pass
4. archive/intake status is clear for non-canonical material
