---
title: '045_my_agentic_development_workflow'
date: '2026-03-06T13:50:29Z'
draft: true
summary: ''
# Valid tags: ai, aws, career, certifications, data-engineering, kubernetes, postgres, reflections, security, serverless, testing, tooling
tags: []
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---

Recently a friend of mine was telling me how they use AI in their development workflows. As soon as he told me he was using the copilot window I told him he was already doing it wrong. I do not need to hear the rest.

I started telling him to do spec driven development, and the workflow I use. I thought I'd document it here to share with others.

## I'm no longer using the IDE

The first thing I told him is that if you really want to get into agentic development, an IDE is no longer necessary because you give the agent all the tools to autonously build and test the features it builds end to end. All you really need to do is review the code and tests once it is done.

Instead I use a CLI agent. In my case I work with github copilot cli. I tell the agent what it needs to build and how the repo works, and I let it crack on with the work. It then uses cli tools and shell commands to achieve my goals.

If you follow this workflow, you don't really need and IDE anymore.

## Spec driven development

![workflow](./workflow.png)

### The spec.md file

This is the workflow I follow.

First I create a spec.md file in the repository. I tell the agent to create the file based on my initial specifications and let it create a detailed initial draft. The quality of the first draft will only be as good as your original specifications.

> Example prompt: _Create a specs.md file with the specifications for this feature I want to build. Focus on the what and why, not tech stack. Here are my original specs <paste your JIRA ticket here>_

The specs.md file will be your home. It is the most important part of the process to get right. With spec driven development, the specifications document is the ground truth that your agent uses to build the features you need, which is why you need to be thoruough reviewing it, and adding any changes or clarifications to it.

You may spend hours or days going through your spec file. You should make corrections and ask the agent to update the spec.md based on your corrections. You may also need to find out more information from your team or the stakeholders. Add all of this information here and ask the agent to update the document each time. Remember, any lack of detail or ambuguity might result in the final feature not turning out the way you wanted.

A lot of times, I use chatgpt's text to speech feature to transcribe all the changes I want in the spec.md file, and then paste it into github copilot cli. I like to speak what I want to change rather than type it. Hopefully copilot adds a Speech to text feature soon.

A bonus tip to create an even better spec is to make use any MCP servers available to you in order to get any additional information from your system. If you are building a feature that needs to write to a table in a database, perhaps you can make use of an MCP server that car access that database (in dev or qa) to understand the current database structure and get the queries right from the start.

Once your spec.md file is watertight and you are ready to start implementing, there is a final tip to make sure the spec is solid: ask the agent to find any ambuguity in the specification or lack of detail and prompt it to ask you for clarifications on whatever it finds.

Once the spec file is ready, I move on to the planning phase.

### The plan.md file

The next step is to create a plan.md file. The plan.md file is where you specify architecture, frameworks, and technical decisions. If you are building an an existing repo, you may want the agent to scan the current repo to understand how to build the feature using the existing patterns. If you are creating something new, you may want to be more specific in the languages, tools and so on.

> Example prompt: _Create a plan.md file. Specify architecture, frameworks, and technical decisions. Use python 3.12, terraform ..._

For the plan you can choose to either provide specific information about the frameworks, or let it do its own thing. That is up to you. Similarly to the spec.md, you need to spend time reviewing the plan and changing anything that does not look right.


Then we are ready to move on to the tasks file.

### The tasks.md file

The tasks.md file is simply a breakdown of the plan into concrete tasks to achieve the goal. The tasks break down plan into executable steps. They help the agent have a clear action plan during implementation, as well as helping it track its own progress.

> Example prompt: _Create a tasks.md file. Break down plan into executable steps._

You don't really need to provide much more information on the prompt. As long as your plan is solid, the tasks will genearally not need any more context than that. Again, read through the tasks, and check they look good. I like to ensure that one of my first tasks is to create the validation script and tests to ensure the agent has a feedback loop when testing the feature, so I will sometimes ask it to add an itnitial task to set that up.


### Implementation

Once you have your tasks.md file finished you can start the implementation. Simply ask you agent to start implementing the tasks. It helps if you break down the implementation per phases (implement tasks 1 - 3), rather than trying to do a big bang.


## Fixing forward

I treat all the files as immutable. If I want to add something else to the spec.md file once I've already created the plan.md or the tasks.md files I won't go back and update the original spec because then I need to cascade all of these changes accordingly to the plan and tasks.

Instead, once I am happy which each phase and I move forward (specs, plan or tasks) I treat each document as immutable. That means that rather than going back and make any changes, I add those as part of a new feature instead. If I missed something that should have been in the original spec, I would rather abandon the current workflow and start from the beggining, or I would implement what I already have and create a new spec.md document after I've implement the current one. I fix forward, rather than going back on myself.

## The feedback loop

Having a feedback loop for the agent is essential if you want the agent to 1) be able to build features autonously end to end and 2) ensure the final code has been tested and verified. To have a feedback loop you need to be able to run your code locally. To be able to run your code locally you need to setup a good local development environment.

If your agent does not have the tools to run its own changes locally, then you will be using the agents at 30% of their actual capacity.

With a solid feedback loop, the agent can 1) run the code to ensure it runs 2) Run unit tests to ensure nothing else has broken and 3) Create its own scripts to spin things up locally and run some integration tests end to end. With all of these things you can ensure the feature has been tested, validated and that it actually works.

## Reviewing changes

You may be thinking, how do I review the markdown files or review the changes if I don't have an IDE? You can still use an IDE for these things if that's what you prefer to use. I personally use lazygit in the terminal to review code changes, and use a lightweight notepad to review the markdown files. Use whatever works best for you.


## Conclusion

If you follaw this approach
