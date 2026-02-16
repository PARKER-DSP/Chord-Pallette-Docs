---
audience: developers
status: canonical
owner: engineering
last_reviewed: 2026-02-16
---

# Architecture Overview

This page is the top-level map for ChordPallette architecture docs.

Use it to understand where a concept lives before reading implementation detail pages.

## System Intent

ChordPallette is designed as a MIDI-first harmony system with:

- deterministic realtime behavior on the audio thread
- non-destructive transformation flow (base state -> derived state -> optional freeze)
- clear separation between musical logic and host/UI adaptation

## Layer Model

| Layer | Owns | Must Not Own |
| --- | --- | --- |
| Core | chord models, operator transforms, voicing decisions, deterministic scoring | JUCE types, host callbacks, UI state |
| Integration | host IO, transport adaptation, snapshot handoff, serialization bridges | business logic rewrites, UI-only rules |
| UI | controls, visualization, explainability surfaces, workflow actions | direct mutation of realtime internals |
| Background workers | heavy analysis, precompute, export helpers | blocking audio-thread work |

## Runtime Paths

1. Capture path: MIDI in -> snapshot -> chord identification -> persisted block.
2. Playback path: trigger -> operator chain -> voice-leading decision -> MIDI out.
3. State path: persisted project/preset -> migration -> config snapshot -> runtime swap.

## Read Next

- [Architecture Principles](architecture-principles.md) for non-negotiable rules.
- [Module Boundaries](module-boundaries.md) for ownership and dependency limits.
- [Realtime Safety](realtime-safety.md) for RT constraints and validation.
- [Threading and Lifecycle](threading-and-lifecycle.md) for thread ownership and host lifecycle.
- [Playability Overlays Spec](playability-overlays-spec.md) for Up/Down/Steady/Original behavior.
- [Current Baseline](current-baseline.md) for the pre-refactor source map.
