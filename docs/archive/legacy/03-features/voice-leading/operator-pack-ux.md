> **Archived (non-authoritative):** This file is retained for historical reference only. Use canonical pages from the main navigation for current guidance.

# ChordPallette — Voice Leading Operator Pack UX & System Design
_Follow-up to MIDI Flow & Engine Spec_

---

# 1. Executive Summary

The **Voice Leading Operator Pack** transforms ChordPallette from a static chord trigger tool into a dynamic harmonic performance engine.

Voice leading is implemented as:

- A **non-destructive operator**
- Usable at both **Chord Block level** and **Chord Bank level**
- Style-driven
- Real-time responsive
- Batch-applicable across large chord collections
- Fully previewable before committing

The goal:  
Make harmonic motion feel smooth, intentional, and expressive — without requiring theory knowledge.

---

# 2. Core UX Philosophy

Voice leading should feel:

- Instant
- Musical
- Invisible
- Reversible
- Playable
- Fun to experiment with

It should never feel like:

- Configuration-heavy
- Academic
- Technical
- Destructive

---

# 3. Where Voice Leading Lives

Voice leading can exist in three scopes:

### A. Per-Chord Block (Local Operator)
Applies only when that block transitions from the previous block.

Use case:
- Specific reharmonization
- Intentional color change
- Special effect chord

---

### B. Per-Bank (Global Style Mode) — Recommended Default

Applies to transitions between ALL blocks in a chord bank.

Use case:
- Entire progression smoothing
- Live performance
- Genre-specific styling

This is the most powerful and intuitive mode.

---

### C. Trigger-Based (Performance Mode)

Applies dynamically depending on trigger order during live performance.

Use case:
- Improvised progression triggering
- Keyboard performance
- MIDI splits + dynamic movement

---

# 4. Frictionless User Experience Design

## 4.1 Entry Point

In the Chord Bank view:

Add a visible but simple toggle:

> [ Voice Leading: OFF ▼ ]

Clicking opens a minimal popover:

- OFF
- Smooth
- Cinematic
- Neo-Soul
- Classical
- EDM Stack
- Custom

Selecting a style activates global voice leading instantly.

No parameter wall.

---

## 4.2 Real-Time Preview

As user triggers blocks:

- Notes animate moving to nearest tones
- Small visual lines show motion paths
- Common tones glow softly
- Jump distance visual indicator (optional minimal arc)

This creates satisfying visual feedback.

---

## 4.3 Advanced Panel (Optional Expansion)

For power users:

> Voice Leading Settings (expandable panel)

Controls:
- Movement tolerance (tight / moderate / free)
- Preserve bass (toggle)
- Preserve top note (toggle)
- Allow voice crossing (toggle)
- Max jump size slider
- Weight bass / top / inner voices

Default state: collapsed.

---

# 5. How It Works Across Large Banks

Voice leading operates on transitions:

Block A → Block B

When active globally:

- Engine analyzes ALL sequential relationships
- Each block stores:
  - BaseChord
  - OperatorChain
  - VoiceLeadingStyleRef

But the actual voicing is recalculated dynamically during playback.

No permanent mutation unless user locks-in.

---

# 6. Handling Large Collections of Chord Blocks

## Strategy: Lazy Evaluation + Caching

When bank voice leading style is enabled:

1. Do not precompute all transitions immediately.
2. Compute transitions on-demand when:
   - Playback occurs
   - User scrubs blocks
   - MIDI export requested

3. Cache transition results:
   Key = (PreviousBlockID + CurrentBlockID + StyleID + SettingsHash)

This keeps performance fast even with large banks.

---

# 7. Style-Based Voice Leading Profiles

Each style defines:

- Movement weight
- Range preference
- Voice crossing tolerance
- Bass behavior
- Density behavior
- Spread bias
- Cluster tolerance

Example:

---

## Smooth (Default)

- Minimize total movement
- Preserve common tones
- Moderate bass stability
- Avoid large jumps

Use case: general songwriting

---

## Cinematic

- Wider spreads allowed
- Prioritize emotional bass shifts
- Allow large leaps in inner voices
- Keep top note lyrical

Use case: film / worship / ambient

---

## Neo-Soul

- Prefer close upper clusters
- Preserve top melody note
- Bass minimal movement
- Avoid open fifth stacks

Use case: R&B / soul / jazz pop

---

## Classical

- Strict voice crossing rules
- Stepwise movement preferred
- Penalize parallel fifths (optional advanced rule)
- Controlled bass movement

Use case: structured harmonic writing

---

## EDM Stack

- Maintain wide supersaw-friendly spacing
- Stable bass anchor
- Large upper voice motion allowed
- Density bias toward stacked intervals

Use case: electronic genres

---

# 8. Can You Apply Voice Leading to a Single Block?

Yes.

Per-block override system:

Each ChordBlock contains:

```
VoiceLeadingMode:
  - InheritFromBank
  - OverrideStyle
  - Disabled
```

User can right-click a block:

> Override Voice Leading → Choose Style

That block transition uses override when triggered.

---

# 9. Batch Operations

User can:

- Select multiple blocks
- Apply voice leading style
- Preview in place
- Accept or revert

Or:

- “Optimize Entire Bank” button

Which:

- Simulates sequential order
- Applies style
- Shows visual diff
- Offers:
  - Apply non-destructively
  - Bake to new blocks
  - Replace base chords

---

# 10. Lock-In Behavior

If user clicks:

> Freeze Voice Leading

System:

1. Computes final derived voicings
2. Replaces BaseChord with new voicing
3. Clears voice leading operator
4. Preserves original in history

Result:

Block becomes “fresh” and no longer dependent on transition logic.

---

# 11. Real-Time Performance Mode

In live trigger mode:

Voice leading uses:

- Last played output chord
- Not bank order

This allows improvisation.

If player jumps from Block 1 → Block 7:

System calculates best movement relative to actual last chord played.

---

# 12. Export Behavior

When exporting MIDI:

User chooses:

- Export base chords
- Export voice-led result
- Export frozen result

This keeps workflow flexible.

---

# 13. Frictionless UX Checklist

Voice leading must:

- Work instantly when toggled
- Require zero parameter setup
- Visually indicate movement
- Never destroy original chord
- Be reversible
- Scale to 100+ chord blocks
- Not add noticeable CPU load

---

# 14. Architecture Integration Strategy

VoiceLeadingOperator should:

- Be a first-class operator
- Have access to previous chord context
- Be deterministic
- Produce voicing result object
- Not mutate BaseChord

System must support:

```
DerivedChord = ApplyOperators(BaseChord)
VoiceLedChord = ApplyVoiceLeading(DerivedChord, PreviousOutputChord)
OutputChord = ApplyBankModifiers(VoiceLedChord)
```

---

# 15. Product Opportunity

Voice leading can be:

- Included in core
- Expanded as premium style packs
- Artist signature style packs
- AI-assisted adaptive style in v2

Marketable as:

“Smart chord transitions”  
“Your progressions finally flow.”  
“Every chord connects.”

---

# 16. Final Recommendation

For v1:

Implement:

- Global bank voice leading
- 3 styles: Smooth, Cinematic, Neo-Soul
- Per-block override
- Freeze functionality
- On-demand caching

Defer:

- Parallel fifth detection
- Advanced harmonic rule systems
- Graph-based voice leading chains

---

End of document.
