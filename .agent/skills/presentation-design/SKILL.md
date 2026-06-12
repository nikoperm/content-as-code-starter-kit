---
name: presentation-design
description: >-
  Creates premium interactive HTML presentations by writing custom slide HTML
  directly. Uses the Telegrafen design system, Telenor brand assets (icons,
  photos, logo), and Google I/O-level visual quality. The agent is the
  designer — each slide is a unique visual composition, not a template output.
---

# Presentation Design Skill

## Core Principle

**You are the designer.** Do NOT use the template engine (`build_presentation.py`) for
premium presentations. Instead, write a complete self-contained HTML file with custom
CSS per slide. Each slide is a unique visual composition tailored to its content.

The canonical reference is `presentations/internal/Strategy_2030_Narrative.html` —
read it before every presentation. It is the gold standard and the source of all
patterns documented here.

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
- **Length**: How many slides? (Default: 8-12 for allmøte, 15-25 for executive narrative)
- **Language**: Norwegian or English?

### Step 2: Read source documents

Read the relevant strategy documents from `strategy/`. Extract:
- The governing thought (the ONE sentence)
- Hero numbers (the most compelling data)
- Evidence structure (what proves the point)
- Customer pain points (from battles/market data)

### Step 3: Design the story arc

**Narrative (15-25 slides):**
Title → Credibility/Paradox → The Problem → Customer Reality → Financial Truth →
Scenarios/Options → Deep Dives (3-5 pillars) → Financial Breakdown → Cost of Inaction →
The Solution → Operating Model → Before/After → Numbers/Capacity → Timeline →
[Photo Divider] → Risk & Mitigation → Closing Call to Action

**Executive preread:** Executive Summary → Situation → Complication → Resolution → Evidence → Recommendation

**AllMøte:** Bold opener → Wins → Strategic context → Deep dives → Commitments → Closing

**Photo dividers** go at narrative transition points (e.g., between "the problem" and "the solution", before the closing section).

### Step 4: Write the HTML

Write a single self-contained HTML file.

---

## HTML Scaffold

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentation Title</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700;0,800;0,900;1,700;1,800;1,900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2"></script>
    <style>/* All CSS here */</style>
</head>
<body>
<div class="progress-bar" id="progress" style="width:5%"></div>
<div class="nav-counter" id="counter">1 / N</div>
<div class="nav-logo"><img src="../../reference/images/telenor_symbol_blue_RGB_Refresh.svg" alt="Telenor"></div>
<!-- Slides -->
<script>/* Charts + Navigation + Animation observer */</script>
</body>
</html>
```

Each slide is a `<div class="slide slide-typename">` with 100vh height and `scroll-snap-align: start`.

---

## Telegrafen Design Tokens

```css
:root {
    --tg-dark-blue:    #070452;   /* body bg, dark slide bg, stat box text */
    --tg-mid-blue:     #1C16C5;   /* title slides, pillar overview, accents on light bg */
    --tg-telenor-blue: #00C8FF;   /* accent highlights, numbers, kicker text on dark */
    --tg-blue:         #2954FF;   /* secondary accent */
    --tg-light-cyan:   #EBFFFF;   /* PRIMARY light background for content slides */
    --tg-light-blue:   #B4FFFF;   /* Telegrafen band, light tones */
    --tg-off-white:    #E8FDFF;   /* icon stages, stat boxes — NOT as main bg */
    --tg-white:        #FFFFFF;   /* cards on blue backgrounds only */
    --tg-accent-green: #B0FBB8;   /* success, timeline end */
    --tg-accent-pink:  #FFB8D7;
    --tg-accent-yellow:#FEF6B8;   /* bridge labels */
    --font: 'DM Sans', Arial, sans-serif;
}
```

### Extended palette used in practice

These non-Telegrafen colors appear throughout the reference and are acceptable:

| Color | Use |
|-------|-----|
| `#ff6b6b` | Declining/negative/warning (red) |
| `#059669` | Growth/positive/achieved (dark green) |
| `#10b981` | Most Likely scenario (teal) |
| `#8b5cf6` | Ambition scenario (purple) |
| `#d97706` | Legacy/amber track |
| `#4a5568` | Body text on light backgrounds |
| `#637381` | Secondary text, captions, labels |
| `#e53e3e` | Pain points, error state |
| `#d69e2e` | Medium risk |

### Colors — when to use what

| Color | When |
|-------|------|
| Light Cyan `#EBFFFF` | **Default background** for most content slides |
| Mid Blue `#1C16C5` | Title slides, pillar overview, statement slides, closing |
| Dark Blue `#070452` | Gap/legacy/dramatic slides needing weight; chart bar fill for baseline |
| Telenor Blue `#00C8FF` | Accent text, highlighted words, key numbers, growth bar fill |
| Off-white `#E8FDFF` | Icon stages, stat boxes — never as main bg |
| White `#FFFFFF` | Cards on blue/dark backgrounds, chart cards on light bg |

### Telegrafen vertical bands

The signature visual element. Title slides only.

```html
<div class="title-visual">
    <div class="tg-band tg-band-1"></div> <!-- flex:1.2; bg: dark-blue -->
    <div class="tg-band tg-band-2"></div> <!-- flex:0.9; bg: telenor-blue -->
    <div class="tg-band tg-band-3"></div> <!-- flex:0.8; bg: light-blue -->
    <div class="tg-band tg-band-4"></div> <!-- flex:0.7; bg: light-cyan -->
</div>
```

**Straight vertical bands, solid color, dark to light. Never diagonal, never transparent.**

---

## Global Slide CSS (required)

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; -webkit-font-smoothing: antialiased; }
body {
    font-family: var(--font);
    scroll-snap-type: y mandatory;
    overflow-y: scroll;
    height: 100vh;
    background: var(--tg-dark-blue); /* dark gaps between slides */
}
.slide {
    width: 100vw; height: 100vh;
    scroll-snap-align: start;
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
```

---

## Navigation & Fixed UI

Three fixed elements — never in per-slide footers.

```css
.progress-bar {
    position: fixed; top: 0; left: 0; height: 3px;
    background: linear-gradient(90deg, var(--tg-mid-blue), var(--tg-telenor-blue));
    z-index: 100; transition: width 0.3s ease;
    box-shadow: 0 0 10px rgba(0, 200, 255, 0.5);
}
.nav-counter {
    position: fixed; bottom: 20px; left: 24px;
    background: rgba(7, 4, 82, 0.85); backdrop-filter: blur(8px);
    color: var(--tg-telenor-blue); padding: 6px 14px;
    border-radius: 20px; font-size: 0.75rem; font-weight: 700; z-index: 100;
    border: 1px solid rgba(0, 200, 255, 0.2);
}
.nav-logo {
    position: fixed; bottom: 18px; right: 24px; z-index: 100; opacity: 0.5;
}
.nav-logo img { width: 36px; height: 36px; }
```

---

## Animation System

### CSS

```css
.anim {
    opacity: 0; transform: translateY(24px);
    transition: opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1),
                transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
}
.anim.visible { opacity: 1; transform: translateY(0) scale(1); }
.anim-fade  { transform: none; }           /* fade only, no slide-up */
.anim-scale { transform: translateY(16px) scale(0.96); }
.anim-d1 { transition-delay: 0.12s; }
.anim-d2 { transition-delay: 0.24s; }
.anim-d3 { transition-delay: 0.36s; }
.anim-d4 { transition-delay: 0.48s; }
.anim-d5 { transition-delay: 0.60s; }
.photo-bg-anim {
    transform: scale(1.06);
    transition: transform 1.8s cubic-bezier(0.16, 1, 0.3, 1);
}
.photo-bg-anim.visible { transform: scale(1); }
```

### JavaScript observer

```js
const animObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => {
        if (e.isIntersecting) {
            e.target.classList.add('visible');
            animObserver.unobserve(e.target);
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.anim, .photo-bg-anim').forEach(el => {
    if (el.closest('.slide-title')) {
        el.classList.add('visible'); // Title slide visible immediately
    } else {
        animObserver.observe(el);
    }
});
```

### Animation stagger pattern

| Element | Class | Notes |
|---------|-------|-------|
| Kicker + heading | `.anim` | First in sequence |
| Governing thought | `.anim anim-d1` | 0.12s after |
| Body text block | `.anim anim-d2` | 0.24s after |
| Cards col 1/2/3 | `.anim anim-d1/.d2/.d3` | Staggered across columns |
| Entire layout row | `.anim anim-d2` | When wrapping the whole layout |
| Stat numbers | `.anim anim-scale anim-d3` | Scale-in effect |
| Photo bg image | `.photo-bg-anim` | Zoom scale(1.06)→scale(1) |
| Photo text | `.anim anim-fade` | Fade only, no Y movement |

**Title slide:** Apply `.visible` immediately (no observer). All other slides: observer-triggered on scroll.

---

## JavaScript: Navigation

```js
const slides = document.querySelectorAll('.slide');
const counter = document.getElementById('counter');
const progress = document.getElementById('progress');
const total = slides.length;

function getCurrentSlide() {
    let idx = 0;
    slides.forEach((s, i) => {
        const rect = s.getBoundingClientRect();
        if (rect.top < window.innerHeight / 2 && rect.bottom > window.innerHeight / 2) idx = i;
    });
    return idx;
}
function scrollToSlide(i) {
    i = Math.max(0, Math.min(i, total - 1));
    slides[i].scrollIntoView({ behavior: 'smooth' });
}
document.addEventListener('scroll', () => {
    const idx = getCurrentSlide();
    counter.textContent = `${idx + 1} / ${total}`;
    progress.style.width = `${((idx + 1) / total) * 100}%`;
});
document.addEventListener('keydown', (e) => {
    const idx = getCurrentSlide();
    if (['ArrowDown', 'ArrowRight', ' ', 'PageDown'].includes(e.key)) { scrollToSlide(idx + 1); e.preventDefault(); }
    if (['ArrowUp', 'ArrowLeft', 'PageUp'].includes(e.key)) { scrollToSlide(idx - 1); e.preventDefault(); }
    if (e.key === 'Home') { scrollToSlide(0); e.preventDefault(); }
    if (e.key === 'End')  { scrollToSlide(total - 1); e.preventDefault(); }
    if (e.key === 'f' || e.key === 'F') {
        if (!document.fullscreenElement) document.documentElement.requestFullscreen();
        else document.exitFullscreen();
    }
});
```

---

## Slide Patterns

### Design philosophy: Open layout

**Prefer open layouts over white cards.** Content should breathe directly on the Light Cyan background. Use subtle visual cues (border-left lines, icon stages, tinted backgrounds) instead of card borders and shadows.

White cards with shadows are only appropriate on **Mid Blue or Dark Blue backgrounds**.

### 1. Title Slide — Split with Telegrafen bands

- Left 55%: Mid Blue, badge + huge italic title + subtitle + logo area
- Right 45%: Vertical Telegrafen bands (Dark Blue → Telenor Blue → Light Blue → Light Cyan)
- Ghost year watermark: absolute positioned, opacity 0.04, top-right
- Title: `clamp(3.5rem, 7vw, 7rem)`, weight 900, italic, white
- Key word: `color: var(--tg-telenor-blue)`
- Badge pill: `background: rgba(0,200,255,0.12); border: 1px solid rgba(0,200,255,0.3)`
- Use `display: grid !important; grid-template-columns: 55% 45%` on `.slide`

```html
<div class="slide slide-title">
    <div class="title-content">
        <span class="badge">Vision Document</span>
        <h1>Strategy 20:30<br>From Turnaround<br>to <span>Transformation</span></h1>
        <p class="subtitle">One-sentence subtitle at opacity 0.55.</p>
        <div class="logo-area">
            <img src="../../reference/images/telenor_symbol_blue_RGB_Refresh.svg" style="width:22px;height:22px;opacity:0.6;">
            <span>Telenor Norge B2B Mobile</span>
        </div>
    </div>
    <div class="title-visual">
        <div class="tg-band tg-band-1"></div>
        <div class="tg-band tg-band-2"></div>
        <div class="tg-band tg-band-3"></div>
        <div class="tg-band tg-band-4"></div>
    </div>
    <span class="year-mark">20:30</span>
</div>
```

### 2. Two-Column: Chart + Governing Thought (light bg)

- Light Cyan background
- `grid-template-columns: 1fr 1fr` (or 55/45 split)
- Left: Chart card in white box with title + canvas + legend
- Right: Governing thought (1.2rem, weight 700) + divider line + stat cards or bullet items
- Stat boxes: off-white bg, mid-blue text, border-radius 12px
- Proof points: large italic number (2.2rem+) with border-left: 3px, no card wrappers

### 3. Dark Statement Slide (Gap / Legacy)

- Dark Blue or Mid Blue background
- Decorative `::before` pseudo-element: gradient from mid-blue (0%) to transparent (70%), clipped with `clip-path: polygon(30% 0, 100% 0, 100% 100%, 0% 100%)`, opacity 0.15-0.2
- Kicker in Telenor Blue (uppercase, letter-spacing 4px)
- Huge italic headline: `clamp(3.5rem, 8vw, 6.5rem)`, Telenor Blue color
- Sub-headline at opacity 0.5 below
- Content in glassmorphism cards: `background: rgba(255,255,255,0.06); backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px`
- Hover on cards: `background: rgba(255,255,255,0.1); transform: translateY(-3px)`

### 4. Cards on Blue — Pillar Overview

- Mid Blue background
- Decorative `::before` subtle gradient at top-right corner
- 5 equal white cards (`border-radius: 16px`, `overflow: hidden`)
- Each card: off-white icon section (`padding: 1.75rem`) + text section below
- Icon: 64px in off-white stage
- GP number: 1.8rem, weight 900, italic, mid-blue
- Card hover: `transform: translateY(-6px); box-shadow: 0 20px 50px rgba(0,0,0,0.25)`

### 5. Deep Dive — Two-Column with Customer Need

- Light Cyan background, `grid-template-columns: 1fr 1fr`
- Left: kicker + title + **customer need callout** + body text + battle rows
- Right: white chart card + stat row (off-white boxes)
- Customer need callout (required on every pillar slide):

```html
<div class="dd-customer-need">
    "Customer quote expressing their exact pain point"
    <div class="cn-source">Source — battle name or segment</div>
</div>
```

```css
.dd-customer-need {
    background: rgba(0,200,255,0.06);
    border-left: 3px solid var(--tg-telenor-blue);
    padding: 0.75rem 1.2rem;
    border-radius: 0 10px 10px 0;
    margin: 0.8rem 0 0.6rem;
    font-size: 1.05rem; font-weight: 600; font-style: italic;
    color: var(--tg-dark-blue); line-height: 1.5;
}
.dd-customer-need .cn-source {
    font-size: 0.82rem; font-style: normal; opacity: 0.4;
    font-weight: 700; margin-top: 0.25rem;
}
```

Battle rows in list form:
```css
.dd-battle-row {
    display: flex; align-items: center; gap: 0.75rem;
    padding: 0.75rem 1rem;
    background: var(--tg-white); border-radius: 12px;
    margin-bottom: 0.6rem;
    border: 1px solid rgba(0, 200, 255, 0.08);
}
```

### 6. Battle Cards — 4-up Grid

- Light Cyan background
- Left: title + body + insight box (border-left: 4px mid-blue)
- Right: 2×2 grid of battle cards
- Each card: off-white icon section (56px icon) + text section (`bc-pain` in red, `bc-need` in gray)

### 7. GP/Financial Chart — Dark Premium

- Mid Blue background (or Dark Blue)
- Full-height layout: header → chart (58% width) + insights (42%)
- Chart card: `background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px`
- Governing thought at top of insights (1.2-1.25rem, weight 700)
- Divider: `height: 1px; background: linear-gradient(90deg, var(--tg-telenor-blue), transparent)`
- Numbered bullets (round circle 28px, `background: rgba(0,200,255,0.12)`, cyan text)
- CAGR bar at bottom: `background: rgba(255,255,255,0.05); border-radius: 14px`

CAGR badges (for waterfall/bridge slides):
```html
<div class="mlb-cagr-badge">
    <span class="rate">+2.5% p.a.</span>
    <span class="label">CAGR 2027–2029</span>
</div>
```
```css
.mlb-cagr-badge {
    background: rgba(0,200,255,0.12);
    border: 1px solid rgba(0,200,255,0.25);
    border-radius: 6px; padding: 0.3rem 0.75rem;
}
```

### 8. BO Density Grid

For showing all 6 strategic areas simultaneously with GP + FTE mini-charts:

- Light Cyan background, `grid-template-columns: repeat(6, 1fr)`
- Each column: white card with header (colored bg), amount, 2yr label, items list
- Mini CSS-only bar chart at bottom of each column (no Chart.js):

```css
.bmc-bar-wrap { width: 100%; height: 38px; display: flex; align-items: flex-end; gap: 2px; }
.bmc-gp-bar   { flex: 3; border-radius: 2px 2px 0 0; background: #86efac; min-height: 3px; }
.bmc-fte-bar  { width: 5px; flex: none; border-radius: 2px 2px 0 0; background: rgba(0,200,255,0.9); }
```

Column accent colors: Core Growth #d1fae5, Mission Critical #a3e635, Security #a7f3d0, CommSol #22c55e, AdvNet #86efac, EffAdmin #bbf7d0

### 9. Before/After — Open Layout

- Light Cyan background, centered header
- Hero section: `grid-template-columns: 1fr auto 1fr`
  - Old side: red accent (`rgba(229,62,62,0.08)` icon bg, red metric 3.5rem)
  - Arrow circle: 72px, Mid Blue bg, `box-shadow: 0 4px 20px rgba(28,22,197,0.3)`
  - New side: cyan accent (`rgba(0,200,255,0.12)` icon bg, mid-blue metric 3.5rem)
- Step flow below: 4-column open grid, icons 64px in `rgba(0,200,255,0.08)` bg
- No white card wrappers — content directly on cyan

### 10. Capacity / Open Chart + Proof

- Light Cyan background
- `grid-template-columns: 1.3fr 1fr`, content directly on background (no cards)
- Governing thought at top with `border-bottom: 2px solid rgba(28,22,197,0.08)`
- Proof items with border-left: 3px (opacity 0.12), large italic number (2rem), description below
- Chart on left with `maintainAspectRatio: false`

### 11. Transformation Timeline — Open Columns

- Light Cyan background, centered header
- **Near-term (1 year):** 3-column grid, `border-left` accents with distinct colors
  - Col 1: Telenor Blue border, Col 2: Blue border, Col 3: Green border
- **Horizon (2+ years):** compact strip below divider, large italic year numbers (1.6rem)
- **Outcome metrics:** 3-column open, `tl-outcome-num` 2.5rem italic mid-blue, label uppercase

### 12. Photo Divider

- Full-bleed brand photo with `.photo-bg-anim` zoom effect
- **No overlay div** — text uses dark highlight boxes instead
- Text on photo: large italic `clamp(3rem, 6vw, 5rem)`, weight 900, centered
- Use `.hl` spans with `background: var(--tg-dark-blue); color: var(--tg-white)` for legibility
- `box-decoration-break: clone; -webkit-box-decoration-break: clone` allows multi-line highlight wrapping
- Key words inside `.hl` use `.accent` for Telenor Blue color

```html
<div class="slide slide-photo">
    <img class="photo-bg photo-bg-anim" src="../../reference/images/brand/DSCF5113.jpg" alt="">
    <div class="photo-content anim anim-fade">
        <h2>
            <span class="hl">The machine<br>is starting.</span><br>
            <span class="hl"><span class="accent">Now.</span></span>
        </h2>
    </div>
</div>
```

```css
.slide-photo { padding: 0; justify-content: center; align-items: center; }
.slide-photo .photo-bg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.slide-photo .photo-content { position: relative; z-index: 1; text-align: center; }
.slide-photo .photo-content h2 {
    font-size: clamp(3rem, 6vw, 5rem); font-weight: 900;
    font-style: italic; letter-spacing: -2px; line-height: 1.3;
}
.slide-photo .photo-content h2 .hl {
    display: inline;
    background: var(--tg-dark-blue); color: var(--tg-white);
    padding: 0.06em 0.32em;
    box-decoration-break: clone; -webkit-box-decoration-break: clone;
}
.slide-photo .photo-content h2 .hl .accent { color: var(--tg-telenor-blue); }
```

### 13. Risk Table

- Light Cyan background
- White rounded table (`border-radius: 20px; overflow: hidden; border-collapse: separate`)
- Dark Blue thead: `background: var(--tg-dark-blue)`, white text, uppercase, letter-spacing 1.5px
- Tbody rows: alternating hover `var(--tg-off-white)`, `border-bottom: 1px solid rgba(0,200,255,0.06)`
- Risk IDs in mid-blue (weight 900), High impact in `#e53e3e`, Medium in `#d69e2e`

### 14. Closing Statement

- Mid Blue background
- Two decorative `::before` + `::after` circles at very low opacity (0.08-0.1)
- Large italic title: `clamp(3rem, 6vw, 5rem)`, weight 900, `max-width: 70%`
- Key phrase in `color: var(--tg-telenor-blue)`
- Sub-text below: 1rem, weight 500, opacity 0.45, `max-width: 50%`
- Left-aligned (`align-items: flex-start`) with generous padding (8vh 10vw)

### 15. Insight Callout Pattern (on dark slides)

Three variants for categorizing insights on dark backgrounds:

```css
.insight-item { padding: 0.8rem 1rem; border-left: 3px solid rgba(0,200,255,0.3);
    background: rgba(255,255,255,0.04); border-radius: 0 8px 8px 0; }
.insight-item.accent  { border-left-color: var(--tg-telenor-blue); }
.insight-item.warning { border-left-color: #FF8A80; }
```

Use `.accent` for the most important insight, `.warning` for a risk/constraint, default for context.

---

## Chart Patterns

### Chart.js Universal Rules

1. Always `responsive: true; maintainAspectRatio: false` for full-height charts
2. Always register `ChartDataLabels` when using data labels: `plugins: [ChartDataLabels]`
3. Always use DM Sans font in all chart text: `font: { family: "'DM Sans'" }`
4. All charts must have progressive animation:

```js
animation: {
    duration: 800,
    delay: function(ctx) {
        return ctx.dataIndex * 300 + (ctx.datasetIndex * 150);
    },
    easing: 'easeOutQuart'
}
```

5. Never show default legend — build custom HTML legend below the chart
6. Turn off grid on x-axis; keep subtle grid on y-axis: `color: 'rgba(7,4,82,0.06)'` (light bg) or `'rgba(255,255,255,0.06)'` (dark bg)
7. Remove axis borders: `border: { display: false }`
8. Hide axis ticks on value axes when values are shown via data labels

### Chart Type: Stacked Bar + Overlay Lines (GP scenario)

Lines must come **before** bars in the datasets array — they render behind bars.
Use `order` to control z-index: lines get `order: 1-4`, bars get `order: 5-6`.
Use dual Y-axes: lines use visible `y` axis, bars use hidden `yBar` (same min/max).

```js
datasets: [
    { type: 'line', yAxisID: 'y', order: 1, ... },   // rendered behind
    { type: 'bar',  yAxisID: 'yBar', stack: 'gp', order: 5, ... },
],
scales: {
    y:    { stacked: false, min: 4000, max: 6800 },
    yBar: { stacked: true,  display: false, min: 4000, max: 6800 }
}
```

### Chart Type: Waterfall / Floating Bars

Use `[start, end]` tuple format for data. Color each bar individually via array.

```js
datasets: [{
    data: bridgeData.map(d => [d.start, d.end]),
    backgroundColor: bridgeData.map(d => d.color),
    borderRadius: 4
}]
```

For anchor bars (totals), use a distinct color (`#00C8FF`). For decline bars, use `#FF6B6B`. For growth bars, use green shades.

### Chart Type: Dual Y-axis Line Chart

For comparing metrics with different scales (e.g., subs share vs revenue share):

```js
datasets: [
    { yAxisID: 'yLeft', data: rmsShare, borderColor: '#00C8FF' },
    { yAxisID: 'yRight', data: subsShare, borderColor: '#ff6b6b', borderDash: [6,4] }
],
scales: {
    yLeft:  { position: 'left',  min: 55, max: 62 },
    yRight: { position: 'right', min: 49, max: 54, grid: { display: false } }
}
```

Use `layout: { padding: { right: 80 } }` to make room for end-of-line labels.

### Custom Canvas Plugin: Line End Labels

Write a custom plugin to draw labels directly at the end of lines (instead of legend):

```js
const lineLabels = {
    id: 'lineLabels',
    afterDraw(chart) {
        const ctx = chart.ctx;
        const meta = chart.getDatasetMeta(0);
        const last = meta.data[meta.data.length - 1];
        ctx.save();
        ctx.font = "700 12px 'DM Sans'";
        ctx.fillStyle = '#00C8FF';
        ctx.textAlign = 'left';
        ctx.fillText('Revenue XX%', last.x + 8, last.y + 4);
        ctx.restore();
    }
};
new Chart(ctx, { ..., plugins: [lineLabels] });
```

### Custom Canvas Plugin: Bridge Lines

Draw connecting dashed lines between bars in a stacked/waterfall chart:

```js
const bridgePlugin = {
    id: 'bridges',
    afterDraw(chart) {
        const ctx = chart.ctx;
        const yAxis = chart.scales.y;
        const meta = chart.getDatasetMeta(2); // the top bar dataset

        // Draw total labels above each bar
        for (let i = 0; i < totals.length; i++) {
            const bar = meta.data[i];
            const yTop = yAxis.getPixelForValue(totals[i]);
            ctx.save();
            ctx.textAlign = 'center';
            ctx.font = "900 italic 16px 'DM Sans'";
            ctx.fillStyle = '#fff';
            ctx.fillText(totals[i].toLocaleString('no-NO'), bar.x, yTop - 10);
            ctx.restore();
        }

        // Draw dashed bridge lines + delta labels between bars
        for (let i = 0; i < totals.length - 1; i++) {
            const barCur  = meta.data[i];
            const barNext = meta.data[i + 1];
            const x1 = barCur.x  + barCur.width / 2  + 3;
            const x2 = barNext.x - barNext.width / 2 - 3;
            const yCur  = yAxis.getPixelForValue(totals[i]);
            const yNext = yAxis.getPixelForValue(totals[i + 1]);

            ctx.save();
            ctx.strokeStyle = 'rgba(254,246,184,0.4)'; // accent-yellow
            ctx.lineWidth = 1.5; ctx.setLineDash([4, 3]);
            ctx.beginPath(); ctx.moveTo(x1, yCur); ctx.lineTo(x2, yCur); ctx.stroke();
            ctx.setLineDash([]);
            ctx.strokeStyle = 'rgba(254,246,184,0.2)';
            ctx.beginPath(); ctx.moveTo(x2, yCur); ctx.lineTo(x2, yNext); ctx.stroke();
            ctx.restore();

            // Delta label
            const labelY = Math.min(yCur, yNext) - 12;
            ctx.save();
            ctx.textAlign = 'center';
            ctx.font = "900 16px 'DM Sans'";
            ctx.fillStyle = '#FEF6B8';
            ctx.fillText('+' + delta, (x1 + x2) / 2, labelY);
            ctx.restore();
        }
    }
};
```

### Data Label Colors

| Bar fill | Data label color |
|----------|-----------------|
| Dark Blue `#070452` baseline | `rgba(255,255,255,0.5)` (dim white) |
| Telenor Blue `#00C8FF` growth | `#070452` (dark blue — readable on cyan) |
| White bars on dark bg | Dark blue text |
| Green bars | White text |

**Always include `datalabels: { display: false }` on datasets that should NOT show labels.**

### Chart Color Palette for Scenarios

| Scenario | Color |
|----------|-------|
| Baseline / Run | `#070452` (dark blue) |
| Growth gap | `#00C8FF` (telenor blue) |
| BOs independent | `#ff6b6b` (red, dashed line) |
| Most Likely | `#10b981` (teal) |
| Ambition | `#8b5cf6` (purple) |
| Full Potential | `#00C8FF` (cyan) |
| Headcount: Run | `#070452` |
| Headcount: Transform | `#1C16C5` |
| Headcount: Growth | `#00C8FF` |

---

## Typography Rules

| Element | Size | Weight | Style | Notes |
|---------|------|--------|-------|-------|
| Hero title (title slide) | `clamp(3.5rem, 7vw, 7rem)` | 900 | italic | letter-spacing -2px |
| Section title | `clamp(2rem, 3.5vw, 3rem)` | 900 | italic | letter-spacing -1px to -2px |
| GP/impact headline | `clamp(3.5rem, 8vw, 6.5rem)` | 900 | italic | Telenor Blue |
| Governing thought | 1.1-1.25rem | 600-700 | normal | Between header and content |
| Body text | 0.92-1rem | 400-600 | normal | line-height 1.65-1.7 |
| Kicker | 0.75-0.82rem | 800 | uppercase | letter-spacing 3-4px |
| Stat number (large) | 2-2.5rem | 900 | italic | letter-spacing -1px |
| Big number (hero) | `clamp(7rem, 18vw, 14rem)` | 900 | italic | |
| Card title | 0.9-1.1rem | 800-900 | italic or normal | letter-spacing -0.2px |
| Battle row label | 0.88-0.92rem | 700 | normal | |
| Caption / source | 0.78-0.82rem | 600-700 | normal | opacity 0.4-0.5 |
| Stat box value | 1.6rem | 900 | italic | letter-spacing -1px |
| Badge text | 0.68rem | 800 | uppercase | letter-spacing 3px |
| Timeline year | 0.82rem | 800 | uppercase | letter-spacing 2px |

**Always** italic for large display text and card stat numbers. It's the Telegrafen way.
**Always** `letter-spacing: -1px` to `-3px` on large headings.
**NEVER** use font sizes below **0.82rem** in a presentation context.

Body text colors: `#4a5568` (primary) and `#637381` (secondary/captions) on light backgrounds. Opacity 0.55-0.6 on dark backgrounds.

---

## Available Brand Assets

### Telenor Logo

```html
<img src="../../reference/images/telenor_symbol_blue_RGB_Refresh.svg">
```

Used in fixed nav-logo (36×36px, opacity 0.5) and title slide logo-area (22×22px, opacity 0.6).

### Icons (56 SVGs in `reference/icons/`)

| Icon file | Use for |
|-----------|---------|
| `Security_expanded.svg` | Security pillar, SafeZone |
| `SecurityPersonal_expanded.svg` | Identity, employee security |
| `SecurityPhone_expanded.svg` | Mobile security |
| `SecurityBrowser_expanded.svg` | SOC, browser security |
| `CellTower_expanded.svg` | Network, 5G |
| `CustomerService_expanded.svg` | Customer Solutions, MBN |
| `Computer_expanded.svg` | Digital, admin, technology |
| `Coverage_expanded.svg` | Growth, reach |
| `Fiber_expanded.svg` | Cloud, infrastructure |
| `Factory_expanded.svg` | Industry, IoT, 20:30 model |
| `Chatbot_expanded.svg` | AI, automation, agentic |
| `Document Sharing_expanded.svg` | Collaboration, process |
| `Document Signature_expanded.svg` | Signing, completion |
| `Deal_expanded.svg` | Partnership, commercial |

#### Icon sizing rules

| Context | Stage size | Icon size | Background |
|---------|-----------|-----------|------------|
| Engine cards (3-col) | 100×100px | 80px | `var(--tg-off-white)`, border-radius 20px |
| 20:30 model goal row | 100×100px | 64px | `var(--tg-off-white)`, border-radius 20px |
| Pillar grid (5-col) | 1.75rem padding stage | 64px | `var(--tg-off-white)` |
| Deep dive sub-pillar | 44×44px icon | 44px | `var(--tg-off-white)`, 16px radius |
| Battle cards | 56px icon | 56px | `var(--tg-off-white)` |
| Before/after hero | 100×100px stage | 64px | color-tinted (red or cyan) |
| Before/after steps | 64×64px stage | 40px | `rgba(0,200,255,0.08)` |
| Open 3-col layout | 100×100px or 64×64px | 64px | `var(--tg-off-white)` |

**NEVER** use icons smaller than 36px. If an icon would be smaller, remove it.
**ALWAYS** use `var(--tg-off-white)` not `rgba(0,200,255,...)` for icon stage backgrounds on light slides.

### Brand Photos

Read `reference/images/brand/INDEX.md` for full catalog.

| Need | Best candidates |
|:-----|:----------------|
| Hero landscape | DSCF5113, DSCF4989, DSCF4982, DSCF5088 |
| Direction metaphor | DSCF4989, DSCF4980, DSCF5110 |
| Team culture | Telenor.bedrift.70, .55, .63 |
| Customer interaction | Telenor.bedrift.31, .28, .66 |
| Customer support | Telenor.bedrift.72, .73, .74 |
| Connectivity in nature | DSCF5087, DSC_5622 |

---

## Generating a PDF from HTML

Use the Playwright script in `reference/temp/generate_pdf.py`:

```bash
cd "/path/to/strategi 2030" && .venv/bin/python reference/temp/generate_pdf.py
```

**Critical settings for correct output:**
- Viewport: **1280×720** (exactly 16:9) with `device_scale_factor=2` → 2560×1440 screenshots
- PDF page size: 13.33"×7.5" (standard 16:9 presentation format)
- Wait time: **2.5s per slide** — CSS transitions take up to 1.3s (0.6s delay + 0.7s duration) + Chart.js 1s
- Scroll method: set `scrollTop = i * window.innerHeight` before calling `scrollIntoView()`
- Use `img2pdf` with `get_layout_fun((in_to_pt(13.33), in_to_pt(7.5)))` for exact fit with no white stripes

The aspect ratio of viewport (1280/720 = 16:9) must match the PDF page ratio (13.33/7.5 = 16:9) exactly, or white letterbox stripes appear.

---

## Quality Checklist

- [ ] Every slide has a clear focal point — one thing dominates
- [ ] Light slides use Light Cyan `#EBFFFF`, not white
- [ ] Dark slides use Mid Blue or Dark Blue
- [ ] Open layout preferred — no unnecessary white cards on cyan backgrounds
- [ ] Key words/numbers highlighted in Telenor Blue or Mid Blue
- [ ] Icons are large (min 56px) — never tiny
- [ ] Icon stages use `var(--tg-off-white)` not cyan tint
- [ ] Telegrafen vertical bands on title slide only
- [ ] Ghost year watermark on title slide (opacity 0.04)
- [ ] No per-slide footers — only fixed nav counter + logo + progress bar
- [ ] All charts have progressive animation (delay per dataIndex)
- [ ] Chart data labels correct colors (white on dark, dark on cyan)
- [ ] `datalabels: { display: false }` on line datasets that shouldn't show labels
- [ ] Custom legend built in HTML — never default Chart.js legend
- [ ] All `.anim` classes applied with appropriate stagger delays
- [ ] Photo dividers use `.hl` highlight boxes (not overlay) for text legibility
- [ ] Photo dividers placed at narrative transition points
- [ ] Typography: all text ≥ 0.82rem, large text is italic weight 900
- [ ] Governing thought placed between header and content (every content slide)
- [ ] Customer need callouts on deep-dive pillar slides
- [ ] No slide has too much text — if so, split into two slides
- [ ] All data grounded in source strategy documents
- [ ] Navigation works (arrow keys, space, home/end, F for fullscreen)
- [ ] Animations trigger correctly on each slide entry
- [ ] CAGR badges on financial chart slides

---

## What NOT to Do

- Do NOT use the template engine for premium presentations
- Do NOT use emoji icons — use Telenor SVG icons from `reference/icons/`
- Do NOT use diagonal/skewed stripe elements — Telegrafen bands are straight vertical
- Do NOT default to dark backgrounds — Light Cyan is the primary content background
- Do NOT wrap content in white cards on Light Cyan slides — use open layout
- Do NOT use small icons (under 36px) — either use large or remove
- Do NOT add per-slide footer elements — use the fixed nav counter + logo
- Do NOT put small text (under 0.82rem) in presentations
- Do NOT use generic CSS frameworks — write custom CSS per slide
- Do NOT invent data — ground everything in source documents
- Do NOT skip animations — every slide must have entry animations
- Do NOT use `rgba(0,200,255,...)` for icon backgrounds — use `var(--tg-off-white)`
- Do NOT use a photo overlay div — use `.hl` highlight boxes for photo text legibility
- Do NOT show default Chart.js legend — build custom HTML legend
- Do NOT put line datasets after bar datasets in mixed charts (lines render behind bars)
- Do NOT forget `layout: { padding: { right: 80 } }` on line charts with end-of-line labels
- Do NOT use a viewport width > 1280 for PDF generation — causes letterbox stripes

---

## Grounding & Single Source of Truth

- All facts and figures MUST come from existing `.md` files in `strategy/`
- If new insights emerge during design, write them back to core documentation first
- Use `CATALOG.md` to find relevant source documents
- Key data reference: `strategy/current_state/value_stream_snapshot.md`
- Brand photo catalog: `reference/images/brand/INDEX.md`

---

## Presentation Types & References

| Type | Reference HTML | When to use |
|:-----|:---------------|:------------|
| **Narrative** | `presentations/internal/Strategy_2030_Narrative.html` | Strategy vision, executive preread, board storytelling (15-25 slides) |
| **AllMøte** | *(not yet created — see AllMøte section below)* | All-hands team meetings (8-12 slides) |
| Data Brief | *(not yet created)* | KPI reviews, monthly reporting (5-8 slides) |

**Always read `RATIONALE_NARRATIVE.md`** before creating a new narrative presentation. It documents why each design decision was made.

The rules in this SKILL.md are **universal** — they apply to all types. The rationale document contains **type-specific** decisions (narrative structure, photo placement, slide density).

---

## AllMøte — Design Specification

The AllMøte (all-hands) format is a **Google I/O keynote, not a PowerPoint meeting.** Every slide should feel like a product reveal moment. The ambition is: people in the room should feel something — pride, excitement, urgency — not just understand something.

It **inherits 100% of the Telegrafen design system**: same tokens, same animation system, same icon sizing, same chart approach, same photo pattern. The differences are in pacing, density, emotional register, and dramatic impact — not in visual language.

### The Google Launch Mindset

Study how Apple/Google launches work:
- **One idea per slide.** If you need two sentences, that's two slides.
- **The number IS the slide.** "97 MNOK" needs nothing else on screen.
- **Build then reveal.** Set up tension first, then deliver the payoff.
- **Dark backgrounds for impact, light for facts, photos for humanity.**
- **"This changes everything" rhythm** — alternate between problem and solution, between scale and human.
- **Silence is OK.** A 3-second pause on a photo slide is a feature, not a failure.
- **The closing should feel inevitable** — the whole deck builds to one sentence.

### What changes vs Narrative

| Dimension | Narrative | AllMøte |
|-----------|-----------|---------|
| Slide count | 15-25 | 8-12 |
| Tone | Strategic, analytical | Cinematic, declarative, human |
| Data density | High (chart + 4 bullets + stat bar) | Extreme low: 1 idea, 1 element |
| Body text | 2-3 paragraphs | 0 sentences (max 1 line) |
| Hero numbers | Supporting proof | THE slide |
| Photo dividers | Narrative transitions | Liberal — every 2-3 slides |
| Background | Mostly light cyan | Mix of full-bleed photo, dark blue, mid blue, light |
| Customer content | Deep dives with battle rows | 1 quote, full-slide treatment |
| Financial content | Full GP bridge + scenarios | One number. Period. |
| Language | English | Norwegian — spoken, not written |
| Animations | Staggered, informational | Dramatic reveals, longer delays |

### AllMøte narrative arc — Google launch structure (8-12 slides)

**Act 1: The Hook (slides 1-2)**
1. **Title** — Same Telegrafen split bands. Bold. No subtitle. Just the title and what division.
2. **The opener stat** — Full dark slide, one enormous number, 3-word caption. No explanation yet.

**Act 2: The Problem (slides 3-4)**
3. **The market reality** — 1 sentence, 1 chart (or just 1 stat). Establish why this matters.
4. **The customer voice** — Full slide, 1 quote, photo background or dark bg. No bullets.

**Act 3: The Product (slides 5-7)**
5. **What we're building** — Telegrafen-style split or dark slide. The strategy in one line.
6-7. **2-3 pillar moments** — Each: full-slide icon or photo + product name + 1 number. Nothing more.

**Act 4: The Transformation (slides 8-9)**
8. **The before/after moment** — Cinematic: OLD vs NEW, one number each side.
9. **Photo divider** — "Nå bygger vi dette." (full-bleed, `.hl` boxes, no overlay)

**Act 5: The Call (slides 10-12)**
10. **The team commitment** — 3 things max, open layout, no cards, large text.
11. **Closing charge** — Mid Blue, large italic, key phrase in Telenor Blue. Nothing else.
12. *(optional)* **Closing photo** — Team. Full-bleed. `.hl` boxes with company/team name.

### AllMøte visual rules

**Full-bleed stat slide (the "number IS the slide" pattern):**
```css
.am-stat-slide {
    background: var(--tg-dark-blue); /* or var(--tg-mid-blue) */
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
}
.am-stat-slide .am-number {
    font-size: clamp(10rem, 25vw, 20rem);
    font-weight: 900; font-style: italic;
    color: var(--tg-telenor-blue);
    letter-spacing: -4px; line-height: 0.9;
    text-align: center;
}
.am-stat-slide .am-number-unit {
    font-size: clamp(3rem, 6vw, 5rem); font-weight: 900; font-style: italic;
    color: rgba(255,255,255,0.4); letter-spacing: -2px;
    display: block; text-align: center; margin-top: 0.5rem;
}
.am-stat-slide .am-caption {
    font-size: 1.1rem; font-weight: 600; letter-spacing: 3px;
    text-transform: uppercase; opacity: 0.4; margin-top: 2rem;
    color: var(--tg-white);
}
```

**Customer voice — full-slide treatment:**
```css
/* Dark blue bg, photo optional in background at very low opacity */
.am-voice-slide {
    background: var(--tg-dark-blue);
    padding: 8vh 12vw;
    align-items: flex-start; justify-content: center;
}
.am-voice {
    font-size: clamp(1.8rem, 3.5vw, 3rem);
    font-weight: 700; font-style: italic;
    letter-spacing: -1px; line-height: 1.35;
    color: var(--tg-white); max-width: 800px;
}
.am-voice .am-voice-hl { color: var(--tg-telenor-blue); }
.am-voice cite {
    display: block; font-size: 0.95rem; font-style: normal;
    font-weight: 600; opacity: 0.4; margin-top: 2rem;
    letter-spacing: 1px;
}
```

**Pillar moment — product reveal:**
Each pillar gets a standalone slide. Not a card in a grid. A full slide.

```css
.am-pillar-slide {
    background: var(--tg-mid-blue); /* or light-cyan for contrast */
    display: flex; flex-direction: column;
    align-items: flex-start; justify-content: center;
    padding: 8vh 10vw;
}
.am-pillar-icon {
    width: 120px; height: 120px;
    background: var(--tg-off-white); border-radius: 28px;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 2rem;
}
.am-pillar-icon img { width: 80px; height: 80px; }
.am-pillar-name {
    font-size: clamp(3rem, 6vw, 5rem);
    font-weight: 900; font-style: italic; letter-spacing: -2px;
    color: var(--tg-white); margin-bottom: 0.5rem;
}
.am-pillar-name span { color: var(--tg-telenor-blue); }
.am-pillar-stat {
    font-size: clamp(2rem, 4vw, 3.5rem);
    font-weight: 900; font-style: italic;
    color: var(--tg-telenor-blue); letter-spacing: -1.5px;
    margin-bottom: 0.5rem;
}
.am-pillar-desc {
    font-size: 1.1rem; font-weight: 500; opacity: 0.55;
    max-width: 500px; line-height: 1.6; color: var(--tg-white);
}
```

**Before/After — cinematic two-panel:**
Full slide, dark background, two halves separated by a glowing divider:
```css
.am-ba-slide {
    background: var(--tg-dark-blue);
    display: grid; grid-template-columns: 1fr 2px 1fr;
    align-items: stretch; padding: 0;
}
.am-ba-panel {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 8vh 6vw; text-align: center;
}
.am-ba-panel.am-ba-before { opacity: 0.5; }
.am-ba-divider {
    background: linear-gradient(180deg, transparent, var(--tg-telenor-blue), transparent);
    align-self: stretch;
}
.am-ba-metric {
    font-size: clamp(5rem, 12vw, 10rem);
    font-weight: 900; font-style: italic;
    letter-spacing: -3px; line-height: 0.9;
}
.am-ba-before .am-ba-metric { color: #ff6b6b; }
.am-ba-after  .am-ba-metric { color: var(--tg-telenor-blue); }
.am-ba-label {
    font-size: 0.9rem; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; opacity: 0.45; margin-top: 1.5rem;
    color: var(--tg-white);
}
```

**Commitment/ask slide:** 3 items max. Open layout on light cyan. Each item: large icon (100px, off-white stage), bold 1.5rem italic title, 1-line description. Staggered animation. No cards, no borders — open layout breathing directly on the background.

**Closing charge:** Mid Blue background. Text `clamp(3.5rem, 7vw, 6rem)`, left-aligned, italic, weight 900. Key phrase in Telenor Blue. One supporting sentence below at opacity 0.45. That's it.

### Animation — cinematic upgrade for AllMøte

Use longer delays for dramatic effect. The fewer elements on screen, the more each one matters:

```css
/* AllMøte animation — same system, cinematic timing */
.anim-am-hero { transition-delay: 0.4s; }          /* big number */
.anim-am-hero-caption { transition-delay: 0.8s; }  /* caption under number */
.anim-am-quote { transition-delay: 0.3s; }
.anim-am-cite  { transition-delay: 0.9s; }
```

For single-element slides (stat-only), apply `.anim anim-scale` and delay 0.3s — the number zooms in from slightly smaller.

### Language rules

- **Write every slide title as a spoken sentence**, not a noun phrase
- Bad: "Strategisk vekst" — Good: "Vi vokser fordi vi leverer mer verdi"
- Bad: "Resultater 2025" — Good: "2025 var bedre enn planen"
- Key words and numbers stay in Norwegian: "XX % av markedsinntektene" not "RMS XX%"
- Product names in original form: SafeZone, mPort, MBN

### Advanced animation toolkit for AllMøte

AllMøte presentations unlock the full CSS/JS animation arsenal. The narrative uses IntersectionObserver fade-ins. The AllMøte goes further. **Every animation must serve the story — not decorate it.**

#### Keyframe animations

```css
/* Number slam-in — for hero stat slides */
@keyframes slamIn {
    0%   { opacity: 0; transform: scale(0.6) translateY(30px); }
    60%  { opacity: 1; transform: scale(1.04) translateY(-4px); }
    100% { transform: scale(1) translateY(0); }
}
.am-slam { animation: slamIn 0.7s cubic-bezier(0.22, 1, 0.36, 1) both; }
.am-slam-d1 { animation-delay: 0.15s; }
.am-slam-d2 { animation-delay: 0.35s; }
.am-slam-d3 { animation-delay: 0.55s; }

/* Text reveal — for quotes and governing thoughts */
@keyframes revealUp {
    from { opacity: 0; transform: translateY(40px); filter: blur(4px); }
    to   { opacity: 1; transform: translateY(0);    filter: blur(0); }
}
.am-reveal { animation: revealUp 0.9s cubic-bezier(0.16, 1, 0.3, 1) both; }

/* Glow pulse — for accent numbers */
@keyframes glowPulse {
    0%, 100% { text-shadow: 0 0 30px rgba(0,200,255,0.4); }
    50%       { text-shadow: 0 0 60px rgba(0,200,255,0.8), 0 0 120px rgba(0,200,255,0.3); }
}
.am-glow { animation: glowPulse 2.5s ease-in-out infinite; animation-delay: 0.7s; }

/* Line draw — for dividers */
@keyframes drawLine {
    from { width: 0; opacity: 0; }
    to   { width: 100%; opacity: 1; }
}
.am-draw-line {
    height: 2px; background: var(--tg-telenor-blue);
    animation: drawLine 0.8s cubic-bezier(0.4, 0, 0.2, 1) both;
    animation-delay: 0.5s;
}

/* Fade in from left (for kickers and labels) */
@keyframes slideFromLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to   { opacity: 1; transform: translateX(0); }
}
.am-from-left { animation: slideFromLeft 0.6s cubic-bezier(0.16, 1, 0.3, 1) both; }
```

**Only trigger keyframe animations when a slide becomes active.** Use the IntersectionObserver to add a `.slide-active` class to the current slide, and scope all keyframe animations to `.slide-active .am-*`:

```js
const slideObserver = new IntersectionObserver((entries) => {
    entries.forEach(e => {
        if (e.isIntersecting) {
            e.target.classList.add('slide-active');
        } else {
            // Reset on exit so re-entering re-triggers
            e.target.classList.remove('slide-active');
        }
    });
}, { threshold: 0.6 });
document.querySelectorAll('.slide').forEach(s => slideObserver.observe(s));
```

```css
/* Animations only fire when slide is active */
.am-slam { opacity: 0; }
.slide-active .am-slam { animation: slamIn 0.7s cubic-bezier(0.22, 1, 0.36, 1) both; }
.slide-active .am-reveal { animation: revealUp 0.9s cubic-bezier(0.16, 1, 0.3, 1) both; }
```

#### Animated number counter (for hero stat slides)

```js
function animateCounter(el, target, duration = 1200, suffix = '') {
    const start = performance.now();
    const update = (now) => {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        // easeOutQuart
        const eased = 1 - Math.pow(1 - progress, 4);
        el.textContent = Math.round(eased * target).toLocaleString('no-NO') + suffix;
        if (progress < 1) requestAnimationFrame(update);
    };
    requestAnimationFrame(update);
}

// Trigger when slide becomes active
const statSlide = document.querySelector('.slide-stat');
const numEl = statSlide.querySelector('.am-number');
slideObserver.observe(statSlide);
statSlide.addEventListener('animationstart', () => {
    animateCounter(numEl, 97, 1000, ' MNOK');
}, { once: false });
// Or: watch for slide-active class
const mo = new MutationObserver(() => {
    if (statSlide.classList.contains('slide-active')) {
        animateCounter(numEl, 97, 1200);
    }
});
mo.observe(statSlide, { attributes: true, attributeFilter: ['class'] });
```

#### Cinematic text split (word-by-word reveal)

For closing charge slides where each word should hit:

```js
function splitReveal(el, baseDelay = 0, delayPerWord = 0.08) {
    const words = el.textContent.trim().split(' ');
    el.innerHTML = words.map((w, i) =>
        `<span style="display:inline-block;opacity:0;transform:translateY(20px);
         transition:opacity 0.5s ${baseDelay + i * delayPerWord}s cubic-bezier(0.16,1,0.3,1),
         transform 0.5s ${baseDelay + i * delayPerWord}s cubic-bezier(0.16,1,0.3,1);">${w}&nbsp;</span>`
    ).join('');
    // Trigger when active
    return () => el.querySelectorAll('span').forEach(s => {
        s.style.opacity = '1'; s.style.transform = 'translateY(0)';
    });
}
```

#### Background gradient animation (ambient motion)

For dark slides that need life without distracting from content:

```css
.am-ambient {
    background: linear-gradient(135deg, var(--tg-dark-blue) 0%, #0a0870 50%, var(--tg-dark-blue) 100%);
    background-size: 200% 200%;
    animation: ambientShift 8s ease infinite;
}
@keyframes ambientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
```

Use sparingly — only on the title slide or closing. Never on data slides.

### What to keep from Narrative (do NOT simplify away)

- **Custom HTML** — AllMøte is still a hand-crafted HTML file. Never use the template engine.
- Telegrafen vertical bands on title slide — always
- Photo divider `.hl` highlight box text pattern — always (no overlay)
- Icon sizing rules — always (64-120px, off-white stage)
- Kicker + title structure — on every content slide (kicker can be tiny, just 1-3 words)
- `clamp()` font sizes — always
- Base IntersectionObserver animation system — always (complement with keyframes, not replace)
- Fixed nav counter + progress bar — always
- DM Sans font, Telegrafen color tokens — always
- Chart animation (progressive delay per dataIndex) — if any chart is used
- The story must be told through content, not animation — animation serves the moment, it doesn't replace the idea
