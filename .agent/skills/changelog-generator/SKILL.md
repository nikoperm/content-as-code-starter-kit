---
name: changelog-generator
description: >-
  Generates a human-readable changelog from git history, grouped by
  strategic domain and change type. Answers "what changed since last time?"
  without requiring git knowledge.
---

# Changelog Generator Skill

## Purpose

When someone asks "what changed since last week?" or "what's new?", the answer should be in strategic language, not git diffs. This skill translates git history into a meaningful summary.

## When to Use

- When asked "what changed?" or "what's new?"
- Before a strategy meeting or review
- When onboarding someone who has been away
- Run `make changelog` for the default weekly view

## How to Generate

### Step 1: Read Git History

```bash
git log --format="%H|%ad|%an|%s" --date=short --since="<date>" -- strategy/
```

Use `--since` to scope the timeframe (default: 7 days).

### Step 2: Categorize Changes

Group commits by type (from the commit message prefix):

| Prefix | Category | Display As |
|:-------|:---------|:-----------|
| `docs:` | New content | "New documents" |
| `data:` | Data updates | "Data updates" |
| `review:` | Strategy reviews | "Reviews completed" |
| `fix:` | Integrity fixes | "Quality improvements" |
| `feat:` | New capabilities | "Platform improvements" |
| `refactor:` | Restructuring | "Restructuring" |

### Step 3: Group by Domain

Map changed files to strategic domains:

| Path Pattern | Domain |
|:-------------|:-------|
| `strategy/roadmap/security/` | Security |
| `strategy/roadmap/customer_solutions/` | Customer Solutions |
| `strategy/transformation/` | Transformation |
| `strategy/overview/` | Strategy & Vision |
| `strategy/presentation/` | Presentation |
| `strategy/current_state/` | Current State |
| `.agent/`, `scripts/` | Platform |

### Step 4: Format Output

```markdown
## Changelog: [start date] — [end date]

### Security
- Updated targets and milestones

### Transformation
- Added new operating model document

### Platform
- Added new skill
- Improved validation

---
*Generated from N commits by M contributors*
```

## Output Options

- **Console**: Print to terminal (default with `make changelog`)
- **File**: Write to `CHANGELOG.md` at project root (with `--save` flag)
- **Timeframe**: `--since=2026-05-01` or `--days=7`
