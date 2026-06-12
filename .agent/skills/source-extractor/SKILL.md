---
name: source-extractor
description: >-
  Extracts structured insights from PDF source documents in reference/pdf/
  and produces machine-readable markdown files in strategy/insights/.
  Turns opaque PDFs into searchable, linkable content.
---

# Source Extractor Skill

## Purpose

PDF documents are opaque to AI agents — extracting their content into markdown makes the data searchable, linkable, and cross-referenceable. This skill defines the extraction process.

## When to Use

- When a new PDF is added to `reference/pdf/`
- When asked to extract data from a specific source document
- When a strategy discussion needs data that exists in a PDF but not yet in markdown

## Extraction Process

### Step 1: Read the PDF

Use multimodal capabilities to read the PDF content. For slide decks, focus on extracting data tables, financial figures, and key strategic statements.

### Step 2: Structure the Output

Create an insight file in `strategy/insights/` with this front-matter:

```yaml
---
title: "Insights: <Source Name> — <Topic>"
purpose: "Extracted insights from <source document name>"
status: active
version: "1.0"
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: agent
domain: insights
source_pdf: "reference/pdf/<filename>.pdf"
related:
  - strategy/path/to/relevant_doc.md
---
```

### Step 3: Content Structure

Organize extracted content into these sections:

1. **Source Summary** — One paragraph describing the document and its context
2. **Key Data Points** — Tables, figures, metrics extracted verbatim
3. **Strategic Insights** — Interpreted findings relevant to the strategy
4. **Cross-References** — Links to existing strategy documents that this data supports or challenges

### Step 4: Integration

1. Add the new insight file to `CATALOG.md` (run `make catalog`)
2. Update `related:` fields in any strategy documents that should reference this new data
3. Run `make validate`

## Quality Standards

- **Verbatim data**: Financial figures, KPIs, and metrics must be extracted exactly as stated in the source
- **Attribution**: Always note which page/slide a data point comes from
- **Norwegian content**: Extract in original language, provide English context around it
- **No invention**: Do not infer or estimate data that is not in the source document
- **Size limit**: Keep each insight file under 300 lines. Split into multiple files by topic if needed.
