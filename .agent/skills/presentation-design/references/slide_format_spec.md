# Slide Format Specification

Complete YAML directive reference for presentation markdown files.

---

## Document-Level Front-Matter

Every presentation markdown file begins with YAML front-matter:

```yaml
---
title: "Presentation Title"
subtitle: "Optional subtitle"
mode: narrative              # executive | narrative | allmote
audience: leadership         # leadership | board | all-company | department | external
sensitivity: internal        # internal | confidential | public
date: 2026-05-29
footer_left: "Telenor Norge B2B Mobile  •  Strategi & Forretningsutvikling"
---
```

| Field         | Required | Default                                                    |
|:--------------|:---------|:-----------------------------------------------------------|
| `title`       | Yes      | --                                                         |
| `subtitle`    | No       | --                                                         |
| `mode`        | Yes      | `narrative`                                                |
| `audience`    | No       | `leadership`                                               |
| `sensitivity` | No       | `internal`                                                 |
| `date`        | No       | --                                                         |
| `footer_left` | No       | `Telenor Norge B2B Mobile  •  Strategi & Forretningsutvikling` |

---

## Slide Heading Convention

Each slide starts with an H2 heading:

```markdown
## Slide 1 — Title of the Slide
```

**Numbering rules:**
- Main slides: `1`, `2`, `3`, ...
- Preread/background slides: `1b`, `2b` (appended `b` = preread role)
- Sub-slides in a deep-dive: `4b`, `4b-2`, `4b-3`, ...
- The parser extracts the ID (`1`, `1b`, `4b-2`) and title from the heading.

---

## `<!-- slide: -->` Block

Optional YAML metadata placed immediately after the slide heading:

```markdown
<!-- slide:
  theme: statement
  layout: insight-chart
  pptx_layout: "Title and Content"
  icon: Security_expanded.svg
  transition: fade
-->
```

| Field         | Values                                        | Default (inferred)     |
|:--------------|:----------------------------------------------|:-----------------------|
| `theme`       | `statement` (dark bg), `light`, `dark`        | Inferred from mode/title |
| `layout`      | Any of the 29 layout names                    | Inferred from content  |
| `pptx_layout` | PowerPoint slide master layout name           | Mapped from `layout`   |
| `icon`        | Filename from `reference/icons/`              | None                   |
| `transition`  | `none`, `fade`, `slide-left`, `slide-right`   | `none`                 |

If omitted, the parser infers theme, layout, and role from the slide content and mode.

---

## `<!-- chart: -->` Block

Inline chart definition (rendered via Chart.js in HTML):

```markdown
<!-- chart:
  type: bar
  title: "Gross Profit Scenarios"
  data:
    labels: [2025, 2026, 2027, 2028, 2029]
    series:
      - name: Baseline
        values: [4480, 4551, 4461, 4371, 4281]
        color: "#070452"
      - name: Target
        values: [4480, 4700, 4900, 5100, 5300]
        color: "#00C8FF"
  annotation: "+603 mNOK gap"
-->
```

See `chart_spec.md` for full type and data format reference.

---

## `<!-- card: -->` Block

Cards for `cards-grid` layout. Each card is a separate HTML comment block followed by body text:

```markdown
<!-- card:
  icon: SecurityPhone_expanded.svg
  title: "Safe Employee"
  accent: "#00C8FF"
-->
Frictionless protection for human behavior risks.

<!-- card:
  icon: CellTower_expanded.svg
  title: "Secure Mobile"
  accent: "#B0FBB8"
-->
End-to-end network-embedded mobile protection.
```

| Field    | Required | Description                                |
|:---------|:---------|:-------------------------------------------|
| `icon`   | No       | Icon filename from `reference/icons/`      |
| `title`  | Yes      | Card heading                               |
| `accent` | No       | Accent color (hex). Defaults to Telenor Blue |

Body text follows the closing `-->` and extends until the next `<!-- card:` or end of slide.

---

## `[[MACRO_NAME]]` Macro References

Reference pre-built chart functions from `build_html.py`:

```markdown
> [[GP_SCENARIOS_CHART]]
```

Macros are expanded during build into full HTML chart blocks. See `chart_spec.md` for the complete macro list.

---

## `**Headline:** *text*` Pattern

Action title displayed prominently at the top of the slide:

```markdown
**Headline:** *XX% market share -- built on clarity, ownership, and commercial spirit.*
```

The parser extracts this into the `headline` field of the slide model. It is rendered as the slide's primary assertion/action title, separate from the body content.

---

## Speaker Notes

Slides with ID suffix `b` (e.g., `1b`) are automatically paired as speaker notes for the parent slide (e.g., `1`). The body content of the `b` slide becomes the `speaker_notes` field on the parent.
