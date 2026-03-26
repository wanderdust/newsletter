---
title: 'Chapter 5 - Agentic engineering for teams'
date: '2026-03-06T13:50:33Z'
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

## Introduction

At this point we have already seen how to use spec driven development to create a structured engineering workflow and using feedback loops te ensure the code is validated and meeting the necessary standards. We already have a very solid workflow we can go and use.

Engineering is more often than not, not done on your own. You usually work in a team where everyone is trying to achieve the same goals. If everyone in the team is using agents differently, this can create inconsistencies on how the code is built. Perhaps one of the approaches from you junior members is not very thorough, and the output code comes out bloated, and in very large pull requests that are very difficult to review. There is a benefit in everyone using the same workflow and principles to ensuere the whole team is building under the same standards.

We already see this with linting tools. It is a lot better when the team uses the same linting rules for the codebase, so that there is consistency accross the repo in how code is built. It also helps so that each team member does not change each others linting rules on every Pull Request, making the reviews more difficult than they need to be. It also helps keeping a tidier codebase. The same idea applies to having a shared workflow across the team (or teams) when using agentic engineering. We want to ensure we all use the same templates when building our specs. We want to ensure the templates include mandatory information about what is mandatory - such as including user journeys in the spec, including data validation as part of the plan, or including running unit testing as part of the tasks. These will help ensure the specifications include enough details and meet the necessary standards for each different implementation across team members. It will also ensure the code output has gone through the necessary quality gates before it is submitted for review.

----
1. Creating re-usable templates for specs, plans, and tasks
2. Automating the workflow with skills
3. Walkthrough: setting up a simplified spec-kit
4. Defining team standards with a constitution
5. When to use and not to use agentic engineering


-----

## Creating re-usable templates for specs, plans, and tasks

In the chapter where talked about spec driven development, we spoke about a workflow where we went through the process of creating a series of documents, where we start by specifying the work that needs done and then start breaking it down into actionable tasks.

Over time we will start finding out what works for us. For example, we might like to include user journeys in our spec document because it makes the solutions better. We may also want to always include a section about success criteria and testing which makes our solutionsn more robust.

The first thing you might do, is to is to save these prompts in a document and reference them each time you need to use them. THe prompt might include all of the information you like the agent to add in your document. THis approach works, but it is very manual, and it also makes it a bit awkward to re-use across your team. We can do better.

We can use templates in our repositories that can be referenced each time we go through this process. The templates include all of the sections that you want to make sure your document includes, and the structure it should follow. Here are some expamples of templates we can use.

By using templates, we can also make it very easy to share across teams, and different teams can easily modify them according to their needs, but at least everyone starts from some base which includes the minumum required criteria for all teams. By using small, concise templates, it is also very easy for teams to review and make small modifications to match their needs.

### The spec template

The spec template captures the _what_ and _why_ of the work. It should include any sections that are important for your team. Some sections should be non-negotiable across all teams, like having clear goals and success criteria. Others will depend on what your team cares about, for example, your team might always want to include user journeys because it leads to better solutions, or maybe constraints are important because you work with strict dependencies.

Here is an example of a spec template:

```markdown
# Spec

## Overview
<!-- What is being built and why. One or two sentences. -->

## Goals
<!-- What this work should achieve. -->

## Non-goals
<!-- What is explicitly out of scope. -->

## User journeys
<!-- Step-by-step descriptions of how users will interact with this feature.
Include the happy path and key edge cases. -->

## Requirements
<!-- Specific functional requirements. What must the system do? -->

## Constraints
<!-- Any limitations, dependencies, or requirements that affect scope. -->

## Success criteria
<!-- How we know this is done. Measurable outcomes that define success. -->
```

### The plan template

The plan template captures the _how_. This is where technical decisions are made. Having a template here ensures the team always thinks about how new code integrates with the existing codebase, and that there is always a testing strategy before implementation starts.

```markdown
# Plan

## Technical decisions
<!-- Key technology choices, frameworks, patterns to use. -->

## Approach
<!-- How the spec will be implemented. What gets added, changed, or removed. -->

## Integration
<!-- How the new code fits into the existing codebase.
File locations, module boundaries, etc. -->

## Validation and testing
<!-- How the implementation will be tested. Tools, strategy (unit, integration, e2e),
and what must pass before this is considered done. -->
```

### The tasks template

The tasks template breaks the plan into small, actionable steps grouped by phase. Each phase should be completable independently, and each phase should include its own validation step. This is important — it forces the agent to validate as it goes rather than leaving all testing to the end.

```markdown
# Tasks

## Phase 1
<!-- Group related tasks into phases. Each phase should be completable independently.
Include validation and testing tasks per phase where possible. -->

- [ ] 1.1 Task description — implementation
- [ ] 1.2 Task description — validation and testing
```

The templates above are a starting point. Your team will likely add or remove sections over time as you figure out what works. The point is that they live in the repo, everyone uses them, and they encode what the team considers important.

Once all of the templates are clearly defined, we can start thinking about how to prompt the model to consistently use these templates when building features.

## Creating templates for our prompts

Having the templates is the first step, and it could be enough to start creating a consitstent workflow across the team. When prompting the model, we can say

> _Create a specifications document using the spec.md file template provided. The specs are these [feature specs here]_

The problem with this workflow is that we still have to write a full prompt referencing the templates each time. A developer can easily forget to reference the provided template, which means all this standardisation is all in vain. It also means that we have to constantly repeat the phrase "_use the provided template in [path to template]_" each time.

We can automate this by using prompt templates. A prompt template is a reusable set of instructions that tells the agent exactly how to use each document template. Instead of the developer having to remember the right prompt each time, the prompt template does it for them. Here are some examples.

As a starting point, we can create the prompt templates in our repository, and re-use them each time.

### The spec prompt template

```markdown
You are creating a feature specification.
The spec captures the **what** and **why**. No technical decisions.

Read the spec template at `templates/spec.md`.
Use the user input to understand what is being built.

Fill in the spec template with these sections:
  **Overview**: what is being built and why
  **Goals**: what this work should achieve
  **Non goals**: what is explicitly out of scope
  **User journeys**: step by step descriptions of how users interact with the feature
  **Requirements**: specific functional requirements
  **Constraints**: limitations, dependencies, or requirements that affect scope
  **Success criteria**: measurable outcomes that define when this is done

Be specific and concrete. Avoid vague language.
Write the spec to the specs/ directory.
---

**User Input Below**

```

### The plan prompt template

```markdown
You are creating an implementation plan from a feature specification.

Read the spec at `specs/spec.md` and the plan template at `templates/plan.md`.
Explore the repository to understand the existing code structure, patterns, and conventions.

Fill in the plan with these sections:
  **Technical decisions**: key technology choices, frameworks, patterns
  **Approach**: what gets added, changed, or removed, and in what order
  **Integration**: how the new code fits into the existing codebase, file locations, module boundaries
  **Validation and testing**: how the implementation will be tested, which tools, what must pass

The plan should be concrete enough that someone could implement it
without needing to make further architectural decisions.
Write the plan to the specs/ directory.
---

**User Input Below**

```

### The tasks prompt template

```markdown
You are creating a task list from an implementation plan.

Read the spec at `specs/spec.md`, the plan at `specs/plan.md`,
and the tasks template at `templates/tasks.md`.

Generate a task list organised into phases.
Each phase should be completable independently.

For each task:
  Use checkbox format: `- [ ] X.Y Description`
  Scope it small enough to implement in a single step
  Include the specific files or areas of code involved where possible

Each phase should include validation and testing tasks, not just implementation.
Write the tasks to the specs/ directory.
```

Each prompt template references the corresponding document template and tells the agent exactly what to do. The developer only needs to provide the feature description, and the prompt template handles the rest. This is already a big improvement because the workflow is now consistent regardless of who in the team is running it.

But we can take this one step further. Instead of having the developer copy and paste these prompt templates each time, we can turn them into skills.


## Automating the workflow with skills

So far we have templates for the specification documents and the prompts. With this workflow, we simply copy paste the prompt and pass it to the agent alongside with the required information about the feature we are trying to implement. This approach is perfectly valid and we could leave it here. However there is still a fair amount of copy pasting across prompts. While no one likes to copy paste, it can also introduce human errors.

We can make use of agent skills to bake the prompts into a skill we can directly invoke from within the agent. Instead of copy pasting the prompt each time, we create a skill, and invoke that skill using a slash (/) command. All of a sudden, your prompt may look like this

> _/spec [my feature information]_

In this case the `/spec` command contains all the prompt information and all we need to do is pass our feature information. THis makes the process a lot simlper and removes the need to copy paste altogether!

Skills were originally a concept impemented in claude code. However most of the agent providers offer this functionality in one way or another. As we have seen in the previous example, a skill is simply a command we invoke which holds some information about the task we want to implement. In claude code, skills live inside the `.claude/skills/` directory in your repository. Each skill is a folder containing a `SKILL.md` file, and the folder name becomes the skill name. For example, to create a `/spec` skill, the directory structure would look like this:

```
.claude/
  skills/
    spec/
      SKILL.md
```

The `SKILL.md` file contains the prompt template we defined earlier, with some metadata at the top. Here is what the spec skill would look like:

```markdown
---
name: spec
description: Create a feature specification for the current branch.
---

You are creating a feature specification.
The spec captures the **what** and **why**. No technical decisions.

Read the spec template at `templates/spec.md`.
Use the user input to understand what is being built.

Fill in the spec template with these sections:
  **Overview**: what is being built and why
  **Goals**: what this work should achieve
  **Non goals**: what is explicitly out of scope
  **User journeys**: step by step descriptions of how users interact with the feature
  **Requirements**: specific functional requirements
  **Constraints**: limitations, dependencies, or requirements that affect scope
  **Success criteria**: measurable outcomes that define when this is done

Be specific and concrete. Avoid vague language.
Write the spec to the specs/ directory.
```

Now any developer in the team can simply type `/spec` followed by their feature description, and the agent will take care of the rest. You can create the same for `/plan` and `/tasks`, each referencing their corresponding templates. Since the skills live in the repository, they are version controlled and shared across the team just like any other code.

## Walkthrough: setting up a re-usable framework

Let us bring everything together. We have templates for our documents, prompt templates that tell the agent how to use them, and skills that make the whole thing invocable with a single command. Now we want to set this up in a way that any developer in the team can clone the repo and start using it straight away.

### The repository structure

Here is what the full setup looks like in your repository:

```
your-repo/
  .claude/
    skills/
      spec/
        SKILL.md
      plan/
        SKILL.md
      tasks/
        SKILL.md
  templates/
    spec.md
    plan.md
    tasks.md
  specs/
    feature/add-user-auth/
      spec.md
      plan.md
      tasks.md
    feature/payment-integration/
      spec.md
      plan.md
      tasks.md
```

The `templates/` directory holds the document templates we defined earlier. The `.claude/skills/` directory holds the skills that reference those templates. And the `specs/` directory is where the generated documents live, organised by branch name.

### Organising specs by branch

Each feature branch gets its own directory inside `specs/`. When a developer creates a new branch and runs `/spec`, the spec file is written to `specs/<branch-name>/spec.md`. The same applies to the plan and tasks. This keeps everything organised and makes it easy to find the specifications for any given feature.

To make this work, the skill needs to know which branch it is running on. You can do this with a small setup script that detects the current branch and passes the path to the skill, or you can simply instruct the skill to use the current git branch name as the directory. Adding this to the skill prompt is straightforward:

```markdown
Detect the current git branch name.
Use it to create or locate the specs directory at `specs/<branch-name>/`.
Write the spec to `specs/<branch-name>/spec.md`.
```

As you adopt this workflow, you might want to add helper scripts that handle branch detection, check whether prerequisite documents exist before running the next step, or validate that the directory structure is correct. These are nice to have and can be added over time as the team gets comfortable with the process.

### Committing the specs

This is an important part. The spec, plan, and tasks files should be committed to the repository alongside the code. They are part of the feature, not throwaway artifacts. Committing them gives you auditability. You can look back at any feature and see exactly what was specified, what was planned, and what tasks were created. During code reviews, reviewers can look at the spec and plan to understand the intent behind the changes, which makes reviews faster and more meaningful.

It also means that if a feature introduces a bug six months later, you can go back and check whether the spec missed something, the plan had a gap, or the implementation diverged from the tasks. This is useful not just for debugging but also for improving your templates over time.

The workflow for any developer on the team now looks like this:

1. Create a feature branch
2. Run `/spec` with the feature description
3. Review the generated spec, make any adjustments
4. Run `/plan` to create the implementation plan
5. Review the plan, adjust if needed
6. Run `/tasks` to break it down into actionable steps
7. Implement the tasks
8. Commit everything: specs, plan, tasks, and code

The whole process is the same for every developer, regardless of experience level. The templates encode what the team considers important, the skills automate the prompting, and the specs directory keeps a record of every decision made.

## Defining team standards with a constitution

The templates and skills we have set up so far define the structure of the workflow. But they do not say anything about how the team actually works. What branching strategy do we use? What testing standards do we expect? What are the hard rules that should never be broken? This is where the constitution comes in.

A constitution is a single document that lives at the root of the specs directory (`specs/constitution.md`) and applies to the entire repository. Unlike the spec, plan, and tasks files which are created per feature branch, there is only one constitution per repo. It captures the team's norms, tools, quality standards, and non-negotiables in one place.

Here is an example of a constitution template:

```markdown
# Constitution

## Project context
<!-- What this repo is, who uses it, and any domain knowledge needed. -->

## Team norms
<!-- How the team works: branching strategy, code review expectations,
PR conventions, etc. -->

## Tools and conventions
<!-- Languages, frameworks, formatters, linters, test runners,
package managers, etc. -->

## Quality standards
<!-- Testing requirements, coverage expectations, CI checks that must pass, etc. -->

## Non-negotiables
<!-- Hard rules that must never be broken. Security requirements, compliance,
architectural boundaries, etc. -->
```

The constitution is created once when the team first adopts this workflow, and updated as the team evolves. It is not something that changes with every feature. Think of it as the equivalent of your linting configuration, but for how the team builds software with agents.

### Referencing the constitution across the workflow

The constitution becomes useful when the rest of the workflow references it. Each skill (spec, plan, tasks) should read the constitution before generating its output. This ensures that every feature, regardless of who is building it, is built according to the same team standards.

In practice, this means adding a line to each skill prompt telling the agent to read the constitution first:

```markdown
Read the constitution at `specs/constitution.md` for team norms and standards.
Ensure the output is consistent with the constitution.
```

When the agent creates a spec, it will check that the spec aligns with the team's quality standards and does not violate any non-negotiables. When it creates a plan, it will use the tools and conventions defined in the constitution. When it creates tasks, it will include the validation steps that the constitution requires.

This is where things start to compound. The constitution sets the rules, the templates enforce the structure, and the skills wire it all together. A junior developer running `/spec` for the first time will produce a specification that meets the same standards as a senior developer, because the constitution and templates are doing the heavy lifting.

The updated repository structure now looks like this:

```
your-repo/
  .claude/
    skills/
      spec/
        SKILL.md
      plan/
        SKILL.md
      tasks/
        SKILL.md
  templates/
    constitution.md
    spec.md
    plan.md
    tasks.md
  specs/
    constitution.md
    feature/add-user-auth/
      spec.md
      plan.md
      tasks.md
```

Notice that `constitution.md` sits directly inside `specs/`, not inside a branch directory. It is shared across all features. The template for the constitution lives in `templates/` like everything else, and you can create a `/constitution` skill to make it easy to set up or update.

## When to use and not to use agentic engineering

Agentic engineering can automate or speed up code writing, which is a positive case in many scenarios. However, when we look at companies, writing code is usually not the bottleneck. Companies are run by people, and as people we tend to be very inefficient. A lot of times the reason we are not shipping fast enough is because reviews are slow, QA takes too long, or simply requirements are not being clarified well enough.

### When to use it

There are some low hanging fruits where agentic engineering can really help. Migrations are a good example, where you need to repeat the same operation for multiple items. You can start doing one, and once it works, ask the agent to repeat it for all items while keeping the item specific configuration. Boilerplate code and proof of concepts are another good case. And more generally, tedious tasks where you are already very familiar with the repository and you know what needs to be done.

### When not to use it

In many cases, it is not about writing faster code, but about reducing the bottlenecks that are making delivery slow. That will have a much bigger impact than shipping faster code.

Even in teams where code truly ships fast, we might be tempted to deliver more than is actually needed, building features that no one asked for. With the tools available to write faster code, adding unnecessary features becomes more tempting than ever.

It may also be tempting to always use agentic engineering for all tasks. However, there are repos where a good understanding of the architecture and decisions made is important, specially if these are customer facing and we need to make deliberate decisions about the functionality we want and expect. Developers should also spend time understanding important repos they will have to deal with when on call. It is beneficial to slow down and build understanding by writing things manually when we are not familiar with a specific repo, rather than being tempted to use agents to implement our tickets, robbing us from building that understanding.
