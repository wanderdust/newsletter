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

1. Introduction — what you will have set up by the end of this chapter
2. IDE agents vs CLI agents — the two flavours, narrow scope to CLI for this chapter
3. Understanding the workspace — mental model of what the agent can see, do, and access before you install anything
4. Installing an agent — now the reader knows what they are installing and why
5. Running your first prompt — first real interaction, what to expect
6. What is agents.md / CLAUDE.md? — general repo configuration for agents
7. Prompt engineering fundamentals — how to communicate effectively with the agent
8. Custom agents — specialised agents for specific tasks, encoding tribal knowledge
9. Skills — automated slash commands, how they differ from custom agents
10. Putting it all together — final repo structure walkthrough

---
## Introduction

## IDE agents vs CLI agents

Traditionally, software engineers use code editors to navigate and edit their code. These are often referred to as IDEs (Integrated Development Environments), and you could say the IDE is the main tool every software engineer uses to write code. Some common examples are VSCode, IntelliJ, or Eclipse.

On the other hand there is the terminal. The terminal is an environment where we can interact with our machine programmatically using commands. It is an alternative way to access our machine and its filesystem rather than using the desktop interface with our mouse. It also gives us more flexibility as developers, as there are things we simply cannot do from the UI directly.

To make interaction with the terminal easier, a lot of the tools we use provide a command line interface (CLI). A CLI is a structured way to run software from the terminal. The way it works is that you type the tool name followed by options to run what you need.

When it comes to working with agents there are plenty of options to choose from. Some of the most popular options include Claude Code, Codex, GitHub Copilot, Cursor, or Windsurf. All of these options can be sub-divided into two main categories: IDE based agents and command line (CLI) agents.

IDE based agents are agents that are embedded within your code editor. With IDE agents you usually have the code files open on one side of your screen, while having an agent chat window open on the other side of the screen. The idea is that you can see live code changes in your editor and manually review changes as they happen. Some popular examples of this are Cursor, Github Copilot or Windsurf.

{{< figure src="IDE-agent-cursor.png" caption="IDE agent example using Cursor" alt="IDE agent example using Cursor" >}}

On the other hand CLI agents, are those that you run directly in your terminal. CLI agents are not attached to a code editor, you can simply ask the agent to complete a task from the terminal without having to see the code if you don't want to. CLI agents provide a bit more flexibility than IDE agents, because you can use them without any IDE, or you can still use them in your IDE by running the agent in your IDE terminal. Many CLI agents also have IDE extensions which means you can still use them within your IDE if you whish to do so. Some popular examples are Claude Code, Codex, Github Copilot CLI, or qwen code.

{{< figure src="cli-agent-claude.png" caption="CLI agent example using Claude Code" alt="CLI agent example using Claude Code" >}}

Whichever you decide to use, all agents have more or less the same capabilities to access the relevant tools to complete tasks autonously. The main difference is the philosophy behind using one or the other. With IDE agents, the philosophy is that there should be a human in the loop during the whole process. With CLI agents, the philosophy is more about letting the agents handle the code writing and execution with less human in the loop, while still leaving flexibility to the developer to decide how involve they want to be.

It is worth noting that most agent providers give you the option to use their agent within the CLI or within the IDE. So it's up to you to find out what works best.

## Understanding the workspace

Agents can: see your files; edit your files; run commands. Permissions & approvals. What the agent cannot see (browser tabs, slack messages etc. unless you use MCPs). Mention sandboxing.



## Installing an agent

Installing an agent is really straightforward. Once you have chosen the type of type of agent you want to run, head to their documentation website and read the installation instructions.

Keep in mind that using agents is not free. Coding agents work within your machine, but they still need to make network requests the the AI models which are usually hosted by an LLM provider. However, some coding agent providers give free or limited access to some of their models, so you can still use them if you do not want to pay for an account.

Let's assume you have instatlled a CLI agent, such as claude or codex. Once the installation is complete, all you need to do is open a terminal and type `claude` or `codex` depending on your installation. This will open chat interface within your terminal ready for you to start giving instructions.

{{< figure src="" alt="[Starting the CLI agent image here]">}}

## Running your first prompt
what to expect, how the agent reads the repo

## What is agents.md / CLAUDE.md?

The [agents.md](https://agents.md/) file should contain any general information which is useful for any agent interacting with that repo. It should include setup commands to execute dev environments, code style, testing principles and anything about how to operate in that repository. The agents.md file can be used to document generic information about the repositiry that any agentic workflow should include as context.

## Prompt engineering fundamentals

## Custom agents

(Needs re-written - agent=goal + own context. Skill = reusable prompt)

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

what they are and how they differ from agents. How to use them together and hierarchy of agents + Skills (TODO: clarify)

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
