---
audience: design
status: canonical
owner: design
last_reviewed: 2026-02-15
---

# UX & Design Overview

Guidelines and specifications for ChordPallette's user interface, interaction design, and visual brand.

---

## Style Guide

Brand attributes, visual direction, typography, and interaction patterns.

- **[Style Guide](style-guide/style-guide.md)** – Brand voice, visual direction, color, typography, interaction principles

---

## UI Components & Patterns

Detailed specifications for user interactions and interface elements.

- **[UI Patterns](ui/ui-patterns.md)** – Chord lane, block editor, mapping panel, operator chains
- **[Voice Leading UX](ui/voice-leading-ux.md)** – Controls, feedback, advanced settings for voice leading

---

## Design Principles

### Playability

Everything should feel fast and intuitive. Users should feel in control of the tool, not the other way around.

### Clarity

Respect user knowledge levels. Show expert features (advanced panel, fine-tuning) but don't force them. Defaults should be smart and musical.

### Immediacy

Voice leading, voicing changes, and operator applications should feel instant. No hidden complexity.

### Reversibility

Nothing should feel permanent. Users should always be able to undo, experiment, and recover from mistakes.

### Musicality

All visual and interaction feedback should enhance the musical experience, not distract from it.

---

## Key Design Decisions

1. **Dark UI with high contrast** – Reduces eye strain during long sessions; makes chord blocks visually distinct
2. **Grid-based layout** – Supports drag-reordering and visual scanning of large chord banks
3. **Tactile chord blocks** – Each chord feels like a playable object, not just data
4. **Minimal but powerful UI** – Hide advanced controls by default; surfac only what matters for current task

---

## Interaction Patterns

### Drag & Drop
- Chord blocks reorder visually with ghost placement
- MIDI files drag directly into bank
- Shift-drag exports MIDI

### Right-Click Context
- Quick access to per-block operations
- Override voice leading, duplicate, delete, edit tags
- No deep menus

### Toggle & Popovers
- Voice leading style: dropdown toggle
- Advanced settings: collapsed by default
- Large parameters: separate floating panel

---

## Accessibility Considerations

- ✅ Keyboard shortcuts for common operations (number keys for quick trigger, arrows for navigation)
- ✅ High contrast ratios for readability
- ✅ Clear focus states for tabbing
- ✅ Tooltips for all controls
- *Future:* Screen reader support for core workflows

---

## Development Phases

| Phase | Deliverables |
|-------|---|
| **1** | Architecture, component library foundation |
| **2** | Chord lane, block editor, bank view MVP |
| **3** | Voice leading controls, operator chain UI |
| **4** | Live mapping panel, keyboard controls |
| **5** | Polish, accessibility, platform-specific refinement |

---

## Related Sections

- **[Foundation](../00-foundation/)** – Product vision and user needs
- **[Features](../02-features/)** – What's being designed (operators, voice leading)
- **[Go-to-Market](../03-go-to-market/)** – Brand and positioning
- **[Developer](../01-developer/)** – Technical architecture and constraints
