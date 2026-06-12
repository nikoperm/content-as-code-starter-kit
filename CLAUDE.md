# Content-as-Code — Agent Instructions

> **You are working in a Content-as-Code strategy repository.**
> This is NOT a software codebase. It contains strategic documents, roadmaps,
> and organizational knowledge managed as code.

---

## 1. Navigation Protocol

### First Action — Always

**Read [CATALOG.md](CATALOG.md) before doing anything else.**
It is the living registry of every document in this workspace — your map.

### Finding Information

1. Check `CATALOG.md` for the document closest to your need
2. Read the document's YAML front-matter to understand status, purpose, and related docs
3. Follow `related:` links in front-matter to discover connected context

### Key Files by Topic

| Topic | Go to |
|:------|:------|
| What is this workspace? | `strategy/overview/executive_summary.md` |
| Strategic pillars & mission | `strategy/current_state/strategic_foundation.md` |
| Market data & position | `strategy/current_state/market_position.md` |
| Team structure & people | `strategy/current_state/team_architecture.md` |
| Operating model | `strategy/transformation/operating_model.md` |
| Growth areas & roadmaps | `strategy/roadmap/` |
| Presentation materials | `strategy/presentation/` |
| How we execute | `strategy/overview/execution_framework.md` |
| How Content-as-Code works | `docs/how_cac_works.md` |

---

## 2. Content Creation Rules

### Before Creating a New Document

1. **Check CATALOG.md** — does a document covering this topic already exist?
2. If yes → **update the existing document** instead of creating a new one
3. If no → proceed with creation using the template below

### Front-Matter Template (Required)

Every `.md` file in `strategy/` MUST start with this YAML header:

```yaml
---
title: "Document Title"
purpose: "One-sentence description of what this document provides"
status: draft | active | archived
version: "1.0"
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: human | agent | collaborative
domain: overview | current_state | transformation | presentation | roadmap
related:
  - strategy/path/to/related_doc.md
---
```

### Naming Conventions

| Element | Rule | Example |
|:--------|:-----|:--------|
| Folders | `snake_case`, lowercase | `current_state/` |
| Files | `snake_case`, lowercase, descriptive | `executive_summary.md` |
| No version suffix | Use front-matter `version` field | ~~`file_v1.md`~~ |
| Links | Always relative paths | `../overview/executive_summary.md` |

### Size Guidelines

- **Target**: Under 500 lines / 30KB per document
- **If larger**: Split into linked sub-documents
- **Exception**: Raw analysis archives in `reference/` may be larger

---

## 3. Content Update Rules

When modifying any document:

1. Update the `updated:` date in front-matter
2. If purpose or scope changed → run `make catalog` to update CATALOG.md
3. If new version → increment `version:` in front-matter
4. **Never delete content without archiving** — move superseded docs to an `_archive/` subfolder and set `status: archived`

### Anti-Bloat Rules

- **Never duplicate information** — link to the canonical source
- **Never use absolute file paths** — always relative from the linking file
- **Never leave placeholder content** (XXX, TBD, TODO) without a clear owner
- **Never create orphan files** — every document must be in CATALOG.md

---

## 4. Language Policy

- **All content**: Written in English
- **Norwegian text**: Allowed for direct quotes and team purpose descriptions
- **Mixed content**: When a document contains Norwegian quotes, provide English context around them

---

## 5. Domain Knowledge (Quick Reference)

These are demo values for learning purposes:

### Market Position (Demo Data)
- Revenue Market Share (RMS): **XX%**
- Subscription Market Share: **XX%**
- Total market: **X.X million** subscriptions
- ARPU: XXX NOK (example values)

### Strategic Direction
- Core challenge: Volume-based growth is slowing → shift to service-led value
- Service areas: **Security**, **Customer Solutions**, **Efficient Admin**, **Access**
- Transformation method: AI-first "Content as Code" + agentic teams

### Execution Model
- All initiatives are structured as **Business Opportunities (BOs)**
- BOs require: Customer Outcome, Value Proposition, Financial Targets, Milestones, Leading Indicators
- Success measured through: Customer Outcomes, Key Milestones, Leading Indicators

---

## 6. Available Skills

| Skill | When to use | Path |
|:------|:-----------|:-----|
| `strategy-review` | Reviewing, scoring, or critiquing strategy documents | `.agent/skills/strategy-review/SKILL.md` |
| `document-lifecycle` | Creating, updating, or archiving documents | `.agent/skills/document-lifecycle/SKILL.md` |
| `presentation-design` | Creating or modifying presentation materials | `.agent/skills/presentation-design/SKILL.md` |
| `workspace-health` | Validating workspace integrity (front-matter, catalog, links) | `.agent/skills/workspace-health/SKILL.md` |
| `quality-gate` | Promoting documents from draft to active status | `.agent/skills/quality-gate/SKILL.md` |
| `source-extractor` | Extracting insights from PDF reference documents | `.agent/skills/source-extractor/SKILL.md` |
| `changelog-generator` | Generating human-readable changelog from git history | `.agent/skills/changelog-generator/SKILL.md` |
| `decision-log` | Recording strategic decisions with context and rationale | `.agent/skills/decision-log/SKILL.md` |
| `ux-review` | Scoring and elevating presentation materials to 10/10 quality | `.agent/skills/ux-review/SKILL.md` |

---

## 7. What NOT to Do

- Do not create large monolithic documents (>500 lines)
- Do not duplicate information that exists in another document
- Do not use absolute file paths (`/Users/...`)
- Do not modify documents with `status: archived`
- Do not create files outside the defined folder structure
- Do not forget to update CATALOG.md after creating/modifying documents
- Do not overwrite without archiving the previous version first
- Do not leave front-matter fields empty or missing

---

## 8. Git Workflow

This is a **local-only** workspace. Git serves as your audit trail and undo mechanism.

### Commit Discipline

1. **Commit after logical units of work** — not after every file edit
2. **Run `make validate` before committing** — fix all ERRORs first
3. **Never force-push**

### Commit Message Format

Use `<type>: <description>` where type is one of:

| Type | When to use |
|:-----|:-----------|
| `feat` | New capability (skill, script, workflow) |
| `docs` | New strategy document |
| `data` | Financial data, market data, KPI updates |
| `review` | Strategy review results |
| `fix` | Fix integrity issues (front-matter, catalog, links) |
| `refactor` | Restructure without content change |

### Validation

Run `make validate` to check workspace integrity. This verifies front-matter, CATALOG.md sync, file sizes, placeholders, and broken links.

### Build

Run `make build` to generate HTML outputs in `build/`. Build after significant content changes to verify the presentation pipeline works.
