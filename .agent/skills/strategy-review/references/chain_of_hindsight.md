# Chain of Hindsight — Learning Framework

## Purpose

The Chain of Hindsight ensures **institutional learning** across strategy reviews. Every review generates insights that should improve future reviews and strategy development. Without this, we repeat mistakes and lose patterns.

This framework implements three mechanisms:
1. **Logging** — Capture learnings after every review
2. **Pattern Detection** — Identify recurring themes across reviews
3. **Active Reference** — Use past learnings to inform future reviews

---

## Learning Classifications

Every learning is classified into one of three types:

### 🧠 Smart Move
Something done well that should become a standard practice.

**Examples:**
- "Using bottom-up market sizing instead of top-down — produced 60% more realistic targets"
- "Including customer quotes in the value proposition section — made the argument 10x more compelling"

### 🕳️ Blind Spot
Something that was missed, underestimated, or overlooked.

**Examples:**
- "No mention of regulatory risk in sovereign cloud strategy — this is a dealbreaker for enterprise customers"
- "Transformation timeline assumed 100% internal capability build — should have considered partner/acquire options"

### 🔄 Pattern
A recurring theme observed across multiple reviews — positive or negative.

**Examples:**
- "3 out of 4 transformation plans underestimate change management effort by 2x"
- "Documents with clear 'customer problem' framing consistently score 2+ points higher on Commercial Viability"

---

## Hindsight Log Format

The living log is maintained at: `.agent/skills/strategy-review/hindsight_log.md`

Each entry follows this format:

```markdown
### [YYYY-MM-DD] — Review of [Document Name]

| Type | Learning | Impact | Action |
|------|----------|--------|--------|
| 🧠/🕳️/🔄 | [Concise description] | [Which dimension(s) affected] | [What to do differently] |
```

---

## How to Use the Hindsight Log

### Before a Review (Step 1)
1. Open `hindsight_log.md`
2. Scan for **🔄 Patterns** — these are the most valuable as they represent systemic issues
3. Check if any past **🕳️ Blind Spots** are relevant to the current document type
4. Actively look for these issues during the review

### After a Review (Step 5)
1. Identify at least **1 learning** from the review (more is better)
2. Classify it as 🧠, 🕳️, or 🔄
3. Append to `hindsight_log.md`
4. If you notice a **🕳️ Blind Spot** appearing for the 3rd+ time, escalate it to a **🔄 Pattern**

### Pattern Escalation Rules
- **2 occurrences**: Flag as "potential pattern" in the log
- **3+ occurrences**: Promote to **🔄 Pattern** with a summary entry at the top of the log
- **Patterns** should be given special weight in future reviews — they represent systemic strategy weaknesses

---

## Quarterly Review Cadence

Every ~10 reviews (or quarterly), conduct a **meta-review** of the hindsight log:

1. **Compile all patterns** — What are the top 3-5 recurring issues?
2. **Assess progress** — Are blind spots being addressed? Are smart moves becoming standard?
3. **Update scoring framework** — Should dimension weights change based on observed patterns?
4. **Create a "Strategy Playbook" entry** — Distill the biggest learnings into actionable guidelines for strategy authors

This meta-review is logged as a special entry in the hindsight log with the heading:

```markdown
## 📊 META-REVIEW — [YYYY-MM-DD]
```

---

## Initial Seed Patterns

Based on industry experience, start with these known patterns:

| Type | Pattern | Frequency |
|------|---------|-----------|
| 🔄 | Telco strategies overestimate market size by 3-5x by using top-down TAM without bottom-up validation | Very Common |
| 🔄 | Transformation plans underestimate change management and cultural resistance | Very Common |
| 🔄 | AI/technology is mentioned as buzzword without concrete operationalization plan | Common |
| 🔄 | B2B strategies are product-push rather than customer-problem-pull | Common |
| 🔄 | Execution timelines assume perfect organizational alignment that doesn't exist | Common |
| 🔄 | Risk sections are boilerplate copy-paste rather than strategy-specific analysis | Occasional |
