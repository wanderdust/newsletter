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

Coding agents work best when they have a good feedback loop they can use to verify their changes. Without a good local environment, LLMs quickly become a time sink, rather than a potentially time saver.

My first experience with software development was javascript and building websites using frameworks like React. One of the first things I learned was the importance of having a good local development setup. I would always have a local server, automaticall refreshing on every change. If anything broke, I would instantly find out and fix the issue right away.

I would also have have my unit tests [running constantly](https://martinfowler.com/bliki/SelfTestingCode.html) catching bugs in near real time.

Having a solid local development is not the norm, at least in the data ecosystem. Even in my earlier days I was the one pushing for local environments for our applications. I have seen many senior developers being content about using CI/CD pipelines to validate their changes, having to wait up to 30 minutes or more to validate their code.

In the age of coding agents, having a local environment can no longer be an afterthought, but rather the foundation that determines whether AI actually makes teams more productive.

## What is a "good" development setup

Earlier I gave a description of what my ideal setup is when I'm doing web development, but I'm not doing web development most of the time. At my work I have to work with complex platforms, some of them have multiple microservices that interact with each other, others might need to run data pipelines to build tables in the data warehouse. Depending on the application, it may be easier or harder to setup a local environment you can use. Also, as your application or platform becomes more complex, the more time you need to spend "protecting" your local environment when introducing new features. You'll have to find yourself asking, "If I implement this new feature X, how do I make sure I can run this locally?".

A "good" local environment has two things. First, you should easily be able to run unit tests locally. You should have a command, perhaps in your makefile, that runs all the tests. You should have all of the necessary environment variables and mock functions to ensure you don't depend on "deployed" systems to ensure your code runs.

The second one, you should be able to spin up a local version of your application and platform where you can manually test things. For example, if you are building an API, you should be able to run a localhost server to send some calls with 'curl'. If you are building Airflow DAGs, you should be able to run Airflow locally and be able to validate your DAG code runs. As I said, depending on the complexity of the application or platform, it may require more effort or setup to maintain a working local environment.

With those two things, you have everything you need to get feedback in real time of any changes you make, making your development experience a lot better, and also reducing the amount of time to build new features.

## In the Age of Coding Agents local development is King

I have recently been experimenting with coding agents a lot. My main finding is that coding agents work best when they have a good feedback loop they can use to verify their changes. And surprise, surprise, you need a good local environment to do that.

If I simply ask a coding agent to implement a task, without any feedback loop, I then become the feedback loop. Every time the agent changes something, I need to check the changes and see that they work. If they don't I need to provide feedback to the agent, such as stacktrace or whatever feedback it is to make the feature how I need it. This is a really exhausting process that quickly becomes into a waste of time.

On the other hand, the most success I've had with coding agents, is where I show them how use the local environment, and how they can use it to validate their changes. With this approach, the agent will have autonomy to get its own feedback and fix any issues on its own. For this to work well though, you need to make sure you prompt the agent with detailed and non ambiguous specifications, so it knows exactly what to validate and how. It can also help if you create unit tests beforehand that it can use to easily validate the code.


## Spec Driven Development

The approach that I've described above works particularly well if you have all the specifications, well defined and completed before starting the agentic process. This means that all the features and the expectations are well defined. It also means you know exactly is expected, so you know what to validate. With spec driven development, you create a document with all the specs, for example, if you are building a data pipeline with Spark, you clearly define the source tables and destination table. You also clearly define schemas, columns and transformations. Before you start any development, you clarify any questions with your stakeholders, and you add all this information into a spec document. You can use a framework like [spec-kit](https://speckit.org/) or simply create a spec.md document where you add all of this information. If you are using the help of LLMs to build this spec doc, you can even use different models (claude, gpt, codex) to validate each others responses and ensure you get something more robust.

Once you have a well defined spec, you need to make sure your agent knows how to spin up the local environment. It is not use to have it setup, if your agent doesn't know it can use it. To do this, you can either create an [agents.md](https://agents.md/) file to create an agent with full instructions on how to use your local setup. It will also help to use specialised agents, one for code generation, and one for code validation.

Now you can go ahead and start the implementation. The agent will have a clear understanding of what needs to be implemented, and more importantly what needs to be validated and how. It can then use the local environment to implement, test and validate any changes.

If you have a good local setup and well defined specs, then your agent may be able to implement this in the first attempt, without you having to manually provide feedback. Your implementation will only be as good your specifications.


## Use the MCPs

MCP servers are the bridge between your local enviornment and external systems. You should use them to provide additional context to your agents. For example, you can give your agents access to JIRA, so you can point to the ticket and it can start building the specs document without you having to copy paste. Or a more useful one, you can give your agents read only access to your dev and qa deployments, for example, to validate schemas and tables if you are working with data. MCPs give your agents the additional context to help them implement tasks more precisely by being more aware of the context the systems they are building are deployed in.

Addittionally, MCP servers are useful beyond spec driven development. You can use them to speed up daily debugging or valiadation tasks. For example, if you are doing a large migration or deployment at scale, you can use MCP servers to validate the deployments (the logs, the errors, the data created) and help you automate the process on task that otherwise you would have to do manually.


## Have you had success with this approach?

I have had moderately good success with this approach. After using LLMs and agents for the past year or so, this has been the first time I can see that this may actually be a way to automate some development work. But as I said, it requires a good development setup first, without that, LLMs quickly become a time sink, rather than a potentially time saver.

## The 95%-5% Principle

With this approach, our teams have been able to go from spec to PR without having to write any code, to build, testing and validating end to end using agents. However, this only gets you 95% of the way. As much as you can try to have a clear spec document, the agent can still misinterpret some of it. Most of the things can be small, but still things that needed to be checked and corrected.

The last 5% is the most important and perhaps the most difficult. That 5% is where you need to take ownership of the generated code. It doesn't just work to simply create the PR and hope for the best, because you trust your agent has implemented the right things. No matter how detailed your spec was, there can be room for ambiguity, and this needs to be checked. I say this 5% is the most difficult because you need to take ownership of code you didn't write. You need to spend time going through the changes and ensure everything was implemented like you wanted to. If you get challenged about any code, you should be able to provide an answer, and not simply "I don't know, the LLM wrote that part".

Ownership is also very important when it comes to avoiding security issues. You can't trust LLMs to follow best security practices. A lot of the times they will implement something in a way that is mainstream, but not necessarily secure. I've seen agents happily encourage long lived tokens for 3rd party authentication to AWS on public CI/CD pipelines. This is a rather subtle security issue, that may seem fine at first glance, but if someone gets hold of the token, and the permissions are too broad, someone can easily get access to your account. If you know what you are doing, you can spot this quickly and use more secure approaches such as short lived credentials.

In order to use agents to write code effectively and securily, you first need to own the code written by your agent, and understand the different options and tradeoffs.

## Conclusion

Having a solid local development environment is essential if you want to make the most if your coding agents. If you pair that with a good specification document, your agent will have all the tools to autonomously develop full features without any assistance from the human.

However, this does not mean this approach is completely hands free. As a developer you still need to own the code the agent has created, and be able to defend it if you get challenged about it in the PR review process, and I believe this is going to be one of the biggest challenges for developers in the coming years as we automate more and more of our work to the agents.
