---
title: 'CLIs, MCPs and debugging'
date: '2026-03-06T13:50:34Z'
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

**Module 6: CLIs, MCPs and debugging**
Hands-on: attendees connect a CLI or MCP to their agent and use it in a spec or debug session.
- What is a CLI tool? — terminal access to external systems, examples
- What is an MCP? — structured tool access, how it differs from a CLI, JSON config example
- When to use them — three scenarios: spec validation, triggering external systems, debugging
- MCP setup walkthrough — install, configure, verify with one concrete example (TODO: pick example)
- Debugging with spec driven development — using CLIs and MCPs in the feedback loop
- CLI agents and IDEs — does the IDE still matter? Getting comfortable with terminal-first workflows

---

When working with agents, your goal is to give them as much context as possible so they have enough information to complete their tasks successfully. Sometimes it is enough to look at the current repo. Other times it helps to have access to external systems to gather additional context that makes for stronger specs and more accurate implementations.

CLIs and MCP servers are how you give the agent that access.

### What is a CLI Tool

A CLI (Command Line Interface) is a tool you interact with via the terminal. Most platforms you work with day to day have one: AWS, Kubernetes, Databricks, GitHub, and many others. If your agent has access to the terminal, it can run CLI commands the same way you would. That means it can query infrastructure, inspect logs, describe resources, or check the state of a system without you having to copy and paste anything manually.

### What is an MCP

An MCP (Model Context Protocol) server is a standardised way to give an agent access to an external tool or data source. Think of it as a plugin purpose-built for agents. Where a CLI is a general terminal tool, an MCP server is specifically designed to be consumed by an agent, exposing a set of actions the agent can call directly.

In practice, you configure MCP servers in your agent's config file. Here is an example of what that looks like:

```json
{
  "mcpServers": {
    "databricks": {
      "command": "uvx",
      "args": ["databricks-mcp"],
      "env": {
        "DATABRICKS_HOST": "https://your-workspace.azuredatabricks.net",
        "DATABRICKS_TOKEN": "your-token"
      }
    }
  }
}
```

Once configured, the agent can call that server to run queries, inspect schemas, or fetch any data the MCP exposes, all without leaving the workflow.

### When to use them

CLIs and MCPs are useful at any point in the workflow where the agent would benefit from access to an external system. A few examples:

**During the spec and planning phase.** Before writing a single line of code, you can ask the agent to verify assumptions against real systems. Building a data pipeline? Have the agent connect to the data warehouse and confirm the source and destination tables exist, the column names match, and the data types align with your spec. This turns assumptions into verified facts before implementation even starts.

**During execution and testing.** If your feature depends on an external service, you can use a CLI to trigger it, track execution, and pull back logs as part of the feedback loop. Rather than manually checking whether a job ran correctly, the agent can do it as part of the validation step.

**During debugging.** This is where CLIs and MCPs arguably provide the most value. Rather than reasoning from code alone, the agent can inspect the actual state of the system: query logs, describe infrastructure resources, check what is deployed and where. Use the findings as input to a new spec and fix the bug through the full workflow.

Use CLIs and MCPs wherever you would normally switch to another tool, look something up manually, or copy and paste external context into your prompt.

### Debugging with spec driven development

One of the best uses for agents is helping you gather information about a bug and build a solid picture of what is actually going on. Instead of jumping straight into the code, you can turn debugging into a spec driven workflow.

Start by using your CLIs and MCPs to gather evidence. Let the agent inspect logs, query the affected system, and describe what it finds. Once you have a clear picture of the observed behaviour and what should be happening instead, write a spec for the fix. From there, follow the normal spec → plan → tasks workflow.

The fix ends up well-scoped, documented, and tested.


### CLI Agents and IDEs

An IDE was designed for a world where you wrote code by hand. You needed to navigate files, read error messages, and type out every line yourself. The IDE was built around that workflow.

With agentic development, most of that changes. When you have a solid spec and a capable agent, the agent is the one reading the codebase, making changes, running tests, and validating the output. Your job shifts to reviewing the result. The IDE becomes less central to the process.

There are two flavours of coding agent available today. Some live inside an IDE, like Cursor, Windsurf, or GitHub Copilot in VS Code. Others run directly in the terminal as CLI tools, like Claude Code or GitHub Copilot CLI. The CLI-based agents are a bet that the future of engineering does not require an IDE at all. I think that is probably right.

That said, it does not matter much which you use. The workflow described in this course works with either. What matters is starting to get comfortable with the idea that the IDE is no longer the centre of the process. You may still open it for a quick manual edit or to review a diff, but the heavy lifting happens elsewhere.
