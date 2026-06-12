---
name: quality-gate
description: >-
  Enforces the draft-to-active promotion process. A document can only move
  from status: draft to status: active when it passes a defined checklist.
  Prevents premature promotion and ensures every active document meets
  quality standards.
---

# Quality Gate Skill

## Purpose

This skill defines the "definition of done" — the explicit checklist a document must pass before promotion from `draft` to `active`.

## When to Use

- When asked to promote a document from draft to active
- When reviewing whether a document is ready for stakeholder consumption
- When a document has been in draft status for more than 2 weeks

## The Checklist

A document may be promoted from `draft` to `active` only when ALL of these are true:

### Metadata (automated — run `make validate`)

- [ ] `purpose:` field is not "TBD" or empty
- [ ] `title:` field is set
- [ ] `author:` field is set
- [ ] `domain:` field matches the folder location
- [ ] `version:` field is set
- [ ] File is under 500 lines
- [ ] File is listed in CATALOG.md

### Content (agent-assessed)

- [ ] No PLACEHOLDER, TBD, TODO, or XXX markers in the body
- [ ] At least one `related:` link to another document
- [ ] All internal links resolve to existing files
- [ ] Content is substantive — not just headers and placeholders

### Review (one of these)

- [ ] Reviewed by `strategy-review` skill with weighted score >= 7.0
- [ ] Reviewed and approved by a human (noted in commit message)

## Promotion Process

When all checks pass:

1. Change `status: draft` to `status: active` in front-matter
2. Update `updated:` to today's date
3. Run `make catalog` to update CATALOG.md
4. Commit with message: `docs: promote <filename> to active status`

## When Checks Fail

If a document fails any check:

1. List which checks failed
2. Propose specific fixes for each
3. Do NOT promote — keep as draft
4. If the human insists, note the override in the commit message

## Batch Promotion

When asked to "promote all documents that are ready":

1. Run `make validate` to get the baseline
2. For each draft document, evaluate the checklist
3. Present a summary: which are ready, which are not, and why
4. Promote only those that pass all checks
