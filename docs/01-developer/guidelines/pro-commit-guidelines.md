---
audience: contributors
status: canonical
owner: docs
last_reviewed: 2026-02-16
---

# Pro Commit Guidelines

This page defines the quality bar for documentation commits in this repository.

## Definition of a Pro Docs Commit

A docs commit is "pro" only when it is:

1. one coherent objective
2. structurally consistent with canonical information architecture
3. validated for nav, links, and brand consistency
4. clear about what changed and why

## Required Workflow

1. Define scope in one sentence.
2. Update only the files needed for that scope.
3. Ensure edited canonical docs have valid frontmatter metadata.
4. If nav changed, run:
   - `python tools/docs_tool.py generate-nav`
5. Run checks:
   - `python tools/docs_tool.py check-all`
6. Build docs:
   - `python tools/docs_tool.py build`
7. Inspect diff for accidental churn before commit.

## Commit Message Standard

Use:

```text
type(scope): imperative summary
```

Recommended `type` values:

- `docs`
- `refactor`
- `chore`

## Hard Fail Conditions

Do not commit when any of the following is true:

1. broken internal links remain
2. canonical nav and generated nav are out of sync
3. edited canonical page is missing required metadata
4. change introduces duplicate canonical pages for same concept
5. diff includes unrelated files

## Related Docs

- [Invariants](invariants.md)
- [AI Agent Rules](ai-agent-rules.md)
- [Documentation Style Guide](documentation-style-guide.md)
