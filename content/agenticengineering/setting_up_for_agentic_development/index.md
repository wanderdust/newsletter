---
title: 'Setting up for agentic development'
date: '2026-03-06T13:50:30Z'
draft: false
summary: ''
tags: ['ai', 'tooling']
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
params:
  showtoc: true
  tocOpen: false

---

**Module 2: Setting up for agentic development**
Instructor-led demo. Attendees follow along passively. Show a working repo live before concepts are introduced. Consider a pre-work guide so no install time is spent on the day.
- Installing a CLI agent (GitHub Copilot CLI or Claude Code) — step by step, assume zero knowledge
- Running your first prompt — what to expect, how the agent reads the repo
- Understanding the workspace — where the agent reads and writes, what it can and cannot see
- What is agents.md / CLAUDE.md? — with a real filled-in example
- Creating templates — spec, plan, tasks skeleton files
- Custom agents — what they are, when to use them, example agent file
- Skills — what they are and how they differ from scripts (TODO: clarify)
- Putting it all together — final repo structure walkthrough

---

### Installing a CLI agent (GitHub Copilot CLI or Claude Code)
— step by step, assume zero knowledge

### Running your first prompt
what to expect, how the agent reads the repo

### Understanding the workspace
where the agent reads and writes, what it can and cannot see. ASking premission

### What is agents.md / CLAUDE.md?

The [agents.md](https://agents.md/) file should contain any general information which is useful for any agent interacting with that repo. It should include setup commands to execute dev environments, code style, testing principles and anything about how to operate in that repository. The agents.md file can be used to document generic information about the repositiry that any agentic workflow should include as context.

### Custom agents

Think of an agent as a markdown file that contains a specific set of instructions for a particular task. Unlike the `agents.md` file, which provides general context for the whole repository, a custom agent is scoped to one specific job.

For example, imagine you have a complex feature with a non-obvious testing process. You could create an agent that documents exactly how to test it: which scripts to run, what to check, and what a passing result looks like. Any time you want to test that feature, you invoke that agent instead of re-explaining the process from scratch.

Custom agents are a way of encoding tribal knowledge into your workflow. Anything you find yourself explaining repeatedly to the agent is a good candidate for one.

```markdown
---
name: readme-creator
description: Agent specializing in creating and improving README files
---

You are a documentation specialist focused on README files. Your scope is limited to README  files or other related documentation files only - do not modify or analyze code files.

Focus on the following instructions:
- Create and update README.md files with clear project descriptions
- Structure README sections logically: overview, installation, usage, contributing
- Write scannable content with proper headings and formatting
- Add appropriate badges, links, and navigation elements
- Use relative links (e.g., `docs/CONTRIBUTING.md`) instead of absolute URLs for files within the repository
- Make links descriptive and add alt text to images
```

### Skills

what they are and how they differ from scripts (TODO: clarify)

### Putting it all together — final repo structure walkthrough

The final repository might look like this

```
my-project/
├── .github/
│   └── agents/               # Custom agents (GitHub Copilot)
│       ├── spec-writer.md
│       └── test-runner.md
├── .claude/
│   └── agents/               # Custom agents (Claude Code)
│       ├── spec-writer.md
│       └── test-runner.md
├── src/
├── agents.md                 # General repo context for all agents
├── CLAUDE.md                 # Repo instructions (Claude Code)
└── README.md
```
