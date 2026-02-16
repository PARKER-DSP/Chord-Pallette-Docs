---
audience: developers
status: canonical
owner: engineering
last_reviewed: 2026-02-16
---

# ChordPallette Architecture - Current Baseline (Phase 0)

> **Status**: Pre-launch. This document describes the current codebase organization before major refactoring work begins. Used as a reference point to preserve behavior during structural improvements.

---

## Build Targets

- `VST3`
- `Standalone`

**Note:** Preview instrument hosting is currently supported in standalone builds only through compile-time guards (`JUCE_STANDALONE_APPLICATION && JUCE_PLUGINHOST_VST3`).

---

## Module Map

### Core Plugin Entry Points

- **`Source/PluginProcessor.*`**
  - JUCE `AudioProcessor` entry point
  - Real-time MIDI/audio processing (`processBlock`)
  - Chord bank mutation APIs consumed by the editor
  - Preview synth rendering and hosted preview-instrument rendering
  - Plugin state read/write bridge (`getStateInformation` / `setStateInformation`)

- **`Source/PluginEditor.*`**
  - JUCE `AudioProcessorEditor` entry point
  - Top-level UI composition, options flow, and interaction orchestration
  - Preset menu flow, undo/redo history, chord context menus
  - MIDI drag/drop import path
  - Plugin-host UI orchestration and scan service integration

### Editor & Orchestration

- **`Source/plugin/EditorController.*`**
  - Non-component editor orchestration logic
  - Currently owns undo/redo history stack behavior

- **`Source/plugin/PreviewHostCatalog.*`**
  - Non-component preview-host catalog state helper
  - Owns scanned-plugin selection, custom folder list, and favorites normalization

- **`Source/plugin/PreviewHostWindowController.*`**
  - Non-component host window lifecycle helper
  - Owns host-settings window and loaded instrument editor window lifetime/focus

- **`Source/plugin/PreviewHostStatus.*`**
  - Centralized host status text boundary for editor-host orchestration

### Background Services

- **`Source/app/PreviewInstrumentHostService.*`**
  - Background scan lifecycle for VST3 preview host discovery
  - Emits scan progress snapshots + message-thread completion callbacks

### Domain & State

- **`Source/domain/ChordModel.*`**
  - Chord domain logic and data structures
  - Chord naming/modifier interpretation
  - **Fingerprint system for deduplication:**
    - Computes deterministic hash of pitch class set + voicing + operators
    - Used to detect duplicate/similar chords on capture, import, paste
    - Unordered pitch class set comparison (C, D, E regardless of register)
    - Supports "identical" (same voicing) vs "similar" (same harmony, different voicing) detection
    - Non-blocking, efficient O(1) lookup with caching

- **`Source/ChordModel.h`**
  - Compatibility shim include for legacy include paths

- **`Source/state/PluginState.*`**
  - ValueTree/XML serialization helpers
  - Backward-compatible extraction/parsing helpers for state payloads

- **`Source/presets/PresetLibrary.*`**
  - Factory presets and user preset file persistence (`.chbpreset`)

### Parameters

- **`Source/parameters/*`**
  - APVTS parameter IDs and parameter layout construction
  - Centralized parameter metadata and validation

### UI Components

- **`Source/ui/*`**
  - Reusable UI components and theme/font modules
  - Chord lane display, block editor, piano roll, mapping panel
  - Style guide implementation

---

## Data Flow (Current)

1. **MIDI input** arrives in `PluginProcessor::processBlock`
2. Processor updates held-note/play-mode state and potentially chord-bank data
3. Processor broadcasts UI-change notifications through `ChangeBroadcaster`
4. Editor listens, pulls snapshots (`getBankSnapshot`, etc.), and updates UI models
5. Preset save/load and plugin state save/load round-trip via ValueTree/XML helpers in `state` and `presets`

---

## Thread Boundaries (Current)

| Thread | Responsibilities | Safety Rules |
|--------|------------------|--------------|
| **Audio Thread** | `processBlock` and all directly called functions | Must be RT-safe: no allocations, locks, or blocking calls |
| **Message Thread** | Editor/UI rendering, interactions, async callbacks, UI-triggered services | May block temporarily; no hard realtime constraints |
| **Background Worker** | Plugin scan workflow and other async discovery tasks | May run indefinitely; does not block message or audio threads |

---

## High-Risk Subsystems (No-Regress Zones)

These subsystems are critical and require extra care during refactoring:

1. **Chord Labeling/Modifier Pipeline**
   - `ChordModel` + all refresh paths
   - Changes here affect user-facing chord names and semantics
   - Must maintain backward compatibility with saved chords

2. **Serialization Compatibility & Schema Keys**
   - `PluginState`, `.chbpreset` file format
   - Old presets must load correctly in new versions
   - Parameter IDs must remain stable

3. **Preview Instrument Hosting Lifecycle**
   - Scan/load/editor/rendering ownership
   - Complex cross-thread orchestration
   - Subtle state machine behavior

---

## Chord Deduplication (Current Implementation)

### Current State
The Phase 0 baseline does **not yet implement deduplication**. Duplicate chord capture is possible and the system has no built-in protection against users accumulating many nearly-identical chord variations in their chord banks.

### Detection Infrastructure
The groundwork for deduplication exists:
- **ChordBlock.fingerprint()** – Computes stable hash from pitch class set, voicing, and metadata
- **ChordLibrary** – Maintains unordered map (no auto-dedup on insert)
- **Capture flow** – Receives chord data but does not filter duplicates before adding to library

### Phase 1 Implementation Plan
When deduplication is enabled:
1. **On Capture**: Fingerprint new chord, check existing library for matches
   - Identical match → Show toast "Added to favorites" (don't insert duplicate)
   - Similar chord (±1-2 semitone variance) → Show "Similar chord exists" dialog with comparison UI
   - New chord → Insert and update fingerprint index

2. **Fingerprint Index**: In-memory LUT mapping fingerprint → ChordID for O(1) collision detection

3. **User Control**: Users can override "smart capture" with "Always Save" button to force capture even if duplicate detected

### Risk Mitigation
- **Backward Compatibility**: Old presets without fingerprints computed on first load. No file format change required.
- **Real-Time Safety**: Fingerprinting is non-blocking; performed asynchronously on library thread
- **Data Loss Prevention**: Dedup is advisory (suggestion to user), not automatic (user always has final choice)

---

## Backward Compatibility Contracts

- **Parameter IDs** (`Source/parameters/ParameterIDs.h`): Do not rename without migration
- **Plugin IDs/Codes** (`CMakeLists.txt`): Do not change without explicit migration plan
- **Preset Schema Keys** (`Source/state/PluginState.cpp`): Parse must handle old versions
- **Preset File Format** (`.chbpreset`): Must remain readable by all shipped versions

---

## Next Phase (Phase 1) Goals

- Finalize Core/Integration layer split
- Extract JUCE-free chord domain library
- Improve testability of chord operations
- Document and stabilize public APIs
- Clarify thread safety contracts
- Plan API for future extensions (controller profiles, cloud sync, etc.)

See [Development Guidelines](../guidelines/overview.md) for refactoring best practices and rules.

Related architecture pages:

- [Architecture Overview](architecture-overview.md)
- [Threading and Lifecycle](threading-and-lifecycle.md)
- [Playability Overlays Spec](playability-overlays-spec.md)
