# AI Agent Rules for This Repository

This file defines how future AI agents should operate to maximize stability,
extensibility, and human readability.

> 🎛️ **Vibe check:** this is a MIDI-first plugin codebase. Keep changes musical,
> predictable, and safe for creators in live/recording workflows.

## Quick Start (Agent Checklist)

- ✅ Read `Docs/invariants.md` before touching code.
- ✅ Keep each change small and reviewable.
- ✅ Preserve plugin IDs, parameter IDs, and preset compatibility.
- ✅ Run required validation before commit.
- ✅ Update commit notes with a version-first heading.

If any checklist item is not satisfied, pause and fix it before continuing.

## Primary Goal

Preserve behavior while improving structure. Prefer low-risk extraction and clear
boundaries over large rewrites.

## Required Working Style

1. Read `Docs/invariants.md` before code changes.
2. Read and follow `Docs/PRO_COMMIT_GUIDELINES.md` before preparing a commit.
3. Work in small, reviewable phases (one focused objective per phase).
4. Build after each phase and report exact failures if build cannot complete.
5. Never silently change persistence schema or public IDs.
6. After each completed change, write/update commit notes using this heading format:
   - `## <Version> - <YYYY-MM-DD> - <Title>`
   - the semantic version must appear first in the heading
   - hard rule: do not commit if any new commit-note heading fails `^## [0-9]+\.[0-9]+\.[0-9]+ - [0-9]{4}-[0-9]{2}-[0-9]{2} - `
7. After each completed change, include commit notes sections summarizing:
   - what changed
   - why it changed
   - any validation performed
8. Before every commit (including AI-authored commits), increment `project(... VERSION X.Y.Z ...)` in `CMakeLists.txt` so it is strictly greater than the previous commit version.
9. Before every commit, run `tools/require-commit-version-bump.ps1`; if it fails, do not commit.
10. Treat `Docs/PRO_COMMIT_GUIDELINES.md` as a blocking quality gate; do not commit until every required workflow step passes.
11. Use professional commit subjects: `type(scope): imperative summary`.
12. After every successful commit, push immediately with `git push origin main` unless the user explicitly requests local-only commits.

## Versioning Rationale and Policy

1. Use semantic versioning (`MAJOR.MINOR.PATCH`) with channel labels from `Docs/RELEASE_NOTES.md`.
2. Version bump rules:
   - `MAJOR`: backward-incompatible changes (IDs, preset/schema compatibility, migration-required behavior).
   - `MINOR`: new user-facing features or behavior changes (default for this Alpha stage).
   - `PATCH`: bug fixes, hardening, or internal refactors without meaningful new user-facing capability.
3. For this project's current maturity (Alpha), bias toward `MINOR` for meaningful UX/workflow additions and `PATCH` for isolated fixes.
4. Before release builds, ensure `CMakeLists.txt` version is greater than `Docs/LAST_RELEASED_VERSION.txt`.
5. In release/commit notes, always include brief rationale for why that bump level was chosen.
6. Per-commit rule: each commit must advance version monotonically from the previous commit. Use patch bumps for normal development commits unless a minor/major bump is explicitly justified.
7. Keep strict semantic version syntax in all version fields (`X.Y.Z` only).

## Version Metadata Consistency

1. Treat these files as one version contract:
   - `CMakeLists.txt` (`project(... VERSION X.Y.Z ...)`)
   - `Docs/RELEASE_NOTES.md`
   - `Docs/LAST_RELEASED_VERSION.txt`
2. `Docs/LAST_RELEASED_VERSION.txt` must always reflect the most recently shipped release.
3. `CMakeLists.txt` should represent the next in-development target version after the last shipped release.
4. If version fields are inconsistent, fix them in the same change before release work continues.
5. Keep git hook enforcement active in local clones by running:
   - `powershell -ExecutionPolicy Bypass -File .\tools\install-git-hooks.ps1`

## CI and Validation Expectations

1. CI must run the version gate and execute automated tests (not build-only checks).
2. For behavior changes, add or update tests when coverage exists in that subsystem.
3. If tests cannot be added, document the exact gap and manual validation performed in `Docs/COMMIT_NOTES.md`.

## Maintainability Guardrails

1. Avoid expanding monolithic files further when practical; prefer extracting focused modules.
2. For major edits in large files (for example `PluginEditor.cpp`, `PluginProcessor.cpp`), include a short extraction/refactor note in commit notes.

## Architecture Expectations

1. Domain logic should not depend on UI components.
2. Audio-thread paths must remain RT-safe.
3. Serialization/state logic should be isolated from audio processing.
4. UI should consume snapshots/copies, not mutate processor internals directly.

## Change-Safety Rules

1. Do not alter chord naming/modifier behavior unless explicitly requested and
   covered by tests/fixtures.
2. Do not change `.chbpreset` compatibility.
3. Do not scatter standalone host `#if` logic; isolate behind services where possible.
4. Do not introduce new dependencies outside JUCE/stdlib.

## Commenting and Documentation

1. Keep top-of-file responsibility banners accurate.
2. Add concise comments at boundary sections:
   - thread ownership
   - mutual exclusion (locks, atomics)
   - ownership/lifetime (raw vs smart pointers)
   - critical invariants (loop count, sample-rate-dependent constants)
3. Use doxygen for public APIs and domain enum/types; use `//` for implementation comments.
4. Align comments with actual code. Stale comments are worse than no comments.

## Testing and Validation

1. Existing test suites should pass on all changes; if they fail, the change is incomplete.
2. For new features, add test coverage proportional to the risk and user-impact surface.
3. Load the plugin standalone and exercise the changed feature manually before committing.
4. If a feature cannot be easily tested in isolation, describe the test path in commit notes.

## Escalation and Uncertainty

1. If an architectural decision is unclear, pause and ask.
2. If a refactor introduces behavior change risk, capture exact re-validation steps in commit notes.
3. If a code path is not obvious, add a clarifying comment before committing.

