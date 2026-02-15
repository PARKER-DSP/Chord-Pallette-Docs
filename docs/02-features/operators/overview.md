---
audience: product
status: canonical
owner: product
last_reviewed: 2026-02-15
---

# Operator Catalog

Complete list of operators available in ChordPallette, organized by category.

---

## Voicing Operators

Transforms that change how notes are arranged within a chord.

- **Invert** – Move root to a different position (1st inversion, 2nd inversion, etc.)
- **Drop2** – Remove 2nd note from top and move to bottom
- **Drop3** – Remove 3rd note from top and move to bottom
- **Spread / Close** – Expand or compress chord spacing
- **Top-Note Lock** – Keep highest note fixed while revoicing others
- **Bass Lock** – Keep lowest note fixed while revoicing upper voices
- **Re-Voice** – Find alternative voicing in target range

---

## Range & Output Operators

Constrains and optimizes voicings for specific instruments.

- **Clamp Range** – Fit all notes within user-defined playing range
- **Only Root in Sub-Bass** – Restrict bass register to root note only
- **Octave Management** – Shift individual notes up/down by octave
- **Safe-Note Bracket** – Automatically fix out-of-range notes

---

## Harmonic Operators

Advanced transformations that alter chord quality or function.

- **Borrowed Chord** – Apply chord from another mode/key
- **Modal Interchange** – Switch between parallel modes
- **Secondary Dominant** (optional) – Add temporary V7 resolution flavor
- **Reharmonize** (optional) – Suggest rich alternatives

---

## Performance Operators

Generators that create rhythmic or melodic variations.

- **Strum** – Play notes sequentially instead of simultaneously
- **Arpeggiate** – Break chord into repeated patterns
- **Rhythm Pattern** – Apply rhythmic variation (syncopation, swing)
- **Humanize** – Add subtle timing/velocity variation
- **Velocity Random** – Randomize note velocities
- **Note Chance** – Make individual notes probabilistic (0-100%)
- **Melodic Play** – Generate melodies within the chord

---

## Legato & Expression Operators

Controls how notes connect and respond to input.

- **Legato Rules** – Smooth note transitions without retriggering
- **Voice-Leading to Previous** – Auto-connect smoothly from last chord
- **Latch/Hold** – Sustain note beyond trigger
- **Retrigger** – Allow simultaneous notes or enforce sequential

---

## Extensibility

The operator system is designed to grow:
- **Phase 3**: Add AI-assisted re-voicing
- **Phase 4**: Genre-specific preset operator chains
- **Future**: User custom operators, third-party operator marketplace

See [Operator System](operator-system.md) for architecture and design principles.
