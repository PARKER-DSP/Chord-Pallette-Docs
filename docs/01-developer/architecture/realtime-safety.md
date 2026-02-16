---
audience: developers
status: canonical
owner: engineering
last_reviewed: 2026-02-16
---

# Realtime Safety

This page defines the minimum realtime safety contract for audio-thread code paths.

## Hard Rules (Audio Thread)

- No heap allocation or container growth.
- No locks, waits, sleeps, or blocking synchronization.
- No file IO, network IO, or host/UI API calls that may block.
- No string-heavy formatting or debug logging in hot path.
- No unbounded search loops.

## Required Design Patterns

- Preallocate buffers and candidate arrays before playback.
- Use immutable snapshots and atomic pointer/version swap for config updates.
- Bound candidate count and operator passes per block.
- Keep heavy analysis and export preparation off the audio thread.

## Suggested Voice-Leading Budgets

- Candidate pool cap: `32-64` per trigger.
- Operator chain: fixed max operator count in RT mode.
- Scoring: linear in candidate count with bounded per-candidate cost.

If your use case exceeds these bounds, move that work to background precompute.

## Validation Checklist

1. Stress test with worst-case buffer sizes and dense MIDI input.
2. Verify no allocations in audio callback path.
3. Verify no contended lock acquisition on audio thread.
4. Verify deterministic output across repeated runs with same input.
5. Record and regress-test max processing time per block.

## Handoff Rules

- UI writes new config snapshot, then performs atomic swap.
- Audio thread reads only fully-built immutable snapshots.
- Worker results are promoted through Integration-safe staging.

Detailed ownership examples are in [Threading and Lifecycle](threading-and-lifecycle.md).

## Related Docs

- [Architecture Principles](architecture-principles.md)
- [Module Boundaries](module-boundaries.md)
- [Invariants](../guidelines/invariants.md)
