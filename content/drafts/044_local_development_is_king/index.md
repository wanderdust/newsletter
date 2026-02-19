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


My first experience with software development was javascript and building websites using frameworks like React. One of the first things I learned was the importance of having a good local development setup. First you would have a local server always running and showing your webapp in one screen, and every time you made a code change, the server would automatically refresh to show the new changes. If anything broke, you would know in real time, and you could easily go back and fix whatever was causing the webapp to fail.

I would also have my unit tests, and one of the things I loved the most was able to run my tests constantly and see the results in real time. I would have a local server that would run all the unit tests every time a new change was introduced, which gave me feedback in real time to see if I unexpectedly broke something when introducing my new change. This appraoch would work best when doing test driven development, where you would see your new test failing until you fully implemented your change and it finally went green.

This approach was really good to get feedback in real time about any potential bugs or breaking changes in real time.

My professional experience has shown me that having a solid local  development is not the norm, at least in the data ecosystem. I have worked as a Machine Learning Engineer, Data Platform Engineer and Data Engineer, and in all the teams I've been in, I have always been the one pushing for better local development environments for our applications and platforms, even during my junior engineer days. This is not to say that no one cared, I have met some very good engineers who made the effort to prioritise building good local environmnents, but from my experience this has not been the norm.

I have seen a lot of developers, including senior engineers happily develop without a local environment to easily get feedback on. THese developers seemed more than happy to have to wait for the CI/CD pipelines to deploy to the dev environments before being able to test their changes. Perhaps these developers were so confident in their programming skills that they knew they were going to get it right first time. In my case, when I have to work in such applications where I need to wait 15 minutes or more (sometimes as much as 30 minutes or more) I start to go crazy to the point of tearing out my hair.

So, a good local environment is not only essential to get rapid feedback on any changes you've implemented, but it is also essential if you want to make the most of your coding agents.

## What is a "good" development setup

Earlier I gave a descriptions of what my ideal setup is when I'm doing web development, but I'm not doing web development most of the time. At my work I have to work with complex platforms, some of them have multiple microservices that interact with each other, others might need to run data pipelines to build tables in the data warehouse. Depending on the application, it may be easier or harder to setup a local environment you can use. Also, as your application or platform becomes more complex, the more time you need to spend "protecting" your local environment when introducing new features. You'll have to find yourself asking, "If I implement this new feature X, how do I make sure I can run this locally?".

A "good" local environment has two things. First, you should easily be able to run unit tests locally. You should have a command, perhaps in your makefile, that runs all the tests. You should have all of the necessary environment variables and mock functions to ensure you don't depend on "deployed" systems to ensure your code runs.

The second one, you should be able to spin up a local version of your application and platform where you can manually test things. For example, if you are building an API, you should be able to run a localhost server to send some calls with 'curl'. If you are building Airflow DAGs, you should be able to run Airflow locally and be able to validate your DAG code runs. As I said, depending on the complexity of the application or platform, it may require more effort or setup to maintain a working local environment.

With those two things, you have everything you need to get feedback in real time of any changes you make, making your development experience a lot better, and also reducing the amount of time to build new features.

## In the Age of Coding Agents local development is King

I have recently been experimenting with coding agents a lot. My main finding is that coding agents work best when they have a good feedback loop they can use to verify their changes. And surprise, surprise, you need a good local environment to da that.

If I simply ask a coding agent to implement a task, without any feedback loop, I then become the feedback loop. Every time the agent changes something, I need to check the changes and see that they work. If they don't I need to provide feedback to the agent, such as stacktrace or whatever feedback it is to make the feature how I need it. THis is a really exhausting process that quickly becomes into a waste of time.

On the other hand, the most success I've had with coding agents, is where I show them how use the local environment, and how they can use it to validate their changes. With this appraoch, the agent will have autonomy to get its own feedback and fix any issues on its own. For this to work well though, you need to make sure you propmt the agent with detailed and non ambiguous specifications, so it knows exactly what to validate and how. It can also help if you create unit tests beforhand that it can use to easily validate the code.


## Spec Driven Development

The approach that I've described above works particularly well if you have all the specifications, well defined and completed before starting the agentic process. This means that all the features and the expectations are well defined. It also means you know exactly is expected, so you know what to validate. With spec driven development, you create a document with all the specs, for example, if you are building a data pipeline with Spark, you clearly define the source tables and destination table. You also clearly define schemas, columns and transformations. Before you start any development, you clarify any questions with your stakeholders, and you add all this information into a spec document. You can use a framework like [spec-kit](https://speckit.org/) or simply create a spec.md document where you add all of this information. If you are using the help of LLMs to build this spec doc, you can even use different models (claude, gpt, codex) to validate each others responses and ensure you get something more robust.

Once you have a spec well defined, you can go ahead and start the implementation. The agent will have a clear understanding of what needs to be implemented, and more importantly what needs to be validated and how. It can then use the local environment to implement, test and validate any changes.

If you have a good setup and well defined specs, then your agent may be able to implement this in the first attempt, without you having to manually provide feedback.

## Have you had success with this approach?

I have had moderately good success with this approach. After using LLMs and agents for the past year or so, this has been the first time I can see that this may actually be a way to automate some development work. But as I said, it requires a good development setup first, without that, LLMs quickly become a time sink, rather than a potentially time saver.

With this approach I was able to go from spec to PR without me having to write any code, to build a spark pipeline which was tested end to end by the agent. However, this only got me there 95% of the way. As much as I tried to have a clear spec document, the agent still misinterpreted some transformations, for example adding filters where it shouldn't have. Most of the things were small, but still things that needed to be checked and corrected.

The last 5% is the most important and perhaps the most difficult. That 5% is where you need to take ownership of the generated code. It doesn't just work to simply create the PR and hope for the best, because you trust your agent has implemented the right things. No matter how detailed your spec was, there can be room for ambiguity, and this needs to be checked. I say this 5% is the most difficult because you need to take ownership of code you didn't write. You need to spend time going through the changes and ensure everything was implemented like you wanted to. If you get challenged about any code, you should be able to provide an answer, and not simply "I don't know, the LLM wrote that part".

## Conclussion

Having a solid local development environment is essential if you want to make the most if your coding agents. If you pair that with a good specification document, your agent will have all the tools to autonously develop full features without any assistance from the human.

However, this does not mean this approach is completely hands free. As a developer you still need to own the code the agent has created, and be able to defend it if you get challenged about it in the PR review process, and I believe this is going to be one of the biggest challenges for developers in the coming years as we automate more and more of our work to the agents.
