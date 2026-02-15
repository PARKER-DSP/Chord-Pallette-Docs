> **Archived (non-authoritative):** This file is retained for historical reference only. Use canonical pages from the main navigation for current guidance.

# Commit Notes

## 0.3.3 - 2026-02-13 - Improve AI rules readability and add VS Code merge guide

### What changed
- Updated `Docs/AI_AGENT_RULES.md` with a small, GitHub-friendly section that adds a quick-start checklist and a short vibe note.
- Updated `README.md` with a more engaging project description section.
- Added a practical `README.md` section documenting how to merge remote changes into a local repository using VS Code + terminal commands.
- Bumped `CMakeLists.txt` project version from `0.3.2` to `0.3.3`.

### Why it changed
- Improve contributor onboarding and make repository guidance easier (and more enjoyable) to read.
- Provide clear, beginner-friendly local merge instructions to reduce Git workflow friction for contributors using VS Code.
- Patch bump chosen because this is documentation/process improvement without behavioral/plugin-runtime changes.

### Validation performed
- `git diff -- Docs/AI_AGENT_RULES.md README.md CMakeLists.txt Docs/COMMIT_NOTES.md`
- `git status --short --branch`

## 0.3.2 - 2026-02-13 - Formalize pro-commit standards and fix version bump utility

### What changed
- Added and finalized `Docs/PRO_COMMIT_GUIDELINES.md` as the canonical "pro commit" standard, including:
  - blocking pre-commit workflow
  - commit-message format
  - commit-notes template
  - hard fail/no-commit conditions
- Updated `Docs/AI_AGENT_RULES.md` to hard-require:
  - following `Docs/PRO_COMMIT_GUIDELINES.md` before commit
  - professional commit subjects in `type(scope): imperative summary` format
- Fixed `tools/bump-project-version.ps1` regex replacement logic so patch/minor/major bumps work correctly in this PowerShell environment.
- Bumped `CMakeLists.txt` project version from `0.3.1` to `0.3.2`.

### Why it changed
- User requested explicit guidelines so every commit is handled as a professional-quality commit.
- The version bump helper had to be corrected because it failed at runtime and blocked the intended workflow.

### Validation performed
- `powershell -ExecutionPolicy Bypass -File .\tools\bump-project-version.ps1`
- `powershell -ExecutionPolicy Bypass -File .\tools\require-commit-version-bump.ps1`
- `powershell -ExecutionPolicy Bypass -File .\tools\require-version-bump.ps1`

## 0.3.1 - 2026-02-13 - Enforce per-commit monotonic version bumps for local and CI workflows

### What changed
- Added local commit version gate script:
  - `tools/require-commit-version-bump.ps1`
  - validates current `CMakeLists.txt` version is strict semver (`X.Y.Z`) and strictly greater than `HEAD` commit version.
- Added CI commit-range monotonicity script:
  - `tools/require-commit-range-version-monotonic.ps1`
  - validates every commit in PR range increments project version monotonically.
- Added helper script for deterministic patch bumps:
  - `tools/bump-project-version.ps1`
- Added hook installer:
  - `tools/install-git-hooks.ps1`
  - configures `core.hooksPath` to `.githooks`.
- Added pre-commit hook:
  - `.githooks/pre-commit`
  - runs the commit version gate before allowing commits.
- Updated CI workflow (`.github/workflows/release-version-gate.yml`):
  - checkout now uses full history (`fetch-depth: 0`)
  - added PR step to enforce per-commit version monotonicity.
- Updated project docs/rules:
  - `Docs/AI_AGENT_RULES.md` now treats per-commit version increments as hard policy.
  - `README.md` now documents commit-level version gate usage.
  - `Docs/RELEASE_NOTES.md` unreleased target updated to `0.3.1 - Alpha`.
- Added AI-guidance documents to `.gitignore` to keep local AI-instruction context files out of future default commit sets:
  - `Docs/AI_AGENT_RULES.md`
  - `Docs/invariants.md`
  - `Docs/architecture.md`
  - `RefactorNotes.md`
  - `AGENTS.md`
- Added explicit pro-commit quality checklist document:
  - `Docs/PRO_COMMIT_GUIDELINES.md`
  - linked from `Docs/AI_AGENT_RULES.md` as mandatory pre-commit reading.
- Bumped project version in `CMakeLists.txt` from `0.3.0` to `0.3.1`.

### Why it changed
- User requested strict enforcement that every commit, including AI-authored commits, advances product version.
- Adds both local and CI enforcement to reduce policy drift.
- Keeps semantic version syntax consistent while allowing many patch-level commits between larger milestones.

### Validation performed
- Ran local commit version gate:
  - `powershell -ExecutionPolicy Bypass -File .\tools\require-commit-version-bump.ps1`
- Ran release version gate:
  - `powershell -ExecutionPolicy Bypass -File .\tools\require-version-bump.ps1`
- Ran configure/build/tests:
  - `cmake --preset vs2026-x64 -DCHBP_BUILD_TESTS=ON`
  - `cmake --build --preset vscode-release`
  - `ctest --test-dir build/chordpallette -C Release --output-on-failure`

## 0.3.0 - 2026-02-13 - Enforce version-first commit-note headings as hard rule

### What changed
- Tightened `Docs/AI_AGENT_RULES.md` commit-note requirements:
  - added hard-fail rule that agents must not commit when new commit-note headings do not match version-first format
  - added explicit heading regex requirement:
    - `^## [0-9]+\.[0-9]+\.[0-9]+ - [0-9]{4}-[0-9]{2}-[0-9]{2} - `
