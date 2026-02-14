# ChordPallette — Migration, Serialization Contract, and Undo/Redo Reducer Model
_Last updated: 2026-02-14_

This document covers three engineering pillars required for a commercial-grade plugin:

1) **Migration / versioning strategy** (detailed)  
2) **Serialization format contract** for JUCE **APVTS** integration  
3) **State reducer model** for **undo/redo** architecture

Assumptions (consistent with previous docs):
- Core is **JUCE-free** and owns the canonical models.
- Integration (JUCE) adapts Core to the host and APVTS.
- Realtime path uses **numeric** data and precomputed/cached assets where possible.
- Object models use `schemaVersion` at object level and an `engineVersion` at package level.

---

# 1) Migration / Versioning Strategy (Detailed)

## 1.1 Goals
- **Never break old sessions** (DAW project recall must work years later).
- Support **forward evolution** (new fields, new features, new packs).
- Migrations must be:
  - deterministic
  - testable
  - safe if partially applied
  - reversible where possible
- Avoid realtime risk: migrations are executed on **load**, not in audio thread.

---

## 1.2 Version Types (Use All Three)

### A) Engine Version (binary / release version)
- Example: `engineVersion = "1.2.0"`
- Set by the plugin build.
- Used to choose migration bundles and feature gates.

### B) Project Schema Version (top-level)
- Example: `EngineProject.schemaVersion = "1.0.0"`
- Represents the structure of the `EngineProject` container.

### C) Object Schema Version (per object)
- Each object includes `schemaVersion`.
- Enables granular updates (e.g., `ChordBlock` changed, but `Bank` didn’t).

**Why all three matter:**
- Engine version = code behavior / capabilities.
- Project schema = top-level serialization layout.
- Object schema = safe evolution of individual object types.

---

## 1.3 Semver Rules (Strict)
We treat `schemaVersion` like SemVer but with stricter expectations.

### Patch (x.y.Z)
Allowed:
- bugfixes
- clarifying fields that don’t change meaning
- adding optional fields with defaults
No migration required if defaults are safe.

### Minor (x.Y.z)
Allowed:
- adding new fields (optional)
- adding new enum values (with fallback behavior)
- adding new object types
Migration required only if old data needs normalization.

### Major (X.y.z)
Allowed:
- changing meaning of existing fields
- restructuring objects
- changing required fields
Migration is mandatory and must be explicit + tested.

---

## 1.4 Compatibility Policies

### Backward compatibility (required)
New plugin version must load older sessions.
- Always support N-2 major versions if feasible.
- If not feasible, provide:
  - “legacy loader mode”
  - export utility
  - user-facing warning

### Forward compatibility (nice-to-have)
Older plugin versions loading newer sessions is not guaranteed, but:
- Use additive changes so older versions can ignore unknown fields.
- Preserve unknown fields when possible to avoid destructive “downgrade loss.”

---

## 1.5 Migration Architecture

### 1.5.1 Canonical pipeline
On load (Integration layer):
1. Deserialize raw bytes → **Raw JSON/CBOR object**
2. Identify `engineVersion` and `schemaVersion`
3. Run migrations (possibly multiple steps):
   - `project migrations`
   - `object migrations`
4. Validate model invariants
5. Build runtime caches (background thread where heavy)
6. Atomically publish config snapshots to audio thread

**Rule:** Migration must finish before Core is used for realtime operations.

---

### 1.5.2 Migrator interface (Core)
Core owns migration logic so it stays portable and testable.

```cpp
// Pseudocode (Core)
struct MigrationResult {
  Json migrated;
  std::vector<std::string> warnings;
  std::vector<std::string> errors;
};

MigrationResult migrateProject(Json raw, std::string engineVersion);
```

Integration calls this at load-time.

---

## 1.6 Invariants (Validation Rules)
After migration, enforce these invariants (fail-safe with warnings):

### Required IDs and references
- Every `Bank.id` is unique
- Every `ChordBlock.id` is unique
- Every `Bank.chordBlockOrder[i]` exists in `EngineProject.chordBlocksById`
- Every `ChordBlock.bankLink.bankId` exists in `EngineProject.banksById`
- Every `Bank.mappingProfileId` exists OR is null (fallback to defaults)
- Every `ChordBlock.operatorChain[*].instanceId` is unique within that block

### Realtime-safe field rules
- Any field used in audio thread must be numeric/enum/bool.
- Strings are allowed only in metadata/labels and must not be required for realtime.

### Model normalization rules
- Ensure `operatorChain` is sorted by `order` then stable tie-break by `instanceId`
- Ensure `pitchClassSet` is sorted, unique, in range 0..11
- Ensure `notesAbs` is sorted if ordering required (define consistent rule)

---

## 1.7 Migration Types (Common Scenarios)

### A) Add a new optional field
Example: add `ChordBlock.metadata.color`
- Migration: none required if absent defaults to null
- Validation: ensure if present it is within allowed palette

### B) Rename a field
Example: `bankModifiers.transpose` → `transposeSemitones`
- Migration required: copy old → new, delete old
- Keep a compatibility shim for at least one major cycle

### C) Split one object into two
Example: keyswitch blocks moved from Bank-local to Project-global
- Migration required:
  - extract each bank’s keyswitch blocks into `keyswitchBlocksById`
  - replace with ID references
  - ensure IDs are unique (dedupe by hash + name)

### D) Change semantics
Example: voice leading reset `inactivityMs` now in seconds
- Major migration: multiply/divide and annotate warnings

---

## 1.8 Migration Testing (Non-Optional)
Create a migration test suite with fixtures:
- `fixtures/v0_9_0/*.json`
- `fixtures/v1_0_0/*.json`

Tests:
- migration produces valid invariants
- serialization round-trip keeps meaning
- no missing references
- determinism: migrating same input yields identical output

---

# 2) Serialization Format Contract (JUCE APVTS Integration)

## 2.1 Goals
- DAW saves/loads reliably (VST3/AU/Standalone)
- Minimal risk of partial state restore
- Separation of concerns:
  - APVTS stores parameters and small values
  - Core stores structured models (banks/blocks/packs)
- Support future migrations cleanly

---

## 2.2 Split State into Two Channels

### A) Parameter State (APVTS)
Use APVTS for:
- continuous parameters: knobs, toggles, UI settings
- performance controls: global transpose, velocity gain, etc. (if exposed as parameters)
- automation-friendly values

### B) Document State (Core Model Blob)
Use a single serialized blob for:
- EngineProject models (banks, chord blocks, mapping profiles, operator instances)
- Presets/packs references
- user tags, chord metadata

**Reason:** APVTS parameter tree is not ideal for large nested documents and makes migrations harder.

---

## 2.3 Format Choice: JSON (Dev) + CBOR (Ship)
Recommended contract:
- Persist as **CBOR** (compact binary, JSON-like)
- Optionally store a readable **JSON debug copy** in dev builds

Why CBOR:
- smaller
- faster
- schema-friendly
- maps cleanly to JSONC examples conceptually

Contract still uses JSON field names and structure.

---

## 2.4 State Payload Layout (Integration)
State stored to host as a single binary block. Inside it:

```text
[Header]
  magic: "CPST" (ChordPallette State)
  containerVersion: u16
  engineVersion: string
  createdAt: ISO string
  checksum: u32 (optional)

[APVTS chunk]
  raw APVTS state (ValueTree xml/binary)

[Core chunk]
  format: "CBOR"
  bytes: EngineProject payload (or Preset payload)
```

**Why a header matters:**
- lets you quickly detect corrupt state
- allows future container format changes
- supports parallel legacy loaders

---

## 2.5 Core Chunk Contract
Core chunk is a serialized `EngineProject` (or subset) with mandatory fields:

Required top-level keys:
- `type = "EngineProject"`
- `id`
- `schemaVersion`
- `banksById`
- `chordBlocksById`
- `metadata.createdAt`

Optional:
- `operatorDefinitionsById`
- `bankModifierDefinitionsById`
- `mappingProfilesById`
- `keyswitchBlocksById`

**Rule:** Unknown fields must be ignored and preserved if possible.

---

## 2.6 APVTS ↔ Core binding contract
Do NOT allow Core to read APVTS directly.

Instead define a thin Integration adapter:

```text
APVTS Parameters  →  EngineConfigSnapshot  →  Core (atomic swap)
Core Model Blob   →  EngineProject         →  Core (on load)
```

### Binding rules
- APVTS parameters must map to a clean `EngineConfigSnapshot` struct.
- Project model changes (blocks/banks) come from UI commands and update Core model store.
- Audio thread reads only:
  - atomic pointer to `EngineConfigSnapshot`
  - stable references/handles to current project store (immutable snapshot or lock-free)

---

## 2.7 Save/Load Ordering (Critical)
On restore:
1. Deserialize container header
2. Restore APVTS parameters
3. Load Core chunk (EngineProject)
4. Run migrations
5. Validate invariants
6. Publish snapshots to audio thread
7. Notify UI

On save:
1. Serialize APVTS
2. Serialize EngineProject (CBOR)
3. Write container header + chunks

---

# 3) Undo/Redo — State Reducer Model

## 3.1 Goals
- Fast and reliable undo/redo across complex edits
- Works with:
  - operator chains (add/remove/reorder/edit params)
  - chord edits (base chord changes, candidate selection)
  - bank edits (modifiers, mapping changes)
  - multi-select batch operations
- Minimal memory overhead
- Deterministic re-application of actions

---

## 3.2 Core Strategy: Action + Reducer + Patch
Use a **reducer** architecture:
- UI emits **Actions**
- Reducer applies action to current `EngineProject` to produce a new `EngineProject`
- UndoStep stores enough info to reverse (patch/diff)

Two viable implementations:
1) **Patch-based** (recommended): store JSON Patch (RFC 6902 style) or your own compact patch
2) **Command-based**: store inverse action payloads

We’ll define a patch-based contract that aligns with earlier `UndoStep` model.

---

## 3.3 Action Model (Canonical)
Actions are small, typed, and serializable.

```jsonc
{
  "type": "Action",
  "actionType": "SetOperatorParam",
  "timestamp": "2026-02-14T12:10:00Z",
  "payload": {
    "blockId": "chord_a1f3e8",
    "operatorInstanceId": "opi_01",
    "param": "tightness",
    "value": 0.75
  }
}
```

Rules:
- Actions must not rely on UI state (e.g., selection objects) unless included in payload.
- Actions should be replayable for deterministic behavior.

---

## 3.4 Reducer Signature
Reducer is pure and deterministic.

```text
reduce(project: EngineProject, action: Action) -> EngineProject
```

Purity rules:
- No IO
- No random
- No time calls (timestamp comes from action)
- No host calls
- No UI dependencies

---

## 3.5 Patch / UndoStep Contract (Upgraded)
Instead of a single `targetPath`, support multiple operations so batch edits become one undo step.

```jsonc
{
  "type": "UndoStep",
  "id": "undo_001",
  "schemaVersion": "1.0.0",
  "description": "Batch: Spread +12 on 8 blocks",
  "timestamp": "2026-02-14T12:10:00Z",

  // A list of atomic operations.
  "ops": [
    {
      "op": "replace", // add | remove | replace | move | copy
      "path": "/chordBlocksById/chord_a1f3e8/operatorChain/0/parameters/spreadSemitones",
      "before": 6,
      "after": 12
    },
    {
      "op": "replace",
      "path": "/chordBlocksById/chord_b91c22/operatorChain/0/parameters/spreadSemitones",
      "before": 6,
      "after": 12
    }
  ],

  // Optional: action reference for analytics/debugging.
  "originActionType": "BatchSetOperatorParam",

  // Optional: multi-step operations grouping.
  "groupId": "group_123"
}
```

### Why this is better than a single diff
- One user gesture may touch many blocks.
- This format supports multi-op undo/redo cleanly.
- Keeps changes explicit and testable.

---

## 3.6 Applying Undo/Redo
Undo stack stores UndoSteps. Redo stack stores UndoSteps popped from undo.

### Apply Undo
For each op in reverse order:
- apply inverse of op using `before` values

### Apply Redo
For each op in forward order:
- apply op using `after` values

This is deterministic and does not require re-running the original action.

---

## 3.7 Common Reducer Operations (Must Support)

### Block operations
- Add block
- Remove block
- Duplicate block (new IDs)
- Reorder blocks within bank
- Edit base chord (notesAbs, pitchClassSet)
- Select detection candidate (update baseChord.rootPc, label override, etc.)

### Operator operations
- Add operator instance
- Remove operator instance
- Toggle enabled
- Reorder instances
- Set parameter values

### Bank operations
- Duplicate bank (new bankId + independent bankModifiers)
- Edit bankModifiers (transpose, range, playable mask)
- Set voiceLeading style/settings/reset
- Change mappingProfileId or edit mapping profile

### Keyswitch operations
- Add keyswitch block
- Attach keyswitch to chord block
- Edit keyswitch timing/channel

---

## 3.8 State Storage Strategy (Performance)
To keep UI responsive and audio thread safe:

### Recommended: Immutable EngineProject snapshots (UI side) + Atomic handle (Audio side)
- UI holds mutable working state (or uses persistent data structure)
- Commit produces a new immutable EngineProject snapshot
- Audio thread sees only the stable snapshot via atomic pointer/handle

Undo/redo just swaps snapshots:
- apply UndoStep → new snapshot
- atomic swap

Heavy caches are rebuilt asynchronously.

---

## 3.9 Cache Invalidation Rules (Undo/Redo Friendly)
Any patch affecting these should invalidate caches:
- ChordBlock.baseChord or operatorChain → invalidate derived + output caches
- Bank.bankModifiers or voiceLeading → invalidate output caches for blocks in that bank
- MappingProfile edits → no need to invalidate chord caches, but update routing views
- Notation overrides → invalidate label caches only

Implement this with:
- `dirtyFlags` or derived hash recomputation
- background refresh jobs

---

# 4) End-to-End Contracts (How the 3 systems connect)

## Load flow
1. Deserialize container
2. Restore APVTS
3. Load EngineProject CBOR
4. Migrate + validate
5. Build EngineConfigSnapshot from APVTS
6. Publish snapshots (atomic swap)
7. UI reads snapshot + begins background cache builds

## Edit flow (with undo)
1. UI emits Action
2. Reducer produces new EngineProject snapshot
3. Create UndoStep patch ops (before/after)
4. Push UndoStep to undo stack, clear redo stack
5. Publish updated snapshot to audio thread (atomic swap)
6. Background rebuild caches if needed

## Save flow
1. Serialize APVTS
2. Serialize EngineProject snapshot
3. Write container header + chunks

---

# 5) Implementation Checklist

## Migration
- [ ] Define migration registry keyed by schemaVersion pairs
- [ ] Write invariants validator
- [ ] Add fixtures + unit tests for migration determinism

## Serialization
- [ ] Implement container header + chunk writer/reader
- [ ] CBOR encode/decode for EngineProject
- [ ] Strict load order (APVTS → Core → migrate → validate → publish)

## Undo/Redo
- [ ] Define Action types + payloads
- [ ] Implement pure reducer
- [ ] Generate UndoStep ops (multi-op)
- [ ] Apply undo/redo by ops
- [ ] Cache invalidation strategy

---

End of document.
