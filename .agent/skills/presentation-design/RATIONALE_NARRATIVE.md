---
title: "Design Rationale — Narrative Presentation Type"
purpose: "Documents why each design decision was made for narrative/strategy vision presentations"
status: active
version: "1.0"
created: 2026-05-29
updated: 2026-05-29
author: collaborative
domain: presentation
related:
  - .agent/skills/presentation-design/SKILL.md
  - .agent/skills/presentation-design/reference_narrative.html
---

# Design Rationale — Narrative Presentations

This document explains why each design decision was made during the iterative creation of Strategy 20:30 Narrative (May 2026). It exists so future agents reproduce the same quality without re-learning through trial and error.

**Reference file**: `.agent/skills/presentation-design/reference_narrative.html`

---

## Open layout over white cards

**Problem**: Early versions used white cards with shadows on light cyan backgrounds. The result was visually cluttered — cards created unnecessary borders, the shadows added visual noise, and the content felt boxed in with wasted space.

**Solution**: Content lives directly on the Light Cyan background. Visual hierarchy comes from typography weight, color, and spacing — not container borders. White cards are only used on dark backgrounds (Mid Blue, Dark Blue) where contrast is necessary.

**Exception**: Engine/pillar overview cards on Mid Blue backgrounds still use white cards because the contrast serves a purpose.

---

## Icons must be large (64-100px)

**Problem**: Small icons (24-44px) in small icon stages looked decorative rather than purposeful. On a presentation projected on screen, they were nearly invisible and added visual noise without communicating.

**Solution**: Icons are either large enough to be a visual anchor (64px minimum in open layout, 100px in icon stages) or removed entirely. If an icon would be smaller than 36px, it shouldn't be there.

---

## Customer need callouts on deep-dive slides

**Problem**: Pillar deep-dives listed features and GP targets but didn't connect to why customers care. The slides were internally focused — "what we sell" rather than "what pain we solve."

**Solution**: Each pillar deep-dive starts with a customer quote in italic, tied to one of the four customer battles (Trust Crisis, AI Dilemma, Efficiency Trap, Complexity Burden). This anchors every pillar in customer reality and creates a through-line from the battles slide.

---

## No per-slide footers

**Problem**: Every slide had a footer with the Telenor logo, "Telenor Norge B2B Mobile" text, and a slide number. Combined with the fixed nav-counter pill, this was redundant — two slide counters visible simultaneously.

**Solution**: Remove all per-slide footers. The fixed nav-counter (bottom-left) handles slide numbering. A fixed Telenor propeller logo (36px, bottom-right) provides brand presence. Cleaner, and every slide gains ~40px of usable vertical space.

---

## Scroll-triggered animations

**Problem**: Slides appeared fully formed on navigation — static, like a PDF. No sense of build-up or narrative progression within each slide.

**Solution**: IntersectionObserver adds `.visible` class when slides enter viewport. Elements fade in with `translateY(24px)` to `0` using staggered delays (0.12s, 0.24s, 0.36s etc.). The user sees the slide "build up" — header first, then governing thought, then content columns. This creates a presenter-like rhythm even in self-navigation.

**Key decisions**:
- Elements animate only once (observer unobserves after trigger)
- Title slide gets `.visible` immediately at load — no animation
- Photo dividers use fade-only (no translateY) plus subtle image zoom
- Easing: `cubic-bezier(0.16, 1, 0.3, 1)` — fast start, gentle landing
- Duration: 0.7s for elements, 1.8s for photo zoom

---

## Progressive chart animations

**Problem**: Chart.js default animation plays all bars/lines simultaneously in 1 second. On a projected presentation, this looks like a flash — you can't follow the data narrative.

**Solution**: Each data point animates with a 300ms delay per year (`dataIndex * 300`) plus 150ms per dataset. A 4-year bar chart with 3 datasets builds over ~2 seconds, letting the audience follow the trajectory year by year.

---

## Photo dividers at transition points

**Problem**: Many content slides in a row creates fatigue. The narrative arc has natural breaks — between "the opportunity" and "the problem," between "the how" and "the cost" — that need visual breathing room.

**Solution**: Photo dividers at narrative transitions. Each has:
- Full-bleed brand photo with dark gradient overlay
- A bridge sentence that connects what came before to what comes next
- Subtle zoom effect (scale 1.06 to 1.0 over 1.8s) for visual dynamism
- No data, no stats — pure narrative pause

**Placement principle**: Photo dividers mark a shift in topic or emotional register. They should never feel like filler.

---

## 0.82rem minimum font size

**Problem**: Font sizes of 0.68-0.75rem were unreadable at presentation distance. Norwegian detail text under battle rows, sub-pillar descriptions, and timeline items were too small to serve their purpose.

**Solution**: Hard minimum of 0.82rem for any text that should be readable. Kickers can be 0.82rem with letter-spacing to compensate. Body text should be 0.92-1rem.

---

## Two-column chart + insights layout

**Problem**: Full-width charts waste horizontal space and force the audience to look at data without interpretation. The chart tells what; the insight panel tells why.

**Solution**: Charts take 55-60% width on the left. The right 40-45% contains a governing thought (the "so what") and 3-4 proof points with colored border-left accents and large italic numbers. This is the McKinsey/BCG pattern adapted to Telegrafen aesthetics.

---

## Off-white (#E8FDFF) for icon stages and stat boxes

**Problem**: Early iterations used `rgba(0,200,255,0.08)` for icon backgrounds, creating a cyan tint that looked different from the card-based slides. Stat boxes used `rgba(28,22,197,0.04)` which was nearly invisible.

**Solution**: Standardized on `var(--tg-off-white)` (#E8FDFF) for all icon stages and stat boxes. Same color as engine cards and pillar overview, creating visual consistency across slide types.

---

## Governing thoughts between header and content

**Problem**: Slides had a header, then jumped straight to data/content. The audience had to figure out the "so what" themselves.

**Solution**: A governing thought — one sentence, 1.05-1.2rem, weight 600-700 — sits between the header and the content. It tells the audience what to take away before they see the evidence. This is the Pyramid Principle applied to slide design.

---

## Narrative story arc for strategy presentations

The approved narrative structure for a Strategy 20:30 presentation:

1. **Title** — Vision Document badge, bold title
2. **Turnaround proof** — We're winning on value (chart + stats)
3. **Growth gap** — But volume is dying, here's the gap (bar chart + bridge)
4. **Customer battles** — What customers actually need (4 battles table)
5. **Pillar overview** — Our five growth answers (cards on blue)
6-9. **Pillar deep dives** — Each with customer need callout + data
10. **GP scenarios** — Financial trajectory with 4 scenario lines
11. **Photo divider** — Transition: opportunity to reality
12. **Legacy trap** — Why we must change (FTE allocation chart)
13. **Transformation engine** — Three levers overview
14. **20:30 model** — The core transformation (goal + 3 enablers)
15. **Agentic proof** — From 10 Hours to 10 Minutes
16. **Photo divider** — Transition: plan to capacity
17. **Capacity equation** — Headcount chart + proof points
18. **Photo divider** — The road ahead
19. **Execution roadmap** — 2026 detail + 2027-2029 horizon
20. **Risk & mitigation** — Table format
21. **Closing statement** — Bold italic call to action
