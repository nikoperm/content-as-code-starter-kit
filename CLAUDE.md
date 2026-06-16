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
| Products & services (what they are) | `strategy/current_state/service_catalog.md` (create this for your own products) |
| Team structure & people | `strategy/current_state/team_architecture.md` |
| Business Opportunities (all) | `strategy/current_state/value_stream_snapshot.md` |
| Operating model | `strategy/transformation/operating_model.md` |
| Growth areas & roadmaps | `strategy/roadmap/` |
| Presentation materials | `presentations/INDEX.md` |
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
5. If a presentation is created, renamed, or deleted → update `presentations/INDEX.md`

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

## 5. Strategic Grounding — Mandatory Before Creating Content

> **Every proposal, BO, roadmap item, or presentation you create must be grounded
> in the actual strategy.** Never generate generic business content. Never invent
> market data. Never propose initiatives that contradict the strategic direction.

### Before You Create Anything Strategic

Read these documents first — they are the source of truth:

| What you need | Read this |
|:--------------|:----------|
| The strategic direction and why | `strategy/overview/executive_summary.md` |
| The strategic pillars and mission | `strategy/current_state/strategic_foundation.md` |
| Market data, ARPU, base numbers | `strategy/current_state/market_position.md` |
| What each product/service is (and is not) | `strategy/current_state/service_catalog.md` |
| All existing BOs and their targets | `strategy/current_state/value_stream_snapshot.md` |
| How we execute (BO framework) | `strategy/overview/execution_framework.md` |
| Financial calculation rules | `strategy/roadmap/bo_calculation_guide.md` |

**Do not skip this step.** The quick reference below is a memory aid — not a substitute for reading the documents.

### Strategic Principles You Must Follow

1. **Volume-based growth is dead.** Shift to service-led value. Never propose initiatives that compete on price or volume alone.
2. **Value for the organization = new revenue streams.** SaaS upsell, platform fees, high-margin services. Never frame value as "cutting the customer's costs" — that cannibalizes your own ARPU.
3. **All initiatives are BOs.** Every strategic proposal must be structured as a Business Opportunity with all 6 fields filled (see `/bo-builder` skill).
4. **Use real numbers first — and verify your understanding.** If the repo states a total, use that — do not add up sub-components to derive your own. If you need a number that does not exist in the repo, you may calculate it, but you must **stop and ask the user**: explain how you arrived at the number, ask if you understood the data correctly, and get confirmation before using it in any document or presentation.
5. **Separate internal facts from external benchmarks.** Numbers from your repo are facts. Numbers from internet research are benchmarks. Never present a benchmark as an internal metric. Always label the source: "According to [competitor]..." or "Industry benchmark:".
6. **Respect what exists.** Before proposing something new, check `value_stream_snapshot.md` — does a similar BO already exist? If yes, build on it.

### Quick Reference (memory aid — verify against source docs)

These are **placeholder values** for the starter kit. Replace them with your organization's real data:

| Fact | Value | Source |
|:-----|:------|:-------|
| Revenue Market Share (RMS) | XX% | `market_position.md` |
| Subscription Market Share | XX% (XXX,XXX subscriptions) | `market_position.md` |
| Total market | X.X million subscriptions | `market_position.md` |
| ARPU | XXX NOK | `market_position.md` |
| Service areas | Your defined pillars (e.g., Security, Solutions, Access) | `strategic_foundation.md` |
| Transformation method | AI-first Content-as-Code + agentic teams | `executive_summary.md` |
| Execution model | Business Opportunities (BOs) with 6 required fields | `execution_framework.md` |

---

## 6. Available Skills

| Skill | When to use | Path |
|:------|:-----------|:-----|
| `strategy-review` | Reviewing, scoring, or critiquing strategy documents | `.agent/skills/strategy-review/SKILL.md` |
| `document-lifecycle` | Creating, updating, or archiving documents | `.agent/skills/document-lifecycle/SKILL.md` |
| `presentation-design` | Creating or modifying presentation materials | `.agent/skills/presentation-design/SKILL.md` |
| `bo-builder` | Creating and validating Business Opportunities | `.agent/skills/bo-builder/SKILL.md` |
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
- Do not create files outside the defined folder structure (exception: `temp/` for demos)
- Do not forget to update CATALOG.md after creating/modifying documents
- Do not overwrite without archiving the previous version first
- Do not leave front-matter fields empty or missing

---

## 8. Demo Mode (`temp/`)

When creating demo or prototype content (live demos, proof-of-concepts, mockups):

- **Output to `temp/`** — this folder is in `.gitignore` and will not pollute the repo
- **Use real data from the repo** — read `market_position.md`, `value_stream_snapshot.md`, etc. Never invent baseline numbers
- **Follow the same skills as production** — use `/bo-builder` for BOs, `/presentation-design` for presentations
- **Never use `build_presentation.py` for premium demos** — write custom self-contained HTML directly (see presentation-design skill)
- **BO documents must follow the exact 6-field template** from the bo-builder skill — this is the whole point of demonstrating Content-as-Code

---

## 9. Git Workflow

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
