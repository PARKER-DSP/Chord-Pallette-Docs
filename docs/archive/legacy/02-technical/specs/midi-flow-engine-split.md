> **Archived (non-authoritative):** This file is retained for historical reference only. Use canonical pages from the main navigation for current guidance.

# ChordPallette — MIDI Flow, Engine Split, and Spec Sheet (Draft)

## 1) Summary of Features (clean list)

### A. Input & Capture
- **MIDI chord capture**
  - From DAW track playback (host MIDI)
  - From external controllers (MIDI input)
  - From on-screen piano roll input
  - From typed chord name
  - From circle-of-fifths / harmonic tools (generation)
- **Audio-to-chord capture** (optional module)
  - Detect chord candidates from audio
  - Present multiple voicing/label options for user selection
- **Reliable chord detection**
  - Windowed “snapshot” detection (time-quantized / threshold-based)
  - Chord naming with enharmonic variants (sharp/flat)
  - Support for inversions, slash chords, and ambiguous pitch sets

### B. Chord Blocks & Banks
- **Chord Block**: a stored chord event with rich metadata and non-destructive edits
- **Multiple chord banks**
- **Sortable / rearrangeable blocks**
- **Custom user tags** per chord block (freeform + predefined)
- **Keyswitch blocks** (separate lane)
  - Drag onto chord blocks; outputs alongside chord events
  - **Not affected** by chord operators or bank modifiers

### C. Notation & Representation (per block)
- Standard chord symbol (e.g., Cmaj9, F#m7b5/G)
- Nashville numbers (relative to key)
- Roman numeral notation (functional harmony, relative to key/mode)
- Staff representation (pitch + voicing; treble/bass clef as needed)
- Guitar tab / fingering position (where feasible via voicing-to-fretboard mapping)
- Voicing information
  - Pitch set (classes + absolute MIDI notes)
  - Inversion / bass note
  - Spread/cluster metrics
  - Range and register
  - “Playable” flags per note (post modifiers)
- Enharmonic spelling variants (C# vs Db) with rule set + user override

### D. Chord Operators (non-destructive)
Operators are modular transforms applied to a block’s **base chord** to produce a **performed chord**:
- **Voicing operators**: inversion, drop2/drop3, spread, close/open, re-voice, top-note lock, bass lock
- **Range operators**: clamp range, “only root in sub-bass”, octave management
- **Harmonic operators**: borrowed chord, modal interchange, secondary dominants (optional), reharmonize (optional)
- **Performance operators**: strum, arpeggiate, rhythm patterns, melodic play, humanize, velocity random, note chance/probability
- **MIDI behavior operators**: latch/hold, retrigger, legato rules, voice-leading optimization to previous block

### E. Bank Modifiers (global post-processing)
Applied after per-block operators, at the bank level:
- **Playable notes mask** (user-defined output note set)
- **Out-of-range repositioning** for notes outside user output range:
  - Fold
  - Cull
  - Nearest
  - Mirror
- **Bank-level redetection** to display “actual output chord” metadata (post chain)

### F. Freeze / Lock-In
- **Lock-in modifications**: bake current operator + bank modifier result into a new “fresh” base chord state
- Preserve provenance:
  - Original base chord retained
  - History of applied operators and bank modifiers
  - Ability to revert / branch (optional)

### G. Mapping / Performance / Routing
- **MIDI mapping algorithms**
  - User-defined mapping
  - Auto mapping “slide bracket”
  - Computer keyboard play modes
  - MIDI splits (ranges)
- **Trigger modes**
  - One-shot, latch, hold, retrigger, strum/arp modes
- **Export / output**
  - Real-time MIDI out to instrument
  - Drag-and-drop MIDI clip generation with chord blocks + keyswitch notes

---

## 2) Recommended Engine Component Split (max reuse + flexibility)

### Core Domain (pure, testable C++ library)
1. **Pitch & Music Theory Core**
   - Pitch class, MIDI note utilities
   - Enharmonic spelling rules
   - Key, scale, mode structures
   - Interval/chord quality definitions
2. **Chord Model**
   - `ChordBase`: pitch set + metadata
   - `ChordVoicing`: ordered notes + register + fingering hints
   - `ChordLabelSet`: chord symbol + Nashville + Roman + spelling variant
3. **Chord Detection**
   - `ChordSnapshotter`: turns a MIDI stream into “note sets” (time window + hold logic)
   - `ChordIdentifier`: maps pitch sets to chord candidates + confidence scores
   - `ChordSpeller`: chooses note names (sharp/flat) based on key context + rules
4. **Operator System**
   - `IChordOperator` interface + registry
   - Deterministic operators (voicing/range/harmony)
   - Performance operators (generate event sequences: strum/arp/rhythm)
5. **Bank Modifier System**
   - `IBankModifier` interface + chain
   - Range remapping algorithms (fold/cull/nearest/mirror)
6. **Rendering / Serialization**
   - Chord → MIDI event generator
   - Chord → notation adapters (symbol/NNS/Roman/staff/tab)
   - State persistence (JSON/binary) + versioning

### Plugin Integration Layer (JUCE / host-specific)
7. **MIDI IO + Host Integration**
   - JUCE `processBlock` integration
   - Separate capture bus vs performance bus
8. **State + Presets**
   - Parameter system (APVTS)
   - Bank storage, operator settings, mappings, tags
9. **UI Layer**
   - Bank view, block editor, mapping tools, circle of fifths, staff/tab view
10. **Audio-to-Chord Module (optional)**
   - Separate compilation unit / feature flag
   - Runs as analysis pipeline, not in real-time audio thread if heavy

**Key principle:** Keep everything in (1–6) free of JUCE so you can reuse it for:
- standalone app
- plugin formats (VST3/AU)
- command-line test harness
- future mobile/embedded

---

## 3) MIDI Processing Tree (Record vs Play)

### 3.1 Record / Capture Mode (from input to stored chord block)

```mermaid
flowchart TD
  A[MIDI In: Host Track + Controller] --> B[MIDI Router]
  B --> C1[Capture Stream]
  B --> C2[Thru/Monitor Stream (optional)]

  C1 --> D[Chord Snapshotter\n(time window + held notes)]
  D --> E[Chord Identifier\n(pitch set -> candidates)]
  E --> F[Chord Speller\n(enharmonics + key context)]
  F --> G[Chord Metadata Builder\n(symbol + NNS + Roman + staff/tab)]
  G --> H[Create Chord Block\n(BaseChord + Meta + Tags)]
  H --> I[Insert into Chord Bank\n(unique/filter options)]
```

**Notes**
- Snapshotter should support:
  - “All held notes” mode
  - “Time window” mode (e.g., 30–80 ms)
  - “Quantized window” mode (to host PPQ)
- Identifier returns **multiple candidates + confidence** so UI can allow user selection when ambiguous.

---

### 3.2 Play / Performance Mode (trigger chord blocks → MIDI out)

```mermaid
flowchart TD
  A[MIDI In: Triggers\n(keys/notes/CC/keyboard)] --> B[Mapping Engine]
  B --> C[Select Bank + Block\n(modes/splits/slide bracket)]
  C --> D[BaseChord (immutable)]
  D --> E[Operator Chain (per-block)\nvoicing/harmony/range/perf]
  E --> F[Bank Modifier Chain (global)\nplayable mask + reposition]
  F --> G[Redetect Output Chord Meta\n(display actual output)]
  F --> H[MIDI Event Generator\n(strum/arp/rhythm/humanize)]
  H --> I[Keyswitch Lane Merge\n(untouched by operators)]
  I --> J[MIDI Out to Host]
```

**Guarantees**
- BaseChord is never destroyed.
- Operators produce a derived `ChordResult` (notes + meta + performance events).
- Bank modifiers produce a derived `OutputChordResult`.
- Keyswitches are merged late and bypass transformation.

---

## 4) Data Model Spec (core objects)

### 4.1 ChordBlock
- `id` (UUID)
- `createdFrom` (source: live MIDI, playback, typed, circle-of-fifths, audio)
- `timestamp` / `ppqPosition` (optional)
- `tags[]`
- `baseChord: ChordBase`
- `operatorChain: OperatorChain` (ordered list + params)
- `cachedDerived` (optional cache):
  - `derivedChord` (post operators)
  - `outputChord` (post bank modifiers)
  - `labelSet` (symbol/NNS/Roman)
  - `staffRenderData`, `tabRenderData`
  - `fingerings` (if computed)
- `freezeHistory[]` (optional): snapshots when lock-in is executed

### 4.2 ChordBase
- `notesAbs[]` (MIDI notes, sorted)
- `pitchClasses` (bitset 12)
- `bassNoteAbs`
- `keyContext` (optional)
- `detectionConfidence`
- `candidateLabels[]` (optional)

### 4.3 OperatorChain
- `operators[]`: `{ typeId, params, enabled }`
- Each operator implements either:
  - **Chord transform**: `ChordVoicing -> ChordVoicing`
  - **Event generator**: `ChordVoicing -> MidiEventSequence`

### 4.4 Bank
- `id`, `name`
- `blocks[]` (ordered)
- `keyswitchLane[]`
- `bankModifiers[]`
- `mappingProfile` (splits, keyboard mapping, CC mapping)
- `outputRange` and playable mask config
- `displayKeyContext` (for NNS/Roman)

---

## 5) Chord Operators — Specification Guidelines

### Operator Categories
1. **Structural** (changes notes): borrowed chord, add/remove tensions, reharmonize
2. **Voicing** (reorders/redistributes): inversion, drop2, spread, voice-leading
3. **Range & Role**: clamp, bass-only, top-note lock
4. **Performance** (event sequencing): strum, arp, rhythm, melodic
5. **Humanization**: timing/velocity randomness, note chance

### Non-destructive rule
- Operators never mutate `baseChord`.
- They emit a derived object with:
  - new note list
  - provenance (what changed and why)
  - re-detection step for accurate naming after any pitch changes

### Re-detection triggers
Perform re-detection when:
- Any operator changes pitch classes
- Any range modifier folds/culls/mirrors notes
- Any clamp changes octave placement
- Any chord-tone removal/addition occurs

---

## 6) Keyswitch Lane Rules
- Keyswitch blocks:
  - store one or more MIDI notes (or note + length)
  - can be renamed by user per instrument
  - may be dragged onto chord blocks
- During playback:
  - keyswitch events are merged after chord output is produced
  - keyswitch notes are excluded from chord detection, naming, and operators
- Export:
  - keyswitch notes appear in generated MIDI clip at configured offsets

---

## 7) Opportunities (product + engineering)

### Reliability & UX wins
- **Ambiguity UI**: show top 3 chord interpretations with confidence; user picks default rule.
- **Key context aware spelling**: consistent sharps/flats based on project key and user preference.
- **Voice-leading as a first-class operator**: “make next chord smooth” is a killer feature.

### Monetizable expansions
- Genre voicing packs (neo-soul, trap stacks, cinematic, worship)
- Operator packs (advanced rhythm engines, style strum, humanize models)
- Instrument profiles (keyswitch presets + tab/fretboard preferences)

### Technical wins
- Pure core library enables:
  - unit tests for detection/operators
  - CLI batch processing of MIDI files
  - reuse in standalone app and plugin
- Deterministic operator outputs enable reliable rendering and preview.

---

## 8) Architecture Options (with pros/cons)

### Option A — Pure Functional Pipeline (recommended baseline)
**Idea:** Everything is immutable transforms: `BaseChord -> Derived -> Output -> Events`.

**Pros**
- Extremely testable and predictable
- Easy caching (hash inputs → cache outputs)
- Non-destructive editing is natural
- Great for undo/redo and branching

**Cons**
- Can generate more allocations if not careful
- Requires thoughtful caching to keep UI snappy

**Best for:** extensibility, correctness, long-term maintainability.

---

### Option B — Event-Sourced State + Render Pipeline
**Idea:** Store a log of actions (“apply operator X”, “change range clamp”, “lock-in”) and rebuild derived state when needed.

**Pros**
- Perfect history and auditing (great for “freeze” and revert)
- Undo/redo is trivial
- Great for collaboration later

**Cons**
- More complex mental model
- Requires rebuild logic and careful performance tuning

**Best for:** deep non-destructive workflows, future-proofing “history timelines”.

---

### Option C — Graph-Based Processing (node graph)
**Idea:** Operators and modifiers are nodes in a DAG with explicit connections.

**Pros**
- Maximum flexibility; power users can build custom chains
- Visual debugging of MIDI flow
- Easy to add parallel processing (e.g., multiple voicing candidates)

**Cons**
- Overkill for v1; UI complexity explodes
- Harder to keep “fast and simple” UX
- More QA surface area

**Best for:** v2+ “advanced mode” if your market demands it.

---

## 9) Practical Recommendations (what to build first)

### v1 “Core that wins”
1. MIDI snapshot + chord detection (reliable)
2. Chord block bank + tags + reorder
3. Operator chain framework + 5–8 essential operators:
   - inversion, spread, clamp, voice-leading, strum, arp, humanize, note chance
4. Bank modifier range system + redetect output metadata
5. Mapping engine for triggering blocks
6. Keyswitch lane merge

### Defer (until core is solid)
- Audio-to-chord detection (high effort + edge cases)
- Guitar tab/fingering generation (do later; requires robust voicing-to-fretboard heuristics)
- Full harmonic reharmonization engines

---

## 10) Appendix — MIDI Threading & Safety Notes (JUCE)

- Keep real-time audio thread safe:
  - No allocations in `processBlock` where possible
  - Pre-allocate event buffers
  - Move heavy detection / audio-to-chord analysis off the audio thread
- Separate capture state vs playback state:
  - Capture state can be updated with lock-free structures or guarded minimal locks
  - UI reads cached copies of chord bank state

---

**End of draft.**
