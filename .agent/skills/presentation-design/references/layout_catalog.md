# Layout Catalog

All 36 layouts available in the presentation engine, organized by mode.
Each layout maps to a PPTX slide master layout for PowerPoint export.

---

## Executive-Only Layouts (6)

Used in `mode: executive` — designed for high-density, self-reading prereads.

### `briefing`
- **PPTX:** Title and Content
- **Purpose:** Standard content slide with action title, structured body text, and optional tables.
- **Visual elements:** Full-sentence action title at top; body fills the slide with sub-sections, bullet points, and tables.
- **When to use:** Default executive slide. Use for argument development, situation analysis, and any slide that needs structured prose with evidence.

### `executive-summary`
- **PPTX:** Long title and Content
- **Purpose:** Extended action title with condensed supporting content below.
- **Visual elements:** Two-line action title spanning full width; compact body with key metrics or summary bullets.
- **When to use:** Opening slide (slide 2) for the governing recommendation. Also for section summaries that capture the "so what?" in one view.

### `evidence-exhibit`
- **PPTX:** Title and Content
- **Purpose:** Chart or data visualization with takeaway box and source footnotes.
- **Visual elements:** Action title; annotated chart (inline or macro); insight callout box; source citation in footer.
- **When to use:** Any slide where a chart or data table IS the evidence proving the action title. The most common data slide in executive mode.

### `dual-analysis`
- **PPTX:** Two Content
- **Purpose:** Side-by-side comparison of two data sets, scenarios, or arguments.
- **Visual elements:** Action title; two equal columns, each with its own chart, table, or structured content.
- **When to use:** Before/after comparisons, scenario analysis (baseline vs. target), or contrasting two strategic options.

### `structured-argument`
- **PPTX:** Title and Content
- **Purpose:** Multi-level argument with numbered steps, sub-arguments, or a logical chain.
- **Visual elements:** Action title; numbered sections with indented supporting evidence; optional callout boxes.
- **When to use:** Complex arguments that require 3-4 sub-points, each with their own evidence. The "deep reasoning" slide.

### `appendix-detail`
- **PPTX:** Title and Content
- **Purpose:** Reference-grade detail for readers who want to go deeper.
- **Visual elements:** Smaller font sizes; dense tables; full data sets; multiple footnotes.
- **When to use:** Appendix slides with raw data, methodology notes, or detailed financial models.

---

## Narrative-Only Layouts (5)

Used in `mode: narrative` — designed for presenter-led strategic storytelling.

### `insight-chart`
- **PPTX:** Title and Content
- **Purpose:** Chart with insight annotation and key takeaway text.
- **Visual elements:** Insight-driven title; chart with annotation callout box; 2-3 sentence takeaway below or beside the chart.
- **When to use:** Default data slide in narrative mode. Use when a chart reveals an insight that advances the story.

### `story-build`
- **PPTX:** Long title and Content
- **Purpose:** Progressive narrative content that builds toward a conclusion.
- **Visual elements:** Provocative title; structured body with 2-3 content blocks; optional icon accent.
- **When to use:** Default non-data slide in narrative mode. For strategic arguments, context setting, and building toward a key insight.

### `context-split`
- **PPTX:** Content Image
- **Purpose:** Text content on one side, visual (icon, image, or chart) on the other.
- **Visual elements:** 60/40 split; text column with title and body; visual column with icon, chart, or illustrative content.
- **When to use:** Introducing context or framing a problem. The visual anchors attention while text provides substance.

### `key-finding`
- **PPTX:** Statement Soft
- **Purpose:** Single insight or finding presented as a bold statement.
- **Visual elements:** Large statement text (1-2 sentences); muted background; optional supporting data point.
- **When to use:** Pivotal moments in the narrative arc. The "aha" slide that makes the audience pause and reflect.

### `dashboard`
- **PPTX:** Numbers Panels
- **Purpose:** Multiple KPIs or metrics displayed as a panel grid.
- **Visual elements:** 3-6 metric cards with hero numbers, labels, and optional trend indicators.
- **When to use:** Status overview, KPI summary, or "where we stand" slides in the narrative.

---

## AllMote-Only Layouts (14)

Used in `mode: allmote` — designed for large-audience inspiration with high visual impact. **All AllMote layouts use dark backgrounds only** (`--tg-dark-blue`, `--tg-mid-blue`, `.am-ambient`, or full-bleed photo). Light cyan (`#EBFFFF`) is never used.

### `hero-statement`
- **PPTX:** Statement Dark
- **Purpose:** One bold statement fills the screen. Text IS the design.
- **Visual elements:** Display-size text (2-4rem); dark background; minimal or no additional content. Speaker notes carry detail.
- **When to use:** Default layout for AllMote. Opening statements, strategic declarations, provocative questions.

### `big-number`
- **PPTX:** Statement Dark
- **Purpose:** A single hero number dominates the slide.
- **Visual elements:** Number at 5-8rem; short label below (1 line); optional unit or delta indicator.
- **When to use:** Revenue milestones, market share, growth percentages. The audience "gets it" in 3 seconds.

### `dual-stat`
- **PPTX:** Statement Dark
- **Purpose:** Two hero numbers side by side with animated counters.
- **Visual elements:** Dark `.am-ambient` background. 2-column stat grid (max 1100px). Each stat: animated counter number (6-8.5rem, weight 900, italic, easeOutQuart animation from 0), cyan label (1.15rem), description paragraph. Numbers animate when slide enters view, reset on exit.
- **When to use:** Scale/context slides — team count + BO count, revenue + market share, or similar paired metrics.

### `title-split`
- **PPTX:** Title Slide
- **Purpose:** Opening title with vertical color band visual.
- **Visual elements:** Grid 65/35 split. Left: badge pill (date/event), massive title (clamp 4-7rem), logo area. Right: 4 vertical color bands (dark blue, cyan, light blue, white). Dark mid-blue background.
- **When to use:** Opening slide of AllMote presentations. Badge pill shows event name and date.

### `triptych`
- **PPTX:** Three Content Dark
- **Purpose:** Three equal full-bleed vertical panels, each with one bold idea.
- **Visual elements:** Full-viewport, no padding. Three flex panels with `::before` separator lines. Each panel: large italic title (2.5-6.5rem), optional icon (72-100px), accent divider (64×4px), description text (max 28ch). Panel colors progress across a gradient (e.g., three blues, or red for problems). Floating title bar at bottom with highlight-box text.
- **When to use:** Principles, problems, commitments — any set of exactly 3 parallel concepts.

### `chain-column`
- **PPTX:** Blank Dark
- **Purpose:** Progressive multi-column hierarchy with sub-stepping.
- **Visual elements:** Full-bleed columns (flex row, no padding). Dynamic chevron arrow at top grows as columns reveal. Each column: distinct background color, italic title, description or bullet list. Hero column in green with glow. Sub-stepping: columns hidden initially, revealed one by one via click/keyboard. Popup overlays triggered at specific steps.
- **When to use:** Strategy-to-execution chains, governance hierarchies, any left-to-right progressive model.

### `bo-showcase`
- **PPTX:** Two Content Dark
- **Purpose:** BO kick-off card with progressive detail reveal.
- **Visual elements:** Grid 1fr 1fr on `.am-ambient` dark background. Left card: solid dark blue, left-rounded, shows BO overview (tag, name, customer outcome, value, GP targets). Right card: glass effect, hidden initially, reveals on click with detailed milestones and indicators. Footer title bar at bottom.
- **When to use:** Showcasing a specific BO structure, governance introductions, "this is what a BO looks like" slides.

### `flywheel`
- **PPTX:** Blank Dark
- **Purpose:** Interactive circular process navigator.
- **Visual elements:** Grid layout (1.15fr + 1fr). Left: 5 circular nodes (170px) positioned on a dashed circle, center hub. Active node scales to 1.1 with cyan fill. Right: detail card with tag, title, frequency, description, bullet list. Arrow keys/clicks step through nodes. Step indicator shows current position.
- **When to use:** Ceremony cycles, process loops, any 4-6 step circular process.

### `collab-triangle`
- **PPTX:** Blank Dark
- **Purpose:** Three-actor relationship diagram around a central node.
- **Visual elements:** Central glowing node (pulsing `pulseGlow` animation). 3 cards at triangle vertices with distinct accent colors. SVG dashed lines with flow animation. Edge callout pills describing interactions. All on dark `.am-ambient` background.
- **When to use:** Governance triangles, stakeholder relationships, any three-party collaboration model.

### `before-after-hero`
- **PPTX:** Two Content Dark
- **Purpose:** Dramatic paradigm shift comparison with detail grid below.
- **Visual elements:** Grid 1fr auto 1fr. Before: transparent/muted, white text. After: white/gradient, 32px radius, deep shadow with ambient glow. Floating animated arrow between. Below: 3-column numbered change cards separated by thin horizontal line.
- **When to use:** Transformation slides, old-vs-new model, legacy-to-future state. More dramatic than standard `before-after` layout.

### `icon-showcase`
- **PPTX:** Blank Dark
- **Purpose:** 3-5 large icons with short labels, no prose.
- **Visual elements:** Icons at 56-80px arranged horizontally or in a grid; one-line label per icon; dark background.
- **When to use:** Presenting categories, capabilities, or pillars visually. Icons carry the narrative.

### `animated-reveal`
- **PPTX:** Title Only
- **Purpose:** Content appears in sequence through staggered animations.
- **Visual elements:** Title; content blocks that fade/slide in one by one; each block is a self-contained point.
- **When to use:** Building tension, revealing steps in a process, or creating "moments" during live delivery.

### `celebration`
- **PPTX:** Cards Soft
- **Purpose:** Recognition, wins, and team achievements.
- **Visual elements:** Cards with names/teams, achievement descriptions, optional photos or icons; warm accent colors.
- **When to use:** Mandatory in AllMote. Celebrate wins, recognize individuals, reinforce culture.

### `photo-impact`
- **PPTX:** Visual Content Mid
- **Purpose:** Full or large photograph with minimal text overlay and ken-burns zoom.
- **Visual elements:** Background image (`object-fit: cover`) with zoom from 1.06 to 1.0 on enter (1.8s transition). Text overlay at bottom with dark-blue highlight-box treatment. Use `.anim-fade` (no translate) for text.
- **When to use:** Team photos, event captures, or visual metaphors that create an emotional connection.

---

## Shared Layouts (11)

Available in all three modes. Visual treatment adapts based on mode and theme.

### `cards-grid`
- **PPTX:** Three Cards Dark
- **Purpose:** 2-4 content cards arranged in a grid.
- **Visual elements:** Cards with optional icon, title, body text, and accent color border.
- **When to use:** Presenting parallel items (growth pillars, product areas, team responsibilities).

### `chart`
- **PPTX:** Title Only
- **Purpose:** Generic chart slide (inline or macro).
- **Visual elements:** Title; chart canvas fills the content area; optional annotation.
- **When to use:** When an inline chart or macro chart is the sole content. For mode-specific chart treatment, prefer `evidence-exhibit` (exec), `insight-chart` (narrative), or `big-number` (allmote).

### `table`
- **PPTX:** Title and Content
- **Purpose:** Data table as the primary content.
- **Visual elements:** Title; full-width markdown table rendered with Telegrafen styling.
- **When to use:** Financial tables, comparison matrices, feature breakdowns.

### `two-column`
- **PPTX:** Two Content
- **Purpose:** Two equal content columns.
- **Visual elements:** Title; left and right columns with independent content.
- **When to use:** Side-by-side comparisons, parallel arguments, or dual content areas.

### `three-column`
- **PPTX:** Three Content
- **Purpose:** Three equal content columns.
- **Visual elements:** Title; three columns for categorized content.
- **When to use:** Three-pillar overviews, triple comparisons, or categorized lists.

### `numbers-panel`
- **PPTX:** Numbers Panels
- **Purpose:** 3-6 key metrics displayed as prominent number cards.
- **Visual elements:** Large numbers with labels arranged in a row or grid.
- **When to use:** KPI summaries, financial snapshots, or scorecard views.

### `comparison`
- **PPTX:** Two Content
- **Purpose:** Structured comparison with clear "vs." framing.
- **Visual elements:** Two columns with contrasting headers (e.g., "Current" vs. "Target", "Legacy" vs. "20:30").
- **When to use:** Strategic pivots, model comparisons, before/after without the dramatic AllMote treatment.

### `timeline`
- **PPTX:** Title and Content
- **Purpose:** Sequential phases or milestones along a time axis.
- **Visual elements:** Horizontal or vertical timeline with labeled phases, dates, and milestone markers.
- **When to use:** Roadmaps, phase plans, implementation sequences.

### `divider`
- **PPTX:** Divider Text Mid
- **Purpose:** Section break between major topics.
- **Visual elements:** Section title in large text; optional icon; optional subtitle. Minimal content.
- **When to use:** Between major sections of the deck (e.g., before "Growth Pillars", before "Transformation").

### `title-only`
- **PPTX:** Title Slide
- **Purpose:** Title/cover slide.
- **Visual elements:** Presentation title, subtitle, date, and branding.
- **When to use:** Opening slide of the deck, or section cover pages.

### `content-image`
- **PPTX:** Content Image
- **Purpose:** Content alongside a visual (icon, diagram, or image).
- **Visual elements:** Split layout with text on one side and visual on the other.
- **When to use:** Any slide requiring a visual anchor paired with explanatory text.

---

## Quick Reference: Layout by Mode

| Layout              | Executive | Narrative | AllMote |
|:--------------------|:---------:|:---------:|:-------:|
| briefing            | x         |           |         |
| executive-summary   | x         |           |         |
| evidence-exhibit    | x         |           |         |
| dual-analysis       | x         |           |         |
| structured-argument | x         |           |         |
| appendix-detail     | x         |           |         |
| insight-chart       |           | x         |         |
| story-build         |           | x         |         |
| context-split       |           | x         |         |
| key-finding         |           | x         |         |
| dashboard           |           | x         |         |
| hero-statement      |           |           | x       |
| big-number          |           |           | x       |
| dual-stat           |           |           | x       |
| title-split         |           |           | x       |
| triptych            |           |           | x       |
| chain-column        |           |           | x       |
| bo-showcase         |           |           | x       |
| flywheel            |           |           | x       |
| collab-triangle     |           |           | x       |
| before-after-hero   |           |           | x       |
| icon-showcase       |           |           | x       |
| animated-reveal     |           |           | x       |
| celebration         |           |           | x       |
| photo-impact        |           |           | x       |
| cards-grid          | x         | x         | x       |
| chart               | x         | x         | x       |
| table               | x         | x         | x       |
| two-column          | x         | x         | x       |
| three-column        | x         | x         | x       |
| numbers-panel       | x         | x         | x       |
| comparison          | x         | x         | x       |
| timeline            | x         | x         | x       |
| divider             | x         | x         | x       |
| title-only          | x         | x         | x       |
| content-image       | x         | x         | x       |
