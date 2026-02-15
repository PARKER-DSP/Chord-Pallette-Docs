# Pro Commit Guidelines

This document defines the required quality bar for every commit (human or AI-authored).

## Pro Commit Definition

A commit is "pro" only if all of the following are true:

1. One coherent objective with minimal, reviewable scope.
2. Project version is incremented in `CMakeLists.txt` and is strictly greater than `HEAD`.
3. Commit notes are updated in `Docs/COMMIT_NOTES.md` with a version-first heading:
   - `## X.Y.Z - YYYY-MM-DD - Title`
4. Validation is executed and recorded.
5. Compatibility risk is explicitly checked (plugin IDs, preset schema, parameter IDs, user-data paths).
6. Diff is clean (no accidental debug code, dead code, temporary files, or unrelated edits).

## Required Workflow (Blocking)

Run these steps in order before every commit:

1. **Define scope:** state the single objective in one sentence.

2. **Bump version:**
   - `powershell -ExecutionPolicy Bypass -File .\tools\bump-project-version.ps1`

3. **Update commit notes** in `Docs/COMMIT_NOTES.md`:
   - add a new top entry with version-first heading
   - include `What changed`, `Why it changed`, `Validation`

4. **Run version gates:**
   - `powershell -ExecutionPolicy Bypass -File .\tools\require-commit-version-bump.ps1`
   - `powershell -ExecutionPolicy Bypass -File .\tools\require-version-bump.ps1`

5. **Run build and tests** relevant to the change:
   - `cmake --build --preset vscode-release`
   - `ctest --test-dir build/chordpallette -C Release --output-on-failure`

6. **Inspect staged diff** for unrelated churn:
   - `git diff --staged --stat`
   - `git diff --staged`

7. **Use a professional commit message** (see format below).

8. **Commit only** after all checks pass.

9. **Push immediately** after each commit unless explicitly told not to:
   - `git push origin main`

## Commit Message Standard

### Format

```
type(scope): imperative summary

Body paragraph(s) with context and rationale.
```

### Subject Line Rules

- Format: `type(scope): imperative summary`
- Length: keep under 72 characters if possible
- Style: use present tense imperatives ("add", "fix", "improve", not "added", "fixed", "improved")

### Allowed `type` values

- `feat` – new user-facing feature
- `fix` – bug fix
- `refactor` – code reorganization without behavior change
- `docs` – documentation only
- `test` – test additions or modifications
- `chore` – maintenance, tooling, or metadata
- `build` – build system changes
- `ci` – CI/CD workflow changes

### Message Body

Must include:

1. **What changed** – concrete summary of modifications
2. **Why it changed** – motivation or problem solved
3. **Risk or compatibility notes** – any breaking changes, schema implications, or migration needs
4. **Validation summary** – commands run and results

### Example Commit

```
fix(selection): support shift-range and ctrl-toggle block selection

Add range selection anchored to the last selected block and ctrl-based 
additive toggling. This removes multi-select friction in dense chord banks.

Compatibility: no state schema or plugin identity changes.
Validation: built Release target and manually verified selection behavior 
in standalone.
```

## Commit Notes Template

Use this exact structure in `Docs/COMMIT_NOTES.md`:

```markdown
## X.Y.Z - YYYY-MM-DD - Short Title

### What changed
- Bullet list of specific changes

### Why it changed
- Motivation or problem solved

### Validation
- Build command and result
- Test commands and result
- Manual testing notes (if applicable)
```

## Hard Fail Conditions (Do Not Commit)

1. Version is unchanged or not strict `X.Y.Z` format.
2. Commit notes heading is not version-first (`## X.Y.Z - ...`).
3. Validation was skipped without explicit reason in commit notes.
4. Commit mixes unrelated objectives (e.g., feature + bugfix + refactor in one commit).
5. Diff contains:
   - unreviewed generated output or binary artifacts
   - temporary debug code or console logging
   - commented-out code sections
   - unrelated file changes

## Related Documents

- [AI Agent Rules](ai-agent-rules.md) – working style and checks for autonomous agents
- [Invariants](invariants.md) – backward compatibility and safety guardrails
- [Commit Notes Log](../../archive/legacy/08-development/COMMIT_NOTES.md) – historical record of all commits
