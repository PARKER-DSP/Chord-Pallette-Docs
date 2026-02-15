> **Archived (non-authoritative):** This file is retained for historical reference only. Use canonical pages from the main navigation for current guidance.

# Realtime Safety (starter)

## Rules
- No allocations in `processBlock`
- No locks/mutex on audio thread
- Preallocate event buffers and candidate arrays
- Use atomics or lock-free queues for UI↔audio thread communication

## Bounded work
- Cap voice leading candidates per trigger (e.g., 32–64)
- Prefer cache hits for common transitions
