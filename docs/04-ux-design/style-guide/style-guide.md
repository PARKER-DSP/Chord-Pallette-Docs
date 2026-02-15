---
audience: design
status: canonical
owner: design
last_reviewed: 2026-02-15
---

# Style Guide

Visual and interaction guidelines for ChordPallette's user interface.

---

## Brand Attributes

- **Bold** – Confident, not apologetic
- **Performance-driven** – Built for real-time creative work
- **Premium** – High-quality feel without pretension
- **Minimal but powerful** – Clear hierarchy, no fluff

---

## Visual Direction

### Color Palette

*(To be defined during Phase 1 UI design)*

**Dark UI Base:**
- Dark background for reduced eye strain
- High contrast between active and inactive elements

**Accent Colors:**
- Chord blocks: distinct, easily differentiated
- Interactive states: hover, selected, locked, muted
- Feedback: success, warning, error

### Typography

- **UI Font:** Modern sans-serif (likely Helvetica Neue, Inter, or similar)
- **Code/Monospace:** For MIDI notes, parameter values
- **Hierarchy:** Consistent weight/size progression
  - Large: Section headings
  - Regular: Control labels, content
  - Small: Hints, secondary info

### Visual Style

- **High contrast** – Text reads clearly against backgrounds
- **Tactile chord blocks** – Touch/click targets clearly defined
- **Clear grid** – Supports alignment and visual scanning
- **Subtle glow accents** – Used sparingly for important state changes
- **Smooth animations** – State transitions feel responsive, not jarring

---

## Interactive States

Every control should have clear visual feedback:

- **Default:** Normal appearance
- **Hover:** Subtle highlight or lift effect
- **Active/Selected:** Distinct color, border, or background
- **Disabled:** Greyed out, clear that it's not available
- **Loading:** Spinner or progress indicator
- **Error:** Red or warning color with tooltip

---

## Interaction Style

### General Principles

- **Fast response:** Hover/click feedback is immediate
- **Avoid deep menus:** Prefer popovers and contextual panels
- **Drag-friendly:** Visual ghost placement during reorder
- **Keyboard accessible:** Number keys, arrows, standard shortcuts

### Common Patterns

**Toggle Controls:**
- Large, obvious targets
- Clear on/off visual distinction
- Tooltip on hover

**Dropdowns:**
- Minimal, clean options list
- Grouped logically if many options
- Keyboard navigable

**Sliders/Parameters:**
- Large hit targets
- Visual range indicators
- Numeric input option

**Context Menus (Right-Click):**
- Quick actions (duplicate, delete, override)
- No more than 5-7 items
- Dangerous actions (delete) clearly marked

---

## Layout Principles

- **Grid-based:** 8px or 16px grid for alignment
- **Generosity:** Adequate whitespace prevents cramped feeling
- **Responsive nesting:** Expandable sections shouldn't overwhelm
- **Clear zones:** Visual separation between logical sections

---

## Feedback & Affordances

### Visual Feedback

- **Chord block movement:** Smooth animation from source to destination
- **Voice leading active:** Subtle glow or animation on block
- **Operator applied:** Visual indicator (badge, color shift)
- **Selection:** Clear border/background change

### Audio Feedback

- *(Future consideration)* Subtle click or tone for button presses during live performance

---

## Dark Mode Considerations

Primary design is dark UI. Light mode may be added in future phases.

---

## Accessibility

- **Color contrast:** WCAG AA minimum (4.5:1 for text)
- **Focus states:** Clear, visible keyboard focus indicator
- **Tooltips:** All controls have tooltips explaining function
- **Keyboard navigation:** All major workflows executable via keyboard
- **Semantic HTML:** Proper labels and ARIA attributes

---

## Brand in Motion

When appropriate, subtle animation reinforces brand attributes:

- **Quick, snappy transitions** – Playable, responsive feel
- **Smooth easing** – Not linear; feels musical
- **Avoid over-animation** – One animation per action
- **Performance first** – Animations don't stutter under load

---

## Related Documents

- [UI Patterns](../ui/ui-patterns.md) – Specific interaction designs
- [Voice Leading UX](../ui/voice-leading-ux.md) – Voice leading controls and feedback
- [Product Positioning](../../00-foundation/positioning.md) – Brand voice and positioning
