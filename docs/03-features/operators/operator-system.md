# Operator System

Operators are modular transforms applied non-destructively.

## Types
- **Chord transforms**: voicing/inversion/spread/clamp/harmony
- **Event generators**: strum/arp/rhythm/melodic/humanize

## Design rules
- Operators never mutate BaseChord
- Any pitch change triggers redetection for accurate labels
- RT-safe subset must be bounded and allocation-free
