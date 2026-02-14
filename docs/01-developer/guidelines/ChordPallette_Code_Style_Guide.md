# ChordPallette — Code Style Guide
_Last updated: 2026-02-14_

This guide applies to human developers and AI agents. It enforces readability, maintainability, realtime safety, and strict Core vs Integration boundaries.

---

# 1. Core Principles

## 1.1 Readability Over Cleverness
Code must prioritize clarity over brevity. Avoid dense abstractions, clever tricks, and unnecessary template complexity.

## 1.2 Core vs Integration Boundary
Core (JUCE-free): pure logic, deterministic, no host calls.
Integration (JUCE): processBlock, APVTS, UI, host IO.
Never mix layers.

---

# 2. Naming Conventions

Classes: PascalCase (EngineProject, ChordBlock)
Functions: camelCase (applyVoiceLeading)
Variables: camelCase (voiceLeadingStyle)
Constants: kPrefix (kMaxPitchClass)

---

# 3. File Rules
Each file must:
- Have a single responsibility
- Begin with a descriptive header
- State Layer (Core/Integration)
- Avoid exceeding 700 lines

---

# 4. Commenting Standards
All public APIs, algorithms, realtime paths, and migration logic must be documented.
Comments must explain:
- What
- Why
- Constraints
- Realtime impact

---

# 5. Realtime Safety
Audio-thread code must:
- Avoid heap allocations
- Avoid locks
- Avoid strings
- Avoid exceptions
- Avoid logging

Precompute heavy logic on background threads.

---

# 6. Threading Rules
Audio thread uses immutable snapshots via atomic swap.
UI may allocate and build caches.
No blocking cross-thread calls.

---

# 7. Reducer Rules
Reducers must be pure, deterministic, and side-effect free.

---

# 8. Serialization Rules
All serialized objects require schemaVersion.
No raw pointers in saved state.
Unknown fields must be safely ignored.

---

# 9. Testing
Core must include unit tests for detection, voice leading, reducer determinism, and migrations.

---

# 10. AI Agent Rules
AI agents must:
- Follow this guide strictly
- Not change schemaVersion without migration
- Update documentation when code changes
- Preserve Core/Integration separation

Generated code must be human-readable.

---

End of Code Style Guide.
