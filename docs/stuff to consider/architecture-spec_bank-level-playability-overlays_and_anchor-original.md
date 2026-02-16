---
audience: [dev, product, ux]
status: draft
owner: parker
last_reviewed: 2026-02-15
---

# Architecture Spec — Bank-Level Playability Overlays & Anchor-Based “Original”

## Relevance to Project

This document formalizes the design and behavior of:

- Bank-level playability overlays (Up / Down / Steady / Original)
- Anchor-based interpretation of “Original”
- Overlay interaction with memory and voice-leading engine
- Realtime-safe scoring extensions
- UX integration with History and Capture workflow

This spec directly impacts:

- Voice-leading engine design
- Core scoring model
- Non-destructive architecture integrity
- Realtime safety constraints
- Performance UX differentiation

---

# 1. Executive Summary

This proposal defines:

1. The canonical meaning of **Original**
2. The complete overlay system
3. The scoring model integration
4. Interaction with Anchor / Realized / Memory layers
5. UX + History integration

The system ensures:

- Non-destructive architecture
- Musical coherence
- Expressive live performance
- Predictable behavior
- Strict realtime safety

---

# 2. Problem Statement

Ambiguity exists around what “Original” means in context of contextual voice leading.

Potential interpretations:
- Anchor voicing
- Chord spelling
- Memory voicing
- Frozen/baked voicing
- Realized output

Without formal definition, user expectations and architectural behavior diverge.

This spec resolves that ambiguity.

---

# 3. Architectural Ground Truth

Layer | Meaning | Mutability
------|---------|------------
Anchor Voicing | Canonical identity of block | Immutable
Realized Voicing | Contextual output | Ephemeral
Memory Voicing | Last-played reference | Ephemeral
Frozen/Baked | User-committed state | Persistent

Overlays must:
- Never mutate anchor
- Never retroactively modify history
- Never rewrite stored voicings
- Only influence scoring

---

# 4. Formal Definition of “Original”

> Original biases the voice-leading engine toward the chord block’s Anchor Voicing and Anchor Register.

Original does NOT:
- Change chord identity
- Force exact anchor reproduction
- Override global safety constraints

Original DOES:
- Add weighted scoring pull toward anchor features
- Reduce memory dominance
- Restore canonical voicing identity

---

# 5. Overlay System Specification

All overlays are:

- Bank-level
- Mutually exclusive
- Intensity-adjustable (0–100%)
- Non-destructive
- Implemented as additive scoring bias

---

## 5.1 Up

Encourages upward motion.

Biases:
- Higher top note
- Higher centroid
- Slight spacing expansion

---

## 5.2 Down

Encourages downward motion.

Biases:
- Lower top note
- Lower centroid
- Mild compression

---

## 5.3 Steady

Encourages register stability.

Biases:
- Stable top note
- Stable centroid
- Minimal drift

---

## 5.4 Original

Encourages anchor identity restoration.

Biases:
- Anchor top note
- Anchor bass
- Anchor spacing profile
- Anchor register center

---

# 6. Scoring Model

For candidate voicing C:

S(C) = S_base(C) + S_overlay(C)

---

## 6.1 Reference Voicing

Blended reference:

V_ref = (1 − μ) * Realized + μ * Memory

μ = memory influence weight (mode-dependent)

---

## 6.2 Overlay Terms

### Up

S_up = w * (α * Δ_top + β * Δ_centroid)

---

### Down

S_down = −w * (α * Δ_top + β * Δ_centroid)

---

### Steady

S_steady = −w * (γ * |Δ_top| + δ * |Δ_centroid|)

---

### Original

S_original = −w * D(C, Anchor)

Where:

D = λ1|top(C) − top(A)| 
  + λ2|bass(C) − bass(A)| 
  + λ3 * spacingDistance(C, A)

---

# 7. Memory Interaction Rules

Memory influences:
- Up
- Down
- Steady

Memory does NOT influence:
- Original

Original references Anchor only.

---

# 8. Mode-Specific Parameterization

Modes modify overlay weight parameters.

Example:

Parameter | Worship Pads | Piano Pop
----------|--------------|------------
α, β | Lower | Higher
Motion penalty | High | Moderate
Memory weight μ | High | Low
Anchor pull λ | Medium | Low

Result:
- Smooth expressive pad behavior
- More dramatic piano motion when desired

---

# 9. UX Specification

Location:
- Bank header controls

Controls:
- Up
- Down
- Steady
- Original
- Intensity slider

Properties:
- Real-time effect
- No block mutation
- Clear visual state
- Optional “None” state

UX Goal:
Instrument-like performance shaping without data risk.

---

# 10. History & Capture Integration

Exploration:
- Overlays shape real-time realization.

Discovery:
- History logs realized voicings.

Capture:
- User may flatten:
  - Harmony only
  - Full voicing (new anchor)

Overlays never rewrite stored anchors.

---

# 11. Realtime Safety Constraints

Overlay scoring must be:

- Allocation-free
- Deterministic
- Bounded candidate count
- O(N candidates) per evaluation

spacingDistance must:
- Avoid heap allocation
- Use fixed buffers
- Limit voice count

---

# 12. Strategic Impact

This system:

✓ Preserves non-destructive architecture  
✓ Resolves “Original” ambiguity  
✓ Enables expressive performance control  
✓ Encourages creative exploration  
✓ Differentiates from static chord tools  
✓ Maintains RT safety  

---

# 13. Promotion Criteria

Before implementation:

- Validate scoring stability under stress
- Profile RT performance
- Test cross-mode consistency
- Confirm intuitive UX in user testing

Upon validation:
Move to Feature Guide and Core Architecture implementation phase.

---
