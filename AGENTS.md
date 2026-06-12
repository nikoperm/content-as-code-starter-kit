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

### Content Rules
- Every `.md` file in `strategy/` must have YAML front-matter (see CLAUDE.md §2)
- Never duplicate content — link to the canonical source
- Keep files under 500 lines
- Archive instead of delete

### Git
- Commit after logical units of work
- Run `make validate` before committing
- Use commit message format: `<type>: <description>`

## Skills

Agents should use the skills defined in `.agent/skills/` when performing specialized tasks. Each skill has a `SKILL.md` file that describes when and how to use it.

To invoke a skill: type `/<skill-name>` (e.g., `/presentation-design`, `/strategy-review`).

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
