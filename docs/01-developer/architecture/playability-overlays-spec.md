---
audience: developers
status: canonical
owner: engineering
last_reviewed: 2026-02-16
---

# Playability Overlays Spec

This spec defines bank-level playability overlays:

- `Up`
- `Down`
- `Steady`
- `Original`

They are performance-time scoring biases, not destructive edits.

## Purpose

Overlays let performers shape feel in realtime while preserving non-destructive architecture.

## State Model

| Layer | Meaning | Mutability |
| --- | --- | --- |
| Anchor voicing | canonical block identity | immutable by overlays |
| Realized voicing | contextual output at runtime | ephemeral |
| Memory voicing | recent runtime reference | ephemeral |
| Frozen/Baked | user-committed result | persistent |

Overlays influence candidate scoring only.

## Overlay Definitions

### Up

Biases scoring toward higher register movement.

### Down

Biases scoring toward lower register movement.

### Steady

Biases scoring toward minimal register drift.

### Original

Biases scoring toward anchor voicing/register identity.

`Original` refers to anchor voicing and register, not only chord spelling.

## Scoring Integration

Total score remains:

```text
S(candidate) = S_base(candidate) + S_overlay(candidate)
```

Reference voicing for motion-driven overlays:

```text
V_ref = (1 - mu) * Realized + mu * Memory
```

Representative overlay terms:

```text
S_up       = +w * motion_up(candidate, V_ref)
S_down     = +w * motion_down(candidate, V_ref)
S_steady   = -w * drift(candidate, V_ref)
S_original = -w * distance(candidate, Anchor)
```

Implementation may tune coefficient details by style profile, but complexity must remain bounded.

## Interaction Rules

- Overlays are bank-level and mutually exclusive in v1.
- Intensity is configurable (`0-100%`).
- Overlays never mutate anchor or rewrite history.
- `Original` reduces memory dominance and restores anchor pull.
- Hard constraints (range, spacing, safety) always win over overlay preference.

## UX Contract

Recommended control location:

- bank header control group
- explicit active state
- optional `None` state
- realtime response with no destructive side effects

## Realtime Constraints

Overlay evaluation must be:

- allocation-free on audio thread
- deterministic
- bounded by configured candidate cap
- linear in candidate count

## Capture and History

Overlays shape realized output.

History and capture should preserve:

- source anchor
- realized output
- overlay mode and intensity at capture time

Freeze/commit may convert a realized voicing into a new anchor, but this is explicit user action.

## Related Docs

- [Voice Leading Overview](../../02-features/voice-leading/overview.md)
- [Voice Leading Operator Pack UX](../../02-features/voice-leading/operator-pack-ux.md)
- [Threading and Lifecycle](threading-and-lifecycle.md)
- [Realtime Safety](realtime-safety.md)
