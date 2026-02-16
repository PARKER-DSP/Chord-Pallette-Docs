# Devlog — Voice-leading UX + Utility Plugin Ladder + Export QoL
**Date:** 2026-02-15  
**Project:** ChordPallette  
**Author:** (compiled from design/research discussion)

---

## TL;DR
We identified repeat pain points in existing harmony/MIDI tools (routing confusion, export mismatches, register drift, “global/group” controls breaking local edits, timing/stuck notes, and compatibility friction). ChordPallette can win by being **predictable**, **range-aware**, **WYSIWYG export-correct**, and **non-destructive** with clear control scope.

We also designed:
- A **Dream Feature**: **Register Drift Target Lane** (right-side vertical finger lane) that visualizes current voicing drift and pulls toward a user-defined target **weighted**, not abruptly.
- A **Dream UX**: **Hold-to-Export Length Picker** that exports/drag-drops MIDI clips at an exact DAW-synced length and with **rich naming/metadata** so clips aren’t anonymous.
- A **Plugin-first product ladder** of **standalone MIDI utilities** that receive MIDI from the DAW and write the same **ChordBlock schema**, building trust and adoption before the full “Studio” product.
- A **usage + quality telemetry** plan that is high-signal and low-creepiness (derived metrics, funnels, undo-as-quality).

---

## 1) Competitive pain points (observed patterns → product opportunities)

### 1.1 Routing / “no sound” friction
**Pattern:** Users insert a MIDI FX but don’t correctly route to an instrument, don’t arm/monitor correctly, or misunderstand host-specific MIDI plumbing.  
**Opportunity:** A routing “trust layer” with:
- signal-flow HUD (Input → Chord → Output → Target Instrument)
- host templates / guided setup
- clear plugin mode labels (MIDI FX vs instrument wrapper)

### 1.2 Export/drag-drop mismatch
**Pattern:** Exported MIDI sometimes doesn’t match what users heard (extra notes, wrong lengths, messy capture).  
**Opportunity:** **WYSIWYG export contract** + export inspector + regression tests per-host.

### 1.3 Register drift / out-of-range voicings
**Pattern:** Adaptive voicing can creep upward or generate out-of-range voicings over longer progressions.  
**Opportunity:** Make register intent visible + controllable:
- range-aware, instrument-aware spacing rules
- explicit “drift/anchor” models
- stable style profiles

### 1.4 Global/group controls break local edits
**Pattern:** “Voice grouping” / global switches can block expected edits or make controls feel broken.  
**Opportunity:** Your non-destructive model solves this if surfaced properly:
- every control shows scope: Bank / Block / Selection / Window
- local operators remain local; global overlays are just biases
- **Freeze/Commit** makes derived results durable

### 1.5 Timing/stuck notes and host quirks
**Pattern:** MIDI generators can cause stuck notes, timing oddities, latency compensation surprises.  
**Opportunity:** Make “boring reliability” a headline feature:
- deterministic bounded work on audio thread
- allocation-free MIDI generation
- stuck-note watchdog + panic
- “export end = clean note-offs” rule

### 1.6 Compatibility / authorization / OS churn
**Pattern:** Users experience breakage after OS/DAW updates and interpret it as vendor disrespect.  
**Opportunity:** Compatibility discipline:
- schema versioning + migration tests
- stable import/export
- clear support matrix
- fast hotfix pipeline

---

## 2) Opportunity pillars we can credibly own
1. **Trustworthy voicing:** range-aware + instrument-aware + no drift surprises  
2. **WYSIWYG MIDI export:** what you hear is what you drag  
3. **Routing that teaches itself:** HUD + per-host templates  
4. **Non-destructive editing with explicit scope:** operators local, overlays visible, Freeze/Commit  
5. **RT-safe reliability:** bounded, deterministic, allocation-free audio-thread behavior  
6. **Compatibility discipline:** schema/versions/packs/presets that don’t rot

---

## 3) Dream Feature — Register Drift Target Lane (Vertical Finger Lane)

### 3.1 Summary
A right-side vertical lane visualizes and controls voicing “register drift”:
- **Current dot:** current register position of realized voicing
- **Target handle:** user-defined target register
- Engine follows target **weighted** (bias), not by teleporting

**Layout:**
- Left: ChordBlock Bank
- Right: Register Drift Target Lane (finger lane)

### 3.2 Drift metric (canonical)
Recommended metric: **voicing centroid**  
`centroidMidi = average(midiNoteNumber across active voices)`  
Drift: `drift = centroidMidi - targetCentroidMidi`

(Advanced options later: weighted centroid, median pitch.)

### 3.3 Interactions
- Click+hold/drag lane target → updates target register
- Double tap lane → set target to current (zero drift)
- Long press → toggle anchor lock (re-anchor at current)
- Optional: two-finger pinch → adjust allowed band (min/max)

### 3.4 Engine behavior (soft constraint)
Treat lane as a **soft constraint penalty** in the voice-leading cost:
- `registerPenalty = wTarget * max(0, abs(centroid(candidate)-target) - tolerance)`
- Hard constraints always win (instrument range, mud spacing rules, etc.)

### 3.5 Operator pipeline integration
Implement as `RegisterTargetOperator`:
- Input: BaseChord + previous realized voicing snapshot
- Params: target, followStrength, tolerance, range band, anchor mode
- Output: DerivedChordState (chosen voicing + explainability metadata)

**Freeze/Commit:** creates new BaseChord from current derived state.

### 3.6 Explainability
One-line “why”:
- Centroid, Target, Drift
- “Biasing down (Follow 35%)”
- Constraints hit (e.g., “low-range spacing clamp”)

---

## 4) Usage data collection opportunities (privacy-forward)

### 4.1 High-signal product analytics
- feature adoption: voice profiles, range controls, drift lane, Freeze/Commit, export
- funnels: load → MIDI in detected → chord out → audible → export success → save preset
- defaults: what users change immediately vs never touch

### 4.2 Voice-leading quality telemetry (derived, not raw notes)
Aggregate (sampled):
- total movement, max leap, common-tone count
- voice crossings, spacing violations, constraint pressure
- drift magnitude, clamp hits
- candidate search stats (count/pruned/chosen rank)

### 4.3 “Undo as a label”
User corrections are a gold dataset:
- undo right after voicing change
- profile switched immediately after playback
- manual inversion override
- Freeze/Commit as positive signal

### 4.4 Reliability/perf diagnostics
- max CPU per block, worst-case candidate evaluation time
- allocation detection flags (should be 0)
- stuck-note recoveries + panic usage
- environment: host, plugin format, OS, buffer size, sample rate

### 4.5 Privacy levels
- Level 0: none
- Level 1: crash/perf only
- Level 2: usage + derived musical metrics
- Level 3: user-generated support bundle export (explicit share)

---

## 5) “Dedup during capture but allow block duplication” — uniqueness semantics
**Concept:** Dedupe in the **bank** (unique chord entities), not in the **timeline** (blocks can repeat).

### 5.1 Why it matters
Users want a clean bank while jamming, but also need repeated blocks in arrangement.

### 5.2 Uniqueness keys (explicit to avoid collapsing musically distinct voicings)
- **Chord class:** pitch classes + root (aggressive dedupe)
- **Exact voicing:** sorted MIDI pitches (strict dedupe)
- **Voicing family:** chord class + register bucket
- **Tolerance-based:** voices within ±N semitones considered duplicate

### 5.3 UX actions
- Duplicate block → new reference to same chord entity
- Fork (Make independent) → create new BaseChord (Freeze/Commit)

---

## 6) Plugin-first ladder (MIDI comes from DAW)
Goal: ship thin, useful MIDI utilities that **receive DAW MIDI**, transform/capture, and output MIDI — all writing the same ChordBlock schema to build buy-in.

### 6.1 Standalone utility plugins (DAW workflow friendly)
1. **ChordBlock Recorder (Dedup Capture)**
   - Listens to MIDI chords → captures blocks + dedup bank → drag/export
2. **Guitar Voicing Mapper (Keyboard → Guitar)**
   - Maps incoming chord MIDI to fretboard-constrained shapes (tuning/capo/fret region)
3. **Voice-Leading Smoother (Clip Doctor)**
   - Fixes jumpy inversions and continuity for MIDI packs/clips (Smooth ↔ Expressive)
4. **Range & Mud Guard**
   - Enforces instrument-aware range + spacing constraints (clarity knob)
5. **Tension Budgeter**
   - Adds tasteful extensions/alterations within a “spice budget” and profile constraints
6. **Melody Protector**
   - Identifies melody (channel/range/highest) and revoices harmony underneath it
7. **Performance Render**
   - Converts block chords to strum/roll/broken-chord patterns deterministically

### 6.2 Why this ladder works
- Every tool is immediately useful inside a DAW.
- Each produces reusable artifacts in the same schema.
- The final “Studio” product is a unification of trusted workflows, not a new learning cliff.

---

## 7) Dream UX — Hold-to-Export Length Picker + Rich Clip Info

### 7.1 Problem
Dragging MIDI into a DAW often requires manual clip resizing and yields unnamed/anonymous clips.

### 7.2 Interaction
On any block/selection:
1. **Click + hold** → overlay appears
2. Overlay shows **DAW-synced export lengths** (subdivisions + bars)
3. Select length while holding → release to confirm → drag produces clip of exact length

### 7.3 Options
- 1/16, 1/8, 1/4, 1/2, 1/1
- 1 bar, 2 bars, 3 bars, 4 bars, 8 bars
- To next bar / end of selection / next chord change (multi-block)

### 7.4 Guarantee
Exported MIDI clip length is exactly the chosen duration.
- Default: “Hold notes to end” for chord blocks
- Always ensure clean note-offs at clip end

### 7.5 Rich naming + embedded metadata
Generate export names and metadata so clips are self-describing.

**Filename template example:**
`{app} - {chords} - {len} - {bpm}bpm - {ts} - {profile}.mid`

**MIDI meta events:**
- Track name: `ChordPallette | Am9 | 2 bars | 120bpm | 4/4`
- Marker events at chord boundaries
- Text events for operator summaries (VL profile, range profile, drift target, etc.)

---

## 8) Immediate documentation checklist (docs-first)
Before coding major features, document:
- ChordBlock schema (IDs, naming, metadata, versioning)
- Uniqueness key modes + dedupe behavior
- Export contract (length rules, note-off rules, metadata)
- Operator scoping rules (Bank/Block/Selection/Window)
- Drift lane metric + behavior (penalty term, tolerance, anchor modes)
- RT safety rules (no alloc on audio thread, bounded compute, deterministic)
- Test plan outline (golden MIDI fixtures for export/voicing; regression per host)

---

## 9) Next implementation steps (practical)
1. **Core schema MVP**
   - chord entity, block references, operator chain serialization
2. **Export subsystem**
   - length picker logic (host-synced math)
   - WYSIWYG MIDI rendering
   - naming + metadata embedding
3. **ChordBlock Recorder v0**
   - dedupe keys + bank/timeline UI
4. **Voice-leading + drift lane prototype**
   - centroid tracking + penalty term
   - explainability metadata
5. **Testing harness**
   - golden fixtures for export lengths
   - property tests for constraints (range spacing, note-offs, determinism)

---

## Appendix — quick diagrams

### Dataflow: MIDI in → capture/transform → export
```mermaid
flowchart LR
  DAW[MIDI from DAW] --> IN[Input Parser]
  IN --> CORE[Core Engine (portable, RT-safe)]
  CORE --> OUT[MIDI Output]
  CORE --> CAP[Capture Buffer + Dedupe]
  CAP --> BANK[Chord Entity Bank]
  CAP --> TL[ChordBlock Timeline]
  TL --> EXP[Export Builder (length + metadata)]
  EXP --> DRAG[Drag/Drop MIDI file]
  DRAG --> DAW2[DAW Clip: named + correct length]
```

### Operator chain integration (concept)
```mermaid
flowchart TB
  BASE[BaseChord (immutable)] --> OP1[Operator A]
  OP1 --> OP2[RegisterTargetOperator]
  OP2 --> OP3[Range/Mud Guard]
  OP3 --> DER[DerivedChordState]
  DER -->|Freeze/Commit| BASE2[New BaseChord]
```

---

**End of devlog.**
