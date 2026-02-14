# Refactor Invariants and Guardrails

These rules are mandatory during staged refactoring.

## Non-Negotiable Compatibility Rules

1. Do not rename APVTS parameter IDs in `Source/parameters/ParameterIDs.h`.
2. Do not change plugin IDs/codes/bundle identifiers in `CMakeLists.txt`
   without an explicit migration plan.
3. Do not change preset/state schema keys in `Source/state/PluginState.cpp`
   unless parsing remains backward compatible.
4. Do not break `.chbpreset` file compatibility in `Source/presets/PresetLibrary.cpp`.
5. Do not add third-party dependencies (JUCE + standard library only).

## High-Risk Areas (Extra Caution)

1. Chord labeling/modifier correctness pipeline.
2. Serialization compatibility and migration behavior.
3. Standalone-only plugin-hosting lifecycle (scan/load/editor/render path).

## Real-Time Safety Rules

1. Audio-thread code (`processBlock` path) must not perform:
   - disk I/O
   - XML parse/write
   - plugin scanning
   - blocking waits
   - long-duration allocations/heavy container churn
2. Prefer snapshots and atomics for UI visibility over shared mutable structures.
3. Any lock used on RT paths must be proven safe/minimal; avoid broad lock scopes.

## Refactor Process Rules

1. Prefer mechanical extraction/moves over behavioral rewrites.
2. Keep each stage small and build after each stage.
3. Preserve external behavior and data formats while reorganizing internals.
4. Add comments/docs at boundaries (threading, ownership, persistence contracts).
5. If a behavior change is unavoidable, isolate it and document migration/rollback.
