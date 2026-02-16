---
audience: developers
status: canonical
owner: engineering
last_reviewed: 2026-02-16
---

# ChordPallette - Core Object Models (Master)
_Last updated: 2026-02-14_

This document consolidates the **canonical data models** for ChordPallette and aligns them for:
- consistency (naming, IDs, versioning)
- interoperability (clean references between objects)
- non-destructive workflows (base → derived → output)
- performance safety (numeric data in realtime; strings/UI in non-RT paths)

> **Note on format:** Examples use **JSONC** (JSON with `//` comments). Many editors support this. If you need strict JSON, generate the same objects without comments.

---

## 0) Global Conventions

### 0.1 ID conventions
IDs are globally unique strings with type prefixes to prevent collisions and simplify debugging:
- Project: `proj_…`
- Bank: `bank_…`
- Chord Block: `chord_…`
- Keyswitch Block: `ksw_…`
- Mapping Profile: `map_…`
- Operator Definition: `opd_…`
- Operator Instance: `opi_…`
- Bank Modifier Definition: `bmd_…`
- Snapshot: `snap_…`
- Detection Result: `det_…`
- MIDI Sequence: `seq_…`

### 0.2 Versioning
Every persisted object includes:
- `schemaVersion`: for migrations and backwards compatibility.

### 0.3 Core vs UI strings
- **Realtime path** (audio thread) should operate on **numbers**, not strings.
- Chord labels, staff/tab, and rich rendering are **UI/background** responsibilities.
- If you cache labels, treat them as *display caches*, never as source of truth.

### 0.4 Bank modifiers belong to banks
ChordBlocks **must not** embed full bank modifiers. Banks can be duplicated with separate modifiers, so block-level duplication would create drift and bugs.

### 0.5 Operators support multiple instances of the same type
Operator chains store **instances** with unique IDs, not just types.

---

# 1) EngineProject (Top-level container)

**Purpose:** Single source of truth for an entire session/preset.  
Owns global catalogs (operator defs, mapping profiles) and central stores (banks, blocks).

```jsonc
{
  // Type helps tooling and future multi-document serialization.
  "type": "EngineProject",

  // Unique project ID.
  "id": "proj_01",

  // Schema version for project-level migrations.
  "schemaVersion": "1.0.0",

  // Optional human-facing name (useful in standalone/preset packs).
  "name": "ChordPallette Session",

  // Defaults used when a bank or block does not provide an override.
  "defaults": {
    // Default key context for notation if a bank doesn’t specify it.
    "musicalContext": {
      "keyTonicPc": null,         // null means “unknown / not set”
      "mode": null,               // major, minor, dorian, etc.
      "spellingPreference": "auto"// auto | sharps | flats
    },

    // Default trigger behavior across the project.
    "triggerBehavior": {
      "mode": "hold",             // oneShot | hold | latch | retrigger
      "monoChord": false          // if true, new chord releases previous chord
    }
  },

  // Central store of banks.
  "banksById": {
    "bank_main_01": { "ref": "See Bank model" }
  },

  // Central store of chord blocks (single source of truth).
  "chordBlocksById": {
    "chord_a1f3e8": { "ref": "See ChordBlock model" }
  },

  // Central store of keyswitch blocks (optional centralization).
  // If you prefer bank-local keyswitch libraries, you can omit this and keep keyswitches inside Bank.
  "keyswitchBlocksById": {
    "ksw_spiccato_01": { "ref": "See KeyswitchBlock model" }
  },

  // Operator definitions are the shipped catalog (“operator pack” capability).
  "operatorDefinitionsById": {
    "opd_voice_leading": { "ref": "See OperatorDefinition model" }
  },

  // Bank modifier definitions are the shipped catalog for bank-level behaviors.
  "bankModifierDefinitionsById": {
    "bmd_note_repositioning": { "ref": "See BankModifierDefinition model" }
  },

  // Mapping profiles can be shared/reused across banks.
  "mappingProfilesById": {
    "map_main_01": { "ref": "See MappingProfile model" }
  },

  // Library of user tags for quick reuse.
  "tagLibrary": {
    "tags": ["jazz", "smooth", "chorus", "verse", "pad", "piano"]
  },

  // Audit metadata for syncing and debugging.
  "metadata": {
    "createdAt": "2026-02-14T10:30:00Z",
    "lastModified": "2026-02-14T10:45:00Z"
  }
}
```

---

# 2) Bank

**Purpose:** Hosts multiple chord blocks and owns all bank-wide behavior:
- bank modifiers (range, transpose, playable mask)
- mapping profile (trigger rules)
- bank-wide voice leading style (performance feel)

```jsonc
{
  "type": "Bank",
  "id": "bank_main_01",
  "schemaVersion": "1.0.0",

  // Display name shown in UI.
  "name": "Main Bank",

  // UI ordering (stable, user-controlled).
  "order": 0,

  // Key/mode context makes Nashville/Roman/spelling consistent and meaningful.
  "musicalContext": {
    "keyTonicPc": 0,               // 0=C
    "mode": "major",
    "spellingPreference": "auto"   // auto | sharps | flats
  },

  // Bank-wide post-processing rules (apply after block operators).
  "bankModifiers": {
    "transposeSemitones": 0,
    "octaveShift": 0,

    // Output range to prevent mud and keep instrument playable.
    "outputRange": { "minNoteAbs": 36, "maxNoteAbs": 84 },

    // Optional constraint: only allow specific pitch classes.
    "playableNotesMask": {
      "enabled": false,
      "pitchClassAllowed": [true, true, true, true, true, true, true, true, true, true, true, true]
    },

    // What to do if notes fall outside range or are disallowed.
    "noteRepositioning": {
      "mode": "fold",              // fold | cull | nearest | mirror
      "preserveBass": true,
      "preserveTop": false
    },

    // Bank-wide velocity shaping for consistent feel.
    "velocity": { "enabled": true, "gain": 1.0, "min": 1, "max": 127 }
  },

  // Voice leading is bank-wide by default to provide a consistent performance personality.
  "voiceLeading": {
    "enabled": true,
    "styleId": "smooth",           // smooth | cinematic | neo_soul | classical | edm_stack | custom

    // Reset behavior prevents “drift” during non-linear performance.
    "reset": { "mode": "onInactivity", "inactivityMs": 1200 }, // continuous | onInactivity | onBar | manual

    // Small numeric settings for realtime safety.
    "settings": {
      "tightness": 0.75,           // 0..1
      "maxJumpSemitones": 12,
      "preserveBass": true,
      "preserveTop": false,
      "allowVoiceCrossing": false
    }
  },

  // Reference to a mapping profile (kept in project store for reuse).
  "mappingProfileId": "map_main_01",

  // Optional: bank-local keyswitch library. You can also centralize keyswitches at project level.
  "keyswitchLane": {
    "enabled": true,
    "keyswitchBlockIds": ["ksw_spiccato_01"]
  },

  // Bank owns the order of blocks; blocks live in the central store.
  "chordBlockOrder": ["chord_a1f3e8", "chord_b91c22", "chord_7d3aa0"],

  "metadata": {
    "tags": ["setlist", "live"],
    "favorite": true,
    "createdAt": "2026-02-14T10:30:00Z",
    "lastModified": "2026-02-14T10:30:00Z",
    "notes": "Primary performance bank."
  },

  // Provenance supports duplication workflows.
  "provenance": { "origin": "original", "sourceBankId": null },

  // Optional caches for fast UI display (never source of truth).
  "caches": {
    "bankSettingsHash": "hash_9a2c...",
    "outputPreviewByBlockId": {
      "chord_a1f3e8": { "labelStandard": "Csus4", "notesAbs": [48, 53, 55] }
    }
  }
}
```

---

# 3) ChordBlock

**Purpose:** A stored chord event with non-destructive operator chain, tags, notation preferences, and freeze history.

Key design decisions:
- `baseChord` is immutable.
- `operatorChain` supports multiple instances of same operator type via `instanceId`.
- Bank settings live in the bank; the block only links to its bank and can optionally ignore some bank rules.

```jsonc
{
  "type": "ChordBlock",
  "id": "chord_a1f3e8",
  "schemaVersion": "1.0.0",

  "title": "Csus4 Spread",

  // Capture provenance helps recreate and debug behavior.
  "source": {
    "type": "midi_live",          // midi_live | midi_playback | piano_roll | typed | circle_of_fifths | audio_detected
    "details": { "ppqPosition": 128.0, "captureWindowMs": 60 }
  },

  // Immutable base chord (pre-operators).
  "baseChord": {
    "pitchClassSet": [0, 5, 7],
    "notesAbs": [48, 53, 55],     // default voicing
    "rootPc": 0,
    "rootConfidence": 0.72,
    "inversion": 0,
    "bassNoteAbs": 48,

    // Optional local key context; if null, use bank/project context for notation.
    "keyContext": { "keyTonicPc": null, "mode": null },

    // Preserve ambiguity so users can choose when needed.
    "candidates": [
      { "labelStandard": "Csus4", "confidence": 0.64, "rootPc": 0, "bassPc": 0 },
      { "labelStandard": "F5/C",  "confidence": 0.31, "rootPc": 5, "bassPc": 0 }
    ]
  },

  // Ordered operator instances (non-destructive).
  "operatorChain": [
    {
      "instanceId": "opi_01",
      "typeId": "voicing_spread",
      "enabled": true,
      "order": 10,
      "parameters": { "spreadSemitones": 12, "inversionSteps": 1 },
      "uiLabel": "Spread + Invert"
    },
    {
      "instanceId": "opi_02",
      "typeId": "harmonic_substitute",
      "enabled": true,
      "order": 20,
      "parameters": { "substitution": "iv", "blend": 0.75 },
      "uiLabel": "Borrowed iv blend"
    },
    {
      // Same operator type can appear again with different settings.
      "instanceId": "opi_03",
      "typeId": "voicing_spread",
      "enabled": false,
      "order": 30,
      "parameters": { "spreadSemitones": 24, "inversionSteps": 0 },
      "uiLabel": "Big Spread (disabled)"
    }
  ],

  // Link to bank that owns modifiers + mapping behavior.
  "bankLink": {
    "bankId": "bank_main_01",

    // Per-block overrides should be rare and minimal.
    "override": {
      "ignoreBankTranspose": false,
      "ignoreBankRangeRules": false
    }
  },

  // Keyswitches must bypass chord processing and be merged late.
  "keyswitch": {
    "attachedKeyswitchBlockIds": ["ksw_spiccato_01"],
    "bypassChordProcessing": true,
    "timing": { "offsetMs": -25 }
  },

  // Notation settings: store structured data + user overrides, not just a single label.
  "notation": {
    "standard": { "primary": "Csus4", "enharmonicAlternates": ["Dbsus4"], "userOverride": null },
    "nashville": { "value": null, "dependsOnKeyContext": true },
    "romanNumeral": { "value": null, "dependsOnKeyContext": true },
    "staff": { "enabled": true, "renderCacheKey": null },
    "guitar": { "enabled": false, "preferredPositions": [], "tabCacheKey": null }
  },

  "metadata": {
    "tags": ["jazz", "smooth"],
    "favorite": true,
    "createdAt": "2026-02-14T10:30:00Z",
    "lastModified": "2026-02-14T10:30:00Z",
    "notes": ""
  },

  // Cache keys enable fast UI without becoming the source of truth.
  "caches": {
    "baseFingerprint": "fp_base_4a7f2e9c1b5d",
    "derivedFingerprint": null,
    "outputFingerprint": null,
    "derivedChordPreview": { "notesAbs": null, "labelStandard": null },
    "outputChordPreview": { "notesAbs": null, "labelStandard": null }
  },

  // Freeze/bake system preserves original while allowing “fresh” blocks.
  "freeze": {
    "isFrozen": false,
    "frozenBaseChord": null,

    // Minimal event history for traceability.
    "history": [
      { "action": "created", "at": "2026-02-14T10:30:00Z", "notes": "Captured from live MIDI" }
    ]
  }
}
```

---

# 4) KeyswitchBlock

**Purpose:** Named MIDI notes used to control articulations/patch behavior in instruments.
Keyswitch notes:
- are merged late into the output
- are excluded from chord detection, naming, and operators

```jsonc
{
  "type": "KeyswitchBlock",
  "id": "ksw_spiccato_01",
  "schemaVersion": "1.0.0",

  // User-facing name (instrument-specific).
  "name": "Spiccato",

  // Notes to send for this keyswitch.
  "notesAbs": [24],

  // Timing rules ensure keyswitch fires before chord notes.
  "timing": {
    "noteLengthMs": 80,
    "offsetMs": -25
  },

  // Channel routing supports multi-timbral setups.
  "midiChannel": 1
}
```

---

# 5) MappingProfile

**Purpose:** Defines how triggers (notes/CC/keyboard/program change) map to actions like triggering blocks or selecting banks.

Stored separately so multiple banks can reuse a profile.

```jsonc
{
  "type": "MappingProfile",
  "id": "map_main_01",
  "schemaVersion": "1.0.0",

  // userDefined | autoSlideBracket | computerKeys | midiSplits
  "mode": "userDefined",

  // What counts as a trigger.
  "triggerSources": {
    "notes": { "enabled": true, "channelPolicy": "any" }, // any | list
    "cc": { "enabled": false, "learnedCc": null },
    "programChange": { "enabled": false }
  },

  // Routes describe how triggers become actions.
  "routes": [
    {
      "trigger": { "type": "note", "noteAbs": 60 },
      "action": { "type": "triggerBlock", "blockId": "chord_a1f3e8" }
    },
    {
      "trigger": { "type": "cc", "ccNumber": 1, "range": [0, 127] },
      "action": { "type": "selectBankByValue", "bankIds": ["bank_main_01", "bank_alt_02"] }
    }
  ],

  // Optional quantization for tighter live feel.
  "timing": {
    "quantizeEnabled": false,
    "grid": "1/16",
    "swing": 0.0
  }
}
```

---

# 6) OperatorDefinition (Catalog / Packs)

**Purpose:** Defines the operator catalog (what operators exist, their parameters, and realtime safety).
Enables shipping “operator packs” without rewriting UI.

```jsonc
{
  "type": "OperatorDefinition",
  "id": "opd_voice_leading",
  "schemaVersion": "1.0.0",

  "typeId": "voice_leading",
  "displayName": "Voice Leading",
  "category": "voicing", // voicing | harmonic | performance | humanize | midi_behavior

  "description": "Smoothly connects the next chord to the last chord you played.",

  "parameters": [
    {
      "id": "styleId",
      "type": "enum",
      "default": "smooth",
      "options": ["smooth", "cinematic", "neo_soul", "classical", "edm_stack"],
      "whyItMatters": "Style changes the musical personality of transitions."
    },
    {
      "id": "maxJumpSemitones",
      "type": "int",
      "default": 12,
      "min": 0,
      "max": 24,
      "whyItMatters": "Limits how far a voice can leap so progressions stay playable."
    }
  ],

  // If false, the engine must not run this operator on the audio thread.
  "realtimeSafe": true
}
```

---

# 7) OperatorInstance (Stored in operator chains)

**Purpose:** A configured instance of an operator with parameters, order, and enabled state.
This is what the user actually edits.

```jsonc
{
  "type": "OperatorInstance",
  "id": "opi_01",
  "schemaVersion": "1.0.0",

  // The operator type this instance uses.
  "typeId": "voice_leading",

  "enabled": true,
  "order": 20,

  // Keep parameters compact and numeric for realtime.
  "parameters": {
    "styleId": "smooth",
    "tightness": 0.75,
    "maxJumpSemitones": 12
  }
}
```

---

# 8) BankModifierDefinition (Catalog)

**Purpose:** Defines bank-wide modifier catalog so UI can render consistent controls and packs can be shipped.

```jsonc
{
  "type": "BankModifierDefinition",
  "id": "bmd_note_repositioning",
  "schemaVersion": "1.0.0",

  "typeId": "note_repositioning",
  "displayName": "Note Repositioning",
  "description": "For notes outside your playable range, choose how the engine moves or removes them.",

  "parameters": [
    {
      "id": "mode",
      "type": "enum",
      "default": "fold",
      "options": ["fold", "cull", "nearest", "mirror"],
      "whyItMatters": "Prevents chords from becoming muddy or unplayable."
    },
    {
      "id": "preserveBass",
      "type": "bool",
      "default": true,
      "whyItMatters": "Keeps the low end stable, which matters most in a mix."
    }
  ],

  "realtimeSafe": true
}
```

---

# 9) ChordSnapshot (Detection input)

**Purpose:** A captured note event group used for reliable chord detection.

```jsonc
{
  "type": "ChordSnapshot",
  "id": "snap_001",
  "schemaVersion": "1.0.0",

  "captureRule": {
    "mode": "timeWindow",      // heldNotes | timeWindow | quantized
    "windowMs": 60,
    "includeShortNotes": true
  },

  "input": {
    "notesAbs": [48, 53, 55],
    "velocities": [92, 85, 78],
    "noteOnOffsetsMs": [0, 18, 35]
  },

  "hostContext": {
    "ppqPosition": 128.0,
    "tempoBpm": 120.0,
    "timeSig": "4/4"
  }
}
```

---

# 10) ChordDetectionResult (Candidates + confidence)

**Purpose:** Preserves ambiguity and allows user choice without breaking workflows.

```jsonc
{
  "type": "ChordDetectionResult",
  "id": "det_001",
  "schemaVersion": "1.0.0",

  "snapshotId": "snap_001",

  "best": {
    "labelStandard": "Csus4",
    "rootPc": 0,
    "bassPc": 0,
    "confidence": 0.64
  },

  "candidates": [
    { "labelStandard": "Csus4", "rootPc": 0, "bassPc": 0, "confidence": 0.64 },
    { "labelStandard": "F5/C",  "rootPc": 5, "bassPc": 0, "confidence": 0.31 },
    { "labelStandard": "Am(add4)/C", "rootPc": 9, "bassPc": 0, "confidence": 0.12 }
  ],

  "spellingHint": {
    "prefer": "sharps",         // sharps | flats | auto
    "reason": "Key context suggests sharp spellings."
  }
}
```

---

# 11) PerformanceContext (Realtime “last chord played” state)

**Purpose:** Enables musically relevant behavior in non-linear performance.  
Voice leading leads from what *actually happened*.

```jsonc
{
  "type": "PerformanceContext",
  "schemaVersion": "1.0.0",

  "lastOutput": {
    "notesAbs": [48, 53, 55],
    "bassNoteAbs": 48,
    "topNoteAbs": 55,
    "sourceBlockId": "chord_a1f3e8"
  },

  "hostTiming": {
    "ppqPosition": 128.0,
    "tempoBpm": 120.0,
    "timeSig": "4/4"
  },

  "resetState": {
    "mode": "onInactivity",
    "lastTriggerTimeMs": 12345678,
    "inactivityMs": 1200
  }
}
```

---

# 12) ChordResult (Derived vs Output chord)

**Purpose:** Explicitly separates:
- `derived`: after block operators
- `output`: after bank modifiers (and voice leading, if treated as part of derived stage)

```jsonc
{
  "type": "ChordResult",
  "id": "res_001",
  "schemaVersion": "1.0.0",

  "blockId": "chord_a1f3e8",
  "bankId": "bank_main_01",

  "derived": {
    "notesAbs": [48, 55, 60],
    "pitchClassSet": [0, 5, 7],
    "labelStandard": "Csus4",
    "provenance": {
      "appliedOperatorInstanceIds": ["opi_01", "opi_02"],
      "notesChanged": true
    }
  },

  "output": {
    "notesAbs": [48, 55, 60],
    "pitchClassSet": [0, 5, 7],
    "labelStandard": "Csus4",
    "provenance": {
      "bankModifiersApplied": ["transposeSemitones", "noteRepositioning"],
      "notesChanged": false
    }
  }
}
```

---

# 13) MidiEventSequence (Core → Integration output)

**Purpose:** Core generates MIDI events as data; Integration injects them into host buffers.
This keeps Core JUCE-free and testable.

```jsonc
{
  "type": "MidiEventSequence",
  "id": "seq_001",
  "schemaVersion": "1.0.0",

  "events": [
    {
      "type": "noteOn",          // noteOn | noteOff | cc | programChange
      "noteAbs": 60,
      "velocity": 96,
      "sampleOffset": 0,
      "midiChannel": 1
    },
    {
      "type": "noteOff",
      "noteAbs": 60,
      "velocity": 0,
      "sampleOffset": 480,
      "midiChannel": 1
    }
  ],

  "meta": {
    "generatedBy": {
      "bankId": "bank_main_01",
      "blockId": "chord_a1f3e8",
      "operatorInstanceIds": ["opi_01"]
    },
    "humanizeSeed": 12345
  }
}
```

---

## 14) Interoperability Summary (How everything fits)

- **EngineProject** owns:
  - `banksById`
  - `chordBlocksById`
  - catalogs (`operatorDefinitionsById`, `bankModifierDefinitionsById`)
  - reusable `mappingProfilesById`

- **Bank** owns:
  - `bankModifiers` (global output rules)
  - `voiceLeading` (bank-wide style)
  - `mappingProfileId`
  - `chordBlockOrder` (ordering only)

- **ChordBlock** owns:
  - `baseChord` (immutable)
  - `operatorChain` (instances)
  - `notation` preferences and overrides
  - `freeze` history
  - `bankLink` (reference)

- **PerformanceContext** is runtime-only (or optionally persisted) and enables non-linear performance coherence.

- **ChordResult** and **MidiEventSequence** are computed outputs used for UI preview and realtime emission.

---

## 15) Recommended next additions (when you’re ready)
To round this out further, the next “core” objects typically needed are:
- **Preset** (packaging EngineProject snapshots)
- **UndoStep** (user actions + reversible diffs)
- **PackManifest** (operator/voicing packs metadata)
- **AudioChordAnalysisJob** (offline audio → chord candidates pipeline)

---

End of master document.
