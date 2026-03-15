---
title: 'Ownership, security and new ways of working'
date: '2026-03-06T13:50:35Z'
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

**Module 7: Ownership, security and new ways of working**
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
