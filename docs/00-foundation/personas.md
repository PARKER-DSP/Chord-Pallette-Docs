---
audience: all
status: canonical
owner: docs
last_reviewed: 2026-02-15
---

# Target Personas

> **Status**: Starter personas defined. Validation interviews required in Phase 1.

---

## Persona 1: Beat Maker / Loop-Based Producer

**Profile:** Fast-paced electronic music producer who works in loops, samples, and quick iterations.

**Characteristics:**
- Age: 22-35
- Skill Level: Intermediate to advanced DAW skills; music theory varies
- Primary Tool: DAW (Ableton, FL Studio, Logic)
- Workflow: Loop-based, non-linear, highly iterative

**Goals:**
- Generate usable harmonic ideas quickly without friction
- Avoid deep theory concepts (wants speed over education)
- Reuse chord progressions across projects with variations
- Pack harmony into compact, playable blocks

**Pain Points:**
- Manual voicing is time-consuming
- Muddy bass notes ruin the mix
- Hard to remember exact voicings from previous projects
- Theory-heavy interfaces slow down creative flow

**Day-in-Life Example:**
*"I'm sketching a new beat. I find a cool 7-chord voicing on my keyboard, record it MIDI, and want to instantly save it. Then I need ChordPallette to auto-fit it to my playable synth range and maybe suggest a smoother voice move to the next chord. I'm doing this 20+ times in a session."*

**How ChordPallette Solves:**
- One-click chord capture
- Auto-voice-leading suggestions
- Quick library access during creative sessions
- Minimal UI / maximum speed

---

## Persona 2: Keys Player / Performer

**Profile:** Live performer or studio session player who triggers chords dynamically during recording or performance.

**Characteristics:**
- Age: 25-45
- Skill Level: Advanced keyboard/keys knowledge; strong music theory
- Primary Tool: Hardware keyboard or VST in DAW
- Workflow: Real-time triggering, expressive control, splits/zones

**Goals:**
- Map chord library to keyboard regions for instant access
- Control voicing through velocity, modulation, and touch dynamics
- Achieve natural, human feel in chords (avoid robotic sound)
- Support arpeggio / broken chord variations

**Pain Points:**
- Managing dozens of chord variations across keyboard zones is complex
- Playback of static chords sounds unmusical
- No easy way to trigger full voicings with expression
- Needs real-time flexibility for improvisational playing

**Day-in-Life Example:**
*"I'm recording a synth layer for an artist. I set up 8 chord voicings and map them to my left hand while playing melodic parts on the right. I need ChordPallette to let me trigger full chords with MIDI velocity dynamics and optional arpeggio. The voicings need to stay in my hand's reach but still sound sophisticated."*

**How ChordPallette Solves:**
- MIDI one-shot triggering of full chord voicings
- Keyboard zone mapping
- Velocity and modulation expression
- Arpeggio alternatives
- Consistent voice leading across triggers

---

## Persona 3: Songwriter / Composer

**Profile:** Composer or songwriter working across genres who cares deeply about harmonic sophistication and vocal/acoustic arrangement.

**Characteristics:**
- Age: 26-50+
- Skill Level: Strong music theory; composition background
- Primary Tool: DAW, often with piano/guitar control
- Workflow: Harmony-first, iteration-focused, long-form composition

**Goals:**
- Discover voicings that sound "finished" and professional
- Conform harmony to vocal or instrumental range
- Understand why certain voicings work better (music theory learning)
- Explore harmonic alternatives without starting from scratch

**Pain Points:**
- Manual voicing is tedious for complex progressions
- Range constraints on acoustic instruments limit possibilities
- Hard to know best voice-leading practices without deep theory study
- Switching instruments requires voicing reconfiguration

**Day-in-Life Example:**
*"I wrote a progression with good harmonic intent but the voicings sound empty. I want ChordPallette to auto-voice for piano range, then show me alternatives. I'd also like to understand why one voicing is smoother than another—help me learn while I work."*

**How ChordPallette Solves:**
- Auto-voicing to target range
- Harmonic suggestions with explanations
- Voice-leading educational feedback
- Quick voicing alternatives
- Range/instrument adaptation

---

## Persona 4: Music Student / Learner

**Profile:** Music student or self-taught musician improving harmony and voice-leading skills.

**Characteristics:**
- Age: 16-35
- Skill Level: Beginner to intermediate; theory knowledge still developing
- Primary Tool: DAW or hardware; often supplemented with music education resources
- Workflow: Practice-focused, exploratory, feedback-seeking

**Goals:**
- Understand voice-leading rules through hands-on experimentation
- Build intuition by seeing results of different voicing choices
- Learn best practices without heavy textbook study
- Practice with real tools, not just exercises

**Pain Points:**
- Traditional voice-leading textbooks are dense and abstract
- Hard to get immediate feedback on voicing quality
- Limited access to mentors for critique
- Resources don't connect theory to practical DAW workflows

**Day-in-Life Example:**
*"I'm learning about voice leading. I create a chord progression and want to understand why certain voicings flow better. ChordPallette explains the concept (smooth movement, voice leading principles) while I experiment, making it stick in my memory."*

**How ChordPallette Solves:**
- Real-time voice-leading feedback with explanations
- Hands-on experimentation environment
- Teachable moments during creative work
- Bridge between theory and practical application

---

## Persona 5: Developer / Product Team (Secondary Audience)

**Profile:** Engineering and product team building and iterating on ChordPallette.

**Characteristics:**
- Age: 24-50+
- Skill Level: Advanced programming, music/MIDI knowledge varies
- Primary Tool: Code editor, Git, documentation
- Workflow: Agile/sprint-based, collaborative

**Goals:**
- Maintain clear architecture and code quality
- Onboard new team members quickly
- Track feature progress and technical decisions
- Document learnings and constraints

**Pain Points:**
- Complex MIDI and voice-leading algorithms are hard to communicate
- Realtime performance optimization is non-obvious
- Team knowledge gets siloed without clear docs
- Refactoring risks breaking subtle behavioral invariants

**Day-in-Life Example:**
*"New team member just joined; I need them to understand the voice-leading engine architecture and why we made certain design choices. I also need to track our progress on Phase 1 deliverables and known constraints."*

**How ChordPallette Solves (via Docs):**
- Architecture principles and module boundaries clearly documented
- Development guidelines and commit standards
- Progress tracking and roadmap visibility
- Recorded decisions and their rationale
- Invariants and safety constraints documented

---

## Persona-Feature Alignment Matrix

| Feature | Persona 1 (Producer) | Persona 2 (Player) | Persona 3 (Composer) | Persona 4 (Learner) | Persona 5 (Team) |
|---------|:---:|:---:|:---:|:---:|:---:|
| Chord Capture | ⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐ | - |
| Voice Leading Suggestions | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | - |
| Range Optimization | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ | - |
| MIDI Triggering | ⭐ | ⭐⭐⭐ | ⭐ | ⭐ | - |
| Chord Library | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | - |
| Learning/Explanations | ⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ | - |
| Architecture Docs | - | - | - | - | ⭐⭐⭐ |
| Dev Guidelines | - | - | - | - | ⭐⭐⭐ |

---

## Research Gaps & Phase 1 Validation Plan

### Questions to Validate:
1. **Chord Capture UX**: Will producers actually re-type chord voicings into a UI, or do they prefer pure MIDI recording?
2. **Voice Leading Algorithm**: How much manual tweaking will users accept vs. relying on auto-suggestions?
3. **Price Sensitivity**: Is this a $50/year, $200/year, or $1000+/year tool?
4. **Integration**: Should this live in DAW as plugin, standalone app, or both?
5. **Range Optimization**: How important are instrument-specific voicing rules vs. generic auto-voicing?

### Phase 1 Validation Activities:
- Conduct 10-15 structured interviews with target personas (3-4 per persona)
- Build low-fidelity prototype of chord capture and create a test scenario
- Observe users attempting to voice a complex progression
- Ask about pain points with existing tools (voice leading, range constraints, workflow)
- Validate pricing hypothesis through willingness-to-pay surveys

---

## Emerging Insights

*(To be updated after Phase 1 interviews)*

- Early indication that Persona 2 (Keys Player) sees most immediate value
- Persona 1 (Producer) wants speed > education; Persona 3/4 want the opposite
- Realtime voice-leading feedback may be more important than batch suggestions
- Library/capture features might be Phase 2+ priority; core voice-leading is MVP
