---
audience: product
status: canonical
owner: product
last_reviewed: 2026-02-16
---

# Voice Leading Overview

Voice leading controls how one chord moves into the next so transitions feel intentional rather than mechanical.

## What It Solves

- reduces abrupt register jumps
- preserves useful common tones when possible
- keeps progression flow consistent across live triggering and sequencing

## User-Facing Behavior

- works during realtime triggering and arranged playback
- supports style-driven motion profiles (for example smooth, cinematic, neo-soul)
- remains non-destructive until user freeze/commit action

## Scope Controls

Voice leading behavior can be applied at:

- bank level (default policy)
- block level override (local behavior)
- performance context based on actual trigger order

Detailed UX behavior is documented in [Voice Leading Operator Pack UX](operator-pack-ux.md).

## Architecture Contracts

- [Playability Overlays Spec](../../01-developer/architecture/playability-overlays-spec.md)
- [Threading and Lifecycle](../../01-developer/architecture/threading-and-lifecycle.md)
- [Realtime Safety](../../01-developer/architecture/realtime-safety.md)
