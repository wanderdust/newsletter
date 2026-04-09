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

**Skills and knowledge:** Git, Python, SQL, PySpark, Airflow. Strong business logic knowledge — they understand the data they work with, not just the technical layer. They are not necesarily very strong software engineers, but can code.

**Production responsibilities:** Own pipelines in production — on-call, support, fix breakages. Follow engineering best practices: monitoring, dashboards, alerts. Some testing, but not much.

**Current AI usage:** Use AI tools (Cursor, Claude) for code completion and quick questions. Not using fully agentic workflows with feedback loops that enable autonomous development with minimal human interaction. AI is underutilised — they know it can do more but haven't bridged the gap.

**Team context:** Work on teams of any size. No standardised approach to AI — every engineer uses it their own way. Want to use AI tools professionally and consistently in their workplace.

### The Problem

They use AI, but it's mostly copy-paste prompts and manual workflows. They know they could automate more but don't know it is possible or if they do they do not know how to get there. Their team has no shared approach — everyone uses AI their own way. They may not even be aware of what's possible with fully agentic workflows.

### The Outcome

They can hand an agent a task — building a pipeline, migrating a table, troubleshooting a support issue — and get back working, validated code with minimal interaction. Their agents have the tools and context to autonomously gather information, execute code, and validate their own implementations.

---

## Step 2 — Transformation Arc

> The book takes the reader from a known starting state to a defined end state.
> Every chapter is a step on that journey — not just a topic.

**Before (reader's starting state):**

They have to babysit every step — providing context, running commands, reviewing output. They use agents as a series of manual steps. There's no real automation.

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
- Enters knowing: `AI is useful for code completion and quick questions. They think of it as a code writing tool.`
- Leaves knowing: `Agents can be autonomous workers with the right structure in place. The shift is from writing code to fully autonomus workflows. Developers spend time on the requirements, agents handle the rest.`
- DE hook: `You already know the fix for most support issues. You already know the pattern for a new DAG. You spend hours doing what an agent could do in minutes — if it had the right context, tools, and guardrails. The bottleneck is not the code. The bottleneck is you being the feedback loop.`

**Part 2 — FOUNDATION** *(the process and the environment — not DE-specific yet)*
- Enters knowing: `They can use an IDE agent to write code. But they are passive — if the tools or local environment aren't there, they work around all of the engineering steps manually. They don't think about what the agent needs to be fully autonomous.`
- Leaves knowing: `How to set up the environment so the agent has the same access you do — local execution, tool access, terminal commands. How spec-driven development works: spec, plan, tasks, implement, validate. What a feedback loop is and why the agent needs one to work autonomously. Without foundations, you are the glue. With them, you are the reviewer.`
- DE hook: `The spec is the focal point. Before you write a single line of pipeline code, you define what needs to be built, how, and what "done" looks like, including the data, schemas, transformations and so on. The agent needs a local environment where it can run code and gather feedback — without that, it can't validate anything and you're back to babysitting.`

**Part 3 — CORE SKILLS** *(applying the process to real DE work — the recipes)*
- Enters knowing: `The process and the environment are set up. They understand specs, feedback loops, and how the agent works. But they haven't applied it to their actual DE workflows yet.`
- Leaves knowing: `How to design feedback loops for DE tasks — what to validate against (logs, output tables, schemas, team practices) and how to give the agent access to gather that feedback. How to use CLIs and MCPs from Databricks, Snowflake, dbt to let the agent run pipelines, query results, and fix issues on its own. How to keep documentation up to date as part of the workflow. How to turn debugging into a structured process: agent investigates, produces a report, report becomes the spec, fix follows spec-driven development through to PR.`
- DE hook: `Building a pipeline: the agent writes the code, triggers it via the warehouse API, reads the logs, queries input and output tables to validate schemas and transformations, refactors against team standards, and updates docs. Debugging: instead of you running SQL in the warehouse, the agent investigates, writes a report, and that report becomes the spec — investigate, report, spec, implement, validate, PR.`

**Part 4 — SCALE** *(from individual workflow to team standard)*
- Enters knowing: `They have a working agentic workflow for themselves. But every engineer on the team uses AI differently — different prompts, different standards, different rigour. No shared guardrails around security or environment access.`
- Leaves knowing: `How to standardise agentic workflows across the team with shared templates, skills, and a constitution. How to scope environments so agents run with the right access and nothing more. Every engineer, regardless of seniority, produces specs and code that meet the same quality bar. The workflow lives in the repo and improves over time.`
- DE hook: `A junior and a senior DE run the same /spec command and get the same structure, the same required sections, the same validation steps. Pipeline standards — naming, testing, documentation — are baked into the workflow, not enforced in code review after the fact. Credentials are scoped to dev only. Specs are committed alongside the code so anyone can understand what was built and why.`
