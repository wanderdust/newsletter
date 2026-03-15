---
title: 'How we got here'
date: '2026-03-06T13:50:29Z'
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

**Module 1: How we got here**
Sets the stage. No hands-on. By the end, attendees understand why this is happening now and what an agent actually is.
- Why this course? ROI framing — what changes for developers, teams, and organisations
- The copy-paste problem — where most developers are today
- What is an LLM? What is an agent? — very short, no-jargon explanation; just enough to understand the rest of the course
- LLMs vs agents: the key difference (tools, loops, autonomy)
- The evolution of development — from copy-paste to agentic; the inflection point we are at
- Agentic development vs Vibe coding

---

### Why this course?
ROI framing — what changes for developers, teams, and organisations

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

### Agentic engineering vs Vibe Coding

There is a difference between vibe coding and agentic engineering.

Vibe coding refers to the process of prompting the model to write some code. It consitsts of incrementally prompting the model to add new features or to fix bugs, but without a workflow that follows engineering rigor. With vibe coding you may get a working version of your app. However the underlying code will lack the structure, readability, tests and ownership required to have code you can trust in production.

Agentic engineering still uses AI agents to write code for us. However we do so following best engineering practices, by writing a detailed specification document, clearly defining scope and success criteria, and making technical decisions in advance. With agentic engineering we define as much as possible in advance, leaving very little autonomy to the agent to make assumptions or decisions on the fly about the implementation. THe agent has clear instructions of what to implement, and how. The agent's job is to write the code for the exact features defined in our document. The agent has no autonomy to make any important decisions on the fly. The implementation plan is clearly defined and documented.

The main difference between both approaches is the level of planning ahead and ownership about what we ship. Vibe coding has little or no planning, and very little ownership. Agentic engineering follows a very rigorous process of defining, planning and ultimately owning any code shipped.
