---
title: 'Implementation and feedback loops'
date: '2026-03-06T13:50:32Z'
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

Once you get to the implementation phase, you can simply ask your agent to implement the task and end it there. The agent will produce the code based on the specifications. If that's all you do, then you still have the job of going through the validation steps required to ensure the code is ready for production, such as running unit tests, locally testing functionality to check it works and all the other things a good engineer needs to do to ensure the code is ready for production.

If that's all you do, then you are not using agentic workflows to the full potential. The real benefit of agentic engineeering is that you can integrate all of these steps as part of your workflow. We do this by giving the agent clear instructions during the specification phase of the required validation steps before marking the task complete. The validation workflow will ensure generated code meets the existing quality standards required for any code to go into production.

There is one big catch. To make this work, the agent needs to have the same level of access as you do when you when you are validating any code. Anything you do as part of the validation process, such as running tests, manual checks, UI checks etc, the agent should also be able to do. This means we really need to make an effort to ensure our project can be ran locally, and that the agent has all the necessary tools to run all of the validations locally.

With this feedback loop the agent has all the tools it needs to gather its own feedback and implement a feature end to end - from code generation to pull request. The feedback loop will ensure the agent can actually validate the code actually runs and achieves its goal, but also it ensures the end code meets the quality standards for any code going into production.





-----
SECTIONS
- What is a feedback loop? - feedback loop cycle (illustrated), difference between "agent wrote code" and "agent wrote, ran, and checked code works and fixed it based on feedback"
- Starting the implementation phase - how to prompt, propmt example
- Setting up a local environment - Why does it need it; What does it mean to run locally (python examples), common blockers (CI/CD tests, lack of permissions)
- Creating your validation loop - Example based - tests, custom scripts, when you need to go manual, choosing the right validations (optimising the solution)
- Giving agent access to CLIs and MCPs - (refer to full chapter for WHAT is CLI & MCP) how they expand your agents capabilities (example of Databricks) - Refer to MCP and CLIs chapter
- Scoping permissions safely - agents run with your credentials, access to dev environments only, do not connect to prod (dev & QA only), Least permissions approach (what if agent goes rogue)
- Sandbox environments - Why you need it (safety + autopilot), what does it look like, how to setup one
- Manual edits vs Fixing forward
- Ownership and the pull request

----

## What is a feedback loop

When you as an engineer implement any code, you have to go through some steps to ensure the code you've implemented actually works and does the thing it is supposed to do. To check this, you usually run the code to check it actually runs. You may also run the unit tests, to check the new code doesn't break any other parts of the system, and you may also write some tests for this new code. If you are building an application with a user interface, you may run the application locally and interact with it, to ensure the User interface looks correct, and that everything works as expected.

All of these things are different types of feedback that we use to check if our code was implemented correctly. Every time we look for feedback, we check if it meets our expectations. If it doesn't we use this feedback to fix our code so that it works as intended. We go through this feedback loop as many times as needed to ensure the code standards meet the expectations to call our work "done" and ready for production.

When it comes to agents, the idea is the same. In our project, we set the different checks that the agent needs to go through before it can mark any task as complete. Every time the agent writes a piece of code, it goes through all the checks. If any of them fails, the agent looks at the feedback and fixes the code. The agent repeats this process until all checks pass.

Let's take a look at these two approaches to implement a feature using agentic engineering. In the first image, we use the agent to implement the code, but there is no validation. In this case, once the code is implemented, it is up to us to run all the checks to ensure everything works. If any of the checks fail, it is up to us to re-propmt the agent with the error message so that it can go back and fix the code.


{{< mermaid >}}
flowchart LR
    A[Spec + Tasks] --> B[Agent Implements]
    B --> C[Human Tests Manually]
    C --> D{Issues Found?}
    D -- Yes --> E[Copy/Paste Error to Agent]
    E --> B
    D -- No --> F[Done]

    style C fill:#f9a8a8,stroke:#333,stroke-width:2px
    style E fill:#f9a8a8,stroke:#333,stroke-width:2px
{{< /mermaid >}}


With this workflow, the engineer becomes the feedback loop. We have to be constantly checking every time the agent finishes running so that we can run all the necessary checks. As you can imagine, this is very time consuming, and not a very fun task for an engineer to do. I'm sure you have better things to do than to copy back and forth.

Another big issue with this approach, is that you are not giving the agent the full context when you provide feedback. When copy pasting an error message, or any logs from a failed check, you may be omitting some crucial information about the check that failed.

On the other hand, if the agent has all the necessary tools to run its own checks and gather its own feedback, it can easily check everytime it needs to validate if the generated solution passes all the checks to call something done. It completely removes the human in the loop, completely automating the code implementation and validation process end to end. It will ensure the solutions meet the standards set by the checks. By having access to the validations, the agent has all the context it needs when looking at the feedback to ensure it fixes the code to a working solution.

{{< mermaid >}}
flowchart LR
    A[Spec + Tasks] --> B[Agent Implements]
    B --> C[Agent Runs Validation]
    C --> D{Issues Found?}
    D -- Yes --> E[Agent Fixes Code]
    E --> B
    D -- No --> F[Done - Ready for PR]
{{< /mermaid >}}

The agent implements, validates its own work, and iterates until all checks pass. No copy/paste. No human in the loop. The agent has full context on every failure and can fix issues autonomously.

## The implementation phase

The implementation phase begins when we've collected all of the specifications in a document and we are ready to start implementing. At this point all of the requirements should be gathered and the specifications should be clear and detailed.

If you follow a spec driven development approach, all you need to do is ask the agent to implement the tasks. If you are not using a spec driven approach then I'd recommend you break down your specifications/plan into concrete tasks the agent can follow so that there is very little wiggle room for the agent to improvise.

The implementation prompt can be as simple as

> *Implement all of the tasks in the task document*

If our implementation plan is large (we reccommend building smaller features that are easy to understand and review), then it may be benefitial to implement the tasks in phases. When implementing incrementally, we can ensure each phase has been implemented correctly, and we can make any changes early on if we detect that something is being implemented differently than we expected. This makes it easier to build on top of correct features, rather than building the whole thing and finding out at the end that the whole thing was built under the wroing foundation.

While this phased approach goes against the philosophy of fully automated end to end engineering without a human in the loop, with this process we can ensure the correct implementation is being follewed for all steps of the process.

With this approach, each phase will still have its own validations and tests to ensure each phase has been implemented correctly.

{{< mermaid >}}
flowchart LR
    P1[Phase 1] --> V1[Validate]
    V1 --> P2[Phase 2] --> V2[Validate]
    V2 --> P3[Phase 3] --> V3[Validate]
    V3 --> Done[Done]

    style V1 fill:#90EE90,stroke:#333
    style V2 fill:#90EE90,stroke:#333
    style V3 fill:#90EE90,stroke:#333
{{< /mermaid >}}

Each phase implements → validates → passes before the next phase begins. Failed validation stops the pipeline early, before more code is built on a broken foundation.

When prompting the agent, you can use something like this

> *Implement phase 1 from the tasks document*

After each phase is implemented, check the changes, commit and implement the following phase.

## Setting up a local development setup

When you are building any software, the fastest way to validate your code is to be able to run things locally.


## Creating a validation loop for your project


## Give the agent more context with MCPs and CLIs


## Scoping your environments safely


## Sandbox environments


## Manual edits vs Fixing Forward (when your specs fail)


## Ownership and the pull request



-------------
[OLD]

## Implementation Phase

Once you have reviewed the tasks.md file and you are happy to move forward with it, it is time to start implementing.

Ask your agent to start implement tasks. You can choose to implement all in one go, or implement the tasks into phases, for example by grouping similar tasks into one agent execution. Example prompt:

> _Implement tasks 1 - 3. When you are done with a task, mark it as completed in the tasks.md file. Do not stop until all tasks in this phase are completed. Do not add unnecessary comments. Do not use any or unknown types. Continuously run the unit tests to make sure you are not introducing new issues._

## Validation Loops

A validation loop is essential for the agent to properly verify if the changes it has made meet the success criteria defined in the specifications. A good validation process is what brings the real benefit of using agents, because they can write, run and validate code end to end with minimal human supervision. A good self validation process also gives you confidence as a developer that the code created meets the necessary standards, even before you review it.

The validation you choose to use depends on the objective you are trying to achieve. For example, if building a website, the validation process might include passing unit tests, taking screenshots of the website to ensure it looks correct, and running simulated user journeys end to end to ensure functionality works as expected. These are all things agents can do for you, but require you specify this as a requirement during your planning.

It is also worth mentioning that the validation loop is only possible if you have a local environment you can run your project on. If your application requires you to test in a deployed dev environment which the agent can't access, you are going to have a difficult time.

## Validation as an optimisation problem

We can compare agentic engineering to how we train machine learning models.

With Machine Learning, we first build a model with random weights, which doesn't have any information about how to solve the task at hand.

During the training process, we ask the model to make a predicition on our data. Once the model makes a predicion on the training data, we check how good the predicion is, by comparing the prediction to the real value. For example, if we were predicting house prices, we would compare the prediction to the real house price.

The difference between the prediction and the real value is what we call the "Error". This error is the feedback we use to update the machine learning model. With enough feedback rounds, the model will get good at the task.

As we can see, we use this feedback loop as a way to optimise our model in the right direction so that it learns the task.

When it comes to agentic engineering, the process is not too different. We can think of the generated code as the "model" in this case. The agent is in charge of taking this feedback and using it to optimise the final solution. We can let the agent run the "model" (generated code) to gather feedback, which we then pass to the agent which uses it to update the model. After a few rounds, we reduce the overall error reaching an optimised solution.

So the question is, how do we get the right feedback?

### What is feedback

When thinking about what is the right feedback, it is as simple as thinking, what do I do as an engineer to be sure my solution is correct before making a pull request?

From the top of my mind, I can think of a few things
- Ensure my code follows standards and practices that currently exist in repo.
- Ensure the code runs locally
- Ensure I've added unit tests.
- Ensure all unit tests pass so that we know other parts of the system are not broken
- Run it locally, test any functionality I've added.
- If I'm working on something that creates artifacts (such as data pipelines), have I checked the artifacts look like they should?

These are all steps an engineer checks before they put request up for review, once they know it is ready and tested for production.

When doing agentic engineering, you want the agents to have access to be able to gather feedback on their own. To be able to do that you neeed to ensure that your app can run locally to get all of this information.

In some cases, for more complex projects, you may need to trigger an external or remote system such as CI/CD pipeline or development environments. Whatever the case is, if we want the agent to be able to gather its own feedback when implementing a solution, it should be able to trigger and connect to this systems autonously, so that it can gather the feedback to optimise the final solution.

Whatever your project looks like, if you want your agent to generate solutions with checks as thorough as you would do yourself, you need to ensure the agent has that same access to the same feedback you would use as an engineer.

### Providing Feedback

There are different ways the model can gather its own feedback so that it can iterate its generated code towards production ready code. Essentially, you need to give the model access to all the same tools you would use to gather feedback when you want to ensure a pull request meets the standards to go for a review.

1. Being able to run the code locally. THe agent can fix any runtime errors. This is the most basic and the minimum you should aim to have.
2. Running unit tests, to ensure new code does'n break older versions of the code.
3. Using Test Driven Development. It gives the model something more concrete that needs to be achieved.
4. Testing user journeys. Create scripts that let the agent interact with the API to ensure basic functionality works end to end.
5. Using scripts or skills to test the UI, if your app has an interface.
6. Load testing. Givin the agent the tools to ensure it can run basic load testing for applications that have low latency requirements under load.



### Optimising towards the right goal
Apart from the agent being able to gather its own feedback, you need to ensure the agent is optimising the code towards the right goal. It is not just about providing the model enough feedback to ensure the code is production ready, but also ensuring the agent is recieving the right feedback from the tests to ensure it steers the final solution towards the right goal.

Depending on what you are trying to build, you may want to check different criteria. Are we optimising for speed? then you will wan to run load tests to ensure loading times stay under a certain threshold. Are we optimising towards code readability to ensure other developers can easily get into the project? then we will want to check are code is well structured using classes with easily testeable methods.

The same project idea could be optimised towards different goals and end up being completely different things. You need to find out what is relevant to you project and ensure the agent is able to access this information to optimise the solution in the right direction.

**Example: Building the same API endpoint, optimised for different goals**

Imagine you're building a simple API endpoint that processes incoming orders. The functionality is identical in all three cases: receive an order, validate it, save it to the database, return a confirmation. But the success criteria you give the agent changes everything.

If you optimise for **speed**, your validation loop measures: response time under 50ms, requests processed per second, database query execution time. The agent will add caching, connection pooling, async processing, maybe batch writes. The code becomes faster but more complex.

If you optimise for **simplicity**, your validation loop measures: lines of code, cyclomatic complexity, number of dependencies, how easily a new developer could understand it. The agent will write straightforward, single-threaded code with clear error handling. It's slower but maintainable.

If you optimise for **reliability**, your validation loop measures: retry success rate, error logging completeness, idempotency checks, circuit breaker triggers. The agent adds retry logic, detailed audit logs, rollback mechanisms, defensive checks. The code is more verbose but resilient.

Same endpoint. Three different implementations. The difference is what you chose to measure and validate.

The point is, what feedback do I need to provide so that the agent optimises to the right goal?

## Making Edits

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

## Manual edits

If the issues are small and localised, a missed edge case or a minor behaviour that's slightly off, the pragmatic move is to review the code yourself and fix it by hand. This is faster than re-running the full workflow for something trivial, and it keeps you close to the code.

## Fixing forward

If the issues are more significant, resist the urge to prompt your way out of them. Instead, treat it as a new iteration. Write a new spec that clearly describes the gap or the incorrect behaviour, go through the full spec → plan → tasks workflow, and implement the fix cleanly in one pass.

The key principle here is that spec, plan, and tasks files are immutable once you have moved past them. You do not go back and edit an earlier document mid-flight, as that cascades changes unpredictably across the whole workflow. Once you are happy with a phase and move forward, it is locked. If something is missing, you either finish what you have and create a new spec for the next iteration, or you abandon the current cycle and start over from the spec.

Fixing forward keeps the problem well-defined, gives the agent a clean starting point, and avoids the compounding drift that comes from patching a half-finished implementation.


## Ownership and the Pull Request

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
