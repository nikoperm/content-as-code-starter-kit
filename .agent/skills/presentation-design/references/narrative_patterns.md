# Narrative Patterns

Strategic narrative presentation best practices for `mode: narrative`.

---

## Core Philosophy

Every narrative slide has BOTH a visual anchor AND substantive content. The presenter enriches the slide, but the slide carries weight on its own. This mode sits between the density of executive and the minimalism of AllMote.

---

## Visual Anchor + Substantive Content Balance

Each slide must contain:

1. **A visual anchor** -- chart, icon, diagram, or structured visual that draws the eye.
2. **Substantive text** -- 2-3 sentences or a compact table that adds meaning beyond the visual.

If a slide has only text, add a chart or icon. If a slide has only a chart, add an insight annotation and takeaway text.

---

## Insight-Driven Titles

Narrative titles go beyond simple action titles. They should make the audience think:

| Weak title                    | Strong insight-driven title                                    |
|:------------------------------|:---------------------------------------------------------------|
| "Market Share Overview"       | "XX% dominance built on clarity, not price"                  |
| "Growth Opportunities"        | "Four battles our customers fight every day"                   |
| "Security Strategy"           | "The perimeter vanished -- identity is the new firewall"       |
| "Financial Projections"       | "Volume logic cannot bridge the 603 mNOK gap"                  |

The title should provoke curiosity or convey an insight, not just label the content.

---

## Chart Annotation Patterns

Every chart in narrative mode requires visible annotations:

1. **Insight callout box** -- Positioned near the key data point. Uses the Telegrafen annotation style: semi-transparent background, Telenor Blue border, bold text.
2. **Key takeaway** -- 1-2 sentences below or beside the chart explaining the "so what?"
3. **Trend highlight** -- Circle, arrow, or color contrast drawing attention to the critical trend.

```markdown
<!-- chart:
  type: bar
  title: "GP Growth Potential by Pillar"
  data:
    labels: [Security, Solutions, "5G/IoT", Admin]
    series:
      - name: Potential
        values: [506, 266, 329, 118]
        color: "#00C8FF"
  annotation: "Security leads with +506 MNOK"
-->
```

The audience should understand the chart's point without the presenter speaking.

---

## Progressive Narrative Build

Each slide earns the right to the next. The narrative follows a deliberate arc:

| Phase            | Purpose                                    | Typical layouts                  |
|:-----------------|:-------------------------------------------|:---------------------------------|
| **Context**      | Set the scene, establish shared reality    | `story-build`, `context-split`   |
| **Key Insight**  | Reveal the critical finding or tension     | `key-finding`, `insight-chart`   |
| **Evidence**     | Prove the insight with data                | `insight-chart`, `dashboard`     |
| **Implications** | What this means for the organization       | `story-build`, `cards-grid`      |
| **Response**     | The strategic answer                       | `cards-grid`, `comparison`       |
| **Next Steps**   | Concrete actions and timeline              | `timeline`, `numbers-panel`      |

Each slide should reference or build on the previous one. Avoid orphan slides that break the narrative flow.

---

## Icon Integration for Categorization

Icons serve a functional role in narrative mode -- they categorize and reinforce meaning:

- Use the **same icon consistently** for a concept throughout the deck (e.g., `Security_expanded.svg` for all security content).
- Place icons at **40-48px** in card layouts, **56px** in dividers.
- Icons should **reinforce**, not decorate. If an icon does not help the audience identify the category faster, remove it.

---

## Subtle Animation Principles

Narrative animations are polish, not spectacle:

- **Chart data reveals** -- Data series animate in over 800ms. Creates a natural "reading" flow.
- **Smooth slide transitions** -- Fade or slide-left between slides. No bouncing, spinning, or flashing.
- **Staggered content** -- In `cards-grid` layouts, cards may appear one by one with 200ms delays.
- **Never animate text** -- Body text appears immediately. Only charts, icons, and structural elements animate.

---

## Narrative Slide Checklist

Before finalizing a narrative slide, verify:

- [ ] Slide has both a visual anchor and substantive text content
- [ ] Title is insight-driven (not just a topic label)
- [ ] Charts have visible annotation callouts and a "so what?" takeaway
- [ ] Slide connects logically to the previous and next slides in the arc
- [ ] Icons are functional (categorize content) not decorative
- [ ] Speaker notes carry additional context the presenter will share verbally
- [ ] 12-25 slides total for a narrative deck
