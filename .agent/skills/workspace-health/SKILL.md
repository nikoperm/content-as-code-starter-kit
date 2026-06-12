---
name: workspace-health
description: >-
  Validates workspace integrity: front-matter compliance, CATALOG.md sync,
  file size limits, placeholder detection, and broken links. Run after any
  structural change or before committing. Produces a health report with
  ERROR/WARNING/INFO classifications.
---

# Workspace Health Skill

## Purpose

This skill ensures that the Content-as-Code workspace remains structurally sound. It catches problems that accumulate silently: orphan files, broken catalog references, incomplete front-matter, oversized documents, and dangling links.

## When to Use

- **After creating or moving files**: Run full validation to catch CATALOG.md sync issues
- **After editing a document**: The PostToolUse hook runs quick validation automatically (Claude Code only)
- **Before committing**: Run `make validate` to confirm no ERRORs exist
- **On demand**: When asked to assess workspace health or fix integrity issues

## How to Run

### Full validation
```bash
make validate
# or directly:
python scripts/validate_workspace.py
```

### Quick single-file check (used by hooks)
```bash
python scripts/validate_workspace.py --quick --file strategy/roadmap/security/security_strategy.md
```

### Summary only
```bash
python scripts/validate_workspace.py --summary
```

## Understanding the Output

### Severity Levels

| Severity | Meaning | Action Required |
|:---------|:--------|:---------------|
| **ERROR** | Structural integrity broken — file missing, catalog out of sync | Must fix before committing |
| **WARNING** | Quality issue — incomplete metadata, oversized file, placeholder content | Should fix, may commit with note |
| **INFO** | Improvement opportunity — missing owners, optional fields | Fix when convenient |

### Check Categories

| Check | Severity | What It Validates |
|:------|:---------|:------------------|
| Front-matter presence | ERROR | Every `.md` in `strategy/` has `---` delimited YAML |
| Front-matter completeness | WARNING | Required fields (title, purpose, status, version, created, updated, author, domain) are non-empty and not "TBD" |
| CATALOG.md sync | ERROR | Every non-archived file is referenced in CATALOG.md |
| Phantom references | ERROR | Every CATALOG.md link points to an existing file |
| File size | WARNING | No file exceeds 500 lines (excluding `_archive/`) |
| Placeholder scan | WARNING | No PLACEHOLDER, TBD, TODO, XXX in active documents |
| Broken links | WARNING | Relative markdown links resolve to existing files |

## Fixing Common Issues

### "Not referenced in CATALOG.md"
Run `make catalog` to auto-regenerate, or add the file manually.

### "Phantom link: strategy/path/file.md does not exist"
The file was likely archived. Run `make catalog` to update automatically.

### "Front-matter field 'X' is 'TBD'"
Read the document content and write a real value for the field.

### "File has N lines (limit 500)"
Split the document into linked sub-documents. Create a new file for the largest section and link from the original.

## Exit Codes

- **0**: No ERRORs found (WARNINGs and INFOs are acceptable)
- **1**: One or more ERRORs found — must resolve before committing
