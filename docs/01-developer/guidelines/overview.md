# Development Guidelines Overview

Welcome to ChordPallette's developer documentation. This section guides contributors through best practices, standards, and requirements for working on the codebase.

---

## Core Guidelines

- **[AI Agent Rules](ai-agent-rules.md)** – How autonomous agents should work with this codebase (checklist, versioning policy, architecture expectations)
- **[Pro Commit Standards](pro-commit-guidelines.md)** – Required quality gates for every commit (scope, validation, message format)
- **[Refactor Invariants](invariants.md)** – Backward compatibility rules and high-risk subsystems (don't break these)

---

## Architecture & Design

- **[Architecture Overview](../architecture/architecture-overview.md)** – Core/Integration/UI layer separation, dependency rules, MIDI processing tree
- **[Module Boundaries](../architecture/module-boundaries.md)** – What lives where in the codebase
- **[Realtime Safety](../architecture/realtime-safety.md)** – Audio-thread constraints and isolation strategy
- **[Current Baseline](../architecture/current-baseline.md)** – Snapshot of codebase organization before major refactoring

---

## Development Workflow

### Before You Code

1. Read [Invariants](invariants.md) to understand what cannot change
2. Check [Architecture Overview](../architecture/architecture-overview.md) to understand the structure
3. Identify which layer(s) your change affects (Core, Integration, UI)

### While You Code

1. Keep changes small and focused (one objective per commit)
2. Preserve RT-safety on audio thread (see [Realtime Safety](../architecture/realtime-safety.md))
3. Don't break plugin IDs, parameter IDs, or preset schemas (see [Invariants](invariants.md))
4. Add tests for new functionality when possible
5. Update comments to reflect actual code

### Before You Commit

1. Run through [Pro Commit Standards](pro-commit-guidelines.md) checklist
2. Bump version in `CMakeLists.txt`
3. Update `Docs/COMMIT_NOTES.md` with version-first heading
4. Run tests: `ctest --test-dir build/chordpallette -C Release`
5. Use professional commit message: `type(scope): imperative summary`
6. Push immediately: `git push origin main`

---

## Key Principles

1. **Minimal Viable Change** – Each commit should be independently reviewable and focused on one goal
2. **Backward Compatible** – Preserve user data, presets, and plugin identity
3. **Realtime Safe** – Audio thread code must never allocate, block, or use locks
4. **Clear Architecture** – Respect layer boundaries; don't let UI logic creep into Core
5. **Testable** – Isolate domain logic from JUCE framework for unit testing
6. **Well-Documented** – Comments, commit notes, and architecture docs matter

---

## Common Tasks

### Adding a New Feature
1. Start with [Pro Commit Standards](pro-commit-guidelines.md)
2. Identify which layer (Core, Integration, UI)
3. Add tests before/after implementation
4. Update architecture docs if boundaries change
5. Follow commit workflow with version bump + commit notes

### Refactoring Existing Code
1. Read [Invariants](invariants.md) for high-risk areas
2. Extract or move, don't rewrite
3. Keep each stage buildable and testable
4. Document why the refactor improves things
5. Run full test suite before committing

### Fixing a Bug
1. Write a test that reproduces the bug (if possible)
2. Fix the bug and verify test passes
3. Check [Invariants](invariants.md) for side effects
4. Use `fix(scope):` commit type
5. Include reproduction steps and validation in commit notes

### Updating Documentation
1. Keep architecture docs in sync with code
2. Use `docs:` commit type for documentation-only changes
3. No version bump needed for typo fixes; use patch bump for substantial docs updates

---

## Validation Commands

```bash
# Build Release target
cmake --build --preset vscode-release

# Run all tests
ctest --test-dir build/chordpallette -C Release --output-on-failure

# Check version gate (before committing)
powershell -ExecutionPolicy Bypass -File ./tools/require-commit-version-bump.ps1

# Install pre-commit hooks (run once per clone)
powershell -ExecutionPolicy Bypass -File ./tools/install-git-hooks.ps1
```

---

## Getting Help

- **Architecture questions?** → Read [Architecture Overview](../architecture/architecture-overview.md)
- **Unsure about compatibility?** → Check [Invariants](invariants.md)
- **Need to understand a subsystem?** → See [Current Baseline](../architecture/current-baseline.md)
- **Workflow unclear?** → Review [Pro Commit Standards](pro-commit-guidelines.md)
- **For AI agents:** → Start with [AI Agent Rules](ai-agent-rules.md)

---

## Related Sections

- **[Technical Architecture](../architecture/)** – Deep dive into system design
- **[Foundation](../../00-foundation/)** – Product strategy and requirements
- **[Features](../../02-features/)** – What we're building
- **[Go-to-Market](../../03-go-to-market/)** – Launch and sales strategy
