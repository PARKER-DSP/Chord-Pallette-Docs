# Realtime Safety Constraints

## Core Rules

### No Allocations in `processBlock`
- All buffers and candidate arrays must be preallocated
- Use fixed-size containers or pre-sized vectors
- Do not use `new`, `malloc`, or dynamic resizing during audio processing

### No Locks/Mutexes on Audio Thread
- Avoid all blocking synchronization primitives
- Use atomics or lock-free queues for UI ↔ audio thread communication
- Keep audio thread paths interrupt-safe

### Preallocate Event Buffers and Candidate Arrays
- Voice leading candidates: max 32–64 per trigger
- MIDI event buffers: fixed size per processBlock
- Result caches: persistent, pre-sized

## Bounded Work

### Voice Leading
- Cap voice leading candidates per trigger (e.g., 32–64)
- Use simple cost function, not exhaustive search
- Prefer cache hits for common transitions
- Predictable runtime regardless of chord complexity

### Operator Chain
- Fixed number of operators per chain
- Each operator has bounded execution time
- No variable-length loops without iteration caps

### Bank Modifiers
- Apply in streaming fashion, not all-at-once
- Keep per-note operations minimal
- Cache results for repeated patterns

## Testing Realtime Safety
- Run under worst-case CPU load
- Use profiling tools to verify allocation-free paths
- Log audio thread violations in debug builds
- Never commit code that allocates on audio thread

## Isolation Strategy
- Keep heavy operations (plugin scanning, UI updates, file I/O) off audio thread
- Use message-thread callbacks for non-realtime work
- Background worker threads for async scans/loading
