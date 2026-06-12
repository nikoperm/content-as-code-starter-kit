# Content-as-Code Starter Kit

A ready-to-use workspace for learning **agentic development** with AI agents managing strategic documents as code. Built for use with [Claude Code](https://claude.ai/claude-code), [Antigravity](https://antigravity.ai), [Cursor](https://cursor.sh), or any AI-powered development environment.

## What is Content-as-Code?

Content-as-Code applies software engineering discipline to strategic documents:

- **Markdown files** with YAML front-matter (structured metadata)
- **Git version control** for history and audit trail
- **Automated validation** (front-matter, broken links, file sizes)
- **AI agent skills** for document creation, review, and presentation design
- **Auto-generated catalog** that keeps navigation in sync with content

## Get Started in 5 Minutes

### Option 1: Clone from GitHub

```bash
git clone https://github.com/nikoperm/content-as-code-starter-kit.git
cd content-as-code-starter-kit
make setup
```

### Option 2: One-command install (no GitHub account needed)

```bash
curl -fsSL https://raw.githubusercontent.com/nikoperm/content-as-code-starter-kit/main/install.sh | bash
```

### Then open in your AI agent IDE:

```bash
# Claude Code
claude

# Or open the folder in Cursor, Antigravity, etc.
```

### Try these commands:

```
/presentation-design    → Create a beautiful HTML presentation
/strategy-review        → Score and critique a strategy document
/workspace-health       → Run a full workspace validation
/changelog-generator    → See what changed recently
make validate           → Check workspace integrity
make build              → Generate HTML outputs
```

## What's Inside

```
content-as-code-starter-kit/
├── CLAUDE.md              ← Agent instructions (read by AI automatically)
├── AGENTS.md              ← Multi-agent coordination rules
├── CATALOG.md             ← Auto-generated document registry
├── Makefile               ← Build, validate, and manage commands
│
├── .agent/skills/         ← 9 reusable AI skills
│   ├── presentation-design/   → Premium HTML presentations
│   ├── strategy-review/       → 8-dimension scoring framework
│   ├── ux-review/             → Presentation quality evaluation
│   ├── document-lifecycle/    → Create, update, archive documents
│   ├── workspace-health/      → Validation and integrity checks
│   ├── quality-gate/          → Draft → active promotion
│   ├── changelog-generator/   → Git history → human-readable summaries
│   ├── decision-log/          → Track strategic decisions
│   └── source-extractor/      → Extract insights from PDFs
│
├── strategy/              ← Demo strategy documents
│   ├── overview/              → Vision, frameworks, decisions
│   ├── current_state/         → Market position, teams, initiatives
│   ├── transformation/        → Operating model, headcount plans
│   ├── presentation/          → Demo slide deck
│   └── roadmap/               → Service area strategies
│
├── reference/icons/       ← 69 SVG icons for presentations
├── scripts/               ← Validation, catalog, and build scripts
└── .claude/settings.json  ← Hooks & permissions for Claude Code
```

## Key Concepts to Learn

### 1. Agent Instructions (CLAUDE.md)
The AI agent reads `CLAUDE.md` on every session start. It defines how the agent navigates, creates content, handles git, and which skills to use. This is the "operating system" for your AI assistant.

### 2. Skills (.agent/skills/)
Skills are reusable AI procedures — codified expert knowledge. Each `SKILL.md` file tells the agent *when* to activate, *how* to execute, and *what guardrails* to follow. Type `/<skill-name>` to invoke.

### 3. Front-Matter Metadata
Every strategy document starts with YAML metadata (title, purpose, status, version, etc.). This enables automated cataloging, validation, and cross-referencing.

### 4. Automated Validation
A PostToolUse hook in `.claude/settings.json` runs validation after every file edit. The validation script checks front-matter, catalog sync, file sizes, and broken links.

### 5. Design System (Telegrafen)
The presentation skills use a design system with defined colors, typography, and layout patterns. See `.agent/design_guidelines.md`.

## Learning Path

1. **Explore**: Read `CATALOG.md`, browse the strategy documents
2. **Create**: Ask the agent to create a new strategy document
3. **Review**: Use `/strategy-review` to score a document
4. **Present**: Use `/presentation-design` to create a slide deck
5. **Validate**: Run `make validate` and fix any issues
6. **Decide**: Use `/decision-log` to record a strategic decision
7. **Extend**: Create your own skill in `.agent/skills/`

## Requirements

- Python 3.9+
- Git
- An AI-powered IDE (Claude Code, Antigravity, Cursor, etc.)

## License

MIT — use freely for learning and building your own Content-as-Code workspaces.
