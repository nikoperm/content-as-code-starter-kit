---
name: presentation-design
description: "Creates premium interactive HTML presentations with custom slide HTML. Uses the Telegrafen design system, Telenor brand assets, and Google I/O-level visual quality."
---

# Presentation Design Skill

## Core Principle

**You are the designer.** Do NOT use the template engine (`build_presentation.py`) for
premium presentations. Instead, write a complete self-contained HTML file with custom
CSS per slide. Each slide is a unique visual composition tailored to its content.

### Canonical references — read before every presentation

| Mode | Reference file | What to do |
|------|---------------|------------|
| **Narrative** | `presentations/internal/Strategy_2030_Narrative.html` | Study patterns, adapt structure |
| **AllMøte (governance)** | `.agent/skills/presentation-design/reference_allmote.html` | **Start from this file** for governance/BO decks. Full architecture with strategy chain, flywheel, popup overlays, and BO showcase cards. |
| **AllMøte (storytelling)** | `.agent/skills/presentation-design/reference_allmote_storytelling.html` | **Start from this file** for transformation/change narratives. Leaner structure with Chart.js axis breaks, click-to-reveal engine panels, zoom-in layers, photo statements, and roadmap cards. |

**AllMøte is architecturally different from Narrative** — it uses full-bleed triptychs, sub-stepping, cinematic dark mode, and interactive elements. You cannot "adapt" a Narrative into AllMøte; you must start from one of the AllMøte references above. Pick the one closest to your story.

### Reference documents (read on demand)

| File | What it covers |
|------|---------------|
| `references/allmote_patterns.md` | AllMøte animation system, sub-stepping, slide patterns, dark mode rules |
| `references/standard_content_slides.md` | Canonical strategic content (mission, pillars, chain, flywheel, triangle) |
| `references/layout_catalog.md` | All 36 layout types across modes |
| `references/slide_format_spec.md` | YAML directive reference for markdown presentations |
| `references/chart_spec.md` | Chart.js types, data format, macros |
| `references/narrative_patterns.md` | Narrative-specific slide patterns |
| `references/icon_catalog.md` | Available icons with use cases |
| `RATIONALE_NARRATIVE.md` | Why each Narrative design decision was made |

## When to Use

- User asks to create a presentation, slide deck, or slides
- User asks to visualize strategy content for a meeting
- User says "lag en presentasjon", "lag slides", or similar

---

## Workflow

### Step 1: Understand the ask

Clarify:
- **Audience**: Leadership (executive preread), strategy workshop (narrative), all-hands (allmøte)?
- **Source**: Which strategy documents to base it on?
- **Length**: How many slides? (Default: 8-12 for allmøte, 15-25 for narrative)
- **Language**: Norwegian or English?

### Step 2: Read source documents

Read the relevant strategy documents from `strategy/`. Extract:
- The governing thought (the ONE sentence)
- Hero numbers (the most compelling data)
- Evidence structure (what proves the point)
- Customer pain points (from battles/market data)

### Step 3: Design the story arc

**Narrative (15-25 slides):**
Title → Credibility → Problem → Customer Reality → Financial Truth →
Deep Dives (3-5 pillars) → Financial Breakdown → Solution → Operating Model →
Before/After → Timeline → [Photo Divider] → Closing Call to Action

**Executive preread:** Executive Summary → Situation → Complication → Resolution → Evidence → Recommendation

**AllMøte (8-12 slides):** Use the AllMøte workflow below — do NOT use the generic Step 4.

### Step 4: Write the HTML

**Narrative / Executive:** Write a single self-contained HTML file. Read the Narrative reference and `references/narrative_patterns.md` for slide patterns.

**AllMøte:** Skip this step entirely. See "AllMøte — Design Specification" below.

---

## Telegrafen Design Tokens

```css
:root {
    --tg-dark-blue:    #070452;
    --tg-mid-blue:     #1C16C5;
    --tg-telenor-blue: #00C8FF;
    --tg-blue:         #2954FF;
    --tg-light-cyan:   #EBFFFF;   /* Narrative content bg — NEVER for AllMøte */
    --tg-light-blue:   #B4FFFF;
    --tg-off-white:    #E8FDFF;
    --tg-white:        #FFFFFF;
    --tg-accent-green: #B0FBB8;
    --tg-accent-pink:  #FFB8D7;
    --tg-accent-yellow:#FEF6B8;
    --font: 'DM Sans', Arial, sans-serif;
}
```

### Colors — when to use what

| Color | Narrative | AllMøte |
|-------|-----------|---------|
| Light Cyan `#EBFFFF` | Default content bg | **NEVER** |
| Mid Blue `#1C16C5` | Title + statement slides | Primary bg + `.am-ambient` |
| Dark Blue `#070452` | Dramatic/legacy slides | Primary bg |
| Telenor Blue `#00C8FF` | Accent text, numbers | Accent, glowing highlights |
| Off-white `#E8FDFF` | Icon stages | Icon stages |

---

## Shared Patterns (all modes)

### HTML scaffold

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentation Title</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700;0,800;0,900;1,700;1,800;1,900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2"></script>
    <style>/* All CSS here */</style>
</head>
<body>
<div class="progress-bar" id="progress" style="width:5%"></div>
<div class="nav-counter" id="counter">1 / N</div>
<div class="nav-logo"><img src="../../reference/images/telenor_symbol_blue_RGB_Refresh.svg" alt="Telenor"></div>
<!-- Slides -->
<script>/* Navigation + Animation observer */</script>
</body>
</html>
```

Each slide is a `<div class="slide ...">` with 100vh height and `scroll-snap-align: start`.

### Animation system

Base entry animations — apply `.anim` to every visible element:

```css
.anim { opacity: 0; transform: translateY(24px);
    transition: opacity 0.7s cubic-bezier(0.16,1,0.3,1), transform 0.7s cubic-bezier(0.16,1,0.3,1); }
.anim.visible { opacity: 1; transform: translateY(0) scale(1); }
.anim-d1 { transition-delay: 0.12s; }  .anim-d2 { transition-delay: 0.24s; }
.anim-d3 { transition-delay: 0.36s; }  .anim-d4 { transition-delay: 0.48s; }
.anim-d5 { transition-delay: 0.60s; }
.anim-fade  { transform: none; }
.anim-scale { transform: translateY(16px) scale(0.96); }
```

Trigger via IntersectionObserver. Title slide: apply `.visible` immediately.

### Telegrafen vertical bands (title slide only)

4 straight vertical bands, dark to light. Never diagonal, never transparent.

### Photo dividers

Full-bleed photo with ken-burns zoom (1.06→1.0). Text uses `.hl` highlight boxes
(`background: var(--tg-dark-blue); box-decoration-break: clone`), NOT overlay divs.
Key words use `.accent` span for `color: var(--tg-telenor-blue)`.

### Typography rules

| Element | Size | Weight | Style |
|---------|------|--------|-------|
| Hero title | `clamp(3.5rem, 7vw, 7rem)` | 900 | italic |
| Section title | `clamp(2rem, 3.5vw, 3rem)` | 900 | italic |
| Governing thought | 1.1-1.25rem | 600-700 | normal |
| Body text | 0.92-1rem | 400-600 | normal |
| Kicker | 0.75-0.82rem | 800 | uppercase |
| Hero number | `clamp(7rem, 18vw, 14rem)` | 900 | italic |
| Caption | 0.78-0.82rem | 600-700 | normal |

Always italic for large display text. Always `letter-spacing: -1px` to `-3px` on large headings.
NEVER use font sizes below **0.82rem**.

### Icon sizing

| Context | Icon size | Background |
|---------|-----------|------------|
| Card icons | 64-80px | `var(--tg-off-white)`, border-radius 20px |
| Pillar grid (5-col) | 64px | `var(--tg-off-white)` |
| Before/after hero | 64px | color-tinted (red or cyan) |
| AllMøte triptych | 72-100px | none (white icons on dark bg) |

Never use icons smaller than 36px. Always use `var(--tg-off-white)` for icon stages on light slides.

### Brand photos

Read `reference/images/brand/INDEX.md` for full catalog. Key picks: DSCF5113 (hero landscape), Telenor.bedrift.70 (team culture), Telenor.bedrift.31 (customer interaction).

---

## AllMøte — Design Specification

> **CRITICAL: AllMøte is NOT "Narrative with fewer words."**
> It is a fundamentally different HTML architecture. You MUST start from
> `reference_allmote.html` — copy it, keep all CSS/JS, replace content.
> Never generate AllMøte from scratch or by adapting a Narrative presentation.
> Read `references/allmote_patterns.md` for the complete animation and interaction system.

### AllMøte workflow (replaces Step 4)

1. **Copy** `reference_allmote.html` to the target location
2. **Read** `references/allmote_patterns.md` for animation/interaction patterns
3. **Read** `references/standard_content_slides.md` for canonical strategic content
4. **Keep** all CSS and JavaScript — they contain the cinematic magic
5. **Replace** slide content — swap titles, numbers, text
6. **Select** which slide types to include (not every deck needs all 12)
7. **Verify** in browser — check animations, sub-stepping, fonts, icons

### What makes AllMøte structurally different

| Element | Narrative | AllMøte |
|---------|-----------|---------|
| Backgrounds | Light cyan gradients | 100% cinematic dark (`#070452`, `#1C16C5`, `.am-ambient`) |
| Layouts | Standard header/body template | Per-slide custom (triptych, chain, flywheel, triangle) |
| Animations | Fade-in stagger | Keyframes + sub-stepping + counter animations |
| Interactivity | Scroll only | Click-to-advance, flywheel, popup overlays |
| Title bars | Header at top | Floating highlight-box at bottom |
| Data | Charts with insight boxes | Single hero number with counter animation |

### Available AllMøte slide types

Pick from these — each has full CSS/HTML in the reference file:

| Slide type | CSS class | What it does |
|-----------|-----------|-------------|
| Title split | `.slide-title-split` | 65/35 grid with Telegrafen color bands |
| Dual stat | `.am-stat-slide` | Two hero numbers with counter animation |
| Problem triptych | `.s3-triptych` | 3 full-bleed panels (red accent) |
| Principles triptych | `.s4-triptych` | 3 full-bleed panels with icons |
| Strategy chain | `.slide-chain` | 7-column progressive reveal with sub-stepping + popups |
| BO showcase | `.slide-bo-showcase` | 2-panel kick-off card with click-to-reveal |
| Photo divider | `.slide-photo` | Full-bleed image with ken-burns + highlight-box text |
| Ceremony flywheel | `.slide-rhythm` | Interactive 5-node circle with detail cards |
| Capacity chart | `.slide-legacy-learn` | Chart.js stacked bar with summary bar |
| Before/after hero | `.slide-hybrid-teams` | Paradigm shift comparison with animated arrow |
| Collab triangle | `.slide-collab` | 3-actor relationship diagram with SVG animations |
| Commitments triptych | `.s10-triptych` | 3 full-bleed panels (blue gradient) |
| Closing charge | `.closing-layout` | Bold centered statement with accent divider |
| Transformation engine | `.slide-engine` | 3-panel triptych with click-to-green animation (from `reference_allmote_storytelling.html`) |
| Zoom-in layers | `.slide-zoom-in` | Bottom-up click-reveal of stacked horizontal layers |
| How-it-works flow | `.slide-how` | 4-step horizontal process with numbered cards and arrows |
| Roadmap phases | `.slide-roadmap` | 4 phase cards with active/done/future states |
| GP scenario chart | (inline) | Stacked bar + click-to-reveal line with axis break plugin |

### AllMøte narrative arc (8-12 slides)

**Act 1 — Hook:** Title (split bands) → Opener stat (hero number)
**Act 2 — Problem:** Market reality (1 stat/chart) → Customer voice (full-slide quote)
**Act 3 — Product:** Strategy headline → 2-3 pillar moments (icon + name + number)
**Act 4 — Transformation:** Before/after → Photo divider
**Act 5 — Call:** Team commitment (triptych) → Closing charge

### AllMøte language rules

- Write titles as spoken sentences: "Vi vokser fordi vi leverer mer verdi" (not "Strategisk vekst")
- Numbers in Norwegian format: "58,1 %" not "58.1%"
- Product names in original form: SafeZone, mPort, MBN

### What AllMøte inherits

- Telegrafen bands on title slide, `.hl` highlight boxes on photos, `clamp()` font sizes
- IntersectionObserver base animation (complemented by keyframes, not replaced)
- Fixed nav counter + progress bar + logo, DM Sans font, color tokens
- Chart animation with progressive delay per dataIndex

### What AllMøte does differently (never simplify away)

- **Start from `reference_allmote.html`** (or `reference_allmote_storytelling.html`) — never from Narrative or scratch
- **Full-bleed layouts** — `padding: 0; flex-direction: row; align-items: stretch`
- **Sub-stepping** — Click/keyboard reveals content within a slide before advancing
- **Popup overlays** — Full-screen backdrop-blur modals for deep-dives
- **Counter animations** — JavaScript easeOutQuart number reveals
- **Floating bottom title bars** — `position: absolute; bottom: 0` with highlight-box
- **Per-slide custom CSS classes** — `.s3-triptych`, `.slide-chain`, `.slide-collab`, etc.
- **Interactive elements** — Flywheel nodes, clickable columns, BO card reveals

---

## Quality Checklist

- [ ] Every slide has one clear focal point
- [ ] Correct backgrounds: light cyan for Narrative, dark for AllMøte
- [ ] Open layout preferred on light backgrounds (no unnecessary white cards)
- [ ] Key words/numbers highlighted in Telenor Blue
- [ ] Icons large (min 56px) with correct stage backgrounds
- [ ] Telegrafen bands on title slide only
- [ ] No per-slide footers — only fixed nav counter + logo + progress bar
- [ ] Charts have progressive animation and custom HTML legend
- [ ] All `.anim` classes applied with stagger delays
- [ ] Photo dividers use `.hl` boxes (not overlay)
- [ ] Typography: all text ≥ 0.82rem, large text italic weight 900
- [ ] Navigation works (arrow keys, space, home/end, F for fullscreen)
- [ ] AllMøte: sub-stepping and interactive elements functional
- [ ] All data grounded in source strategy documents

## What NOT to Do

- Do NOT use the template engine for premium presentations
- Do NOT use emoji icons — use Telenor SVG icons
- Do NOT use diagonal stripe elements — bands are straight vertical
- Do NOT use light backgrounds in AllMøte — cinematic dark mode only
- Do NOT skip animations — every slide needs entry animations
- Do NOT invent data — ground everything in source documents
- Do NOT use a photo overlay div — use `.hl` highlight boxes

---

## Grounding & Sources

- All facts and figures MUST come from `.md` files in `strategy/`
- Use `CATALOG.md` to find source documents
- Key data: `strategy/current_state/value_stream_snapshot.md`
- Brand photos: `reference/images/brand/INDEX.md`

## Bundling for email

Run `make bundle-html` to create a self-contained HTML file (~1.3 MB) with all fonts, scripts, and images inlined as base64.
