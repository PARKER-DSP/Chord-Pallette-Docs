# UI Patterns

Specifications for key user interface components and interaction patterns in ChordPallette.

---

## Chord Bank Lane

The primary view showing all chords in a bank.

**Visual:**
- Horizontal scrolling lane of chord blocks
- Each block shows:
  - Chord symbol (e.g., "Cmaj7")
  - Voice leading indicator (if active)
  - Operator chain count (small badge)
  - Tags (optional, collapsed list)

**Interactions:**
- **Drag to reorder:** Visual ghost placement during drag
- **Multi-select:** Shift-click range, Ctrl-click toggle
- **Right-click:** Context menu (duplicate, delete, override VL, edit tags)
- **Double-click:** Open in block editor
- **Number keys (1-9):** Quick trigger for performance

**Performance:**
- Smooth reordering with ghost visual
- Quick context menu appearance
- No lag on large banks (100+ blocks)

---

## Chord Block Editor

Detailed editor for a single chord block.

**Sections:**
1. **Chord Info** (read-only or edit)
   - Chord symbol
   - Voicing details (notes, inversion, spread)
   - Nashville/Roman numeral notation (if applicable)

2. **Operator Chain Stack**
   - List of applied operators
   - Drag to reorder
   - Add operator (+ button → picker)
   - Remove operator (X or right-click)

3. **Live Audition**
   - Play button (trigger chord)
   - Note lock preveiusly
   - Sustain toggle

4. **Non-Destructive History** *(future)*
   - Undo states
   - Branch previews

---

## Mapping Panel

Controls for keyboard/MIDI trigger mapping and live performance setup.

**Sections:**
1. **Learn Mode Toggle**
   - Button: "Learn Mode ON/OFF"
   - Instruction: "Play notes to map chords"

2. **Split Ranges**
   - Visual piano roll showing mapped regions
   - Drag to adjust split boundaries
   - Right-click to edit mapping

3. **Trigger Visualization**
   - Current MIDI note(s) highlighted in real-time
   - Visual feedback of which chord zone is active

4. **Output Range Safety**
   - Visual bracket showing playable output range
   - Buttons to adjust (up/down octave)
   - Status: "X notes safe, 0 out of range"

---

## Voice Leading Control (Quick Toggle)

Minimal, prominent control in chord bank header.

```
Voice Leading: [ OFF ▼ ]
```

Click to reveal popover:
```
☐ OFF
☐ Smooth
☐ Cinematic
☐ Neo-Soul
☐ Classical
☐ EDM Stack
☐ Custom...
```

Selection applies instantly.

---

## Operator Picker

Modal/popover for selecting operators to add to a chord.

**Sections:**
1. **Search** – Filter operators by name/category
2. **Categories:**
   - Voicing (invert, drop2, spread, etc.)
   - Range (clamp, octave, etc.)
   - Harmony (borrowed, modal interchange, etc.)
   - Performance (strum, arpeggiate, humanize, etc.)
3. **Operator List** – Click to add; live preview on selection

---

## Quick Inline Edit

Minimal editing without full block editor.

- **Chord label:** Click to edit, Enter to save
- **Tags:** Click to add/remove tags
- **Voice leading override:** Right-click block → "Override Voice Leading"

---

## Piano Roll Visualization *(future)*

Visual display of chord voicing notes.

- Shows MIDI notes on keyboard
- Color-coded active notes
- Draggable notes in editor mode
- Optional: fingering hints for guitar/keys

---

## Preset/Bank Browser

Access and manage chord banks and presets.

- Folder tree on left
- File list on right
- Search across all banks
- Favorites/recents section
- New/rename/delete operations

---

## Key Interaction Principles

1. **Drag = Reorder** – Chord blocks and operators both reorder via drag
2. **Right-Click = Context** – Right-click reveals quick actions
3. **Double-Click = Edit** – Double-click opens detailed editor
4. **Popovers > Modals** – Prefer inline popover controls to full modals
5. **Number Keys = Trigger** – Quick access during performance

---

## Related Documents

- [Voice Leading UX](voice-leading-ux.md) – Detailed voice leading controls and feedback
- [Style Guide](../style-guide/style-guide.md) – Visual design and branding
