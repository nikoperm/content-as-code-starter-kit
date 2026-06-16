---
name: bo-builder
description: >-
  Creates, validates, and places Business Opportunities (BOs) according to the
  Execution Framework. Ensures every BO has all 6 required fields, calculates
  accumulated value per the BO Calculation Guide, and cross-checks against
  existing BOs in value_stream_snapshot.md.
---

# BO Builder Skill

## Purpose

The Business Opportunity is the core execution unit of the strategy. This skill ensures every BO is created with commercial rigor — no "XXX" placeholders, no missing fields, no financial guesswork.

## When to Use

- When asked to create a new Business Opportunity
- When asked to evaluate or validate an existing BO
- When a roadmap discussion identifies a new initiative that should become a BO

## The BO Format — All 6 Fields Are Mandatory

Every BO follows this exact structure. **No field may be skipped or left empty.** The canonical visual reference is the BO showcase example in `presentations/` (see the `.slide-bo-showcase` layout in the presentation-design skill).

### Visual Layout (two-panel card)

```
+-------------------------------------+--------------------------------------+
| [CATEGORY TAG]                      | Customer Outcome                     |
| # BO Name                           | WHAT DOES THE CUSTOMER EXPERIENCE?   |
| One-sentence description            | - Bullet 1                           |
|                                     | - Bullet 2                           |
| Customer Outcome                    | - Bullet 3                           |
| WHAT DOES THE CUSTOMER EXPERIENCE?  |                                      |
| Summary paragraph from customer POV | Key Milestones                       |
|                                     | WHAT WILL BE DELIVERED WHEN?         |
| Value for the Organization          | - Q1: Binary deliverable             |
| WHY ARE WE DOING THIS?              | - Q2: Binary deliverable             |
| Summary paragraph                   | - Q3: Binary deliverable             |
|                                     |                                      |
| +--------+ +--------+ +----------+  | Leading Indicators                   |
| | Year 1 | | Year 2 | |  Total   |  | HOW DO WE KNOW IT'S WORKING?        |
| | X mNOK | | X mNOK | | X mNOK   |  | - Measurable metric 1               |
| +--------+ +--------+ +----------+  | - Measurable metric 2               |
+-------------------------------------+--------------------------------------+
```

### Markdown Template

Use this exact structure when generating a BO document:

```markdown
---
title: "Business Opportunity: [Name]"
purpose: "One-sentence description"
status: draft
version: "1.0"
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: agent
domain: roadmap
related:
  - strategy/roadmap/[growth_area]/[strategy_file].md
  - strategy/roadmap/bo_calculation_guide.md
---

# BO: [Name]

**Category:** [e.g., Security | Customer Solutions | Efficient Admin | Access | Enablement]

**Description:** [One-sentence summary of the initiative]

## 1. Customer Outcome

> "As a [customer role], I experience [tangible value]. [Specific benefit 1], [specific benefit 2], and [specific benefit 3]."

**What does the customer experience?**
- [Concrete outcome 1]
- [Concrete outcome 2]
- [Concrete outcome 3]

## 2. Value for the Organization

**Why are we doing this?**

[1-2 sentences on strategic/commercial value — new revenue, churn prevention, market position, etc.]

## 3. Financial Targets

Calculated per [BO Calculation Guide](../../roadmap/bo_calculation_guide.md).

| Year | Incremental Growth | Accumulated BO Value |
|:-----|:-------------------|:---------------------|
| Year 1 | +X mNOK | X mNOK |
| Year 2 | +X mNOK | X mNOK |
| Year 3 | +X mNOK | X mNOK |
| **Total** | | **X mNOK** |

## 4. Key Milestones

**What will be delivered when?**
- **Q1**: [Binary deliverable — done or not done]
- **Q2**: [Binary deliverable]
- **Q3**: [Binary deliverable]
- **Q4**: [Binary deliverable]

## 5. Leading Indicators

**How do we know it's working?**
- [Measurable metric that shows traction before financial results]
- [Another leading indicator]
- [Another leading indicator]

## 6. Dependencies & Risks

- [Key dependency or risk]
- [Another dependency or risk]
```

### Guardrails for Each Field

| Field | Rule |
|:------|:-----|
| Customer Outcome | Written from the customer's perspective ("As a..."). Must be specific enough that a customer would nod. |
| Value for the Organization | Must connect to strategic value creation — SaaS revenue, service-led growth, churn prevention. **Never frame as cost-cutting for the customer that cannibalizes your own ARPU.** |
| Financial Targets | Must use the accumulation method from `bo_calculation_guide.md`. Never flat annual numbers. |
| Key Milestones | Binary (done/not done). Never "continue to..." or "ongoing". |
| Leading Indicators | Measurable (number, percentage, ratio). Never vague ("improve quality"). |
| Dependencies | Technical, organizational, or market dependencies that could block execution. |

## Step 1: Gather Input

Ask for or derive these inputs:

| Input | Required? | Source |
|:------|:----------|:-------|
| What the initiative does | Yes | Conversation with human |
| Which growth area it belongs to | Yes | Your organization's defined growth areas (e.g., Security / Customer Solutions / Efficient Admin) |
| Which strategic pillar it supports | Yes | One of the pillars in `strategy/current_state/strategic_foundation.md` |
| Customer problem it solves | Yes | Conversation or existing roadmap docs |
| Revenue/GP estimates per year | Yes | Conversation, market data, or analogies |

## Step 2: Understand the Product and Ground Financial Data

Before writing anything, read these files:

1. **`strategy/current_state/service_catalog.md`** — look up the product your BO involves. Read what it IS and what it is NOT. If your BO description contradicts the service catalog, your BO is wrong.
2. `strategy/current_state/market_position.md` — subscription base, ARPU, market share
3. `strategy/current_state/value_stream_snapshot.md` — existing BOs and their targets
4. `strategy/roadmap/bo_calculation_guide.md` — the accumulation methodology

**Never invent baseline numbers.** Use the real data from the repo.

> **Note:** These file paths are examples from the starter kit structure. Adapt them to match your workspace's actual file layout.

## Step 3: Calculate Financial Value

Follow the methodology in `strategy/roadmap/bo_calculation_guide.md`:

1. Estimate incremental growth for each year
2. Accumulated value = previous year's value + this year's increment
3. Total BO value = sum of all accumulated annual values
4. Report both **Total BO value** (accumulated) and **Annual run-rate at final year**

## Step 4: Cross-Check

Before finalizing:

1. Read `strategy/current_state/value_stream_snapshot.md` — does a similar BO already exist?
2. If yes: update the existing BO instead of creating a duplicate
3. If no: proceed with placement

## Step 5: Place the BO

1. Add the BO to the appropriate roadmap file under `strategy/roadmap/`:
   - Example: Security BOs go in `strategy/roadmap/security/security_strategy.md`
   - Example: Customer Solutions BOs go in `strategy/roadmap/customer_solutions/customer_solutions_strategy.md`
2. Update `strategy/current_state/value_stream_snapshot.md` with the new BO summary
3. Update CATALOG.md if a new file was created
4. Run `make validate` to confirm integrity

## Step 6: Generate BO Presentation Slide (if asked for a presentation)

When the BO should be presented visually (in a presentation or demo), use the **BO Showcase** slide layout from the presentation-design skill:

1. Read the HTML structure in `reference_allmote.html` (the `.slide-bo-showcase` layout)
2. The layout is a two-panel card:
   - **Left card** (`.bo-kick-top`): Category tag, BO name, description, Customer Outcome summary, Value for the Organization, 3 financial target pills (Year 1, Year 2, Total)
   - **Right card** (`.bo-kick-bottom`, click-to-reveal): Customer Outcome bullets, Key Milestones, Leading Indicators
3. Write it as self-contained HTML with Telegrafen styling — **never** use `build_presentation.py`
4. All 6 BO fields must be visible in the slide — this is the visual proof that the BO is complete

This step is triggered automatically when the user asks to "present", "visualize", or "demo" a BO.

---

## What NOT to Do

- **Never create a BO without all 6 fields filled** — that makes it "discovery", not an executable BO
- **Never use "XXX" or "TBD" for financial values** — estimate conservatively if uncertain
- **Never use flat annual numbers** — always calculate accumulated value
- **Never frame value as customer cost-cutting** — the strategy is about service-led SaaS growth, not volume discounting
- **Never invent baseline data** — read `market_position.md` and `value_stream_snapshot.md`
- **Never skip Leading Indicators** — they are the early-warning system for whether the BO is working
