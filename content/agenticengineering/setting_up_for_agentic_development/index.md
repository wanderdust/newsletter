---
title: 'Chapter 2 - Setting up for agentic development'
date: '2026-03-06T13:50:30Z'
draft: true
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
## Introduction

## IDE agents vs CLI agents

When it comes to working with agents there are plenty of options to choose from. Some of the most popular options include claude code, codex, github copilot, cursor, or windsurf. All of these options can be sub-divided into two main categories: IDE based agents and command line agents.

IDE based agents are agents that are embedded within your code editor. With IDE agents you usually have the code files open on one side of your screen, while having an agent chat window open on the other side of the screen. The idea is that you can see live code changes in your editor and manually review changes as they happen. Some popular examples of this are Cursor, Github Copilot or Windsurf.

On the other hand CLI agents, are those that you run directly in your terminal. CLI agents are not attached to a code editor, you can simply ask the agent to complete a task from the terminal without having to see the code if you don't want to. CLI agents provide a bit more flexibility than IDE agents, because you can use them without any IDE, or you can still use them in your IDE by running the agent in your IDE terminal. Many CLI agents also have IDE extensions which means you can still use them within your IDE if you whish to do so. Some popular examples are Claude Code, Codex, Github Copilot CLI, or qwen code.

Whichever you decide to use, all agents have more or less the same capabilities to access the relevant tools to complete tasks autonously. The main difference is the philosophy behind using one or the other. With IDE agents, the philosophy is that there should be a human in the loop during the whole process. With CLI agents, the philosophy is more about letting the agents handle the code writing and execution with less human in the loop, while still leaving flexibility to the developer to decide how involve they want to be.

## Installing a CLI agent (GitHub Copilot CLI or Claude Code)
— step by step, assume zero knowledge

## Running your first prompt
what to expect, how the agent reads the repo

## Understanding the workspace
where the agent reads and writes, what it can and cannot see. ASking premissions. Briefly mention sandboxing.

## What is agents.md / CLAUDE.md?

The [agents.md](https://agents.md/) file should contain any general information which is useful for any agent interacting with that repo. It should include setup commands to execute dev environments, code style, testing principles and anything about how to operate in that repository. The agents.md file can be used to document generic information about the repositiry that any agentic workflow should include as context.

## Custom agents

(Needs re-written)

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

## Skills

what they are and how they differ from scripts (TODO: clarify)

## Prompt engineering fundamentals

## Putting it all together — final repo structure walkthrough

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
