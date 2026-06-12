---
name: document-lifecycle
description: >-
  Governs how AI agents create, modify, archive, and maintain documents in the
  Content-as-Code workspace. Activates automatically when agents work with content.
  Ensures front-matter compliance, CATALOG.md updates, anti-duplication, and
  proper archival. Prevents content bloat and orphan files.
---

# Document Lifecycle Skill

## Purpose

This skill ensures that all AI agents follow a consistent, disciplined process when working with documents in a Content-as-Code workspace. It prevents the two most common failure modes:

1. **Content bloat** — documents growing too large, duplicating information, or existing without clear purpose
2. **Navigation decay** — the document catalog falling out of sync with actual files

---

## Protocols

### Protocol 1: Create a New Document

Before creating ANY new `.md` file in `strategy/`, follow these steps in order:

#### Step 1: Duplication Check
1. Read `CATALOG.md` (root of workspace)
2. Search for documents with overlapping purpose or domain
3. If a document already covers this topic → **UPDATE that document instead**
4. If creating a new document is justified → proceed

#### Step 2: Choose the Right Location

| Document Type | Folder | Examples |
|:-------------|:-------|:--------|
| Vision, strategy, frameworks | `strategy/overview/` | Executive summary, audit reports |
| Market data, team info, current metrics | `strategy/current_state/` | Market position, team architecture |
| Transformation plans, operating model | `strategy/transformation/` | Headcount plan, operating model |
| Presentations and slide companions | `strategy/presentation/` | Slide decks, speaker notes |
| Future plans, growth area roadmaps | `strategy/roadmap/` | Security roadmap, growth roadmap |

#### Step 3: Create with Front-Matter

Every document MUST begin with this YAML header:

```yaml
---
title: "Clear, Descriptive Title"
purpose: "One sentence explaining what this document provides and who it's for"
status: draft
version: "1.0"
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: human | agent | collaborative
domain: overview | current_state | transformation | presentation | roadmap
related:
  - strategy/path/to/related_doc.md
---
```

**Field rules:**
- `status`: `draft` → `active` → `archived` (lifecycle progression)
- `version`: Semantic — increment minor for updates, major for rewrites
- `author`: Use `collaborative` when both human and agent contributed
- `related`: Relative paths to documents that provide context or overlap

#### Step 4: Apply Naming Convention

- **Filename**: `snake_case`, lowercase, descriptive. No version suffixes.
  - Good: `market_position.md`
  - Bad: `Market_Position_v1.md`
- **Max size**: 500 lines / 30KB. If larger, split into linked sub-documents.

#### Step 5: Update CATALOG.md

After creating the file, run `make catalog` to regenerate CATALOG.md automatically.

---

### Protocol 2: Update an Existing Document

1. Read the document's front-matter — check `status`
   - If `status: archived` → **DO NOT MODIFY**. Create a new document instead.
2. Make your changes
3. Update `updated:` date in front-matter
4. If the document's purpose or scope changed → run `make catalog`
5. If this is a major rewrite → increment `version:` major number

---

### Protocol 3: Archive a Document

When a document is superseded or no longer current:

1. Create an `_archive/` subfolder in the document's parent directory (if it doesn't exist)
2. Move the document to `_archive/`
3. Set `status: archived` in front-matter
4. Run `make catalog` to update CATALOG.md
5. Update any documents that linked to it with the new path

**Rule**: Never delete documents. Always archive.

---

### Protocol 4: Link, Don't Duplicate

When you need to reference information that already exists in another document:

1. **Link to the canonical source** using relative paths
2. Provide a brief summary or context sentence, then link
3. **Never copy-paste content blocks** between documents

**Pattern:**
```markdown
For the full team structure, see [Team Architecture](../current_state/team_architecture.md).
```

---

### Protocol 5: Multi-Owner Documents

Documents in `strategy/roadmap/` are designed for multi-owner collaboration. Special rules apply:

1. **Section ownership**: Use HTML comments to mark section owners:
   ```markdown
   <!-- owner: @username -->
   ## Section Title
   Content...
   ```
2. **Conflict resolution**: If two agents/humans want to modify the same section, the `owner` listed in the comment has priority
3. **Change log**: Multi-owner documents should maintain a brief change log at the bottom:
   ```markdown
   ## Change Log
   | Date | Author | Change |
   |:-----|:-------|:-------|
   | 2026-06-12 | agent | Initial creation |
   ```

---

## Guardrails

### DO
- Check CATALOG.md before every create/update operation
- Use relative paths for all links
- Keep documents focused and under 500 lines
- Archive instead of delete
- Run `make catalog` after every structural change

### DO NOT
- Create files outside the defined folder structure
- Duplicate content that exists elsewhere
- Use absolute paths (`/Users/...`)
- Leave front-matter fields empty
- Modify archived documents
- Create orphan files (files not listed in CATALOG.md)
