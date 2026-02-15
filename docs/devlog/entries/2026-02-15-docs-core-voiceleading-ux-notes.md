---
audience: [dev, product, ux]
status: archived
owner: parker

created_at_utc: "2026-02-15T12:00:00Z"
created_at_cst: "2026-02-15T06:00:00-06:00"

last_reviewed: 2026-02-15
---

# Devlog — Docs + Core + Voice Leading UX Notes (Meeting Minutes)

## Meeting header

**Date (UTC):** 2026-02-15  
**Date (CST):** 2026-02-15

**Meeting start (UTC):** 2026-02-15T00:00:00Z *(time not recorded)*  
**Meeting start (CST):** 2026-02-14T18:00:00-06:00 *(time not recorded)*

**Meeting end (UTC):** 2026-02-15T00:00:00Z *(time not recorded)*  
**Meeting end (CST):** 2026-02-14T18:00:00-06:00 *(time not recorded)*

**Participants:** Parker (User), ChordPallette Architect (Assistant)  
**Purpose:** Clarify docs roadmap, core/JUCE boundary, serialization, voice-leading behavior/UX, and mode/operator design ideas.

---

## Context
- Goal: Flesh out the documentation project into a robust starting point before core development.
- Secondary goal: Align on tricky voice-leading behavior and UX concepts early so architecture + persistence contracts don’t drift later.

---

## Discussion notes

### 1) Docs project direction (docs-first before core)
- We affirmed the plan to flesh out documentation before core development.
- The missing “robust product” doc areas were identified as: requirements discipline, decision history, toolchain, CI, testing/profiling strategy, persistence/versioning contracts, and UX workflow specs.

**Why it matters:** If the docs don’t define boundaries and contracts now, implementation will drift and later changes will break user trust (especially around saved projects/presets).

---

### 2) Serialization (plain-language alignment)
- Serialization = saving the plugin’s state so it can be restored exactly later (DAW projects + presets/libraries).
- “Good serialization” must be:
  - **Complete** (restores what the user expects)
  - **Stable** (works across versions)
  - **Consistent** (loads back into the same musical result)
- Versioning of saved data is a contract, not a convenience.

**Why it matters:** “My session recalled wrong” is a top-tier trust breaker for music tools.

---

### 3) Rust core (benefits and costs)
- Potential benefits: memory safety (no GC), strong testing culture/tooling, clean portable “JUCE-free core” boundary, safer concurrency.
- Costs: FFI/build complexity, cross-language debugging friction, platform packaging nuance; Rust does not automatically guarantee RT safety.
- A viable compromise is Rust core + thin C++ JUCE wrapper, but C++ core may ship faster.

**Why it matters:** Language choice is a workflow/productivity decision as much as a technical one.

---

### 4) CI (Continuous Integration) alignment
- CI = automatic checks on PRs/merges (docs build, link checks, linting, tests).
- Docs CI should ensure the documentation is always publishable (mkdocs build `--strict`, link validation, diagram checks).
- Later CI can expand to multi-platform builds, unit tests, performance/RT checks.

**Why it matters:** CI prevents slow “docs drift” and catches breakage immediately.

---

### 5) Docs co-located with JUCE repo + automation
- Confirmed docs can live inside the plugin repository to reduce drift.
- Automation strategy:
  - PR: validate docs build/links/quality
  - main: publish docs (e.g., GitHub Pages)
  - optional: generate deterministic docs artifacts (indexes, operator tables, ADR index) into `*.generated.md` only

**Guardrail:** Avoid auto-editing hand-written docs. Generate only clearly marked outputs.

**Why it matters:** Automation should increase reliability without creating noisy or misleading diffs.

---

### 6) JUCE ↔ Core interaction model (high level)
- **Core** = musical brain (chords, operators, voice leading, serialization); no JUCE, portable, testable.
- **JUCE plugin** = host + UI shell (MIDI IO, parameters/automation, timing info, rendering).
- Audio thread: JUCE gathers inputs → calls core → outputs MIDI events.
- UI thread: reads snapshots; sends commands; does not mutate audio-thread internals directly.
- Serialization: host asks plugin; plugin delegates to core to serialize/deserialize musical state.

**Why it matters:** A crisp boundary makes behavior testable and prevents RT-unsafe UI coupling.

---

### 7) Voice leading ambiguity in sequence 1→2→3→2
**Issue:** Chord block 2 can end up with different “best” voicings depending on context:
- entering from 1 (1→2)
- entering from 3 (3→2)

**Proposed model:**
- **Anchor voicing** (“home” identity)
- **Realized voicing** (context-specific realization)
- **Memory / last-played voicing** (ephemeral performance state)
- Scoring approach: motion + constraints + anchor pull + memory pull

**Policy:** Do not retroactively rewrite past realized voicings. New realizations affect future transitions only.

**Why it matters:** This keeps the instrument predictable in live play and avoids “time travel” surprises.

---

### 8) Worship Pads voice-leading mode (example rules)
We outlined a scoring-based selection strategy emphasizing:
- preserve common tones
- minimize motion
- stable bass
- avoid low mud (spacing constraints below ~C4)
- open spread / airy register
- gentle approved colors (add2/sus/6/9)
- keep top “shimmer” stable

**RT approach:** precompute bounded candidate sets off-thread; audio thread selects among candidates deterministically.

**Why it matters:** The mode needs a consistent “pad feel” without sacrificing realtime safety.

---

### 9) Additional genre/mode rule sets (10)
Plain-English rule sets were proposed for:
- Classical chorale
- Jazz comping
- Neo-soul / R&B
- EDM / pop
- Cinematic / trailer
- Gospel / church keys
- Lo-fi / chillhop
- Metal / power chord
- Strummed guitar realism
- Modal / ambient

**Why it matters:** “Modes” can be implemented as different constraint/weight profiles rather than separate engines.

---

### 10) Freeze + variants UX problem (and solution direction)
**Problem:** If blocks can yield many context-dependent voicings, “freeze” can imply storing too many realizations.

**Solution direction: separate layers**
- Anchor chord (identity)
- Frozen recipe (operators/modifiers locked)
- Realized voicing (context result)
- Optional saved variants (finite, user-curated)
- Last played voicing (ephemeral unless captured)

**Two freeze concepts**
1) **Freeze Recipe** (locks operators; still allows contextual voice leading)
2) **Bake Voicings** (commits realized notes into stable, editable data)

**Editing clarity**
- Piano roll must indicate editing layer: Anchor vs Locked/Baked vs Variant
- “Capture Last Played” is the key conversion from discovery → stable artifact

**Why it matters:** “Freeze locks the recipe; Capture locks the result” keeps users confident and reduces UI clutter.

---

### 11) Voice leading as chord-block operator vs bank operator
**Idea:** Make voice leading a chord-block operator rather than a bank operator.

**Pros**
- per-chord musical intent (destination vs passing)
- mixed styles in one bank
- better explainability
- aligns with non-destructive operator model

**Cons**
- voice leading is transitional; semantics must be explicit (incoming/outgoing)
- local choices can fight global smoothness
- more cache granularity and potential UX complexity
- global optimization becomes more complex (but feasible)

**Compromise direction**
- Bank-level defaults/safety rails
- Optional per-block override

**Why it matters:** This impacts both user mental model and caching/RT strategy.

---

### 12) Bank-level playability operators + History capture workflow (new direction)
**Idea:** Keep performance “feel controls” as bank operators:
- **Up / Down / Steady / Original**
These bias whatever algorithm mode is active, improving playability without per-block UI complexity.

**Discovery → Curation workflow**
- A **History panel** records realized chords/voicings/progressions discovered during play.
- Users can drag history blocks into the bank as new **flattened operatorless** chord blocks.

**Flatten types**
- Flatten Harmony (save chord identity)
- Flatten Voicing (save exact notes)

**RT note:** history should be built from lightweight audio-thread events into a ring buffer and processed on the UI thread.

**Why it matters:** This provides an intuitive loop: Explore → Discover → Capture → Curate, while preserving realtime safety.

---

## Decisions / current alignment
- Maintain a strict **core vs JUCE** boundary (snapshots + commands).
- Keep audio-thread work bounded; do heavy compute off-thread via caches.
- Avoid infinite voicing storage; prefer **capture/bake** user actions.
- Bank-level playability overlays (Up/Down/Steady/Original) look promising for performance UX.

---

## Open questions
- Define “Original”: anchor voicing/register identity vs chord spelling vs both.
- Final placement strategy for voice leading: bank default + per-block override vs purely block-based.
- Capture granularity: flatten harmony vs flatten voicing vs flatten progression.
- Language/toolchain decision: C++ core vs Rust core + JUCE wrapper.

---

## Action items
1) Write **Voice Leading Semantics** doc: anchor vs realized vs memory; no retroactive rewriting.
2) Write **Freeze/Capture/Bake UX spec**: explicit edit layers in piano roll; variants drawer concept.
3) Write **Bank Playability Overlays** spec: Up/Down/Steady/Original as bias terms with intensity control.
4) Write **History + Drag-to-Bank** spec: flatten harmony/voicing/progression and persistence implications.
5) Write **RT budgets + caching strategy** doc: bounded candidates, cache keys, invalidation strategy.
6) Write **CI + toolchain** docs: docs build checks now; expand to core/plugin later.

---

## Promotion links (optional)
- **Promoted to spec:** (TBD)
- **Promoted to ADR:** (TBD)

---
