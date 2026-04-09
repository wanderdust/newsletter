---
title: 'Book Structure'
date: '2026-04-09T00:00:00+01:00'
draft: true
summary: ''
tags: []
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---


## Step 1 - Target Audience

> Complete this before writing or restructuring anything. If you can't answer these clearly, the book isn't ready to write.

**Who exactly is reading this?**
Describe one specific person: their role, seniority, tech stack, and current relationship with AI tools.


```

A junior, mid, or senior data engineer who builds data pipelines in the warehouse (DBT, Databricks, Snowflake) and orchestrates them with Airflow.

**Skills and knowledge:**
- Git, Python, SQL, PySpark, Airflow
- Strong business logic knowledge — they understand the data they work with, not just the technical layer

**Production responsibilities:**
- Own pipelines in production — on-call, support, fix breakages
- Follow engineering best practices: monitoring, dashboards, alerts
- Some testing, but not much

**Current AI usage:**
- Use AI tools (Cursor, Claude) for code completion and quick questions
- Not using fully agentic workflows with feedback loops that enable autonomous development with minimal human interaction
- AI is underutilised — they know it can do more but haven't bridged the gap

**Team context:**
- Work on teams of any size
- No standardised approach to AI — every engineer uses it their own way
- Want to use AI tools professionally and consistently in their workplace
```
---

**What problem brought them here?**
What pain, frustration, or missed opportunity made them pick up this book?

```
They use AI, but it's mostly copy-paste prompts and manual workflows. They know they could automate more but don't know how to get there. Their team has no shared approach — everyone uses AI their own way. They may not even be aware of what's possible with fully agentic workflows.
```

---

**What can they do after finishing?**
One concrete, observable outcome.

```
They can hand an agent a task — building a pipeline, migrating a table, troubleshooting a support issue — and get back working, validated code with minimal interaction. Their agents have the tools and context to autonomously gather information, execute code, and validate their own implementations.
```

---

## Step 2 — Transformation Arc

> The book takes the reader from a known starting state to a defined end state.
> Every chapter is a step on that journey — not just a topic.

**Before (reader's starting state):**

```
[e.g. Uses LLMs reactively — prompts ChatGPT, accepts Copilot suggestions, but drives everything manually.]
```

**After (reader's end state):**

```
[e.g. Designs and delegates to autonomous agents that handle DE tasks end-to-end, with the right
guardrails, tooling, and team practices in place.]
```

---

**The Arc (Parts of the book):**

| Part | Name | What it does for the reader |
|------|------|-----------------------------|
| 1 | WHY | Shifts mindset — explains why agentic now, and why DEs specifically benefit |
| 2 | FOUNDATION | Builds the base — environment, spec-driven thinking, planning before building |
| 3 | CORE SKILLS | Teaches the techniques — DE-specific: dbt, Airflow, Spark, data quality, pipelines |
| 4 | SCALE | Expands to teams and production — multi-agent, security, shared standards |

> For each part, fill in:

**Part 1 — WHY**
- Reader enters knowing: `[fill in]`
- Reader leaves knowing: `[fill in]`
- The DE-specific hook: `[the concrete DE scenario that opens this part]`

**Part 2 — FOUNDATION**
- Reader enters knowing: `[fill in]`
- Reader leaves knowing: `[fill in]`
- The DE-specific hook: `[fill in]`

**Part 3 — CORE SKILLS**
- Reader enters knowing: `[fill in]`
- Reader leaves knowing: `[fill in]`
- The DE-specific hook: `[fill in]`

**Part 4 — SCALE**
- Reader enters knowing: `[fill in]`
- Reader leaves knowing: `[fill in]`
- The DE-specific hook: `[fill in]`
