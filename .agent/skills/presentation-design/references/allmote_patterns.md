# AllMote Patterns

AllMote / Google Launch inspiration best practices for `mode: allmote`.

---

## Core Philosophy

Text IS the design element. One idea fills the screen. Every slide creates a moment. The audience "gets it" in 3 seconds. All detail lives in speaker notes.

---

## Cinematic Dark Mode — Mandatory

**AllMøte presentations NEVER use light backgrounds.** No `slide-light`, no `--tg-light-cyan`, no `#EBFFFF`. Every content slide uses one of:

- `--tg-dark-blue` (`#070452`) — primary dark background
- `--tg-mid-blue` (`#1C16C5`) — secondary dark background
- `.am-ambient` — animated gradient between mid-blue and blue
- Full-bleed photo — with dark overlay text treatment (`.hl` boxes)

Accent and glow colors: `--tg-telenor-blue` (`#00C8FF`) for highlights, `--tg-accent-green` (`#B0FBB8`) for success/hero elements, `--tg-accent-pink` (`#FFB8D7`) for human/warm accents.

This is the standard established by `BO_Governance_NorgeULF.html` — the canonical AllMøte reference.

---

## Animation System

AllMote presentations use a layered animation system. All animations are CSS-driven and triggered by IntersectionObserver adding `.slide-active` to slides.

### Entry Animations (`.anim` class)

The base animation system for staggered element reveals:

```css
.anim {
    opacity: 0;
    transform: translateY(24px);
    transition: opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1),
                transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
}
.anim.visible {
    opacity: 1;
    transform: translateY(0) scale(1);
}
```

**Delay classes** for staggered reveals:
- `.anim-d1` — 0.12s delay
- `.anim-d2` — 0.24s delay
- `.anim-d3` — 0.36s delay
- `.anim-d4` — 0.48s delay
- `.anim-d5` — 0.60s delay

**Variants:**
- `.anim-fade` — Opacity only (no translate). For text overlays on images.
- `.anim-scale` — Translate + scale from 0.96. For emphasis elements like arrows.

**Rule:** Every visible element on an AllMote slide must have the `.anim` class. Elements appear in reading order, staggered ~120ms apart.

### Advanced Keyframe Animations

Triggered by `.slide-active` on the parent slide — used for high-impact moments:

```css
/* Slam In — bold, bouncy entrance for hero numbers/titles */
@keyframes slamIn {
    0%   { opacity: 0; transform: scale(0.6) translateY(30px); }
    60%  { opacity: 1; transform: scale(1.04) translateY(-4px); }
    100% { opacity: 1; transform: scale(1) translateY(0); }
}

/* Reveal Up — smooth blur-to-sharp rise for supporting text */
@keyframes revealUp {
    from { opacity: 0; transform: translateY(40px); filter: blur(4px); }
    to   { opacity: 1; transform: translateY(0);    filter: blur(0); }
}

/* Draw Line — accent divider that grows from left */
@keyframes drawLine {
    from { width: 0; opacity: 0; }
    to   { width: 100%; opacity: 1; }
}
```

**CSS classes:**
- `.am-slam` — Applies slamIn. Use for hero numbers, bold titles.
- `.am-reveal` — Applies revealUp. Use for supporting text, descriptions.
- `.am-draw-line` — Animated accent line, max-width 180px.
- `.am-slam-d1`, `.am-slam-d2` — Delay variants (0.18s, 0.38s).

### Ambient Background Animation

Statement and flywheel slides use a shifting gradient background:

```css
.am-ambient {
    background: linear-gradient(135deg, var(--tg-mid-blue) 0%, var(--tg-blue) 50%, var(--tg-mid-blue) 100%);
    background-size: 200% 200%;
    animation: ambientShift 12s ease infinite;
}
```

Use `.am-ambient` on `.slide-dark` or `.slide-mid` slides that need visual energy.

### Counter Animations

JavaScript-driven animated counters for stat slides:

```javascript
function animateCounter(el, target, duration = 1500, suffix = '') {
    const start = performance.now();
    const update = (now) => {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 4); // easeOutQuart
        el.textContent = Math.round(eased * target).toLocaleString('no-NO') + suffix;
        if (progress < 1) requestAnimationFrame(update);
    };
    requestAnimationFrame(update);
}
```

**Pattern:** Use MutationObserver on `slide-active` class to trigger counters when the slide enters view. Reset to "0" when leaving. Duration: 1200ms for standard, 1500ms for large numbers.

### Photo Ken Burns Effect

Full-bleed photo slides zoom from 1.06 to 1.0 when entering view:

```css
.photo-bg {
    transform: scale(1.06);
    transition: transform 1.8s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-active .photo-bg {
    transform: scale(1);
}
```

### Pulsing Glow

For hero/central nodes in relationship diagrams:

```css
@keyframes pulseGlow {
    0%   { transform: scale(0.92); opacity: 0.5; }
    100% { transform: scale(1.08); opacity: 0.9; }
}
```

Apply with `animation: pulseGlow 3s ease-in-out infinite alternate;`

---

## Sub-Stepping (Click-to-Advance Within a Slide)

The most important AllMote interaction pattern. Allows presenter to reveal content progressively within a single slide using keyboard arrows or clicks.

### Pattern

1. Elements start hidden with `opacity: 0 !important` and `pointer-events: none`
2. A JavaScript step counter tracks current reveal state per slide
3. Arrow keys / clicks increment the counter and add `.col-visible` or `.card-visible`
4. When all steps are exhausted, the next arrow key navigates to the next slide
5. Navigating backward reverses the reveal

### Implementation (Chain Slide Example)

```css
.chain-col {
    opacity: 0 !important;
    transform: translateY(24px) !important;
    transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1),
                transform 0.6s cubic-bezier(0.16, 1, 0.3, 1) !important;
    pointer-events: none;
}
.chain-col.col-visible {
    opacity: 1 !important;
    transform: translateY(0) !important;
    pointer-events: auto;
}
```

```javascript
let chainStep = 0;
// Forward: chainStep++ → show next column
// Backward: chainStep-- → hide last column
// At max step: next arrow navigates to next slide
// Entering from previous slide: chainStep = 0
// Entering from next slide: chainStep = max (fully revealed)
```

### Sub-Stepping with Popup Overlays

Certain steps can trigger full-screen popup overlays (e.g., mission statement, pillar details):

```javascript
if (chainStep === 2) {
    popupMission.classList.add('popup-visible');
} else if (chainStep === 4) {
    popupPillars.classList.add('popup-visible');
}
```

Popup CSS:
```css
.chain-popup-overlay {
    position: fixed;
    inset: 0;
    background: rgba(3, 2, 40, 0.92);
    backdrop-filter: blur(12px);
    z-index: 200;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.4s ease;
}
.chain-popup-overlay.popup-visible {
    opacity: 1;
    pointer-events: all;
}
```

### When to Use Sub-Stepping

- Chain/hierarchy visualizations where progressive build tells a story
- BO showcase slides where overview precedes detail
- Any slide with >3 conceptual layers that benefit from paced reveal
- **Never** on simple content slides — only when the build sequence adds meaning

---

## Text as Design Element (Display Typography)

In AllMote, text is not read — it is experienced visually:

- **Hero statements** at 2-4rem fill the screen with one bold idea.
- **Hero numbers** at 5-8rem dominate the slide — the number IS the slide.
- Use **font weight 700-800** for maximum visual impact on dark backgrounds.
- Limit visible text to **15 words maximum** per slide (excluding speaker notes).
- Never use bullet points on screen. Use cards, icons, or separate slides instead.

---

## Hero Number Technique

The `big-number` layout presents a single metric that creates an emotional reaction:

```markdown
## Slide 3 — Market Dominance

<!-- slide:
  theme: statement
  layout: big-number
-->

**Headline:** *58.1%*

Revenue Market Share -- built on clarity, ownership, and commercial spirit.
```

**Rules for hero numbers:**
- One number per slide. Never two.
- Include the unit or context label (%, mNOK, FTE) in a smaller size below.
- Add a delta indicator when showing change (+12.3%, -100m).
- The number must provoke an emotional response: pride, urgency, or surprise.

---

## Dual Stat Slide Pattern

Two hero numbers side by side for scale/context slides:

```html
<div class="stat-grid">
    <div class="stat-card anim anim-d1">
        <div class="stat-card-number" id="animated-num-1">0</div>
        <span class="stat-card-label">Label</span>
        <p class="stat-card-desc">Supporting text</p>
    </div>
    <div class="stat-card anim anim-d2">
        <!-- second stat -->
    </div>
</div>
```

- Numbers animate from 0 to target using counter animation
- Use `.am-ambient` background for visual energy
- Maximum 2 stats per slide. For 3+, use `numbers-panel`

---

## Full-Bleed Triptych Pattern

Three equal vertical panels filling the entire viewport. Used for principles, problems, or commitments:

```css
.triptych {
    padding: 0 !important;
    flex-direction: row !important;
    align-items: stretch;
}
```

Each panel:
- Different shade of blue (or red for problems)
- Large italic title (2.5-4rem)
- Optional icon (72-100px, white)
- Accent divider line (64px wide, 4px height)
- Short description text (max 28ch, ~85% white opacity)

**Title bar** floats at bottom with colored background highlight:
```css
.title-bar h2 {
    display: inline;
    background: var(--tg-dark-blue);
    padding: 0.08em 0.35em;
    box-decoration-break: clone;
}
```

This "highlight box" title technique is used throughout AllMote as the standard footer title treatment.

---

## Before/After Transformation Pattern

Hero comparison layout for showing paradigm shifts:

```html
<div class="ht-hero">
    <div class="ht-side ht-side-old"><!-- muted, transparent bg --></div>
    <div class="ht-arrow-flow">&rarr;</div>
    <div class="ht-side ht-side-new"><!-- white/gradient bg, elevated --></div>
</div>
```

**Key design rules:**
- Old/before: transparent background, white text, subdued
- New/after: white/gradient background, rounded corners (32px), deep box-shadow with ambient glow
- Arrow between: cyan circle with floating animation
- Below: 3-column grid of radical changes, numbered with `01`, `02`, `03`
- Grid separated by thin `1px solid rgba(255,255,255,0.1)` horizontal line

```css
.ht-arrow-flow {
    animation: htArrowFloat 3s ease-in-out infinite;
}
@keyframes htArrowFloat {
    0%, 100% { transform: translateX(0); }
    50%      { transform: translateX(8px); }
}
```

---

## BO Showcase Pattern (Kick-off Card)

Two-panel BO presentation with sub-stepping:

- **Left card** (`.bo-kick-top`): Dark blue, rounded left corners. Shows BO name, customer outcome, value for Telenor, GP targets.
- **Right card** (`.bo-kick-bottom`): Semi-transparent glass effect, hidden initially. Shows detailed customer outcomes, milestones, leading indicators.
- Click/arrow reveals the right card via `.card-visible` class.

GP target display:
```html
<div class="bo-kick-gp">
    <div class="bo-kick-gp-row"><span>2026</span><strong>46 mNOK</strong></div>
    <div class="bo-kick-gp-row"><span>2027</span><strong>86 mNOK</strong></div>
    <div class="bo-kick-gp-row bo-kick-gp-total"><span>Total</span><strong>258 mNOK</strong></div>
</div>
```

---

## Interactive Flywheel Pattern

Circular navigation for process/ceremony cycles:

- 5 nodes positioned in a circle using absolute positioning
- Central hub circle with border and glow
- Clicking a node: scales it to 1.1, fills with cyan, shows detail card
- Detail card on the right with tag, title, frequency, description, and bullet list
- Arrow keys step through nodes sequentially

Step indicator:
```html
<div class="ceremony-step-indicator">01 / 05</div>
```

---

## Collaboration Triangle Pattern

Three actors around a central node with animated connections:

- Central node: glowing circle with `pulseGlow` animation
- Three cards at triangle vertices, each with distinct accent color
- SVG dashed lines with `stroke-dasharray` and CSS `collabFlow` animation
- Edge callout pills on each connection describing the interaction

---

## Icon Showcase Pattern

Present 3-5 concepts using large icons with minimal labels:

- Icons at **56-80px** arranged horizontally or in a 2x3 grid.
- **One-line label** per icon (3-5 words maximum).
- No prose, no descriptions. The icon + label = the entire message.
- Use `layout: icon-showcase` on a dark background.

Best for: growth pillars, capability areas, team functions, strategic themes.

---

## Celebration / Recognition Sections

AllMote decks MUST include 2-3 celebration slides. This is not optional.

- Use `layout: celebration` with warm accent colors (accent_green, accent_yellow).
- **Name individuals and teams** who delivered results.
- Include the specific achievement, not just "good job" — state what they did and the measurable outcome.
- Place celebration slides after the strategic context section, before deep dives.

---

## Photo Divider Pattern

Full-bleed image slide with text overlay:

```html
<div class="slide slide-photo">
    <img class="photo-bg" src="..." alt="">
    <div class="photo-content anim anim-fade">
        <h2><span class="hl">Text with <span class="accent">highlight.</span></span></h2>
    </div>
</div>
```

- Image: `object-fit: cover` filling entire viewport
- Ken Burns zoom: 1.06 → 1.0 on enter
- Text at bottom with dark-blue highlight box treatment
- Use `.anim-fade` (no translate) for text overlay

---

## Closing Charge Pattern

Bold centered statement for the final slide:

```css
.closing-layout h2 {
    font-size: clamp(3rem, 6vw, 5.5rem);
    font-weight: 900;
    line-height: 1.08;
}
```

Structure: large statement with cyan accent word + accent divider line + smaller supporting text.

---

## Popup Overlay Pattern

Full-screen dark blur overlay for detailed content exploration:

- Fixed position, inset 0, z-index 200
- Background: `rgba(3, 2, 40, 0.92)` with `backdrop-filter: blur(12px)`
- Content animates in with `revealUp`
- Close button: circular, top-right, with hover glow
- Click outside content area closes the popup

Used for: mission statement, pillar details, BO deep-dives.

---

## Dynamic Arrow Pattern

Horizontal directional arrow that grows with revealed content:

```css
.chain-container::before {
    clip-path: polygon(0 20%, calc(100% - 80px) 20%, calc(100% - 80px) 0, 100% 50%, calc(100% - 80px) 100%, calc(100% - 80px) 80%, 0 80%);
    background: linear-gradient(90deg, rgba(255,255,255,0.12), rgba(0,200,255,0.35));
    width: var(--arrow-width, 100%);
    transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
```

Width controlled by JavaScript CSS custom property as columns are revealed.

---

## Chart Animation Pattern

Chart.js charts use staggered bar animations:

```javascript
animation: {
    duration: 800,
    delay: function(ctx) {
        return ctx.dataIndex * 200 + (ctx.datasetIndex * 100);
    },
    easing: 'easeOutQuart'
}
```

Charts are created/destroyed based on slide visibility to avoid memory leaks:

```javascript
const mo = new MutationObserver(() => {
    if (slide.classList.contains('slide-active')) {
        initChart();
    } else {
        destroyChart();
    }
});
mo.observe(slide, { attributes: true, attributeFilter: ['class'] });
```

---

## Navigation System

AllMote presentations include fixed navigation UI:

- **Progress bar:** Top of screen, gradient fill, 4px height, glowing shadow
- **Slide counter:** Bottom-left pill badge showing `n / total`
- **Logo:** Bottom-right, 36px, 50% opacity (90% on hover)
- **Keyboard:** Arrow keys, Space, PageDown/Up, Home/End, F for fullscreen
- **Click navigation:** Click anywhere (except interactive elements) advances to next slide/step

---

## Fast Pacing Guidelines

AllMote pacing follows a 30-second-per-slide rhythm:

| Metric        | Target         |
|:--------------|:---------------|
| Seconds/slide | ~30 seconds    |
| Total slides  | 20-40          |
| Total time    | 10-20 minutes  |
| Words on screen | 5-15 per slide |
| Words in notes | 50-150 per slide |

**Exception:** Sub-stepping slides may take 60-90 seconds total as content is progressively revealed.

---

## Emotional Impact Test

Before finalizing an AllMote slide, apply this test:

> If someone photographs this one slide and shares it on Slack, does it make immediate emotional impact?

If the answer is "no," the slide needs:
- A bigger number
- Fewer words
- A stronger visual contrast
- A more provocative statement

---

## AllMote Slide Checklist

Before finalizing an AllMote slide, verify:

- [ ] Audience understands the point within 3 seconds
- [ ] Maximum 15 words visible on screen (detail in speaker notes)
- [ ] Every slide has a clear visual anchor (number, icon, statement, or image)
- [ ] Speaker notes contain 50-150 words of context for the presenter
- [ ] Celebration slides are present (minimum 2-3 in every AllMote deck)
- [ ] Animations are purposeful (reveal = builds tension, not just "looks cool")
- [ ] Sub-stepping is used only where progressive build adds meaning
- [ ] The Slack photo test passes for key slides
- [ ] Total deck is 20-40 slides at ~30 seconds each
- [ ] All `.anim` elements have appropriate delay classes for stagger order
- [ ] Counter animations reset on slide exit and replay on re-entry
