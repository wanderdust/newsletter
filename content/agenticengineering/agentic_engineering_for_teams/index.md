---
title: 'Agentic Engineering for teams'
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

**Module 5: Agentic Engineering for teams**
- Creating re-usable framework using templates
- Standardising the workflow across the team

---

## Creating re-usable framework

Templates are essential for standardisisg the workflow and create re-usable and consistent templates the whole team can use. The templates ensure that the spec, plan and tasks files contain any mandatory sections that you want to always include, such as ensuring our specs clearly defines success criteria, important dependencies relevant to the tasks, or ensuring tests and formatting are always ran as part of implementing features.

First, create some templates in your repository in a templates folder. Create templates for the spec, plan and tasks md files with the skeleton and mandatory sections each one should have. At the top of each file describe the purpose of the file, with a sample prompt.

Then, when you are about to create a new spec, you can simply say "_I have these specs [copy paste here]_. Create a specs.md file using the template in templates/specs.md_".

## Using Agentic engineering to speed up code

Agentic engineering is the promise to automate or speed up code writing, which can be a positive case in many scenarios. However, when we look at companies, writing code is usually not the bottleneck. Companies are run by people, and as people we tend to be very inefficient. A lot of times the reason we are not shipping fast enough is because reviews are slow, QA takes too long, or simply requirements are not being clarified well enough.

### When to use Agentic Engineering

There are some low-hanging fruits where agentic engineering can really help. One of the first examples is migrations, where you need to repeat the same migration for multiple items. With agentic engineering you can start doing one, and once it works, you can easily ask the agent to repeat the operation with all items, while keeping the item specific configuration.

Another exapmple is for creating boilerplate code or proof of concepts.

Finally, it can be really benefitial for tedious tasks, or when you are already very familiar with one repository and you actually know what needs to be done and agentic engineering can save you some time.

### When not to use agentic Engineering

In many cases, it is not about writing faster code, but about reducing the bottlenecks that are making delivery slow. That will have a much bigger impact that shipping faster code.

Even when work in an agile team where code truly ships fast, we might end up in a situation where we may be tempted to deliver more that it is actually needed, potentially building features that no one asked for and that no one will use. However, developers might just build these features because they can, and with the tools available to write faster code, it makes adding more unnecessary features more tempting than ever.

ALso, it may be tempting to always use agentic engineering for all tasks. However, there are some repos where a good understanding of the architecture and decisions made might be important, specially if these are customer facing and we need to make deliberate decisions about the functionality we want and expect. Developers should also spend time understanding important repos they will have to deal with when on-call. It will be benefitial to slow down and build understanding by writing things manually when we are not familiar with a specific repo or a part of a repo, rather than being tempted to use agents to implement our tickets, robbing us from builidng that understanding.


## cognitive debt
