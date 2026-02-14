# Principles

## Product principles
- **Performance-first**: immediate output, no friction
- **Non-destructive**: edits are reversible and branchable
- **Musically smart**: decisions feel like a skilled player made them
- **Fast UI**: clear, minimal, tactile
- **Trustworthy**: predictable, stable, deterministic in realtime

## Engineering principles
- **RT-safe**: no allocation/locks on audio thread
- **Core library is JUCE-free**: portable + testable
- **Bounded complexity**: cap operator work per trigger
- **Cache everything**: smooth UI + stable performance
