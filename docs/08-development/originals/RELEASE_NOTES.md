# Release Notes

## Versioning Policy

This project uses semantic versioning (`MAJOR.MINOR.PATCH`) plus a release channel label (`Alpha`, `Beta`, `Stable`).

1. `Alpha`: feature development and rapid iteration.
2. `Beta`: feature-complete hardening; avoid compatibility-affecting changes.
3. `Stable`: production release with backward compatibility expectations.

Release process requirements:

1. Bump `project(... VERSION X.Y.Z ...)` in `CMakeLists.txt` before a release build.
2. Ensure `X.Y.Z` is greater than `Docs/LAST_RELEASED_VERSION.txt`.
3. Record release notes entry before publishing.
4. After publishing, update `Docs/LAST_RELEASED_VERSION.txt` to the shipped version.

## Unreleased

- Target: `0.3.1 - Alpha`
- Added detect-from-file workflow UI scaffolding:
  - settings toggle
  - drag/drop audio file load
  - waveform rendering
  - horizontal zoom
  - draggable/resizable selection bounds
- Hardened standalone lifecycle behavior:
  - startup now initializes to Init preset
  - explicit processor teardown path for cleaner shutdown/resource release
- Improved project governance:
  - AI agent rules now enforce version metadata consistency and CI test execution expectations.
- Added commit-level versioning enforcement:
  - commit gate script for local monotonic version checks
  - CI commit-range monotonicity check on pull requests
  - local pre-commit hook installer and hook entrypoint

## 0.2.0 - Alpha - 2026-02-12

- Introduced new plugin identity for side-by-side DAW registration.
- `PRODUCT_NAME`: `ChordPallette Alpha`.
- `COMPANY_NAME`: `Parker DSP`.
- `BUNDLE_ID`: `com.parkerdsp.chordpallette.alpha`.
- `PLUGIN_MANUFACTURER_CODE`: `PDSP`.
- `PLUGIN_CODE`: `CHPL`.
- Isolated settings and user presets into `AppData/Roaming/com.parkerdsp.chordpallette`.
- Added release version gate script and release CI workflow.
- Added DAW rescan/cache-clearing guide for side-by-side verification.

## 0.1.2 - Stable Baseline

- Previous baseline release before Alpha re-identification.
