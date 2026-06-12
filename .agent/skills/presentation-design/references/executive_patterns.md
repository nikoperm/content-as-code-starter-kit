# Executive Patterns

McKinsey-style preread/slideument best practices for `mode: executive`.

---

## The Pyramid Principle (Barbara Minto)

Structure every executive deck as an inverted pyramid:

1. **Governing thought first** -- State the conclusion/recommendation on slide 2.
2. **Supporting arguments** -- Each section proves one part of the conclusion.
3. **Evidence at the base** -- Data, charts, and analysis support each argument.

The reader should understand the complete recommendation by slide 2. Everything that follows is evidence proving why that recommendation is correct.

---

## Action Title Rules

Every main slide MUST have an action title -- a full sentence that:

- **States a conclusion**, not a topic. Write "Volume logic cannot bridge the 603 mNOK gap" not "Growth Challenges."
- **Proves the body.** The slide body must be evidence supporting the title. If the body does not prove the title, either the title or the body is wrong.
- **Reads as a standalone narrative.** Reading ONLY the action titles of all slides should tell the complete story from problem to recommendation.

**The Ghost Deck Test:** Print only the action titles on a blank page. If a board member can understand the complete argument and recommendation from the titles alone, the deck passes.

---

## Vertical Logic

On every slide, apply vertical logic top to bottom:

```
Action Title (the assertion)
    |
    v
Body Content (the evidence)
    |
    v
Source Footnote (the authority)
```

Every element on the slide body MUST prove the action title. If an element does not contribute to proving the title, remove it or move it to an appendix.

---

## Evidence Exhibit Pattern

The most common data slide in executive mode. Structure:

1. **Action title** -- The insight the data proves.
2. **Chart or table** -- The visual evidence (annotated with the key data point).
3. **Takeaway box** -- 1-2 sentence callout restating the "so what?" of the chart.
4. **Source citation** -- "Source: NKOM 2H 2025, Telenor internal data"

Use `layout: evidence-exhibit` for this pattern.

---

## Source Citation Format

Every data slide requires a source footnote. Format:

```
Source: [Authority], [Date/Period]. Internal analysis by [Team].
```

Examples:
- "Source: NKOM Ekom Market Report, 2H 2025."
- "Source: Telenor internal financial model, May 2026. All figures in MNOK."
- "Source: Gartner, Q1 2026. Adapted for Norwegian market by S&F."

Place source citations at the bottom of the slide body, after all content.

---

## Information Density Guidelines

Executive slides are self-reading documents. Density is a feature, not a bug.

| Element             | Executive target                                        |
|:--------------------|:--------------------------------------------------------|
| Text per slide      | 100-200 words (more than narrative, much more than allmote) |
| Tables              | Preferred. Use tables to structure comparisons.         |
| Sub-sections        | Use H3/H4 within the slide body for structure.          |
| Font size (HTML)    | Body at 0.85-0.95rem. Footnotes at 0.75rem.            |
| Charts              | Annotated "exhibits" with callout boxes and sources.    |
| Speaker notes       | Optional -- the slide IS the document.                  |

**Every chart needs an insight label** -- the "so what?" must be visible on the chart itself, not buried in surrounding text.

---

## SCR Framework for Story Arc

Structure the overall executive deck using Situation-Complication-Resolution:

| Phase          | Slides | Content                                              |
|:---------------|:-------|:-----------------------------------------------------|
| **Executive Summary** | 1-2   | The governing recommendation in full.           |
| **Situation**  | 3-4    | Current state, market position, what is working.     |
| **Complication** | 5-6  | The gap, the threat, why the status quo fails.       |
| **Resolution** | 7-10   | The strategic response, growth pillars, evidence.    |
| **Evidence**   | 11-15  | Deep dives, financial models, proof points.          |
| **Recommendation** | 16-17 | Specific actions, timelines, resource asks.       |
| **Appendix**   | 18+    | Supporting data, methodology, detailed tables.       |

Target: 10-20 slides total. The reader should be able to stop at slide 2 and understand the recommendation, or continue to any depth for evidence.

---

## Executive Slide Checklist

Before finalizing an executive slide, verify:

- [ ] Action title is a complete sentence stating a conclusion
- [ ] Body content proves the action title (vertical logic)
- [ ] Source citation present on every data slide
- [ ] Reading all action titles in sequence tells the complete story
- [ ] No decorative elements -- every visual element carries information
- [ ] Preread slides (Nb) provide deep-dive evidence for the parent slide
- [ ] Tables used for structured comparisons (not bullets)
- [ ] The deck prints to PDF with zero loss of information
