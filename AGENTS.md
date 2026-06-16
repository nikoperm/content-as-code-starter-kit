# Content-as-Code — Multi-Agent Instructions

> This file provides instructions for all AI agents working in this workspace,
> regardless of platform (Claude Code, Antigravity/Gemini, Cursor, etc.).
> For Claude-specific hooks and settings, see `.claude/settings.json`.

---

## Core Principle

This is a **Content-as-Code** repository. Strategic documents are managed with the same discipline as software code: version control, automated validation, structured metadata, and machine-readable formats.

## Agent Behavior

### First Action — Always
Read `CATALOG.md` before doing anything else. It is the living registry of every document.

### Navigation
1. Check `CATALOG.md` for the document closest to your need
2. Read the document's YAML front-matter to understand status, purpose, and related docs
3. Follow `related:` links in front-matter to discover connected context

### Key Files by Topic

| Topic | Go to |
|:------|:------|
| What is this workspace? | `strategy/overview/executive_summary.md` |
| Strategic pillars & mission | `strategy/current_state/strategic_foundation.md` |
| Market data & position | `strategy/current_state/market_position.md` |
| Products & services (what they are) | `strategy/current_state/service_catalog.md` |
| Business Opportunities (all) | `strategy/current_state/value_stream_snapshot.md` |
| Operating model | `strategy/transformation/operating_model.md` |
| Presentation materials | `presentations/INDEX.md` |
| How we execute | `strategy/overview/execution_framework.md` |
| How Content-as-Code works | `docs/how_cac_works.md` |

### Content Rules
- Every `.md` file in `strategy/` must have YAML front-matter (see CLAUDE.md section 2)
- Never duplicate content — link to the canonical source
- Keep files under 500 lines
- Archive instead of delete
- If a presentation is created, renamed, or deleted — update `presentations/INDEX.md`

### Strategic Grounding

Every proposal, BO, roadmap item, or presentation must be grounded in the actual strategy documents. Before creating anything strategic:

1. Read the source documents listed in CLAUDE.md section 5
2. Never invent market data or financial numbers — use what exists in the repo
3. Never propose initiatives that contradict the strategic direction
4. Separate internal facts from external benchmarks — always label the source
5. Check `value_stream_snapshot.md` before proposing new BOs — build on existing ones

### Demo Mode

Demo and prototype content goes in `temp/` (gitignored). Use real data from the repo, follow the same skills as production.

### Git
- Commit after logical units of work
- Run `make validate` before committing
- Use commit message format: `<type>: <description>`

## Skills

Agents should use the skills defined in `.agent/skills/` when performing specialized tasks. Each skill has a `SKILL.md` file that describes when and how to use it.

To invoke a skill: type `/<skill-name>` (e.g., `/presentation-design`, `/strategy-review`, `/bo-builder`).

## Validation

After any structural change (file create, move, archive), run:
```bash
make validate
```

This checks front-matter compliance, CATALOG.md sync, file sizes, and broken links.

## Design System

This workspace uses the **Telegrafen** design system for all visual outputs.
See `.agent/design_guidelines.md` for the full specification including colors,
typography, and layout patterns.
