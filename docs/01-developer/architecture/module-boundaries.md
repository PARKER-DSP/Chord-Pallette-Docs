---
audience: developers
status: canonical
owner: engineering
last_reviewed: 2026-02-16
---

# Module Boundaries

This page defines ownership boundaries so feature changes do not leak across layers.

## Boundary Table

| Module Area | Owns | Depends On | Must Not Depend On |
| --- | --- | --- | --- |
| Core musical engine | chord representation, operator transforms, voicing/scoring math | stdlib and core domain types | JUCE, UI components, host APIs |
| Integration adapter | host callbacks, transport context, snapshot handoff, persistence wiring | Core interfaces, host/plugin framework | UI rendering internals |
| UI surface | interaction components, visualization, explainability readouts | Integration-facing state, read-only snapshots | mutable audio-thread state |
| Worker services | precompute, batch analysis, export helpers | Core algorithms and serialized snapshots | direct host callback ownership |

## Allowed Data Flow

1. UI emits user intent to Integration.
2. Integration builds immutable config snapshots for Core.
3. Core computes outputs; Integration publishes read-only snapshots back to UI.
4. Worker jobs publish completed artifacts through Integration-safe handoff.

## Forbidden Patterns

- UI mutating core state directly.
- Core importing framework-specific types.
- Audio-thread code waiting on worker completion.
- Ad hoc persistence logic spread across multiple layers.

## Change Checklist

Before merging a boundary-touching change:

1. Identify which layer owns the behavior.
2. Verify no reverse dependency was introduced.
3. Confirm snapshot/handoff model is preserved.
4. Update architecture docs if ownership moved.

## Related Docs

- [Architecture Overview](architecture-overview.md)
- [Architecture Principles](architecture-principles.md)
- [Realtime Safety](realtime-safety.md)
