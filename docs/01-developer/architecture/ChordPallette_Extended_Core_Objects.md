---
audience: developers
status: canonical
owner: engineering
last_reviewed: 2026-02-16
---

# ChordPallette - Extended Core Objects
_Last updated: 2026-02-14_

This document defines additional core-level objects required to complete the system:

- Preset (packaging EngineProject snapshots)
- UndoStep (user actions + reversible diffs)
- PackManifest (operator/voicing packs metadata)
- AudioChordAnalysisJob (offline audio → chord candidates pipeline)

These models are fully compatible with the existing:
- EngineProject
- Bank
- ChordBlock
- OperatorDefinition
- MappingProfile
- PerformanceContext
- ChordResult
- MidiEventSequence

All examples use JSONC (JSON with comments).

---
# 1) Preset
Purpose:
A Preset packages a portable snapshot of an EngineProject or a subset of it (e.g., a single bank) for:
- distribution
- preset libraries
- sharing
- pack sales
- version-safe recall

Key principle:
Presets should be self-contained and versioned.

```jsonc
{
  "type": "Preset",
  "id": "preset_neo_soul_01",
  "schemaVersion": "1.0.0",

  // Display name shown in preset browser.
  "name": "Neo Soul Movement Pack",

  // What kind of preset this is.
  // full_project | single_bank | block_collection | mapping_only
  "presetType": "single_bank",

  // Engine version that created this preset (important for migrations).
  "engineVersion": "1.0.0",

  // Embedded snapshot of data required to reconstruct the preset.
  "payload": {
    // For single_bank preset, include only referenced bank + blocks.
    "banksById": {
      "bank_neo_01": { "ref": "Bank object" }
    },

    "chordBlocksById": {
      "chord_01": { "ref": "ChordBlock object" },
      "chord_02": { "ref": "ChordBlock object" }
    },

    // Include operator definitions if preset depends on custom ones.
    "operatorDefinitionsById": {},

    // Optional mapping profile if unique to preset.
    "mappingProfilesById": {}
  },

  // Metadata for browser sorting and marketing.
  "metadata": {
    "author": "MPAKT MEDIA",
    "description": "Smooth neo-soul progressions with expressive voice leading.",
    "tags": ["neo_soul", "jazz", "live_performance"],
    "createdAt": "2026-02-14T12:00:00Z"
  }
}
```

Compatibility:
- Payload uses the exact same Bank and ChordBlock schemas.
- Missing fields fallback to EngineProject.defaults.

---
# 2) UndoStep
Purpose:
Provides reversible state changes without duplicating entire EngineProject.

Key principle:
Undo should store minimal diffs, not full project snapshots.

```jsonc
{
  "type": "UndoStep",
  "id": "undo_001",
  "schemaVersion": "1.0.0",

  // Describes what kind of change happened.
  "actionType": "update_operator_parameter",

  // Human-readable description for UI undo history panel.
  "description": "Changed Voice Leading Tightness from 0.6 → 0.75",

  // Timestamp for ordering.
  "timestamp": "2026-02-14T12:10:00Z",

  // Path-based diff system referencing EngineProject structure.
  "diff": {
    "targetPath": "chordBlocksById.chord_a1f3e8.operatorChain.opi_01.parameters.tightness",

    // Previous value before change.
    "before": 0.6,

    // New value after change.
    "after": 0.75
  },

  // Optional grouping key for multi-step operations.
  "groupId": "group_123"
}
```

Compatibility:
- Uses JSON path style referencing consistent with EngineProject structure.
- Works with immutable snapshot system or diff-based state reducer.

---
# 3) PackManifest
Purpose:
Defines metadata for downloadable packs (operator packs, voicing packs, preset collections).

Key principle:
Separate content from engine so packs can evolve independently.

```jsonc
{
  "type": "PackManifest",
  "id": "pack_voice_leading_pro",
  "schemaVersion": "1.0.0",

  "name": "Voice Leading Pro Pack",

  // operator_pack | preset_pack | voicing_pack | hybrid
  "packType": "operator_pack",

  "engineCompatibility": {
    "minVersion": "1.0.0",
    "maxTestedVersion": "1.2.0"
  },

  // What this pack contains.
  "contents": {
    "operatorDefinitions": [
      "opd_voice_leading_cinematic",
      "opd_voice_leading_jazz_advanced"
    ],

    "presets": [],
    "banks": [],
    "voicingLibraries": []
  },

  // Commercial metadata for storefront.
  "metadata": {
    "author": "MPAKT MEDIA",
    "description": "Advanced voice leading algorithms for cinematic scoring.",
    "priceTier": "pro",
    "tags": ["cinematic", "advanced"],
    "releaseDate": "2026-03-01"
  }
}
```

Compatibility:
- References OperatorDefinition IDs used in EngineProject.
- Packs never override core engine schema.

---
# 4) AudioChordAnalysisJob
Purpose:
Handles offline audio-to-chord detection pipeline safely outside audio thread.

Key principle:
Heavy DSP and detection must run on background thread and produce structured ChordDetectionResults compatible with ChordBlock.

```jsonc
{
  "type": "AudioChordAnalysisJob",
  "id": "job_001",
  "schemaVersion": "1.0.0",

  // Reference to audio source.
  "audioSource": {
    "filePath": "C:/audio/song.wav",
    "channel": "stereo_mix"
  },

  // Analysis configuration.
  "settings": {
    "windowSizeMs": 100,
    "hopSizeMs": 50,
    "minConfidenceThreshold": 0.4,
    "preferSharpsOrFlats": "auto"
  },

  // Status lifecycle: queued | running | completed | failed
  "status": "completed",

  // Output: list of detection results mapped to time regions.
  "results": [
    {
      "startTimeSec": 12.0,
      "endTimeSec": 14.5,
      "detection": {
        "labelStandard": "Am7",
        "rootPc": 9,
        "confidence": 0.78
      }
    }
  ],

  // Optional: conversion policy to ChordBlocks.
  "conversion": {
    "autoCreateChordBlocks": true,
    "targetBankId": "bank_main_01"
  }
}
```

Compatibility:
- Produces data compatible with ChordDetectionResult.
- Converts cleanly into ChordBlock.baseChord + metadata.
- Runs entirely off audio thread.

---
# Interoperability Summary

Preset:
- Wraps EngineProject-compatible structures.
- Version-aware and portable.

UndoStep:
- Targets JSON paths within EngineProject.
- Lightweight and reversible.

PackManifest:
- References OperatorDefinition and Preset structures.
- Compatible with project loading system.

AudioChordAnalysisJob:
- Produces ChordDetectionResult-compatible data.
- Feeds directly into ChordBlock creation pipeline.

---
# Architectural Integrity

These additions preserve:

- Core vs Integration separation
- Non-destructive editing model
- Bank-scoped modifiers
- Operator instance multiplicity
- Realtime safety constraints

They extend the system without introducing circular dependencies or schema inconsistencies.

---

End of Extended Core Objects document.
