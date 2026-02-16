---
audience: developers
status: canonical
owner: engineering
last_reviewed: 2026-02-16
---

# Threading and Lifecycle

This document defines thread ownership and plugin lifecycle behavior so engineering, UX, and docs all describe the same runtime model.

## Thread Ownership Model

### Audio Thread (Realtime)

Owns:

- trigger processing during playback
- bounded operator and voice-leading evaluation
- MIDI event emission

Must never do:

- heap allocation
- lock waits
- file IO
- expensive string/UI work

### Message Thread (UI)

Owns:

- rendering and interaction
- control edits and command intent
- explainability text and labels

Must never block the audio callback.

### Worker Threads (Background)

Own:

- batch analysis
- long-running precompute
- heavy export generation

Publish results back through safe handoff to Integration/UI.

## Threading Diagram

```mermaid
flowchart LR
  subgraph HOST[Host]
    HCB[Audio callback]
    HUI[UI host window]
  end

  subgraph AUDIO[Audio Thread]
    A1[process block]
    A2[trigger and mapping]
    A3[operators and voice leading]
    A4[MIDI event emit]
  end

  subgraph UI[Message Thread]
    U1[user edits]
    U2[render and inspect]
  end

  subgraph BG[Background Workers]
    B1[analysis and precompute]
    B2[batch export tasks]
  end

  HCB --> A1 --> A2 --> A3 --> A4
  HUI --> U1 --> U2
  U1 -->|new config snapshot| A2
  U1 --> B1
  B1 --> U2
  B2 --> U2
```

## UI to Audio Handoff Contract

Preferred pattern:

1. UI builds complete immutable config snapshot.
2. Integration atomically swaps active snapshot pointer/version.
3. Audio thread consumes only stable snapshot.
4. Retired snapshots are reclaimed off audio thread.

## Lifecycle Sequence

```mermaid
sequenceDiagram
  participant Host
  participant Plugin
  participant Core
  participant UI
  participant Worker

  Host->>Plugin: Create instance
  Plugin->>Core: Initialize defaults
  Plugin-->>Host: Ready

  Host->>Plugin: Restore state
  Plugin->>Core: Build and apply config snapshot
  Plugin-->>Host: State restored

  Host->>Plugin: Open editor
  Plugin->>UI: Create UI
  UI->>Plugin: Request read-only snapshot
  Plugin-->>UI: Snapshot response

  loop Playback loop
    Host->>Plugin: processBlock
    Plugin->>Core: Evaluate and emit MIDI events
    Plugin-->>Host: Output buffer updated
  end

  UI->>Plugin: Edit operator or mapping
  Plugin->>Core: Apply new snapshot atomically

  UI->>Plugin: Request heavy analysis or export
  Plugin->>Worker: Queue job
  Worker-->>UI: Result payload

  Host->>Plugin: Save state
  Plugin-->>Host: Serialized payload

  Host->>Plugin: Close editor
  Plugin->>UI: Destroy UI

  Host->>Plugin: Destroy instance
  Plugin->>Core: Shutdown
```

## State Restore Ordering

Restore order should be:

1. deserialize persisted parameter/model state
2. build complete runtime snapshot
3. atomically publish snapshot to runtime
4. allow UI to rehydrate from same snapshot

This avoids partial state visibility and first-block mismatch behavior.

## Related Docs

- [Realtime Safety](realtime-safety.md)
- [Module Boundaries](module-boundaries.md)
- [Current Baseline](current-baseline.md)
