> **Archived (non-authoritative):** This file is retained for historical reference only. Use canonical pages from the main navigation for current guidance.

# Data Model (starter)

This document defines the canonical objects and their responsibilities.

## Objects
- **ChordBase**: immutable pitch set + detection provenance
- **ChordBlock**: base chord + operator chain + tags + caches
- **ChordBank**: ordered blocks + bank modifiers + mapping profile
- **KeyswitchBlock**: separate lane merged late; bypasses chord ops
- **ChordResult**: derived chord after operators + modifiers

> Keep this synced with implementation types.
