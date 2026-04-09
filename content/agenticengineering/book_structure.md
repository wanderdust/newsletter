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


## Step 1 — Target Audience

### The Reader

A junior, mid, or senior data engineer who builds data pipelines in the warehouse (DBT, Databricks, Snowflake) and orchestrates them with Airflow.

**Skills and knowledge:** Git, Python, SQL, PySpark, Airflow. Strong business logic knowledge — they understand the data they work with, not just the technical layer.

**Production responsibilities:** Own pipelines in production — on-call, support, fix breakages. Follow engineering best practices: monitoring, dashboards, alerts. Some testing, but not much.

**Current AI usage:** Use AI tools (Cursor, Claude) for code completion and quick questions. Not using fully agentic workflows with feedback loops that enable autonomous development with minimal human interaction. AI is underutilised — they know it can do more but haven't bridged the gap.

**Team context:** Work on teams of any size. No standardised approach to AI — every engineer uses it their own way. Want to use AI tools professionally and consistently in their workplace.

### The Problem

They use AI, but it's mostly copy-paste prompts and manual workflows. They know they could automate more but don't know how to get there. Their team has no shared approach — everyone uses AI their own way. They may not even be aware of what's possible with fully agentic workflows.

### The Outcome

They can hand an agent a task — building a pipeline, migrating a table, troubleshooting a support issue — and get back working, validated code with minimal interaction. Their agents have the tools and context to autonomously gather information, execute code, and validate their own implementations.

---

## Step 2 — Transformation Arc

> The book takes the reader from a known starting state to a defined end state.
> Every chapter is a step on that journey — not just a topic.

**Before (reader's starting state):**

They have to babysit every step — providing context, running commands, reviewing output. The agent never really works on its own because the human is the glue holding it together.

**After (reader's end state):**

Confidently delegates data engineering tasks to autonomous agents with the right guardrails, tooling, and team practices in place. They trust the process, not just the output.

---

**The Arc (Parts of the book):**

| Part | Name | What it does for the reader |
|------|------|-----------------------------|
| 1 | WHY | Shifts mindset — explains why agentic now, and why DEs specifically benefit |
| 2 | FOUNDATION | Builds the base — environment, spec-driven thinking, planning before building |
| 3 | CORE SKILLS | Teaches the techniques — DE-specific: dbt, Airflow, Spark, data quality, pipelines |
| 4 | SCALE | Expands to teams and production — multi-agent, security, shared standards |


**Part 1 — WHY**
- Reader enters knowing: `AI is useful for code completion and quick questions. They think of it as a faster way to write code.`
- Reader leaves knowing: `Agents are not assistants — they are autonomous workers that need structure, not hand-holding. The shift is from writing code to owning systems. More delegation requires more planning, not less. The engineers who figure this out first have a massive advantage.`
- The DE-specific hook: `You already know the fix for most support issues. You already know the pattern for a new DAG or pipeline. You spend hours doing what an agent could do in minutes — if it had the right context, tools, and guardrails. The bottleneck is not the code. The bottleneck is you being the feedback loop.`

**Part 2 — FOUNDATION**
- Reader enters knowing: `They can use an IDE agent to implement code. Maybe they have some MCP tools available. But they are passive — if the tools or local environment are not there, they work around it manually instead of building what's missing. They don't think proactively about what the agent needs to succeed.`
- Reader leaves knowing: `When you build the foundations — local environments, tool access, spec-driven workflows — the agent can access the same information you would, gather its own feedback, and work autonomously. The spec is the focal point. A clear, detailed spec with a structured process removes you from the loop. Without foundations, you are the glue. With them, you are the reviewer.`
- The DE-specific hook: `Before: you write the pipeline, push it, test in dev, run it, check the output, fix, repeat. After: the agent writes the pipeline, triggers it locally or in a dev environment, reads the logs, queries input and output tables to validate schemas and data, reviews its own code against team practices, and fixes issues on its own. What's left for you is the final review before production — making sure the business logic is right and the code is ready to ship.`

**Part 3 — CORE SKILLS**
- Reader enters knowing: `They understand specs, feedback loops, and foundations in theory. They have the environment set up. But they haven't wired it all together into a real end-to-end workflow for their actual DE work. They don't know what the full process looks like from ticket to trusted PR.`
- Reader leaves knowing: `How to build end-to-end agentic workflows for DE tasks. How to design feedback loops that validate against the right things — logs, output tables, schemas, team practices. How to use CLIs and MCPs from Databricks, Snowflake, dbt etc. to give the agent access to run pipelines, query results, and gather its own feedback. How to keep documentation up to date as part of the process. How to turn debugging into a structured workflow: investigate with the agent, produce a report, use the report as a spec, implement the fix through the full spec-driven process. The agent knows how to use these tools better than you — let it.`
- The DE-specific hook: `Building a pipeline: the agent writes the code, triggers it locally or via the warehouse API, reads the logs, queries input and output tables to validate schemas and data transformations, refactors against team standards, and updates documentation. Debugging an issue: instead of you opening the warehouse and running SQL, the agent investigates, produces a report with findings and potential solutions, and that report becomes the spec for the fix — investigate, report, spec, implement, validate, PR. These are recipes, not concepts. This is what it looks like when it all comes together.`

**Part 4 — SCALE**
- Reader enters knowing: `[fill in]`
- Reader leaves knowing: `[fill in]`
- The DE-specific hook: `[fill in]`
