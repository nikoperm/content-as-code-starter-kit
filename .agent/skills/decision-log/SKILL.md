---
name: decision-log
description: >-
  Tracks strategic decisions with context, rationale, alternatives considered,
  and impact. Prevents decision amnesia — the pattern where teams revisit
  the same questions because no one recorded why the last decision was made.
---

# Decision Log Skill

## Purpose

This skill fills the gap between identifying tradeoffs and recording which decisions were made and why. It captures decisions-as-they-happen.

## When to Use

- When a significant strategic choice is made during a session
- When the human says "we've decided to..." or "let's go with..."
- When an initiative is approved, rejected, or deprioritized
- When targets are changed
- When organizational changes are decided

## Decision Record Format

Append to `strategy/overview/decision_log.md`:

```markdown
### DEC-YYYY-NNN: [Decision Title]

- **Date**: YYYY-MM-DD
- **Context**: [Why this decision was needed — what triggered it]
- **Decision**: [What was decided, stated clearly]
- **Alternatives considered**:
  - [Option A — rejected because...]
  - [Option B — rejected because...]
- **Impact**: [What changes as a result — which documents, initiatives, or teams are affected]
- **Owner**: [Who is responsible for executing this decision]
- **Review date**: [When to revisit — empty if permanent]
```

## Decision Numbering

Format: `DEC-YYYY-NNN` where:
- `YYYY` = year (e.g., 2026)
- `NNN` = sequential number within the year, zero-padded

To find the next number, read the last entry in `strategy/overview/decision_log.md`.

## What Qualifies as a Decision

| Qualifies | Does NOT Qualify |
|:----------|:----------------|
| New initiative approved or rejected | Content edits within a document |
| Financial target changed | Formatting or structural improvements |
| Growth area prioritized/deprioritized | Agent skill additions |
| Organizational change (team, headcount) | Bug fixes or integrity repairs |
| Technology/vendor choice | Routine updates to existing data |
| Strategy pivot or direction change | Meeting notes without decisions |

## Cross-Referencing

After logging a decision:
1. Update any affected documents with a reference: `(see DEC-YYYY-NNN)`
2. If the decision affects other documents, update their `related:` fields
