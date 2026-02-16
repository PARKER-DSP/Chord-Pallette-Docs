---
audience: product
status: canonical
owner: product
last_reviewed: 2026-02-16
---

# Voice Leading Operator Pack — UX & System Design

> This document details how voice leading will work as a user-facing feature, including interaction design, architectural strategy, and implementation recommendations.

---

## Executive Summary

The **Voice Leading Operator Pack** transforms ChordPallette from a static chord trigger tool into a dynamic harmonic performance engine.

Voice leading is implemented as:
- A **non-destructive operator**
- Usable at **Chord Block level** and **Chord Bank level**
- Style-driven (Smooth, Cinematic, Neo-Soul, Classical, EDM Stack)
- Real-time responsive
- Batch-applicable across large chord collections
- Fully previewable before committing

**Goal:** Make harmonic motion feel smooth, intentional, and expressive — without requiring music theory knowledge.

## Related Contracts

- [Playability Overlays Spec](../../01-developer/architecture/playability-overlays-spec.md)
- [Threading and Lifecycle](../../01-developer/architecture/threading-and-lifecycle.md)
- [Realtime Safety](../../01-developer/architecture/realtime-safety.md)

---

## Core UX Philosophy

Voice leading should feel:

✅ Instant  
✅ Musical  
✅ Invisible (not overwhelming)  
✅ Reversible  
✅ Playable  
✅ Fun to experiment with  

It should NOT feel:

❌ Configuration-heavy  
❌ Academic  
❌ Technical  
❌ Destructive  

---

## Where Voice Leading Lives

Voice leading operates across three scopes:

### A. Per-Chord Block (Local Operator)

Applies voice leading only to transitions *from* this specific block.

**Use case:**
- Special reharmonization on one chord
- Intentional color change
- Effect chord with unique movement

**User interaction:**
```
Right-click chord block → "Override Voice Leading" → Select style
```

---

### B. Per-Bank (Global Style Mode) — *Recommended Default*

Applies voice leading to ALL transitions in the chord bank.

**Use case:**
- Smoothing entire progression
- Live performance consistency
- Genre-specific styling

**User interaction:**
```
Bank Header: [ Voice Leading: OFF ▼ ]
Dropdown: OFF | Smooth | Cinematic | Neo-Soul | Classical | EDM Stack | Custom
```

This is the most powerful and intuitive mode.

---

### C. Trigger-Based (Live Performance Mode)

Applies voice leading dynamically based on *actual* trigger order during keyboard play.

**Use case:**
- Improvised progression triggering
- Non-sequential chord jumping
- MIDI splits + dynamic movement

**System behavior:**
- Uses "last played output chord" as reference, not bank order
- If player jumps Block 1 → Block 7, calculates movement from Block 1's output

---

## Frictionless UX Design

### Entry Point

In Chord Bank view:

```
Voice Leading: [ OFF ▼ ]
```

Clicking opens minimal popover:

```
☐ OFF
☐ Smooth (default)
☐ Cinematic
☐ Neo-Soul
☐ Classical
☐ EDM Stack
☐ Custom...
```

Instantly activates global voice leading. No parameter wall.

### Real-Time Preview

As user triggers chord blocks:
- Notes animate moving to nearest destinations
- Small visual lines show motion paths
- Common tones glow subtly
- Jump distance indicator (optional, minimal arc)

Provides satisfying visual feedback.

### Advanced Panel (Optional, Collapsed by Default)

For power users who want fine-tuning:

```
Voice Leading Settings (expandable)

Movement tolerance: [Tight ─────●──── Free]
☐ Preserve bass
☐ Preserve top note
☐ Allow voice crossing
Max jump size: [──────●────── ]
Voice weighting:
  Bass: [──●──]  Top: [──●──]  Inner: [──●──]
```

---

## Style Profiles

Each style defines movement behavior:

| Style | Movement | Bass Behavior | Spread | Use Case |
|-------|----------|---------------|--------|----------|
| **Smooth** | Minimal, stepwise | Moderate stability | Compact | Songwriting, general |
| **Cinematic** | Wide, emotional | Strong shifts | Variable | Film, worship, ambient |
| **Neo-Soul** | Controlled, clustered | Very stable | Close uppers | R&B, soul, jazz-pop |
| **Classical** | Stepwise preferred | Traditional | Structured | Formal harmony, education |
| **EDM Stack** | Large inner jumps | Anchored| Wide | Electronic, synth-heavy |

---

## Handling Large Chord Banks

**Strategy: Lazy Evaluation + Caching**

When bank voice leading is active:

1. **Do NOT precompute all transitions upfront** – expensive for large banks
2. **Compute on-demand** when:
   - Playback occurs
   - User scrubs blocks
   - MIDI export requested

3. **Cache transition results** with key:
   ```
   (BlockID_A + BlockID_B + StyleID + SettingsHash) → VoicedResult
   ```

This keeps performance fast even with 100+ chord blocks.

---

## Per-Block Override

Each ChordBlock can override bank-level style:

```
VoiceLeadingMode:
  - InheritFromBank (default)
  - OverrideStyle: [style name]
  - Disabled
```

**User action:**
```
Right-click chord block → "Override Voice Leading" → Choose style
```

That block's transition uses the override when triggered.

---

## Batch Operations

### Visual Diff & Preview

Select multiple blocks → "Optimize Voice Leading"

System:
- Simulates sequential order
- Applies style
- Shows visual diff
- User chooses:
  - ✅ Apply non-destructively
  - ✅ Bake to new blocks
  - ✅ Replace base chords
  - ❌ Cancel

---

## Lock-In (Freeze) Behavior

User clicks: **"Freeze Voice Leading"**

System:
1. Computes final derived voicings
2. Replaces BaseChord with new voicing
3. Clears voice leading operator
4. Preserves original in history

Result: Block becomes "fresh" and independent; no longer depends on transition predecessor.

---

## Export Options

When exporting to MIDI:

```
Export as:
☐ Base chords (original voicings)
☐ Voice-led result (processed)
☐ Frozen result (locked-in voicings)
```

Keeps workflow flexible.

---

## Performance Checklist

Voice leading must:

- ✅ Work instantly when toggled
- ✅ Require zero parameter setup (defaults work great)
- ✅ Visually indicate movement
- ✅ Never destroy original chord
- ✅ Be reversible
- ✅ Scale to 100+ chord blocks
- ✅ Add negligible CPU load
- ✅ Feel musical, not gimmicky

---

## Architecture Integration

`VoiceLeadingOperator` should:

- Be a first-class operator in the chain
- Have access to previous output chord context
- Be deterministic (same input = same output)
- Produce voicing result object
- Never mutate BaseChord

**Processing pipeline:**

```
BaseChord
   ↓ [Apply standard operators]
DerivedChord
   ↓ [Apply voice leading]
VoiceLedChord
   ↓ [Apply bank modifiers]
OutputChord (to MIDI)
```

---

## Product Opportunity

Voice leading is marketable as a differentiator:

> "Smart chord transitions"  
> "Your progressions finally flow."  
> "Every chord connects."

Can also be expanded:
- Premium style packs
- Artist signature styles
- AI-assisted adaptive styles (v2+)

---

## Phase 1 Recommendation

**Implement in MVP:**
- Global bank voice leading
- Smooth, Cinematic, Neo-Soul styles
- Per-block override
- Freeze functionality
- On-demand caching

**Defer to Phase 2+:**
- Parallel fifth detection
- Advanced harmonic rule systems
- Graph-based voice-leading chains
- AI-powered style adaptation
