---
title: "Telegrafen Design Guidelines"
purpose: "Codifies the Telenor Telegrafen design system for all generated outputs (HTML, PDF, PPTX) in this workspace"
status: active
version: "1.1"
created: 2026-05-21
updated: 2026-05-22
author: collaborative
domain: overview
related:
  - strategy/overview/how_cac_works.md
  - strategy/overview/cac_template_architecture.md
---

# Telegrafen Design Guidelines

All HTML, PDF, and PPTX outputs generated from this workspace must comply with the Telenor Telegrafen design system. This document is the canonical reference.

## 1. Color Palette

### Primary Colors

| Token | Hex | CSS Variable | Usage |
|:------|:----|:-------------|:------|
| Dark Blue | `#070452` | `--tg-dark-blue` | Primary text on light backgrounds |
| Mid Blue | `#1C16C5` | `--tg-mid-blue` | Statement backgrounds, bold sections, chart containers |
| Telenor Blue | `#00C8FF` | `--tg-telenor-blue` | Primary accent, highlights, logo, links |
| Blue | `#2954FF` | `--tg-blue` | Secondary accent |
| Light Cyan | `#EBFFFF` | `--tg-light-cyan` | Light content backgrounds |
| White | `#FFFFFF` | `--tg-white` | Cards, content areas on colored backgrounds |
| Off White | `#E8FDFF` | `--tg-off-white` | Subtle backgrounds, alternate sections |

### Secondary Colors (use sparingly, amplify never dominate)

| Token | Hex | CSS Variable | Usage |
|:------|:----|:-------------|:------|
| Light Blue | `#B4FFFF` | `--tg-light-blue` | Soft highlights |
| Accent Cyan | `#ADFFFE` | `--tg-accent3` | Chart fills, subtle accents |
| Accent Green | `#B0FBB8` | `--tg-accent4` | Success states, growth indicators |
| Accent Yellow | `#FEF6B8` | `--tg-accent5` | Warnings, attention |
| Accent Pink | `#FFB8D7` | `--tg-accent6` | Decorative accents |

### Attention Grabbers (use only for CTAs and critical highlights)

| Token | Hex | Usage |
|:------|:----|:------|
| Hot Pink | `#FF2483` | Call-to-action buttons |
| Bright Yellow | `#FDE408` | Critical highlights |
| Vivid Orange | `#FF700A` | Urgent alerts |

### Forbidden Colors

These legacy values must NOT appear in any generated output:

- `#00193C` / `#001940` (old dark blue)
- `#00A9E0` (old light blue)
- `#0b132b` (old bg-primary)
- `#1c2541` (old bg-secondary)
- `#48cae4` (old accent-cyan)

## 2. Typography

### Font Stack

| Purpose | Font | Google Fonts Import | Weights |
|:--------|:-----|:-------------------|:--------|
| Headings | DM Sans | `DM+Sans:wght@400;500;700;800` | 700, 800 |
| Body | DM Sans | (same import) | 400, 500 |
| Code / Console | JetBrains Mono | `JetBrains+Mono:wght@400;500` | 400, 500 |
| PPTX | Telenor Evolution PPT | Via template | All weights |

**Fallback chain**: `'DM Sans', Arial, sans-serif`

DM Sans is the official web fallback for Telenor Evolution. Never use Outfit, Inter, or Calibri in generated outputs.

### Type Scale (for presentations/slides)

| Level | Size | Weight | Usage |
|:------|:-----|:-------|:------|
| Display | 3.2rem | 800 | Cover slide titles |
| H1 | 1.8rem | 700 | Slide section titles |
| H2 | 1.25rem | 700 | Card titles |
| Body | 0.9rem | 400 | Paragraph text |
| Caption | 0.75rem | 500 | Footer, labels, metadata |
| Code | 0.75rem | 400 | Console/code blocks |

## 3. Layout Patterns

### Slide Types

**Light Content** (default):
- Background: `#EBFFFF` (Light Cyan)
- Text: `#070452` (Dark Blue)
- Cards: `#FFFFFF` with `border-radius: 12px`
- Accent text: `#00C8FF` (Telenor Blue)

**Blue Statement** (emphasis/data):
- Background: `#1C16C5` (Mid Blue)
- Text: `#FFFFFF` (White)
- Cards: `#FFFFFF` with `border-radius: 12px` and dark text
- Used for: charts, key metrics, strong statements

**Dark Inset** (technical content):
- Background: `#070452` (Dark Blue)
- Text: `#FFFFFF` / `#B4FFFF`
- Used for: code blocks, console views, technical diagrams
- Always contained within a card on a light or statement slide

**Photo Divider**:
- Full-bleed image background
- Overlay box: `#1C16C5` with `#00C8FF` text
- Used sparingly for section breaks

### Spacing

All spacing follows an **8dp grid**: 8, 16, 24, 32, 48, 64, 96px.

CSS variable: `--tg-space-unit: 8px`

### Border Radius

| Size | Value | Usage |
|:-----|:------|:------|
| Small | 8px | Badges, tags, small elements |
| Medium | 12px | Cards, containers |
| Large | 16px | Feature cards, hero areas |
| Pill | 20px | Badges, status indicators |

## 4. Footer Standard

Every slide/page must include:

```
Left:  "Telenor Norge B2B Mobile  •  Strategi & Forretningsutvikling"
Right: [Telenor propeller SVG]  "Side N av M"
```

For external-facing materials, add: `"Sensitivity: Internal"` in the footer.

### Telenor Propeller SVG

```svg
<svg width="20" height="20" viewBox="0 0 24 24" fill="none">
  <circle cx="12" cy="12" r="2.5" fill="#00C8FF"/>
  <path d="M12 4c-1.5 0-3 1-3.5 2.5C10 7.5 11 9 12 10c1-1 2-2.5 3.5-3.5C15 5 13.5 4 12 4z" fill="#00C8FF"/>
  <path d="M20 12c0-1.5-1-3-2.5-3.5C16.5 10 15 11 14 12c1 1 2.5 2 3.5 3.5C19 15 20 13.5 20 12z" fill="#2954FF"/>
  <path d="M12 20c1.5 0 3-1 3.5-2.5C14 16.5 13 15 12 14c-1 1-2 2.5-3.5 3.5C9 19 10.5 20 12 20z" fill="#00C8FF"/>
  <path d="M4 12c0 1.5 1 3 2.5 3.5C7.5 14 9 13 10 12 9 11 7.5 10 6.5 8.5 5 9 4 10.5 4 12z" fill="#2954FF"/>
</svg>
```

## 5. Chart Styling

### Chart Containers

- Background: `#1C16C5` (Mid Blue) — always dark for contrast
- Text: `#FFFFFF` for labels, `#B0C4DE` for secondary
- Grid lines: `rgba(255, 255, 255, 0.1)`
- Tooltip background: `rgba(7, 4, 82, 0.95)`

### Data Series Colors

For categorical data, use these in order:
1. `#00C8FF` (Telenor Blue)
2. `#FFFFFF` (White)
3. `#2954FF` (Blue)
4. `#B0FBB8` (Accent Green)
5. `#FEF6B8` (Accent Yellow)
6. `#FFB8D7` (Accent Pink)

## 6. PDF-Safe CSS Rules

When generating HTML intended for PDF conversion (via Chrome headless):

**Never use:**
- `background-clip: text` / `-webkit-background-clip: text` (causes rendering artifacts in macOS Preview)
- `filter: drop-shadow()` on non-SVG elements
- `radial-gradient` on slide backgrounds
- CSS `@import` for critical fonts (use `<link>` instead)
- **Un-scoped `position: fixed` elements when mixing page margins**: Mixing different page margins (e.g., `margin: 0` for cover pages and `margin: 20mm` for content pages) with an un-scoped fixed/absolute element (like a footer) triggers Chrome's engine to downscale (shrink) the larger pages by ~81% to fit within the smaller margin boxes, introducing white margins. Always scope fixed elements using `page: [named-page];` or omit them entirely.
- **Running `position: fixed` footers in portrait flowing documents**: Fixed elements do not reserve layout height in normal HTML document flow, which causes normal flowing text to overlap with the footer. Avoid running footers in A4 flow documents unless utilizing complex page margin box hacks.

**Always use:**
- Solid `color` values instead of gradient text effects
- `print-color-adjust: exact` / `-webkit-print-color-adjust: exact`
- `@page { size: A4 landscape; margin: 0; }`
- Local HTTP server for font loading (not `file://` protocol)

## 7. PPTX Rules

- Always use `a .pptx template (not included in starter kit)` as the base template
- Use named layouts from the template, never blank slides
- Font: Telenor Evolution PPT (embedded in template)
- Colors come from theme — do not hardcode RGB values in shapes
- Slide dimensions: 13.33" x 7.50" (16:9)

## 8. Validation

Run `python scripts/validate_design.py` before committing changes to:
- Any file in `build/`
- `scripts/build_html.py` or `scripts/build_pptx.py`
- Any `.html` or `.css` file

The validator checks for forbidden colors, fonts, and CSS patterns.

## 9. A4 PDF Pagination, Sizing & Table Density Standards

To prevent layout breakages, fragmentation, and awkward empty gaps when compiling HTML documents to A4 portrait or landscape PDFs (e.g., using headless Chrome), follow these layout orchestration standards:

### A. Page Fragmentation & Orphan Prevention
- **Avoid Forced Breaks on Sub-headings**: Never apply CSS `page-break-before: always;` to lower-level subheadings (e.g., `<h3>`, `<h4>`, `<h5>`). This forces tiny sections onto separate pages, creating severe fragmentation.
- **Orphan Protection**: Ensure headings are never printed alone at the bottom of a page by keeping them bound to their starting block of text:
  ```css
  h1, h2, h3, h4, h5, h6 {
      page-break-after: avoid;
      break-after: avoid;
  }
  ```

### B. Table Break Orchestration (Break-Inside vs. Avoid)
- **Tall Multi-Row Tables (Deep-Dives, Roadmaps)**: When a table's height exceeds approximately 300px or half-page height, **do not** use `page-break-inside: avoid;` on the `<table>` element itself. This forces the entire table to the next page, leaving the preceding heading orphaned and creating vast blank gaps.
  - **Standard Pattern**: Allow the table to break between rows naturally, but keep individual rows intact:
    ```css
    table.long-table {
        page-break-inside: auto !important;
    }
    table.long-table tr {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
    }
    ```
- **Unified Short Tables/Dashboards (Calendars, Gantt)**: For cohesive, visual blocks like a 12-month calendar or a strategic Gantt chart that should never be separated across pages:
  - Wrap the section heading and the table/chart in a common container and prevent breaks:
    ```css
    .dashboard-container {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
    }
    ```

### C. Table Compression & Squeeze Optimization
When a unified layout must be fitted onto exactly one page alongside its heading:
- **High-Density Typography**: Reduce table text size and leading height to minimize vertical footprint:
  ```css
  .calendar-table td, 
  .calendar-table th {
      font-size: 0.75rem !important;
      line-height: 1.2 !important;
  }
  ```
- **Cell Padding Compression**: Standard padding of 12-16px is too loose for compact dashboards. Squeeze padding to:
  ```css
  .calendar-table td {
      padding: 5px 8px !important;
  }
  .calendar-table th {
      padding: 6px 8px !important;
  }
  ```
- **Label Simplification (Icon Badges)**: Avoid repeating verbose textual labels within tabular layouts (e.g., repeating `"Ceremony"` or `"Active"` inside a grid). Strip repetitive text and replace it with small, stylized CSS-styled icon-only badges:
  ```html
  <span class="ceremony-marker">🔺</span>
  <span class="activity-marker">▬▬</span>
  ```

### D. Relative Link Handling in PDF Outputs
- **The Issue**: Relative Markdown links (e.g., `[Security Strategy](../roadmap/security/security_strategy.md)`) are non-functional and broken when printed to a static PDF report, pointing out of the compiled document.
- **Standard Solution**: In the HTML compilation pipeline, convert local relative Markdown links into clean, non-clickable visual badges indicating references to related files. Use professional icons:
  - 📄 `[Document Name]` (with class `.local-ref-doc`) for related strategy files.
  - 📸 `[File/Image Name]` (with class `.local-ref-img`) for slide artifacts, visual models, or assets.
  - 🛠️ `[Tool Name]` (with class `.local-ref-tool`) for tools/systems.
  - **CSS Styling for Links**:
    ```css
    .local-ref-doc, .local-ref-img, .local-ref-tool {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background-color: #EBFFFF;
        color: #070452;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.85em;
        font-weight: 500;
        border: 1px solid #ADFFFE;
    }
    ```

## 10. Table & Semantic Content Standards

To maintain visual excellence, premium alignment, and professional layout standards across all strategic outputs (HTML, PDF), use the following standard designs for tabular structures and custom indicators:

### A. Core Table Elements & Styles
All standard tables in the workspace must use the Telegrafen-compliant styles below. Avoid browser defaults:
- **Header (`th`)**:
  - **Background**: `#070452` (Dark Blue) — provides a solid, authoritative base.
  - **Text Color**: `#FFFFFF` (White) with bold weight (`700`).
  - **Border Bottom**: `2px solid #00C8FF` (Telenor Blue, primary accent). This visual stripe anchors the table.
  - **Typography**: Font-size `0.78rem` to `0.8rem`, `text-transform: uppercase`, and `letter-spacing: 0.04em`.
  - **Alignment**: Left-aligned by default (use `text-align: center` only for short codes or numeric columns).
- **Cells (`td`)**:
  - **Padding**: `8px 12px` (standard density) or `5px 8px` (squeeze optimization).
  - **Border Bottom**: `1px solid #E2E8F0` (subtle slate grey).
  - **Text Color**: `#333333` (refined charcoal, much softer and more readable than pure black `#000000`).
  - **Vertical Alignment**: `top` (except for trackers/grids, which should be `middle`).
  - **Line-height**: `1.4` to `1.5`.
- **Alternating Zebra Rows (`tr`)**:
  - Zebra striping is mandatory for data readability. Even rows must use `#F8FAFC` as their background color.
  ```css
  tr:nth-child(even) td {
      background-color: #F8FAFC;
  }
  ```

### B. Grid Column Control
- **Explicit Widths**: Always specify percentage-based widths for every column in the CSS stylesheet (e.g., `.hierarchy-table th:nth-child(1) { width: 22%; }`). PDF rendering engines frequently collapse auto-layout columns, causing awkward wrapping and text truncation.
- **Center Alignment**: Numeric columns, statuses, or index numbers must be centered horizontally:
  ```css
  .data-column {
      text-align: center;
  }
  ```

### C. Semantic Content Indicators
Instead of relying on standard text or unstyled emojis, utilize these precise custom indicators to denote status, categories, and levels:
- **Professional Status Dots**: Replace colored emoji spheres (🟢, 🟡, 🔴) with clean, CSS-styled status circles. This guarantees crisp, cross-platform consistent vector shapes:
  - **Green (Success/Active)**: `#00D28A`
  - **Yellow (In Progress/Warning)**: `#FFC700`
  - **Red (Delayed/Critical)**: `#FF3B30`
  - **CSS Styling**:
    ```css
    .status-dot {
        display: inline-block;
        width: 9px;
        height: 9px;
        border-radius: 50%;
        margin-right: 6px;
        vertical-align: middle;
    }
    .status-dot.green { background-color: #00D28A; }
    .status-dot.yellow { background-color: #FFC700; }
    .status-dot.red { background-color: #FF3B30; }
    ```
- **Category & Level Badges**: Use rounded pill badges to highlight specific organizational hierarchy levels (e.g., `Level 1`, `Level 2`, `Level 3`) or classifications:
  - **Dark Badge**: Background: `#1C16C5` (Mid Blue), Text: `#FFFFFF` (White).
  - **Light Badge**: Background: `#EBFFFF` (Light Cyan), Text: `#070452` (Dark Blue).
  - **CSS Styling**:
    ```css
    .level-badge {
        background-color: #1C16C5;
        color: #FFFFFF;
        font-weight: 800;
        font-size: 0.72rem;
        padding: 2px 7px;
        border-radius: 4px;
        display: inline-block;
    }
    ```
