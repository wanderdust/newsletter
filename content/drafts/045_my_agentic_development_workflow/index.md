---
title: 'My agentic development workflow'
date: '2026-03-06T13:50:29Z'
draft: false
summary: ''
# Valid tags: ai, aws, career, certifications, data-engineering, kubernetes, postgres, reflections, security, serverless, testing, tooling
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

---
COURSE TODOS

Module 1: How we got here
- [ ] **ROI framing** — why is this worth a team's time? Rough numbers from your own experience. Aimed at the manager or CTO in the room.

Module 2: Setting up for agentic development
- [ ] **Getting started content** (before "Building a Reusable Framework") — step by step: how to install a CLI agent (e.g. GitHub Copilot CLI, Claude Code), initial config, how to run your first prompt. Assume zero prior knowledge.
- [ ] **What is agents.md / CLAUDE.md in practice** (agents.md subsection) — show a real example with actual content, not just a description. A filled-in template would be ideal.
- [ ] **Skills section** — clarify what Skills are and how they relate to scripts in the scripts directory. Resolve the TODO currently in that subsection.

Module 5: CLIs, MCPs and debugging
- [ ] **MCP setup walkthrough** — walk through installing an MCP server, configuring it, and verifying the agent can use it. Pick one concrete example (e.g. a database MCP).

Module 6: Ownership, security and new ways of working
- [ ] **Team guardrails** (Ownership & security subsection) — what to put in place before rolling this out to a team: shared credential policies, what should and should not be committed, audit considerations, who reviews AI-generated code at scale.
- [ ] **Common questions** — write up proper answers to each question. These are the exact questions a sceptical developer will ask on the day.

Course structure — proposed module breakdown

**Module 1: How we got here**
Sets the stage. No hands-on. By the end, attendees understand why this is happening now and what an agent actually is.
- Why this course? ROI framing — what changes for developers, teams, and organisations
- The copy-paste problem — where most developers are today
- What is an LLM? What is an agent? — very short, no-jargon explanation; just enough to understand the rest of the course
- LLMs vs agents: the key difference (tools, loops, autonomy)
- The evolution of development — from copy-paste to agentic; the inflection point we are at
- Agentic development vs Vibe coding

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

**Module 3: Spec driven development**
First hands-on moment. Attendees write a spec for a real or dummy feature by the end of this module.
- Why spec-first? — what changes when you plan before implementing
- The planning phase overview — spec → plan → tasks as a pipeline, not a negotiation
- The spec.md file — purpose, required sections, what good looks like vs what bad looks like
- The annotation loop — how to use the agent to fill gaps and surface edge cases in the spec before implementation
- The plan.md file — breaking the spec into ordered steps
- The tasks.md file — granular tasks with validation criteria baked in

**Module 4: Implementation and feedback loops**
Hands-on: attendees run an implementation cycle on their spec from Module 3.
- The implementation phase — how to prompt the agent to start, what to include in the prompt
- Validation loops — why the agent needs a way to verify its own work
- Types of feedback — tests, scripts, manual checks; when to use each
- Making edits — when to prompt vs when to edit manually
- Fixing forward — why you never edit the spec backwards; how to handle change
- Ownership and the pull request — reviewing AI-generated code, the 95-5 principle, what to check, security
- Committing spec, plan and tasks alongside code

**Module 5: CLIs, MCPs and debugging**
Hands-on: attendees connect a CLI or MCP to their agent and use it in a spec or debug session.
- What is a CLI tool? — terminal access to external systems, examples
- What is an MCP? — structured tool access, how it differs from a CLI, JSON config example
- When to use them — three scenarios: spec validation, triggering external systems, debugging
- MCP setup walkthrough — install, configure, verify with one concrete example (TODO: pick example)
- Debugging with spec driven development — using CLIs and MCPs in the feedback loop
- CLI agents and IDEs — does the IDE still matter? Getting comfortable with terminal-first workflows

**LAB**
Full end-to-end run through using everything from Modules 2-5. Attendees work in a sandboxed environment on a real feature using spec driven development, with agents.md, MCPs, and the full workflow.

**Module 6: Ownership, security and new ways of working**
Closing section. Reflection and discussion. No hands-on needed. Leaves attendees with the right mindset to take this back to their team.
- Cognitive debt of using agents (TODO: write this up)
- Security is part of ownership — what agents get wrong, what you are responsible for
- Scope your environments properly — credentials, prod vs dev, worst-case thinking
- Team guardrails — what to put in place before rolling this out to a team (TODO: write this up)
- More upfront design — how agentic dev revives the value of thorough specs
- When not to use agents — learning through doing; knowing when to keep your hands on the keyboard
- Your own knowledge is the limiting factor — why deep expertise matters more now, not less
- Common questions — cost, context windows, efficiency, automation ceiling, are engineers obsolete
---

## Module 1: How we got here

### The copy-paste problem

The user writes a prompt, and the LLM returns a response. The user copies the code provided into their code. This is pretty much how we've been interacting with ChatGPT over the past few years. However, this is a very manual process that requires a human in the middle finding files and updating code in the right places. THis is not onnly inconvenient, but also a recipe for introducing bugs.

Another inconvenience is when the LLM doesn't have access to our codebase, which it needs to make the right decisions about how to implement new code. With tools like chatgpt, we need to provide this context manually each time. Wouldn't it be much more helpful if the agent lived inside our repository, and it could access all the same files we can, so it can find the information it needs without us having to provide it each time?

What makes an LLM truly useful is when it can do things on its own. Give the LLM the right tools and the right environment, and it will solve any problems you have without minimal interaction.

### LLMs vs agents: what's the difference

An LLM is the Large Language Model. WHen we send a propmt, and the model returns a response.

{{< mermaid >}}
flowchart LR
    A[User Prompt] --> B[LLM] --> C[Response]
{{< /mermaid >}}

An agent is an LLM that interacts with the environment. An agent lives in an "environment", and in that environment it needs to achieve a goal. In this environment the agent has access to tools or actions it can use to achieve this goal.

We can have different types of agents that need to achieve different types of goals. Here we are talking about coding agents. With coding agents, the agents's environment is our terminal. The goal of the agent is what we specify in the prompt, such as "Add this feature" or "Find and fix this bug". To achieve these goals, the agent has access to different tools, such as
- Being able to modify files.
- Being able to search
- Being able to read files
- Being able run commands in the terminal

An agentic loop will look like this behind the scenes.

{{< mermaid >}}
flowchart TD
    A[User Prompt] --> B[LLM]
    B --> C{Run tools?}
    C -- Yes --> D[Execute Tool]
    D --> B
    C -- No --> E[Final Answer]
    E --> F{Goal achieved?}
    F -- No --> B
    F -- Yes --> G[Done]
{{< /mermaid >}}


Essentially the coding agent now has all the same tools you have to write, run, validate and debug code. With the right instructions, the agent will have a goal to achieve and all the necessary tools to build any features end to end with minimal assistance. A feedback loop for the agent looks more like this


### The evolution of development

{{< mermaid >}}
%%{init: { 'theme': 'base', 'themeVariables': { 'cScale0': '#94a3b8', 'cScale1': '#93c5fd', 'cScale2': '#60a5fa', 'cScale3': '#6ee7b7', 'cScale4': '#2dd4bf' } }}%%
timeline
    title Evolution of Writing Code
    pre 2021 : Manual Coding
             : Writing every line by hand
    2021 : AI-Assisted Human Coding
         : GitHub Copilot launches
    2022 : AI-Assisted Human Coding
         : ChatGPT launches
    2024 : Human-Assisted AI Coding
         : Claude Sonnet 3.5
         : Agentic dev workflows emerge
  2025 : Human-Assisted AI Coding
         : Claude Sonnet & Opus 4.6+
         : Fully agentic end-to-end development
{{< /mermaid >}}

Not long ago, the first AI coding tools emerged. GitHub Copilot (2021) and then Cursor (2023) could index your codebase and combine that local context with the broad knowledge baked into the model. Googling and browsing Stack Overflow became optional. Cursor in particular made the experience coherent by wrapping it in a custom IDE with AI-powered autocomplete and chat built in.

Then came the agent promise. MCPs, autonomous workflows, articles about agents running overnight started popping up everywhere. This was a different use of AI. No longer AI-assisted human coding, but human-assisted AI coding. The developer was no longer the one typing; they were the one reviewing.

Many developers tried it and got burned. Agents made small mistakes constantly. The AI-first process required a complete paradigm shift. You were no longer controlling software with if/else branches and explicit logic. You were controlling it with prompts, system instructions, and `CLAUDE.md` files, and hoping the model produced the output you expected. And it often didn't, not consistently enough to trust.

Then the models got good enough. The workflows everyone had been talking about started to just work. Not always, but often enough to matter. Engineers began shipping features they hadn't written a single line of by hand.

The full automation dream, the one where agents run entirely unsupervised overnight, is still more aspiration than reality. Anthropic's CEO predicted AI would write 90% of code within three to six months of March 2025. We are not there yet. The trajectory is real, but the timeline keeps slipping.

Engineering work is still very much required. The job has simply shifted. Agents write the code; engineers are responsible for everything around it. Understanding the system, working with stakeholders, making architectural decisions, ensuring reliable deployments, and knowing what to do when things go wrong in production. A software system is much more than a repository, and it takes a human who knows what they are doing to keep it running well.

The key is learning to work with agents effectively. That starts with how you communicate what needs to be built.

> *This section was inspired by Tom Wojcik's excellent post [Finding the Right Amount of AI](https://tomwojcik.com/posts/2026-02-15/finding-the-right-amount-of-ai/).*

### Agentic developmnent vs Vibe Coding
TODO

## Module 2: Setting up for agentic development

*TODO: Instructor-led demo section. Cover: installing a CLI agent (GitHub Copilot CLI, Claude Code), initial configuration, running a first prompt, and a live walkthrough of a configured repo. Consider a pre-work guide for attendees to install tooling before the day.*

### Building a Reusable Framework

In your day to day, you may be using this framework multiple times. You may create several specs files for different features. You don't want to have to rewrite the same prompts each time. So here are some tricks to create a re-usable framework for you and your teams.

#### Create templates
First, create some templates in your repository in a templates folder. Create templates for the spec, plan and tasks md files with the skeleton and mandatory sections each one should have. At the top of each file describe the purpose of the file, with a sample prompt.

Then, when you are about to create a new spec, you can simply say "_I have these specs [copy paste here]_. Create a specs.md file using the template in templates/specs.md_".

#### Create an agents.md file

The [agents.md](https://agents.md/) file should contain any general information which is useful for any agent interacting with that repo. It should include setup commands to execute dev environments, code style, testing principles and anything about how to operate in that repository. The agents.md file can be used to document generic information about the repositiry that any agentic workflow should include as context.

#### Use specific agents for particular tasks

Most coding agent tools let you define custom agents. Think of an agent as a markdown file that contains a specific set of instructions for a particular task. Unlike the `agents.md` file, which provides general context for the whole repository, a custom agent is scoped to one specific job.

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

#### Skills

TODO - is this the same as having scripts in my scripts directory?


#### Putting it all together

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
├── docs/
│   └── spec-templates/       # Reusable templates
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
├── src/
├── agents.md                 # General repo context for all agents
├── CLAUDE.md                 # Repo instructions (Claude Code)
└── README.md
```

## Module 3: Spec driven development

![workflow](./workflow.png)

The workflow I follow consists of 3 parts, planning phase, implementation phase and final code review phase.

### The Planning Phase

The planning phase consists of an in depth set of documents that contian in deputh specifications of WHAT needs to built, WHY and HOW we are going to implement it. This is the most important part, and where we have to focus all of our attention to ensure we gather all of the correct requirements and make the correct decisions.

During this psahe, we do not implement any code.

#### The spec.md file

First I create a spec.md file in the repository. I tell the agent to create the file based on my initial specifications and let it create a detailed initial draft. The specs file contains information about WHY we are building this feature and WHAT this feature is. At this point we do not specify technologies or anything related to HOW we are going to build this. This file needs to be a reflection of what we are building, agnostic of any technical decisions.

Some of the things you can include in this file are:
- context around the purpose of the current repo
- What is being implemented and why; User stories
- Functional Requirements
- Key Entities (ie data schemas)
- Success Criteria.
- Architecture (non-technical)

The quality of the first draft will only be as good as your original specifications. Example prompt:

> _Create a specs.md file for this feature. Focus on the what and why, no technical decisions. Include context about the repo, user stories, functional requirements, key entities, and success criteria. Here are my original specs: [paste your JIRA ticket here]_

From this, the agent should have created an initial specs document ready for you to review and provide feedback on.

#### The annotation loop

The specs.md file will be where you spend most of your time during the whole process. You need to carefully read the contents and ensure all of the information is correct. If the model made any assumptions, they need to be corrected. You can either annotate them directly in the spec file or propmt the model with the changes you want to make. The agent will then update the spec file to include all the new changes.

You may spend hours or days going through your spec file. You should make corrections and ask the agent to update the spec.md based on your corrections. You may also need to find out more information from your team or the stakeholders. Add all of this information here and ask the agent to update the document each time. Remember, any lack of detail or ambiguity might result in the final feature not turning out the way you wanted. You may go through this annotation process multiple times.

Once your spec.md is ready to go, ask the model to analyze the current state of the file to find any ambiguity or lack of clarification. This will help identify any ambiguity in the file that need clarifying from you, which will reduce any assumptions made by the model at implementation time, which is what we want to minimise as much as possible. Example prompt:

>: _Check the existing spec.md and identify any lack of detail or ambiguity. Ask me for further clarification on what you find._

When the final clarifications are done, and the final spec is ready, I move on to the planning phase.

#### The plan.md file

The next step is to create a plan.md file. The plan contains the technical implementation details, such as architecture, frameworks and technical decisions. The plan should be aware of the structure of the current repository, and know which changes will be applied and where. In the plan we con specify which tests and validations we are going to run. It should know how to spin up a local environmont to run test things.

If you are building an an existing repo, you may want the agent to scan the current repo to understand how to build the feature using the existing patterns. If you are creating something new, you may want to be more specific in the languages, tools and so on. Example prompt:


> _Create a plan.md file with technical implementation details and chosen tech stack. Specify technical decisions. Do a deep research of the relevant sections of the repo before suggesting how the changes will be made. Any decisions should be backed up by data, to ensure functionality is available and changes are based on existing practices and functionality. The plan does not need to be broken down into tasks (we will do that later). We want a detailed overview of the technical decisions and how we will implement the changes._

For the plan you can choose to either provide specific information about the frameworks, or let it do its own thing. That is up to you. Similarly to the spec.md, you need to spend time reviewing the plan and changing anything that does not look right.


Then we are ready to move on to the tasks file.

#### The tasks.md file

The tasks.md file is a breakdown of the plan into executable steps. It is essentially a sequential TODO list of what needs to be implemented from the plan, broken down into small tasks. The tasks.md file is essential for you to know exactty what it is that will be implemented, and the model will follow these steps one by one. It makes the model run exactly what is there, rather that it making its own choices about implementation.

You can structurre the file into small TODOs that the model can update as it implements things. Example prompt:

> _Create a tasks.md file as detailed todo list to the plan, with all the phases and individual tasks necessary to complete the plan - don’t implement yet._

The most important thing in the tasks file, is ensuring there are validation steps for each task. These can be unit tests, or custom scripts the agent creates to test functionality. These validation tasks will serve the agent as a validation loop that it can use to verify functionality to ensure it meets the success criteria before marking it done.

## Module 4: Implementation and feedback loops

### Implementation Phase

Once you have reviewed the tasks.md file and you are happy to move forward with it, it is time to start implementing.

Ask your agent to start implement tasks. You can choose to implement all in one go, or implement the tasks into phases, for example by grouping similar tasks into one agent execution. Example prompt:

> _Implement tasks 1 - 3. When you are done with a task, mark it as completed in the tasks.md file. Do not stop until all tasks in this phase are completed. Do not add unnecessary comments. Do not use any or unknown types. Continuously run the unit tests to make sure you are not introducing new issues._

### Validation Loops

A validation loop is essential for the agent to properly verify if the changes it has made meet the success criteria defined in the specifications. A good validation process is what brings the real benefit of using agents, because they can write, run and validate code end to end with minimal human supervision. A good self validation process also gives you confidence as a developer that the code created meets the necessary standards, even before you review it.

The validation you choose to use depends on the objective you are trying to achieve. For example, if building a website, the validation process might include passing unit tests, taking screenshots of the website to ensure it looks correct, and running simulated user journeys end to end to ensure functionality works as expected. These are all things agents can do for you, but require you specify this as a requirement during your planning.

It is also worth mentioning that the validation loop is only possible if you have a local environment you can run your project on. If your application requires you to test in a deployed dev environment which the agent can't access, you are going to have a difficult time setting up a validation loop, and therefore any generated code might not be as trustworthy as it could be. A good local environment needs to be a requirement for every application we are building.

#### Types of feedback

There are different levels of feedback which are useful for the model to test and validate the code.
1. Being able to run the code locally. THe agent can fix any runtime errors. This is the most basic and the minimum you should aim to have.
2. Running unit tests. Possible using Test Driven Development, where we create the tests first. It gives the model something more concrete that needs to be achieved.
3. Testing user journeys. Ask the model to build scripts which test user journeys end to end, to ensure functionality. This gives the model the confidence that all features work together with each other, not just in individual blocks.
4. Any other criteria can be created using custom scripts, such as taking screenshots from the UI.

Basically anything that you would do yourself as part of your review process before making a Pull Request, you should be able to ask the agent to do as part of the development process.

### Making Edits

Sometimes, after implementation is finished, you notice that something was built incorrectly or not built at all. This is usually a symptom of one of two things: a poorly defined spec (the agent solved the wrong problem), or a weak feedback loop (the agent never got signal that something was wrong).

When this happens, there is a temptation to start firing off quick fixes. "Just change this bit", "actually make it do this instead". This is where spec driven development quietly becomes vibe coding. Each prompt narrows the context a little more, the model loses track of the bigger picture, and the quality of the output degrades with each exchange.

A useful rule of thumb: the fewer prompts it takes to implement something, the better the result. Quality and prompt count tend to move in opposite directions.

{{< mermaid >}}
%%{init: { 'theme': 'base', 'themeVariables': { 'xyChart': { 'plotColorPalette': '#e11d48' } } }}%%
xychart-beta
    title "Code Quality vs Number of Prompts"
    x-axis "Number of Prompts" ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    y-axis "Code Quality (%)" 0 --> 100
    line [95, 80, 60, 40, 25, 15, 10, 7, 5, 5]
{{< /mermaid >}}

When you spot issues after implementation, you have two options depending on the severity.

#### Manual edits

If the issues are small and localised, a missed edge case or a minor behaviour that's slightly off, the pragmatic move is to review the code yourself and fix it by hand. This is faster than re-running the full workflow for something trivial, and it keeps you close to the code.

#### Fixing forward

If the issues are more significant, resist the urge to prompt your way out of them. Instead, treat it as a new iteration. Write a new spec that clearly describes the gap or the incorrect behaviour, go through the full spec → plan → tasks workflow, and implement the fix cleanly in one pass.

The key principle here is that spec, plan, and tasks files are immutable once you have moved past them. You do not go back and edit an earlier document mid-flight, as that cascades changes unpredictably across the whole workflow. Once you are happy with a phase and move forward, it is locked. If something is missing, you either finish what you have and create a new spec for the next iteration, or you abandon the current cycle and start over from the spec.

Fixing forward keeps the problem well-defined, gives the agent a clean starting point, and avoids the compounding drift that comes from patching a half-finished implementation.


### Ownership and the Pull Request

With a solid spec, a good feedback loop, and a capable agent, you can go from spec to pull request without writing a single line of code yourself. The agent builds it, tests it, and validates it end to end.

But this only gets you 95% of the way there.

No matter how detailed your spec is, the agent can and will misinterpret something. It can be small things, but they still need to be caught and corrected. That last 5% is where you come in, and it is arguably the most important part of the whole process.

The agent writes the code. You own it. There is a difference.

Owning the code means you can vouch for every line that goes to production. If someone asks you why a particular approach was taken, you should be able to answer. "The LLM wrote that part" is not an acceptable answer in a production system, and it is not fair to your reviewers to hand them code you have not personally understood. It is not the reviewer's responsibility to decypher code you have not checked.

This is one of the biggest shifts in agentic development. That accountability is what separates professional engineering from vibe coding.

**Do this:**
- Go through every change before raising the PR. Read the diff. Understand what was built and why.
- Check that the implementation matches the intent of the spec, not just that the tests pass.
- Be able to explain any piece of the code if someone challenges it in review. If you cannot, that is a flag.
- Keep PRs small. The smaller the change, the easier it is to review thoroughly and the easier it is for your colleagues to give useful feedback.

**Do not do this:**
- Do not raise a PR for code you have not personally read. It is not the reviewers job to be the gatekeeper of code.
- Do not assume passing tests means the feature is correct. Tests validate what was written, not what was intended.
- Do not trust the agent to catch its own security issues. Agents will suggest things that are common but not necessarily secure. Long-lived tokens, overly broad permissions, accidentally committed `.env` files. These get through if you are not paying attention.

## Module 5: CLIs, MCPs and debugging

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


---
## LAB

TODO: lab will run in a sandbox environment hosted in github workspaces. They will run qwen-code. I provide a real use case of adding a feature to an existing repo using spec driven development, which includes agents.md, MCPs and all the things mentioned above.

---

## Module 6: Ownership, security and new ways of working

### Security is part of ownership

Agents are not security-aware by default. They will produce code that looks right and works, but may not be secure. I have seen agents happily suggest long-lived tokens for third-party authentication on public CI/CD pipelines. They will use overly broad IAM permissions, hardcode credentials, or accidentally include `.env` files in a commit. If you are not paying attention, these things get through.

Security issues do not get caught by tests. They get caught by a developer who understands what the code is doing and knows what to look for. That developer is you.

You cannot trust an LLM to follow best security practices. The only way to avoid security issues is to understand what the code is doing and what the tradeoffs are.

### Scope your environments properly

Agents run with your credentials. Whatever access you have, the agent has. This makes proper environment scoping more important than ever.

Production systems should be read-only or off-limits entirely to your local agent. Changes to production infrastructure should go through a controlled process, like Terraform with a PR review, not a CLI command the agent decided to run. Dev and QA environments can be more permissive, but they should still have boundaries.

Before you connect an agent to any external system, check what it has access to and make sure you are comfortable with the worst case if something goes wrong.

### New ways of working

#### Cognitive debt of using agents

*TODO: Write about the risk of shipping code you do not fully understand. When an agent writes the implementation, it is easy to end up with a codebase that works but that nobody on the team can confidently reason about. This is different from technical debt — it is a debt of understanding. Over time it compounds: features become harder to extend, bugs become harder to diagnose, and onboarding becomes harder because nobody really knows how things work. The antidote is the 95-5 principle and deep review. Write about what this looks like in practice and how to guard against it.*

#### More upfront design

Agentic development quietly brings back something that agile methodologies pushed aside: the value of thinking carefully before you start building. Waterfall gets a bad reputation, and rightly so in many contexts, but one thing it got right was investing time upfront to understand what you are building before you write a single line of code.

With agents, that upfront investment pays off more than ever. The better your spec, the better the output. You now have a reason to go deep on requirements early, ask hard questions of your stakeholders, and use MCPs to validate your assumptions against real systems before implementation begins. The agent can even help you do it, by scanning the codebase, surfacing edge cases, and identifying gaps in the spec before you start.

This is not waterfall. You are still working iteratively, one spec at a time. But each iteration starts with more rigour than before.

#### When not to use agents

Not everything should be delegated to an agent. If you are learning something new, working through a problem manually is often the point. Expertise comes from doing things yourself, making mistakes, and understanding why they happened. An agent that solves the problem for you does not give you that.

Use agents for work you already understand well enough to review and own. If you are in unfamiliar territory and you cannot evaluate whether the output is correct, slow down and do it by hand first. Build the understanding, then bring the agent in.

#### Commit your spec, plan and tasks

Spec, plan, and tasks files are not just scaffolding to throw away after implementation. They are a record of the decisions you made and why. Commit them to the repo alongside your code changes.

This gives your reviewers context they would not otherwise have. They can see what was intended, what tradeoffs were considered, and what the scope of the change was. It also gives you and your team a reference point when a feature needs to be revisited or extended in the future.


#### Your own knowledge is the limiting factor

With coding agents you can build almost anything in no time. The only thing stopping you is having enough knowledge of the system you want to build to ensure you can build something robust and consistent. Now, it is more important than ever to keep learning.

### Common questions

#### What does this cost?

*TODO: Write about token/API costs and how to think about the ROI.*

#### Context window and context switching

*TODO: Write about managing context limits, running one agent at a time, and the cognitive overhead of switching between tasks mid-session.*

#### How efficient is this vs working manually?

*TODO: Write about how efficiency depends on spec quality and incremental implementation — but solutions can be more thorough from the first pass.*

#### How much can we automate?

*TODO: Write about the realistic ceiling for automation and why human-in-the-loop remains essential.*

#### Are software engineers becoming obsolete?

No. But the job has shifted.

The role is no longer primarily about writing code. It is about working with stakeholders to understand what needs to be built, making good architectural decisions, and ensuring agents implement features accurately and responsibly. The code writing itself is increasingly delegated.

What has not changed is everything around the code. A software system is much more than a repository. It needs to be deployed, monitored, and maintained. When things go wrong in production, someone needs to understand the system well enough to diagnose the problem, coordinate across teams, and get things back to a stable state. That requires deep context that no agent currently has on its own.

Good engineering practices matter more now, not less. It is easier than ever to ship something that looks right but is not built reliably. Engineers are the ones responsible for ensuring that what goes to production has been built, tested, and deployed in a way that holds up. That judgment still requires a human who knows what they are doing.
