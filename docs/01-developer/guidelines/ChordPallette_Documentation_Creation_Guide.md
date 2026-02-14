# ChordPallette — Documentation Creation Guide
_Last updated: 2026-02-14_

This guide ensures documentation always reflects the real codebase.

---

# 1. Documentation Categories
- Architecture
- Core Object Models
- Migration
- Serialization
- Operators
- Parameters
- Marketing

Never mix technical and marketing documentation.

---

# 2. Parameter Documentation Template
Name
Type
Default
Valid Range
Layer
Realtime Safe
Musical Explanation
Serialization Location

---

# 3. Operator Documentation
Must include:
- Purpose
- Algorithm
- Parameters
- Complexity
- Realtime safety
- Edge cases

---

# 4. Object Model Documentation
For each object:
- Purpose
- Relationships
- Lifecycle
- Serialization behavior
- Migration notes

---

# 5. Migration Documentation
Every schema change requires:
- Before example
- After example
- Reason
- Version bump

---

# 6. Enforcement Rules
When code changes:
- Update object docs
- Update parameter docs
- Update migration docs
- Update version numbers
Pull requests are invalid if docs are outdated.

---

# 7. AI Agent Documentation Rules
AI must:
- Update docs when changing schema
- Not invent undocumented parameters
- Verify examples match schema

---

# 8. Storage Structure
/docs
    /architecture
    /core-models
    /migration
    /serialization
    /operators
    /parameters
    /guides
    /marketing

---

# 9. Review Checklist
Before merge:
- Docs match code
- New parameters documented
- schemaVersion correct
- Migration included if needed

Documentation is part of the product.

---

End of Documentation Creation Guide.
