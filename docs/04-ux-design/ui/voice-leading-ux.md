---
audience: design
status: canonical
owner: design
last_reviewed: 2026-02-15
---

# Voice Leading UX

Detailed interaction design for voice leading controls and feedback.

---

## Primary Control: Global Style Toggle

Located in Chord Bank header, always visible.

```
Voice Leading: [ OFF ▼ ]
```

**States:**
- **OFF** – Voice leading inactive
- **Smooth, Cinematic, Neo-Soul, Classical, EDM Stack** – Active style
- **Custom** – User-defined style settings (advanced)

**Interaction:**
- Click to open style picker popover
- Select style to apply instantly to bank
- No additional configuration needed
- Voice leading activates immediately on next trigger

**Visual feedback:**
- Style name visible in button
- Subtle glow/animation when active
- No performance impact

---

## Secondary Controls (Collapsed by Default)

Expandable panel for power users who want fine-tuning.

```
Voice Leading Settings (toggle to expand)
  ├─ Movement tolerance: [Tight ────●──── Free]
  ├─ □ Preserve bass
  ├─ □ Preserve top note
  ├─ □ Allow voice crossing
  ├─ Max jump distance: [────●────]
  └─ Reset all changes (button)
```

**Interaction:**
- Click "Settings" to expand/collapse
- Slider adjustments apply in real time to preview
- Checkboxes toggle constraints
- "Reset" reverts to style defaults

**Visual feedback:**
- Settings panel slides open/closed
- Slider position reflects current value
- Checkbox states clearly indicated

---

## Real-Time Preview Feedback

As user triggers chords or adjusts settings:

### Motion Lines *(optional)*
- Subtle lines show note movement paths
- Only visible on active transitions
- Fade out after chord trigger completes

### Common Tone Highlight
- Shared notes between adjacent chords subtly glow
- Visual indication of what's being preserved
- Reduces cognitive load of understanding transitions

### Jump Distance Indicator *(optional)*
- Small arc or number shows max interval jumped
- Helps user understand movement characteristic of current style
- Visible on mouse-over or during playback

---

## Per-Block Override

Users can override bank-level style for specific chords.

**Right-click on chord block → "Override Voice Leading"**

Options:
```
☐ Inherit from bank (default)
☐ Smooth
☐ Cinematic
☐ Neo-Soul
☐ Classical
☐ EDM Stack
☐ Custom
☐ Disabled
```

**Visual indicator:**
- Block shows small badge if override active
- Tooltip on hover shows which style override

---

## Batch Application

Select multiple blocks → "Optimize Voice Leading" button

**Dialog:**
```
Batch Optimization

This will apply and preview voice leading
across all selected blocks in sequence.

[Preview] [Apply] [Cancel]
```

**Preview:**
- Shows visual diff of original vs. voice-led result
- User can toggle before/after view
- Shows which blocks change, which stay same

**Apply Options:**
- ☑ Apply non-destructively (preserves originals)
- ☑ Bake to new blocks (creates copies with voice leading frozen)
- ☐ Replace base chords (destructive; confirm dialog)

---

## Freeze / Lock-In

User clicks chord block → "Freeze Voice Leading"

**Confirmation:**
```
This will bake the current voice-led result
into a new base chord and remove voice leading.
This action cannot be undone (Undo still works).

[Freeze] [Cancel]
```

**Result:**
- Block's BaseChord updates to voice-led voicing
- Voice leading operator removed
- Original preserved in undo history
- Block now appears "fresh" to system

---

## Export Behavior

When exporting bank to MIDI:

```
Export Options

Export as:
○ Base chords (original voicings)
○ Voice-led result (current processing)
○ Frozen result (if any chords are frozen)

[Export] [Cancel]
```

Allows user flexibility in what gets exported.

---

## Feedback & Educational Hints

*Optional for Phase 2+*

When user applies voice leading for first time:

```
Voice Leading is now active for this bank!

✨ Each chord will smoothly transition from the previous one.
✨ You can override individual chords or adjust settings.
✨ Everything is non-destructive—experiment freely!

[Got it] [Learn more...]
```

Appears once, can be re-triggered from Help menu.

---

## Performance Feedback

Voice leading computation:
- **Instant:** For typical banks (<100 blocks), no visible delay
- **Large banks:** Shows subtle spinner if computation needed
- **Status:** "Voice leading active" indicator visible in header

---

## Troubleshooting & Help

Right-click chord block → "Help" → "Voice Leading Tips"

Common questions:
- "Why is this chord sounding different?"
- "How do I freeze/lock-in a voicing?"
- "Can I customize voice leading further?"
- "What does each style do?"

---

## Style Preview / Comparison

*Optional future feature*

User hovers over style option → See quick audio/visual preview.

```
Smooth: [Low-motion example chord progression plays]
Cinematic: [High-motion example chord progression plays]
```

Helps user choose appropriate style quickly.

---

## Status & Indicators

Always visible in chord bank header:

```
Voice Leading: [Smooth ▼]  ✨ Active on 24 blocks
```

Shows:
- Active style name
- How many chords have overrides
- If any chords are frozen

---

## Related Documents

- [Voice Leading Overview](../../02-features/voice-leading/overview.md) – Why voice leading matters
- [Voice Leading System Design](../../02-features/voice-leading/operator-pack-ux.md) – Technical architecture
- [UI Patterns](ui-patterns.md) – General UI interaction patterns
- [Style Guide](../style-guide/style-guide.md) – Visual design and brand
