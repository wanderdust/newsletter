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

**Module 4: Implementation and feedback loops**
Hands-on: attendees run an implementation cycle on their spec from Module 3.
- The implementation phase — how to prompt the agent to start, what to include in the prompt
- Validation loops — why the agent needs a way to verify its own work
- Types of feedback — tests, scripts, manual checks; when to use each
- Making edits — when to prompt vs when to edit manually
- Fixing forward — why you never edit the spec backwards; how to handle change
- Ownership and the pull request — reviewing AI-generated code, the 95-5 principle, what to check, security
- Committing spec, plan and tasks alongside code

---

## Implementation Phase

Once you have reviewed the tasks.md file and you are happy to move forward with it, it is time to start implementing.

Ask your agent to start implement tasks. You can choose to implement all in one go, or implement the tasks into phases, for example by grouping similar tasks into one agent execution. Example prompt:

> _Implement tasks 1 - 3. When you are done with a task, mark it as completed in the tasks.md file. Do not stop until all tasks in this phase are completed. Do not add unnecessary comments. Do not use any or unknown types. Continuously run the unit tests to make sure you are not introducing new issues._

## Validation Loops

A validation loop is essential for the agent to properly verify if the changes it has made meet the success criteria defined in the specifications. A good validation process is what brings the real benefit of using agents, because they can write, run and validate code end to end with minimal human supervision. A good self validation process also gives you confidence as a developer that the code created meets the necessary standards, even before you review it.

The validation you choose to use depends on the objective you are trying to achieve. For example, if building a website, the validation process might include passing unit tests, taking screenshots of the website to ensure it looks correct, and running simulated user journeys end to end to ensure functionality works as expected. These are all things agents can do for you, but require you specify this as a requirement during your planning.

It is also worth mentioning that the validation loop is only possible if you have a local environment you can run your project on. If your application requires you to test in a deployed dev environment which the agent can't access, you are going to have a difficult time.

### Validation as an optimisation problem

We can compare agentic engineering to how we train machine learning models.

With Machine Learning, we first build a model with random weights, which doesn't have any information about how to solve the task at hand.

During the training process, we ask the model to make a predicition on our data. Once the model makes a predicion on the training data, we check how good the predicion is, by comparing the prediction to the real value. For example, if we were predicting house prices, we would compare the prediction to the real house price.

The difference between the prediction and the real value is what we call the "Error". This error is the feedback we use to update the machine learning model. With enough feedback rounds, the model will get good at the task.

As we can see, we use this feedback loop as a way to optimise our model in the right direction so that it learns the task.

When it comes to agentic engineering, the process is not too different. We can think of the generated code as the "model" in this case. The agent is in charge of taking this feedback and using it to optimise the final solution. We can let the agent run the "model" (generated code) to gather feedback, which we then pass to the agent which uses it to update the model. After a few rounds, we reduce the overall error reaching an optimised solution.

So the question is, how do we get the right feedback?

#### What is feedback

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

#### Gathering the correct Feedback
Earlier I mentioned some types of feedback I would use as an engineer. However, different projects have different criteria, so it does not work to try and have a generic set of tests we run for each project to call it a day.

Depinding on the feedback, we can optimise towards different things. Do we optimise for speed? Code duplication? Do we simply optimise that we want the code to run but don't care about anything else? The feedback sets in which direction we optimise.


### Types of feedback

There are different levels of feedback which are useful for the model to test and validate the code.
1. Being able to run the code locally. THe agent can fix any runtime errors. This is the most basic and the minimum you should aim to have.
2. Running unit tests. Possible using Test Driven Development, where we create the tests first. It gives the model something more concrete that needs to be achieved.
3. Testing user journeys. Ask the model to build scripts which test user journeys end to end, to ensure functionality. This gives the model the confidence that all features work together with each other, not just in individual blocks.
4. Any other criteria can be created using custom scripts, such as taking screenshots from the UI.

Basically anything that you would do yourself as part of your review process before making a Pull Request, you should be able to ask the agent to do as part of the development process.

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

### Manual edits

If the issues are small and localised, a missed edge case or a minor behaviour that's slightly off, the pragmatic move is to review the code yourself and fix it by hand. This is faster than re-running the full workflow for something trivial, and it keeps you close to the code.

### Fixing forward

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
