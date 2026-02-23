---
title: 'In the Age of coding agents local development is King'
date: '2026-02-19T08:27:51Z'
draft: false
summary: ''
tags: []
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---

Coding agents work best when they have a good feedback loop they can use to verify their changes. Without a good local environment, LLMs quickly become a time sink, rather than a time saver.

My first experience with software development was javascript, building websites using frameworks like React. One of the first things I learned was the importance of having a good local development setup. I would always have a local server, automatically refreshing on every change. If anything broke, I would instantly find out and fix the issue right away. I would also have have my unit tests [running constantly](https://martinfowler.com/bliki/SelfTestingCode.html) catching bugs in near real time.

Having a local development setup is not the norm, at least in the data ecosystem. This is usually because data applications require high memory and compute resources or access to data warehouse environments, which means it can take a lot of engineering effort to setup.

Even in my earlier days I found myself pushing for local environments for our applications. I have seen senior developers being content about using CI/CD pipelines to validate their changes, having to wait up to 30 minutes or more to validate their code.

In the age of coding agents, having a local environment can no longer be an afterthought, but rather the foundation that determines whether AI can actually make you more productive.

## What is a "good" development setup

Earlier I gave a description of what my ideal setup is. At my work I work with complex platforms, some of them have multiple microservices that interact with each other, others might need to run data pipelines to build tables in the data warehouse.
Depending on the application, it may be easier or harder to setup a local environment you can use. As your application or platform becomes more complex, the more time you need to spend "protecting" your local environment when introducing new features. You'll have to find yourself asking, "If I implement this new feature X, how do I make sure I can run this locally?".

A “good” local environment has two things.

First, you should easily be able to run unit tests locally. You should have a command, perhaps in your makefile, that runs all the tests, along with all the necessary environment variables and mock functions so you don’t depend on deployed systems to ensure your code runs.

Second, you should be able to spin up a local version of your application and platform where you can manually test things. If you are building an API, you should be able to run a localhost server, send calls with `curl` and get a response. If you are building data pipelines, you should be able to run Airflow locally and validate your DAGs. Depending on the complexity of the application or platform, it may require more effort or setup to maintain a working local environment.

With those two things, you have everything you need to get feedback in real time making the development experience a lot better and reducing the amount of time to ship new features.

## In the Age of Coding Agents local development is King

When I talk about coding agents, I'm not referring to AI autocomplete, or interacting with an LLM via the chat window. I am referring to giving the "agent" access to my code and terminal so that it can autonomously write code and execute the commands it needs to run and validate code without any assistance from me.

If I ask a coding agent to build something without a feedback loop, I become the feedback loop. Every change it makes, I have to review, run, and validate myself. When it breaks, I have to paste stack traces and explain what went wrong. It is exhausting and quickly turns into a time sink and with agents, the more iterations it takes, the messier your codebase becomes.

The best results I’ve had with coding agents came when I showed them how to use the local environment to validate their own changes. Once they can run the app and the tests themselves, they can get feedback and fix issues without relying on me.

For this to work, the specs need to be detailed and unambiguous so the agent knows exactly what to build and what to validate. Having unit tests in place beforehand also helps a lot, since they give the agent a clear target to work against.

## Spec Driven Development

The approach that I've described above works particularly well if you have all the specifications well defined and completed before starting the agentic process. This means that all the features and the expectations are well defined. It also means you know exactly is expected, so you know what to validate.

With spec driven development, you create a document with all the specs, for example if you are building a data pipeline, you clearly define the source tables and destination table. You also clearly define schemas, columns and transformations. Before you start any development, you clarify any questions with your stakeholders, and you add all this information into a spec document. You can use a framework like [spec-kit](https://speckit.org/) or simply create a spec.md document where you add all of this information. If you are using the help of LLMs to build this spec doc, you can even use different models (claude, gpt, codex) to validate each others responses and ensure you get something more robust.

Once you have a well defined spec, you need to make sure your agent knows how to spin up the local environment. It is no use to have it setup, if your agent doesn't know it can use it. To do this, you can either create an [agents.md](https://agents.md/) file to create an agent with full instructions on how to use your local setup. It will also help to use specialised agents, one for code generation, and one for code validation.

Now you can go ahead and start the implementation. The agent will have a clear understanding of what needs to be implemented, and more importantly what needs to be validated and how. It can then use the local environment to implement, test and validate any changes.

If you have a good local setup and well defined specs, then your agent may be able to implement this in the first attempt, without you having to manually provide feedback. Your implementation will only be as good your specifications.

## Use the MCPs

MCP servers are the bridge between your local environment and external systems. Local development gives agents a feedback loop framework. MCPs extend that loop to the rest of your system.

Giving your agent read only access to dev & qa environments will give it additional information it needs during planning or implementation to get the features right first time. For example, if your application needs to read or write data, having direct access to the system, will ensure the agent gets the implementation right first time.

MCP servers are useful beyond spec driven development. You can use them to speed up daily debugging or validation tasks. For example, if you are doing a large migration or deployment at scale, you can use MCP servers to validate the deployments (the logs, the errors, the data created) and help you automate the process on task that otherwise you would have to do manually.


## Have you had success with this approach?

I’ve had good success with this approach. After a year of using LLMs and agents, this is the first time it feels like a real way to automate some development work. But it only works if you have a good development setup. Without that, LLMs quickly become a time sink instead of a time saver.

## The 95%-5% Principle

With this approach, we have been able to go from spec to PR without having to write any code. Building, testing and validating end to end using agents. But this will only gets you 95% of the way. As much as you can try to have a clear spec document, the agent can still misinterpret some of it. Most of the things can be small, but still things that needed to be checked and corrected.

The last 5% is the most important and perhaps the most difficult. That 5% is where you need to take [ownership of the generated code](https://antirez.com/news/159). It doesn't just work to simply create the PR and hope for the best, because you trust your agent has implemented the right things. No matter how detailed your spec was, there can be room for ambiguity, and this needs to be checked.

I say this 5% is the most difficult because you need to take ownership of code you didn't write. You need to spend time going through the changes and ensure everything was implemented like you wanted to. If you get challenged about any code, you should be able to provide an answer, and not simply _"I don't know, the LLM wrote that part"_.

Ownership is also very important when it comes to avoiding security issues. You can't trust LLMs to follow best security practices. A lot of the times they will implement something in a way that is mainstream, but not necessarily secure. I've seen agents happily encourage long lived tokens for 3rd party authentication to AWS on public CI/CD pipelines. This is a rather subtle security issue, that may seem fine at first glance, but if someone gets hold of the token, and the permissions are too broad, someone can easily get access to your account. This can only be avoided if you know what the code is doing and its implications.

To use agents effectively and securely, you need to own the code they generate and understand the tradeoffs behind it.

## Conclusion

Having a solid local development environment is essential if you want to make the most of your coding agents. If you pair that with a good specification document, your agent will have all the tools to autonomously develop full features without any assistance from the human.

However, this doesn't mean this approach is completely hands free. As a developer you still need to own the code the agent has created, and be able to defend it if you get challenged about it in the PR review process. I believe this is going to be one of the biggest challenges for developers in the coming years as we automate more and more of our work to the agents.


## Acknowledgments

Thanks to Oleksandr for providing feedback on earlier versions of this post!
