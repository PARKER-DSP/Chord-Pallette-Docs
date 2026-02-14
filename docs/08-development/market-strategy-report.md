# Chord Palette Plugin: Technical and Market Strategy Report

Date: 2026-02-13  
Method: Codebase-first audit plus previously collected competitor/source notes. No new research was performed for this draft.

## 1. Executive Summary

This product is not just a chord generator. The current codebase is a low-latency MIDI chord performance engine with composition utilities layered on top.

Key conclusion:
- Strongest strategic wedge is live harmonic performance on pads/keys/controllers, not direct head-to-head theory browsing against Scaler-style products.
- Core moat is the combination of real-time trigger mapping, safe-note remapping, rapid chord-bank manipulation, and practical MIDI export workflows.
- Product already supports a path to ecosystem revenue via presets, controller profiles, and community chord sharing without major architectural rewrites.

Top priorities:
1. Position category around performance mapping and fast harmonic control.
2. Productize controller-first workflows (profiles, scenes, setlists, low-friction live UX).
3. Ship a free lead magnet (Lite plugin or web tool) that demonstrates "one-note to full progression" in under 60 seconds.
4. Build recurring value via content ecosystem before heavy AI investment.

## 2. Feature Map

### 2.1 Feature Extraction (Code-Derived)

Legend:
- Market status: `Unique`, `Rare`, `Commodity`
- Category: `Core Value`, `Differentiator`, `Power User`, `Latent Opportunity`, `Technical Advantage`

| Capability | Category | Evidence in Code | Market Status | Why It Matters |
|---|---|---|---|---|
| Record vs Play engine modes | Core Value | `Source/PluginProcessor.cpp`, `Source/engine/ChordEngine.cpp` | Commodity | Standard chord-capture then trigger workflow. |
| Snapshot capture window (5-750 ms, default 90 ms) | Core Value | `Source/parameters/ParameterLayout.cpp` | Rare | Better control over how human input is grouped into chord snapshots. |
| Chord triggering from note range + base note mapping | Core Value | `Source/PluginProcessor.cpp`, `Source/ui/components/PianoRollDisplay.cpp` | Commodity | Core one-note chord triggering behavior expected in category. |
| Chord identification and naming with slash/bass handling | Core Value | `Source/domain/ChordModel.cpp` | Commodity | Required for trust and readability of generated chord names. |
| Tabbed chord banks (create/rename/duplicate/merge) | Differentiator | `Source/PluginEditor.cpp`, `Source/plugin/EditorController.cpp` | Rare | Supports song-part organization and fast arrangement iteration. |
| Per-entry voicing/spread/note-count transform cycling | Differentiator | `Source/PluginProcessor.cpp`, chord lane actions in UI | Rare | Fast harmonic variation without opening external tools. |
| MIDI import from dropped files grouped by onset | Power User | `Source/PluginProcessor.cpp` import flow | Rare | Speeds reuse of existing MIDI libraries and references. |
| Shift-drag chord block to export `.mid` | Differentiator | `Source/ui/components/ChordLaneComponent.cpp` + export helpers in processor | Rare | Removes export friction and fits modern DAW workflows. |
| Global export controls (beats, velocity, clip metadata) | Power User | `Source/parameters/ParameterLayout.cpp`, `Source/PluginProcessor.cpp` export methods | Commodity | Important for DAW compatibility and deterministic output. |
| Safe-note bracket remapping with maintain-root option | Differentiator | `Source/engine/ChordEngine.cpp`, safe-range logic in `PianoRollDisplay` | Unique | Strong live-play safety system not commonly implemented this explicitly. |
| Global octave shift and constrained trigger range | Core Value | `Source/parameters/ParameterLayout.cpp`, engine mapping path | Commodity | Basic but necessary for keyboard/pad adaptation. |
| Number-key quick trigger mode (1-0) | Power User | `Source/ui/components/ChordLaneComponent.cpp`, editor key handling | Rare | Very fast audition/performance path for desktop users. |
| Note-lock/latch preview workflow | Power User | `Source/PluginEditor.cpp`, chord preview control paths | Rare | Better for sustained testing and live continuity. |
| Built-in preview synth (poly sine, normalized gain) | Technical Advantage | `Source/PluginProcessor.cpp` | Commodity | Reliable no-host-instrument fallback for immediate sound. |
| Standalone VST3 preview-host scan/load/favorites/editor | Differentiator | `Source/plugin/PreviewHostCatalog.*`, `PreviewHostWindowController.*`, `Source/app/PreviewInstrumentHostService.cpp` | Rare | Improves out-of-box usability and demo quality for non-technical users. |
| Hosted instrument state stored in presets | Differentiator | `Source/state/StateSerializer.cpp`, preview host data fields | Rare | Presets become full performance scenes, not only chord lists. |
| Nashville / scale-fit labeling (46 scale definitions) | Differentiator | Scale analysis in `Source/PluginEditor.cpp` | Rare | Adds musician-facing harmonic context beyond raw chord names. |
| Guitar chord builder (fingering, capo, tuning metadata) | Differentiator | `Source/ui/components/GuitarChordBuilderComponent.*` | Rare | Bridges keyboard and guitar workflows in one plugin. |
| Preset browser with factory + user categories and search | Core Value | `Source/presets/PresetLibrary.*`, editor preset UI | Commodity | Baseline discoverability/recall feature expected by users. |
| Factory preset generator target (250 total, uniqueness constraints) | Technical Advantage | `Source/presets/PresetLibrary.cpp`, `Tests/PresetLibraryTests.cpp` | Rare | Content scale plus quality guardrails are already codified. |
| Backward-compatible state serialization paths | Technical Advantage | `Source/state/StateSerializer.*`, `Tests/StateSerializationTests.cpp` | Rare | Reduces version upgrade risk and support burden. |
| RT-safe process path (no blocking/XML in `processBlock`) | Technical Advantage | `Source/PluginProcessor.cpp`, architecture docs | Rare | Performance reliability under host load is a major trust factor. |

## 2. Workflow Advantages Embedded in Architecture

- High-speed capture-to-variation loop:
  - Capture held notes, dedupe, apply transform cycles, reorder by drag, export by shift-drag.
- Dual-preview architecture:
  - Built-in synth for immediate feedback and optional hosted instrument for realistic audition.
- Scene-like preset behavior:
  - Chord content + optional hosted instrument state creates reproducible performance context.
- Bank-level and chord-level editing granularity:
  - Users can operate globally (transpose/export defaults) or surgically per entry.

## 3. Competitive Matrix

(omitted for brevity)
