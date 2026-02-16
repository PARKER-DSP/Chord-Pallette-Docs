---
audience: product
status: canonical
owner: product
last_reviewed: 2026-02-16
---

# Operator System

Operators are modular transforms applied non-destructively to chords.

## Design Principles

- **Non-Destructive** – Operators never mutate the BaseChord; they produce derived states
- **Composable** – Operators can be chained and reordered
- **Deterministic** – Same input + operator always produces same output
- **RT-Safe Subset** – Performance operators must be bounded and allocation-free

## Operator Types

### Chord Transforms
- Voicing: inversion, drop2/drop3, spread, close/open, re-voice
- Range: clamp to bounds, "only root in sub-bass"
- Harmony: borrowed chord, modal interchange, tensions

### Event Generators
- Strum, arpeggiate, rhythm patterns, melodic play
- Humanize, velocity randomization, note chance/probability
- Legato rules, voice-leading optimization to previous block

## Design Rules

1. Operators never mutate `BaseChord`
2. Any pitch change triggers redetection for accurate labels
3. RT-safe subset must be bounded and allocation-free
4. Each operator produces a new derived state
5. Operator chains are data-first (stored, versionable, undoable)

## Extensibility

The operator system is designed to support future additions:
- AI-assisted voicing suggestions
- Advanced harmonic transforms
- Genre-specific rhythm and performance patterns
- Custom user-defined operators (future)

See [Operator Catalog](operator-catalog.md) for the current list of available operators.

See [Playability Overlays Spec](../../01-developer/architecture/playability-overlays-spec.md) for bank-level overlay behavior.
