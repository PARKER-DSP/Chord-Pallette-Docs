# Chord Pallette Architecture (Current Baseline)

This document captures the **current** architecture before staged refactoring.
It is intentionally descriptive (not aspirational) so behavior can be preserved
while code is reorganized.

## Build Targets

- `VST3`
- `Standalone`

Preview instrument hosting is currently supported in standalone builds only
through compile-time guards (`JUCE_STANDALONE_APPLICATION && JUCE_PLUGINHOST_VST3`).

## Module Map

- `Source/PluginProcessor.*`
  - JUCE `AudioProcessor` entry point.
  - Real-time MIDI/audio processing (`processBlock`).
  - Chord bank mutation APIs consumed by the editor.
  - Preview synth rendering and hosted preview-instrument rendering.
  - Plugin state read/write bridge (`getStateInformation` / `setStateInformation`).
- `Source/PluginEditor.*`
  - JUCE `AudioProcessorEditor` entry point.
  - Top-level UI composition, options flow, and interaction orchestration.
  - Preset menu flow, undo/redo history, chord context menus.
  - MIDI drag/drop import path.
  - Plugin-host UI orchestration and scan service integration.
- `Source/plugin/EditorController.*`
  - Non-component editor orchestration logic.
  - Currently owns undo/redo history stack behavior.
- `Source/plugin/PreviewHostCatalog.*`
  - Non-component preview-host catalog state helper.
  - Owns scanned-plugin selection, custom folder list, and favorites normalization.
- `Source/plugin/PreviewHostWindowController.*`
  - Non-component host window lifecycle helper.
  - Owns host-settings window and loaded instrument editor window lifetime/focus.
- `Source/plugin/PreviewHostStatus.*`
  - Centralized host status text boundary for editor-host orchestration.
- `Source/app/PreviewInstrumentHostService.*`
  - Background scan lifecycle for VST3 preview host discovery.
  - Emits scan progress snapshots + message-thread completion callbacks.
- `Source/domain/ChordModel.*`
  - Chord domain logic and data structures.
  - Chord naming/modifier interpretation.
  - Fingerprint helpers used for uniqueness.
- `Source/ChordModel.h`
  - Compatibility shim include for legacy include paths.
- `Source/state/PluginState.*`
  - ValueTree/XML serialization helpers.
  - Backward-compatible extraction/parsing helpers for state payloads.
- `Source/presets/PresetLibrary.*`
  - Factory presets and user preset file persistence (`.chbpreset`).
- `Source/parameters/*`
  - APVTS parameter IDs and parameter layout construction.
- `Source/ui/*`
  - Reusable UI components and theme/font modules.

## Data Flow (Current)

1. **MIDI input** arrives in `PluginProcessor::processBlock`.
2. Processor updates held-note/play-mode state and potentially chord-bank data.
3. Processor broadcasts UI-change notifications through `ChangeBroadcaster`.
4. Editor listens, pulls snapshots (`getBankSnapshot`, etc.), and updates UI models.
5. Preset save/load and plugin state save/load round-trip via ValueTree/XML helpers
   in `state` and `presets`.

## Thread Boundaries (Current)

- **Audio thread**:
  - `processBlock` and all functions directly called by it.
  - Must remain RT-safe.
- **Message thread**:
  - Editor/UI rendering and interactions.
  - Async callbacks and UI-triggered service actions.
- **Background worker thread(s)**:
  - Currently used in editor-driven plugin scan workflow.

## High-Risk Subsystems (No-Regress Zones)

1. Chord labeling/modifier pipeline (`ChordModel` + refresh paths).
2. Serialization compatibility and schema keys (`PluginState`, `.chbpreset`).
3. Preview instrument hosting lifecycle (scan/load/editor/rendering ownership).
