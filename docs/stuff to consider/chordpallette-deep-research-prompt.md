---
audience: [dev, product]
status: draft
owner: parker
last_reviewed: 2026-02-15
---

# Deep research prompt for ChordPallette

## Why this prompt is structured this way

These research instructions are designed to produce output that is *immediately useful for building a standout product*, not just an info dump.

### What the prompt optimizes for
- **Differentiation you can actually own:** It forces competitor/user pain analysis, then turns it into a “Top 10 differentiators” list with evidence.
- **Musical credibility + instrument playability:** It prioritizes voice-leading quality, range/mud handling, and live-friendly controls—areas that make users *feel* the product is “smart” and “trustworthy.”
- **Realtime feasibility:** It explicitly demands RT-safe patterns (bounded work, no allocations/locks on audio thread) so ideas don’t become unshippable.
- **Compatibility discipline:** It highlights serialization/versioning and distribution realities that often sink plugin trust after v1.
- **Actionability:** It requires a prioritized backlog, roadmap, validation metrics, and a risk register.

### How it avoids common research failure modes
- **Source quality + citations:** Requires high-quality sources and URLs per non-obvious claim.
- **Separates facts vs recommendations:** Prevents overconfident conclusions from weak evidence.
- **Covers both market and engineering:** Ensures “what users want” is connected to “what we can ship safely.”
- **Includes a watchlist:** Keeps the project current over time (MIDI 2.0 adoption, plugin format changes, competitor shifts).

## The prompt (copy/paste)

```text
You are an expert research analyst + product strategist + realtime-audio/MIDI software architect. 
Your task is to perform deep, source-cited research to help a new MIDI-first harmony plugin called **ChordPallette** become a standout product people love.

## Project context (read carefully)
ChordPallette is a MIDI-first harmony tool whose differentiators are:
- high-quality voice leading (musically credible, configurable profiles)
- range-aware voicing (avoid mud, instrument-aware spacing)
- a non-destructive operator pipeline (BaseChord immutable; operators produce derived states; “Freeze/Commit” creates a new base)
- realtime safety (bounded, allocation-free, deterministic on audio thread; heavy tasks off-thread)
- DAW plugin (likely JUCE wrapper) with a portable, testable core engine

The docs emphasize: core engine = “musical truth” (portable, unit-testable); UI reads snapshots; compatibility discipline for presets/schema; small reviewable changes; phased roadmap.

## Output requirements (strict)
1) Use only high-quality sources (official docs/standards, reputable audio dev blogs, academic papers, well-known industry outlets). Provide citations as URLs for every non-obvious claim.
2) Separate “facts” from “inferences/recommendations.” Label assumptions.
3) Deliver in a structured report with:
   - Executive summary (product opportunities + risks)
   - Competitive landscape and positioning map
   - Technical research findings
   - UX/workflow research findings
   - Go-to-market and pricing signals
   - A prioritized action backlog (Impact vs Effort + dependencies)
   - Appendices: source list, glossary, and “watchlist” for ongoing tracking

## Research questions (cover all)
### A) Market & product differentiation
- Who are the primary personas in the market for harmony/voicing tools (producers, worship keys, film composers, learners, live performers)?
- What are the main competitor products and adjacent workflows (DAW chord tools, MIDI FX, chord packs, performance tools)? 
- What do users praise/complain about most (especially around voice leading, predictability, UI friction, library management)?
- What “moments of delight” do standout tools create, and how?
- What unmet needs exist in: worship keys/pads, cinematic composing, neo-soul/R&B voicing, live MIDI performance?

### B) UX patterns that win
- Best-in-class UX for chord libraries, capture/history, drag-drop to DAW, chord blocks, and operator chains.
- Explainability patterns: how tools show “why this voicing happened” without overwhelming users.
- Instrument-like playability controls (e.g., Up/Down/Steady/Original overlays) and how similar products implement live-friendly controls.
- Preset sharing/community patterns: what makes libraries feel “collectible” and easy to manage?

### C) Technical implementation research (plugin + core)
- Realtime-safe patterns in audio plugins: threading, lock-free queues, memory allocation avoidance, bounded computation.
- MIDI 1.0 vs MIDI 2.0 readiness; MPE considerations; host quirks across VST3/AU/CLAP (if relevant).
- Modern plugin distribution: signing/notarization, installers, content packs, compatibility discipline, preset versioning.
- Voice-leading algorithms used in literature/products: cost functions, candidate generation, dynamic programming/Viterbi, constraints for register/mud avoidance, style profiles.
- Testing strategies for musical correctness: golden MIDI tests, property-based testing, fuzzing for edge cases.
- Serialization best practices for plugin state + user libraries (forward migration, schema versioning, human-readable vs binary).

### D) Standards and credibility
- Relevant standards guidance for usability/quality (ISO 9241-210/110, ISO/IEC 25010) and software lifecycle/reliability thinking (ISO/IEC/IEEE 12207/29148).
- Accessibility guidance relevant to plugin UIs (where applicable).

### E) Monetization and growth
- Pricing models and what customers accept (one-time, subscription, tiers, content packs, marketplace).
- Evidence-based marketing channels and community hubs (e.g., worship communities, producer communities, film scoring forums).
- Beta strategy that minimizes support load while maximizing learning.

## Deliverables (make it practical)
Provide:
1) A “Top 10 differentiators we can credibly own” list with evidence.
2) A recommended feature set for v1 that maximizes delight while staying RT-safe.
3) A “Docs-first improvements” checklist (what must be documented before coding).
4) A 6–12 month roadmap with milestones and validation metrics.
5) A risk register (technical, UX, market) with mitigations.

## Citation format
- Include direct URLs next to the claim they support.
- Prefer primary sources (official docs/specs/papers). Use multiple sources for key claims when possible.

Begin now.
```
