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

1. Intro
2. Agent workflow (for loop and choosing actions, check if terminal state)
2. Agents back in the day of reinforcement learning - workflow
4. Agents today - workflow
5. What is common and what has changed (conclusion)


## What Is an agent?

An agent is anything on anyone taking actions within an environment.

Usually trying to complete a goal.

An agent could be your robot hoover, whose goal is to clean your livingroom (and getting stuck halfway)

![Image of robot hoover]()

An agent could be a person, making choices to try and find the meaning of life

![Image of a person]()

Or an agent could simply be a computer program, like this guy.

![frozen lake agent](./frozen_lake.gif)

This guf is trying to reach the present without falling into the lake.



## How do agents work?

In very simple terms, an agent is simply a program taking actions an an environment and constantly checking if it has achieved its goal.

In the case of the robot hoover it goes like this. The goal of the hoover is to remove all fluff from your livingroom.

1. Before doing anything, hoover looks around the livingroom. Hoover sees some fluff to its left.
2. Hoover takes action to move left, and hoover the fluff.
3. Hoover has now removed the fluff, so hoover checks if it has accomplished its goal. In this case, it needs to clean the whole livingroom. The answer is no, so hoover repeats step one.

As you can see this is an infinite loop that only breaks when the livingroom has been cleaned. 

There is also the possibilty of the hoover running out of battery or getting stuck (very likely this one) before accomplishing its goal. These would also cause the loop to break.

If you like diagrams, this is what it would look like

![Diagram of an agent]()

So that is basically all it is. Agents try to achieve their goals the best of their abilites using that basic loop.

Sometimes they achieve their goals, and sometimes they get stuck along the way. 

But don't we all.


## Building an agent with LLMs

Building an agent with an LLM is pretty much the same.

Except we use the LLM
