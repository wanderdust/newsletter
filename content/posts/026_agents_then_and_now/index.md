---
title: '026_agents_then_and_now'
date: '2025-08-25T09:55:49+01:00'
draft: true 
summary: ''
tags: []
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---

I was starting to get a bit overwhelmed with all the agent stuff I see on Linkedin. I kept reading agent this and agent that, without really being sure of what an agent really was, expect knowing it involved some sort of LLM calls.

I came across [this blog post](https://ghuntley.com/agent/) which shows the basic flow of an agent, and it encouraged me to build my own. 

I have [previously done some work with agents](https://pablolopezsantori.substack.com/p/q-learning-explained-through-billys) when I was learning about reinforcement learning, and I was curious to know how different agents today are from agents back then.

This is a blop post that explains the basics of agents, and how LLM agents are still pretty much the same, expect we've added some LLM magic in the loop.

At the end of this post, I show an example of a Sofware Engineering Agent I've build for the purpose of this blog.


## What Is an agent?

An agent is something or someone taking actions within an environment.

Usually trying to complete a goal.

An agent could be your robot hoover, whose goal is to clean your livingroom (and getting stuck halfway)

![Image of robot hoover]()

An agent could be a person, making choices to try and find the meaning of life

![Image of a person]()

Or an agent could simply be a computer program, like this guy.

![frozen lake agent](./frozen_lake.gif)

This guf is trying to reach the present without falling into the lake.


## How do agents work?

In very simple terms, an agent takes action within an environment. Every time it takes an action, it checks if it has accomplished its goal, and if it hasn't it continues.

Lets take a look at the elf in the frozen lake.

The agent is the little elf, whose goal is to get to the present at the bottom right corner.

The agent starts in an initial *state*, in this case, at the very top left of the map. A *state* is the position of the agent in the environment.

The agent acts within an environment, which is in this case it is a grid of 4x4.

In this environment the agent can take 4 *actions*, move up, down, left or right.

The basic loop looks something like this.

![agent diagram](./agent_diagram.png)

Every time the agent takes an action, it evaluates whether it has achieved its goal, and if not it continues to take more actions until it finally achieves its goal or dies along the way.

## Taking actions

This is where it gets interesting. It is up to us to define how the agent acts in the environment.

A very naive approach can be to get the agent to select an action randomly until it achieves its goal. However this will not only be inefficient, but it will not work for complex environments with more complex goals.


A better approach is to take an action by taking your current position in the environment. For example, if there is a hole in front of you, move right to avoid falling into it.

For this you can have rule based agents, which may work in some environments.

For more complex environments, machine learning models can come in handy.

And this is where LLMs come in.

## Building an agent with LLMs

LLMs can be used to create agents to solve non trivial tasks such as "*Add unit tests to my project*".

The agent flow remains pretty much the same, except we use an LLM to decide which actions to take and to evaluate whether the task has been completed.

Lets look at an updated diagram that we can use to build an agent.

![LLM Diagram](./llm_diagram.png)

In this case, the agent is the LLM, which has to take actions to achieve the goal defined in the user prompt.

The environmnent is your laptop, with its files, directories, the shell, etc.

The actions available to the agent are those that you define within your program. For example, if we are building a software engineering agent, we could give it access to tools such as reading files, listing directories, searching files and writing files. You can add whichever actions you want.

The flow goes like this:
1. THe user writes a prompt. THis will be the goal the agent needs to achieve. For example "*Write unit tests for my program*".
2. The prompt is passed to an LLM. THe LLM is aware of the available tools you have given it access to. It processes the prompt and returns a response. The response can be one of two:
    1. The LLM lists a list of tools that it wants to run to be able to achieve its task. To write some tests it may ask to run the read tool to read the files it needs to create tests for, and the list tool to know where it creates the new test files. 
    2. A final response. If the LLM does not want to use any tools, we can assume that the response is final.
3. If the LLM wants to use tools, your program goes ahead and executes them, it gathers all the information and feeds them back to the LLM so it can generate a response. Again, the LLM can choose to use more tools, or generate a final response. In this case, the LLM has not yet written the tests, so it may ask to write the test file now that it has the relevant info it needs. We repeat the process until the lLM generates a response that does not want to use more tools.
4. When we have a final response, we want to evaluate it agains the inital goal. Did the agent solve the task I originally asked for? We can also use an LLM to evaluate this.

## Tools instead of actions

When talking about LLM agents, we talk about tools instead of actions. With the simple agent, we had specific actions the agent could take. With LLMs, we provide a set of tools, and the LLM can use them to run specific actions.

In the same way you can use a hammer to hammer a nail, or to kill a fly, the LLM can use the write tool to create files or to edit existing files. The action is what the agent decides to do with the tool.

## Coding agent in action


![example swe agent](./swe_agent_demo.gif)

## Conclussion

I built a coding agent to get more familiar with LLM agents. It all boils down to the same loop.

LLM agents today are very much the same as the agents we've been building in the past, including your robot hoover. 

I hope this blog post has clarified the topic a bit, and encourages everyone to build their own.

After all, all it is, is an API call within a for loop.
