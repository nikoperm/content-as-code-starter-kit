# How Content-as-Code Works

> This document explains how the Content-as-Code (CaC) system works using a concrete example.
> Use it to onboard new team members or understand the system architecture.

---

## The Use Case

**Situation**: A leader asks for a presentation for a board meeting. The presentation should cover the Security roadmap and the headcount transformation. During the work, the agent discovers that some numbers are outdated and a new initiative was discussed last week but not yet documented.

**What happens** — step by step:

---

## Step 1: The Human Describes the Task

```
Human:  "Create a board presentation covering our Security roadmap
         and the headcount transformation. Focus on the three security
         initiatives and how we're freeing up capacity for growth."
```

The human writes this in natural language to the agent (Claude Code, Gemini/Antigravity, or Cursor). No technical knowledge required.

---

## Step 2: The Agent Navigates the Workspace

```
┌─────────────────────────────────────────────────────┐
│  Agent reads CLAUDE.md / AGENTS.md                  │
│  → "Read CATALOG.md before doing anything else"     │
│                                                      │
│  Agent reads CATALOG.md                              │
│  → Finds relevant documents:                        │
│     - strategy/roadmap/security/security_strategy.md │
│     - strategy/transformation/headcount_transformation.md │
│     - strategy/current_state/value_stream_snapshot.md│
│                                                      │
│  Agent follows related: links in front-matter        │
│  → Discovers additional context documents            │
└─────────────────────────────────────────────────────┘
```

The `CATALOG.md` is the agent's map. The `related:` links in front-matter create a navigable knowledge graph.

---

## Step 3: The Agent Discovers Issues

While reading the source documents, the agent notices:
- Security BO financial targets haven't been updated in 3 weeks
- A new "SOC Light" initiative was mentioned in the decision log but has no BO document

The agent reports this to the human before proceeding.

---

## Step 4: The Agent Creates Content

Using the `presentation-design` skill, the agent:

1. **Reads the skill** — `.agent/skills/presentation-design/SKILL.md` (defines slide patterns, colors, layout rules)
2. **Reads the design system** — `.agent/design_guidelines.md` (Telegrafen colors, typography)
3. **Generates HTML** — a self-contained slide deck with charts, icons, and animations
4. **Validates** — runs `make validate` to check all documents are consistent

---

## Step 5: Hooks Enforce Quality

Every time the agent edits a file, a **PostToolUse hook** in `.claude/settings.json` automatically runs:

```bash
python scripts/validate_workspace.py --quick --file <changed-file>
```

This catches problems immediately — missing front-matter, broken links, oversized files.

---

## Step 6: The Agent Commits

The agent creates a git commit with a structured message:

```
docs: create board presentation for Security roadmap and headcount transformation
```

Git serves as the audit trail. Every change is versioned, attributed, and reversible.

---

## The Architecture

```
┌────────────────────────────────────────────────────────────┐
│                      Human Intent                          │
│              "Create a presentation about X"               │
└───────────────────────────┬────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│                     AI Agent (Claude/Gemini/Cursor)        │
│                                                            │
│  1. Reads CLAUDE.md → understands the workspace rules      │
│  2. Reads CATALOG.md → finds relevant documents            │
│  3. Reads strategy/ documents → gathers content            │
│  4. Activates skill → follows SKILL.md procedures          │
│  5. Creates output → markdown, HTML, or both               │
│  6. Validates → hooks catch errors automatically           │
│  7. Commits → git audit trail                              │
└───────────────────────────┬────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│                    Workspace (this repo)                    │
│                                                            │
│  CATALOG.md ←→ strategy/ documents ←→ CLAUDE.md            │
│       ↕              ↕                    ↕                │
│  Auto-generated   Front-matter         Agent rules         │
│  from scripts     + related:           + skills            │
│                   links                                    │
└────────────────────────────────────────────────────────────┘
```

## Key Insight

The power of Content-as-Code is that **the agent doesn't need to be told how to work** — it reads the instructions (`CLAUDE.md`), follows the skills (`SKILL.md`), respects the guardrails (validation hooks), and creates output that fits the existing knowledge structure. The human only needs to describe *what they want*, not *how to do it*.
