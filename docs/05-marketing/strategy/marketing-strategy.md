# Marketing Strategy (short)
## TEST
## Positioning
ChordPallette is a performance-driven chord capture + voicing instrument that makes progressions **flow**.

## Primary angles
- Speed: capture and reuse chord moments instantly
- Quality: voicings that sound finished, less mud
- Performance: trigger banks like an instrument
- Flow: voice leading makes transitions musical

## Channels
- YouTube short demos
- Instagram/TikTok clips (workflow transformations)
- Producer Discords + micro-influencer affiliates


# Marketing Strategy Verbose | Chord Palette Plugin: Technical and Market Strategy Report

Date: 2026-02-13  
Method: Codebase-first audit plus previously collected competitor/source notes. No new research was performed for this draft.

## 1. Executive Summary

This product is not just a chord generator. The current codebase is a low-latency MIDI chord performance engine with composition utilities layered on top.

Key conclusion:
- Strongest strategic wedge is live harmonic performance on pads/keys/controllers, not direct head-to-head theory browsing against Scaler-style products.
- Core moat is the combination of real-time trigger mapping, safe-note remapping, rapid chord-bank manipulation, and practical MIDI export workflows.
- Product already supports a path to ecosystem revenue via presets, controller profiles, and community chord sharing without major architectural rewrites.

Top priorities:
1. Position category around performance mapping and fast harmonic control.
2. Productize controller-first workflows (profiles, scenes, setlists, low-friction live UX).
3. Ship a free lead magnet (Lite plugin or web tool) that demonstrates "one-note to full progression" in under 60 seconds.
4. Build recurring value via content ecosystem before heavy AI investment.

## 2. Feature Map

### 2.1 Feature Extraction (Code-Derived)

Legend:
- Market status: `Unique`, `Rare`, `Commodity`
- Category: `Core Value`, `Differentiator`, `Power User`, `Latent Opportunity`, `Technical Advantage`

| Capability | Category | Evidence in Code | Market Status | Why It Matters |
|---|---|---|---|---|
| Record vs Play engine modes | Core Value | `Source/PluginProcessor.cpp`, `Source/engine/ChordEngine.cpp` | Commodity | Standard chord-capture then trigger workflow. |
| Snapshot capture window (5-750 ms, default 90 ms) | Core Value | `Source/parameters/ParameterLayout.cpp` | Rare | Better control over how human input is grouped into chord snapshots. |
| Chord triggering from note range + base note mapping | Core Value | `Source/engine/ChordEngine.cpp`, `Source/ui/components/PianoRollDisplay.cpp` | Commodity | Core one-note chord triggering behavior expected in category. |
| Chord identification and naming with slash/bass handling | Core Value | `Source/domain/ChordModel.cpp` | Commodity | Required for trust and readability of generated chord names. |
| Tabbed chord banks (create/rename/duplicate/merge) | Differentiator | `Source/PluginEditor.cpp`, `Source/plugin/EditorController.cpp` | Rare | Supports song-part organization and fast arrangement iteration. |
| Per-entry voicing/spread/note-count transform cycling | Differentiator | `Source/PluginProcessor.cpp`, chord lane actions in UI | Rare | Fast harmonic variation without opening external tools. |
| MIDI import from dropped files grouped by onset | Power User | `Source/PluginProcessor.cpp` import flow | Rare | Speeds reuse of existing MIDI libraries and references. |
| Shift-drag chord block to export `.mid` | Differentiator | `Source/ui/components/ChordLaneComponent.cpp` + export helpers in processor | Rare | Removes export friction and fits modern DAW workflows. |
| Global export controls (beats, velocity, clip metadata) | Power User | `Source/parameters/ParameterLayout.cpp`, `Source/PluginProcessor.cpp` export methods | Commodity | Important for DAW compatibility and deterministic output. |
| Safe-note bracket remapping with maintain-root option | Differentiator | `Source/engine/ChordEngine.cpp`, safe-range logic in `PianoRollDisplay` | Unique | Strong live-play safety system not commonly implemented this explicitly. |
| Global octave shift and constrained trigger range | Core Value | `Source/parameters/ParameterLayout.cpp`, engine mapping path | Commodity | Basic but necessary for keyboard/pad adaptation. |
| Number-key quick trigger mode (1-0) | Power User | `Source/ui/components/ChordLaneComponent.cpp`, editor key handling | Rare | Very fast audition/performance path for desktop users. |
| Note-lock/latch preview workflow | Power User | `Source/PluginEditor.cpp`, chord preview control paths | Rare | Better for sustained testing and live continuity. |
| Built-in preview synth (poly sine, normalized gain) | Technical Advantage | `Source/PluginProcessor.cpp` | Commodity | Reliable no-host-instrument fallback for immediate sound. |
| Standalone VST3 preview-host scan/load/favorites/editor | Differentiator | `Source/plugin/PreviewHostCatalog.*`, `PreviewHostWindowController.*`, `Source/app/PreviewInstrumentHostService.cpp` | Rare | Improves out-of-box usability and demo quality for non-technical users. |
| Hosted instrument state stored in presets | Differentiator | `Source/state/StateSerializer.cpp`, preview host data fields | Rare | Presets become full performance scenes, not only chord lists. |
| Nashville / scale-fit labeling (46 scale definitions) | Differentiator | Scale analysis in `Source/PluginEditor.cpp` | Rare | Adds musician-facing harmonic context beyond raw chord names. |
| Guitar chord builder (fingering, capo, tuning metadata) | Differentiator | `Source/ui/components/GuitarChordBuilderComponent.*` | Rare | Bridges keyboard and guitar workflows in one plugin. |
| Preset browser with factory + user categories and search | Core Value | `Source/presets/PresetLibrary.*`, editor preset UI | Commodity | Baseline discoverability/recall feature expected by users. |
| Factory preset generator target (250 total, uniqueness constraints) | Technical Advantage | `Source/presets/PresetLibrary.cpp`, `Tests/PresetLibraryTests.cpp` | Rare | Content scale plus quality guardrails are already codified. |
| Backward-compatible state serialization paths | Technical Advantage | `Source/state/StateSerializer.*`, `Tests/StateSerializationTests.cpp` | Rare | Reduces version upgrade risk and support burden. |
| RT-safe process path (no blocking/XML in `processBlock`) | Technical Advantage | `Source/PluginProcessor.cpp`, architecture docs | Rare | Performance reliability under host load is a major trust factor. |

### 2.2 Workflow Advantages Embedded in Architecture

- High-speed capture-to-variation loop:
  - Capture held notes, dedupe, apply transform cycles, reorder by drag, export by shift-drag.
- Dual-preview architecture:
  - Built-in synth for immediate feedback and optional hosted instrument for realistic audition.
- Scene-like preset behavior:
  - Chord content + optional hosted instrument state creates reproducible performance context.
- Bank-level and chord-level editing granularity:
  - Users can operate globally (transpose/export defaults) or surgically per entry.

### 2.3 UI/UX Differentiators

- Chord lane supports drag reordering with visual ghost placement and direct context actions.
- Piano roll visualizes active/input/transposed notes plus interactive trigger and safe-zone brackets.
- Guitar builder is embedded, not bolted on, and stores fingering context with each chord entry.
- Number overlays, Nashville labels, and optional trigger labels support both theory users and performers.

### 2.4 Performance, DSP, and MIDI Routing Advantages

- Real-time path designed to avoid blocking operations during audio processing.
- Event processing is centralized in `ChordEngine`, improving deterministic behavior under rapid MIDI input.
- Safe-note remap plus root-preservation reduces wrong-note failures on constrained controllers.
- Built-in synth gain normalization avoids clipping when previewing dense chords.

### 2.5 Extensibility Capabilities

- Stable parameter IDs and explicit schema fields support forward-compatible feature additions.
- Preset/state serialization can already hold extended metadata (instrument state, chord metadata).
- Existing tab and entry data model can back cloud sync, community sharing, and marketplace SKUs.
- Controller profile support can be added without rewriting core chord mapping.

### 2.6 Latent / Undeveloped Opportunities (Already Enabled by Current Architecture)

- Controller profiles (Launchpad/Push/MPK/foot controllers) mapped to trigger zones and colors.
- Setlist/song sections built on top of existing tab model.
- Phrase/arpeggio layer fed from existing chord output events.
- Cloud/shared preset IDs using current serialization payloads.
- Assisted progression suggestions powered by existing scale-fit and chord metadata.

## 3. Competitive Matrix

### 3.1 Competitor Profiles

Pricing below is tier-level guidance from previously collected public product pages and may vary by sale/region.

| Competitor | Core Positioning | Unique Features | Weaknesses | Target Market | Price Tier | UX Philosophy |
|---|---|---|---|---|---|---|
| Scaler 3 | Comprehensive chord/scale composition workstation | Deep theory views, progression tools, broad content ecosystem | Can feel dense for fast live performance | Producers/composers needing theory depth | Mid (`~$79-99` perpetual street tier) | Feature-rich, panel-driven exploration |
| Xfer Cthulhu | Fast chord memory + arp tool | Very quick chord triggering and arp pairing | Less modern content/workflow depth vs newer suites | EDM/trap producers and live trigger users | Budget (`~$39`) | Minimal, speed-first |
| Captain Plugins | Multi-plugin song-building suite | Integrated chord, melody, bass, rhythm workflow | Heavier ecosystem; less focused single-plugin immediacy | Beginner-intermediate creators | Mid-high (bundle tiers) | Guided, suite-based production |
| InstaChord 2 | Chord trigger/performance helper | Easy mapping and immediate playability | Narrower advanced ecosystem and analysis depth | Beginners and beatmakers | Budget-mid (`~$59-79`) | Immediate and simplified |
| ChordPotion | Chord generation from melody and transformation | Efficient idea generation from MIDI context | Smaller brand/content moat and narrower workflow breadth | Producers needing quick harmonic variants | Budget (`~EUR 29` class) | Utility-centric |
| LANDR Composer (Orb successor) | AI-assisted chord/progression generation | AI-first generation framing | Subscription resistance for some plugin buyers | Idea-seeking producers | Subscription (entry monthly) | Prompt/suggestion-oriented |
| Ableton MIDI tools (Chord/Scale + Live 12) | DAW-native MIDI effects | Native integration, low friction in Live | Not cross-DAW plugin-first, less specialized chord UX | Ableton users | DAW-tier | Native utility modules |
| Logic Pro chord/scale features | DAW-native composition aids | Tight Apple ecosystem integration | Mac-only and DAW-bound | Logic users | DAW-tier | Integrated workflow tools |

### 3.2 Feature Overlap Matrix

Legend: `Y` = strong support, `P` = partial/basic, `N` = not a focus

| Feature | This Product | Scaler | Cthulhu | Captain | InstaChord | ChordPotion | LANDR Composer | Ableton/Logic Native |
|---|---|---|---|---|---|---|---|---|
| One-note chord triggering | Y | Y | Y | Y | Y | P | P | P |
| Chord detection/naming from MIDI | Y | Y | P | P | P | P | P | P |
| Scale/key recommendation context | Y | Y | N | P | P | P | Y | P |
| Fast live mapping safety (safe ranges/remap) | Y | P | P | P | P | N | N | N |
| Tabbed chord-bank scene workflow | Y | P | N | P | P | N | P | N |
| Direct drag-export MIDI per chord | Y | Y | P | Y | P | P | P | P |
| Built-in guitar chord builder metadata | Y | N | N | N | N | N | N | N |
| Hosted preview instrument in standalone | Y | N | N | N | N | N | N | N |
| Number-key rapid trigger mode | Y | N | P | N | P | N | N | N |
| AI progression generation | N (latent) | P | N | P | N | N | Y | N |
| Deep integrated content marketplace | N (latent) | P | N | P | N | N | P | N |
| DAW-native tight integration advantage | N | N | N | N | N | N | N | Y |

### 3.3 Missing Features vs Competitors

Highest impact gaps:
1. No true phrase/arpeggiator module (Cthulhu category expectation).
2. No large curated progression/song assistant UX comparable to Scaler/Captain depth.
3. No AI-assisted suggestion layer (LANDR/Orb trend).
4. No built-in cloud/community exchange loop for content/network effects.
5. No explicit controller profile marketplace yet (clear monetization opportunity).

### 3.4 Features Where This Product Can Outperform

1. Live-safe harmonic mapping reliability:
- Safe-note brackets plus root-preserving remap is stronger than typical one-note trigger tools.

2. Cross-instrument harmonic workflow:
- Guitar builder metadata + keyboard/pad triggering in one pipeline is uncommon.

3. Scene portability:
- Presets that can include hosted preview instrument state provide stronger reproducibility.

4. Operational speed:
- Per-chord transform cycles + drag reorder + shift-drag export supports rapid ideation and production handoff.

## 4. Positioning Diagnosis

### 4.1 How the Product Is Currently Positioned by Its Actual Capabilities

Current functional position (from code, not marketing copy):
- Primary: Workflow accelerator for harmonic input and arrangement.
- Secondary: Live performance instrument for pad/keyboard control.
- Secondary: Compositional utility with scale/Nashville context.
- Tertiary: Creativity device (variation via transforms), but not yet AI idea engine.

### 4.2 Is It a Scaler Alternative?

- Partial alternative, not direct replacement.
- It overlaps on chord detection, key/scale context, and MIDI workflow.
- It does not yet match Scaler-style theory depth, guided progression ecosystems, and broad educational UX.
- It can win where immediacy and live mapping are more important than deep theory browsing.

### 4.3 Crowded vs Differentiated

- Crowded at headline category level ("chord plugin").
- Differentiated at workflow level if framed as:
  - "Live Harmonic Mapping Engine" or
  - "Performance-first chord control for pads/keys/controllers."

Diagnosis:
- Competing as "another chord plugin" is crowded.
- Competing as "reliable live harmonic control + fast production handoff" is meaningfully differentiated.

## 5. Niche Opportunity Ranking

### 5.1 Scoring Model

Opportunity Score (1-5) weighted by:
- Market size: 30%
- Architecture alignment: 30%
- Ease of entry: 25%
- Low competition (inverse density): 15%

### 5.2 Ranked Niches

| Niche | Market Size | Competition Density | Ease of Entry | Alignment to Current Code | Opportunity Score | Messaging Angle | Small Additions to Dominate |
|---|---:|---:|---:|---:|---:|---|---|
| Hardware MIDI controller users | 4 | 3 | 5 | 5 | 4.35 | "Turn any controller into a harmonic instrument" | Controller profiles, pad color maps, profile import/export |
| Live performers using MIDI pads | 4 | 3 | 4 | 5 | 4.10 | "Play full progressions safely on stage" | Performance mode, panic/reset, latch scene switching |
| Worship musicians (keys/pads) | 3 | 2 | 4 | 5 | 4.05 | "Reliable chord transitions under pressure" | Song section tabs, key-change macros, setlist presets |
| Streamers / live loopers | 3 | 3 | 4 | 4 | 3.65 | "Build rich loops fast without theory overhead" | OBS-friendly mini view, quick scene recalls, footswitch support |
| Music educators / classrooms | 3 | 3 | 4 | 4 | 3.65 | "See and hear harmony instantly" | Education mode overlays, assignment preset packs |
| Film/game composers | 4 | 4 | 3 | 4 | 3.55 | "Rapid harmonic exploration with controlled voicing" | Mood packs, articulation presets, cue template export |
| Lo-fi/chill producers | 4 | 4 | 4 | 3 | 3.50 | "Instant colorful chord moods" | Genre packs, texture-aware presets |
| Beginner songwriters | 5 | 5 | 3 | 3 | 3.35 | "Write full chord progressions from one hand" | Guided progression wizard, simplified labels |
| Disabled musicians (adaptive control) | 2 | 1 | 3 | 4 | 3.35 | "Accessible harmonic performance" | Switch control mappings, larger high-contrast UI mode |
| DAWless setups | 2 | 2 | 2 | 3 | 2.70 | "Harmonic brain for compact rigs" | Hardware MIDI routing mode, lightweight host profile |
| Touchscreen performers | 2 | 2 | 2 | 2 | 2.35 | "Playable chord surfaces for touch" | Touch-first UI scaling, gesture mappings |

### 5.3 Best-Fit Niche Right Now

Best immediate niche: `Hardware MIDI controller users` with `live pad performers` as adjacent segment.

Why:
- Highest architecture fit with existing trigger mapping and safe-range logic.
- Lower direct competition density than generic "producer chord plugin" messaging.
- Fastest path to demonstrable value in product demos.

## 6. Ecosystem Strategy

### 6.1 Ecosystem Options Evaluation

| Initiative | Revenue Model | Technical Feasibility | Moat Potential | Long-Term Defensibility | Recommendation |
|---|---|---|---|---|---|
| Preset marketplace | Revenue share on paid presets | High | Medium-high | High if creator supply grows | Build in first wave |
| Expansion packs | One-time pack purchases | High | Medium | Medium | Ship immediately |
| Genre packs | One-time + bundles | High | Medium | Medium | Ship immediately |
| AI chord suggestion module | Add-on subscription | Medium | Medium | Medium (depends on data moat) | Phase 2 after content loop |
| Cloud sync | Subscription feature in Pro+ | Medium | Medium | High when tied to workflow lock-in | Phase 2 |
| Mobile companion app | Subscription add-on | Low-medium | Medium | Medium | Defer until desktop loop matures |
| MIDI pack store | Direct sales + creator rev share | High | Medium | Medium-high with community effects | Bundle with marketplace |
| Community chord sharing | Freemium (public/private libraries) | Medium | High network effect | High | Prioritize early |
| Controller integration profiles | Paid profile packs + partner licensing | High | High in niche | High if profile catalog dominates | Core moat initiative |
| API for third-party developers | Platform fees / certification | Medium | High | High if ecosystem adopts standard | Phase 3 |
| Hardware integration | OEM bundles + affiliate licensing | Medium | High | High with exclusive mappings | Start with pilot partners |
| Education platform | Course + pack bundles | Medium | Medium | Medium | Secondary growth track |

### 6.2 Ecosystem Build Order

1. Content revenue now:
- Genre/expansion packs and premium preset bundles.

2. Community loop next:
- Shared libraries, ratings, creator profiles.

3. Platform layer third:
- Controller profile SDK/API and selected hardware partnerships.

## 7. Freebie Growth Strategy

Goal: create high-intent acquisition assets that demonstrate value quickly and convert to Pro.

| Freebie Idea | Code Reuse Basis | Effort | Viral Potential | Lead Magnet Strength | Upsell Pathway |
|---|---|---|---|---|---|
| Chord Palette Lite VST (8 slots, 1 tab, no merge) | Existing engine + UI flags + preset limits | Medium | High | High | Upgrade for unlimited tabs, transforms, advanced mapping |
| Web chord detector + Nashville labeler | `ChordModel` naming logic and scale-fit logic | Medium | Medium | High | Email gate for desktop plugin download |
| Controller Profile Starter Pack (free mappings) | Existing trigger range/remap architecture | Low | Medium-high | Medium-high | Sell advanced profile bundles |
| Free MIDI progression starter library (genre mini pack) | Current export/preset content pipeline | Low | Medium | Medium | Upsell to full marketplace and Pro pack bundles |
| Guitar voicing mini utility | Reuse guitar builder component logic | Medium | Medium | Medium | Upsell to full plugin with triggering/export |
| "Safe Range" mini MIDI utility plugin | Reuse safe-note remap logic from engine | Medium | Medium-high | Medium-high | Upsell to full chord workflow suite |
| Beginner progression template set + tutorial | Existing preset architecture | Low | Medium | High | Upsell to full preset library and advanced workflow |
| Chord-to-MIDI drag web widget | Reuse export mapping and chord metadata format | Medium | Medium | Medium | Upsell to plugin for real-time live use |

Recommended first freebie:
1. `Chord Palette Lite VST` (highest product-qualified lead quality).
2. `Web chord detector` as SEO and list-building feeder.

## 8. 12-Month Strategic Vision

### 8.1 Strategic Positioning Recommendation

Category design recommendation:
- Define category as `Live Harmonic Mapping` rather than generic `Chord Generator`.

Differentiated value proposition:
- "Map complex harmony to simple performance gestures, safely and fast, then export production-ready MIDI instantly."

JTBD framing:
- "When I am producing or performing under time pressure, help me trigger musically correct, expressive chord movement without stopping to program theory-heavy tools."

Blue Ocean angle:
- Avoid direct feature race on theory encyclopedias.
- Own the intersection of live reliability, controller mapping, and fast arrangement handoff.

### 8.2 Messaging Angle

Primary message:
- "Performance-first chord control for modern controllers and DAW workflows."

Secondary proof points:
- Safe-note remap with root integrity.
- Rapid chord-bank transforms and reorder.
- Guitar plus keyboard harmonic workflow.
- Immediate preview and one-gesture MIDI export.

### 8.3 Pricing Model Recommendation

Recommended commercial stack:
- Free: Lite plugin + starter packs.
- Pro perpetual: full feature set (`$69 intro`, `~$99 list` range positioning).
- Pro+ annual (`~$49/year`): cloud sync, marketplace perks, advanced profile library, early AI suggestions.

Rationale:
- Perpetual aligns with plugin buyer expectations.
- Optional recurring tier funds ecosystem features and improves retention economics.

### 8.4 Launch Strategy (PLG + Community-Led)

Phase 1 (0-3 months): Wedge launch
- Ship Lite + "Controller Performer" narrative.
- Onboarding must reach first successful mapped trigger in under 3 minutes.
- Creator demos focused on pad/keys workflows.

Phase 2 (4-8 months): Content flywheel
- Launch genre packs + controller profile packs.
- Enable community preset sharing and ratings.
- Add in-product recommendation rails for pack discovery.

Phase 3 (9-12 months): Ecosystem lock-in
- Cloud sync for presets/tabs/profiles.
- Creator marketplace beta with rev share.
- Partner pilots with controller manufacturers.

### 8.5 12-Month Product Roadmap

| Quarter | Product Goals | Commercial Goals | KPI Targets |
|---|---|---|---|
| Q1 | Positioning refactor, onboarding polish, controller profile v1, Lite release | Build top-of-funnel and email capture | Activation rate, time-to-first-progression, Lite-to-trial conversion |
| Q2 | Setlist/tab scene tooling, performance mode, first premium pack wave | First content revenue stream | Paid conversion, pack attach rate, weekly active performers |
| Q3 | Community sharing, ratings, cloud account alpha, creator onboarding | Start marketplace liquidity | UGC upload rate, retained creators, D30 retention |
| Q4 | Marketplace beta, hardware partner profiles, AI suggestion prototype | Expand ARPU and defensibility | ARPU, creator GMV, D90 retention, profile pack sales |

### 8.6 Retention and Moat Metrics

Track these as product health indicators:
- Activation: users who create/import a bank and trigger at least 4 chords in session 1.
- Habit: weekly active users who load saved presets in 3+ sessions.
- Ecosystem depth: average paid pack attach per paying user.
- Network effect: percentage of active users who import community content.
- Defensibility: percentage of sessions using controller profiles or cloud-synced presets.

## Appendix A: Source Footprint Used for This Report

Codebase evidence reviewed includes:
- `Source/PluginProcessor.*`
- `Source/engine/ChordEngine.*`
- `Source/domain/ChordModel.*`
- `Source/ui/components/*`
- `Source/plugin/*`
- `Source/presets/*`
- `Source/state/*`
- `Tests/*`
- `Docs/architecture.md`, `Docs/invariants.md`

Previously collected competitor/source notes referenced (no new pulls for this draft):
- Scaler: https://www.scalermusic.com/products/scaler-3/ , https://www.pluginboutique.com/products/14118-Scaler-3
- Cthulhu: https://xferrecords.com/products/cthulhu , https://www.pluginboutique.com/products/1044-Cthulhu
- Captain Plugins: https://www.mixedinkey.com/captain-plugins/ , https://www.mixedinkey.com/captain-plugins-pricing/
- InstaChord: https://www.waproduction.com/plugins/view/instachord , https://www.pluginboutique.com/products/11326-InstaChord-2
- ChordPotion: https://www.feelyoursound.com/chordpotion/
- LANDR Composer: https://www.landr.com/plugins/landr-composer
- Ableton MIDI docs/pricing: https://www.ableton.com/en/live-manual/12/live-midi-effect-reference/ , https://www.ableton.com/en/shop/live/
- Logic Pro chord tools: https://support.apple.com/en-mz/guide/logicpro/lgcp246dd829/mac , https://www.apple.com/logic-pro/
