---
audience: contributors
status: canonical
owner: docs
last_reviewed: 2026-02-15
---

# Documentation Migration Summary

## Moved directories

- `docs/00-overview` → `docs/archive/legacy/00-overview`
- `docs/01-product` → `docs/archive/legacy/01-product`
- `docs/03-features` → `docs/archive/legacy/03-features`
- `docs/04-ux-brand` → `docs/archive/legacy/04-ux-brand`
- `docs/05-marketing` → `docs/archive/legacy/05-marketing`
- `docs/06-sales` → `docs/archive/legacy/06-sales`
- `docs/08-development` → `docs/archive/legacy/08-development`
- `docs/02-technical` → `docs/archive/legacy/02-technical`

## Merged into canonical locations

- `03-features/operators/operator-catalog.md` → `02-features/operators/operator-catalog.md`
- `05-marketing/copy/copy-vault.md` → `03-go-to-market/marketing/copy-vault.md`
- `06-sales/press-kit/press-kit.md` → `03-go-to-market/sales/press-kit.md`
- `08-development/market-strategy-report.md` → `03-go-to-market/market-analysis.md`
- `02-technical/architecture/ChordPallette_Architecture_Principles.md` → `01-developer/architecture/architecture-principles.md`

## Deprecated

All files under `docs/archive/legacy/` are deprecated and non-authoritative.

## Remaining TODOs

- Continue splitting oversized architecture docs into smaller deep-dive pages.
- Add periodic docs ownership review for `last_reviewed` metadata freshness.
