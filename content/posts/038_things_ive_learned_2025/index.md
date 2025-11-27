---
title: '038_things_ive_learned_2025'
date: '2025-11-27T08:15:55Z'
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

This has been one of the years where I've learned the most things, probably since I first started learning programming almost 10 years ago. I thought it would be a great excercise to put them all into writing to reflect on each thing, and why - or why not - it's been a useful thing to learn.

[
  Draft list
  - Load testing
  - Postgres - Indexes, partitioning, replication, sharding, failover
  - Reverse ETL & Pyspark
  - Tmux
  - Neovim
  - Connection Pooling
  - GraphQL
  - AWS in depth and advanced cloud architectures
  - How to build Agents (coding agent)
  - DVORAK
]


## The Dvorak keyboard layout

The first thing I set out to learn in 2025 was how to type using the DVORAK keyboard layout. The main reason was simply because it sounded like a fun thing to do. I still remember how much fun it was to learn QWERTY in school, going through all of those timed excercises. This time around it wasn't as fun, and to be honest, it was very frustrating at times, especially when my brain completely forgot how to QWERTY and I was stuck typing DVORAK full time at very low speeds.

I can't say this is a very useful skill to have, and I actually type slower than I did QWERTY, despite claims that DVORAK should make you type faster. On the other hand, it was super fun to learn, and learning new things is always a good idea, so no regrets.

## Neovim, tmux

Back in 2024 I started to ditch my VScode setup for other alternatives. Not for any particular reason, mainly because my colleague Oleksandr (A die hard Java guy) kept saying how bad VScode was as compare to IntelliJ. I quote "You need to stop using a kids editor and start using a real enterprise tool for professionals". So this got me into trying Intellij. At this point I thought it was really good, and really liked working with it. I was starting to learn all the shortcuts to use the mouse less and less, and that's when I decided that I might as well learn something like VIM instead rather than specific IntelliJ shortcuts. I really enjoyed the extension and worked well, so I did this for a couple of months.

Then I remembered how my ex-colleague Gordon used to work on this thing called NeoVim, so I decided to look into it. It looked like fun so I decided to give it a go. It was quite hard to setup at first, but once I got it working I've never looked back. It is hard to explain the satisfaction of being able to work in the terminal, never leaving the keyboard, not having to click UIs. It also made me realise how bloated code editors can be, and how little you really need to be productive. It also forced me to learn what goes behind all of these extensions that you take for granted, which is mostly open source tools and libraries that have been integrated behind a Graphical UI. It also made me find out about new tools such as lazygit or tmux which I absolutely love.

You don't need to know what goes behind the scenes of your tools to be productive at your job. In fact, it may be considered a waste of time. However I feel like this deeper understanding of my local setup and all the things that come into play have made me understand my system much better, feeling more competent as an engineer.

## Helix

About a month ago I kept seeing blog posts about people using helix instead of neovim. It really got my curiosity going so I decided to take a look to see what it was all about. It is basically a similar editor to Neovim, with very similar key bindings, but with a lot simpler configuration to setup. I've been using it for the past month and I really love it. Setting up neovim was quite hard and time intensive (also probably because it was my first time) and I really didn't care about the tinkering. I kept thinking how hard I was going to find it when I had to setup neovim in a new laptop. With Helix the setup is super easy, and it's all done in a couple of TOML files. I feel like I can install it in any laptop and set it up in minutes, which is exactly what I want - something that works out of the box. Also, the keybindings are incredibly similar, so the learning curve from Vim to Helix is very low.


## Postgres, Scalability and Failover

Over the past year I've taken an interest in Postgres, which has suprised me more than anyone else. I never thought I'd find databases interesting but here I am. This year I've gone from passive Postgres user, to really trying to understand how it works inside out.

A lot of this started when I interviwed for SkyScanner and was told that I didn't really cover scalability in the systems design interview. THis made open the "Designing Data Intensive Applications" book to dive deeper into the topic. At the time I was working a lot with Aurora Postgres for a platform my team was building, so I was able to put all I reading into the postgres perspective.

THis last year I've written over 5 blog posts covering Postgres, whether it is scalability, replication, indexes, partitioning and so on. Writing this content has really helped me solidy my understanding of how Postgres works, how it scales and how it handles failover, but most importantly all the tradeoffs involved when designing a database system. By learning about Postgres, I also started to learn how other databases do things differently, and why. Over the past year I feel like I've gone from very littile knowledge into scalable systems to a very solid understanding of how to build for scale, and which systems are most suitable for different scenarios. 

I think this has been the biggest leap in learning I've done in the last few years. Not only understanding databases, but how a lot of the same principles apply to any other system that is built with scalability in mind.

## Dive Deep into AWS

I have been an AWS user for the last 5 years, just using the services that I need. I thought I knew it pretty well until I went I went through an interview process for an internal role in which AWS was heavily discussed. I realised that even though I used a lot of the services, there were many more I either never heard about or I used them but didn't really learn about them beyond the surface. The feedback I got into this interview was that they were looking for someone with a bit more expertise in AWS, and the recruiter recommended the AWS Architect Associate certification. So I went ahead and looked into it.

Preparing for the cert was very time intensive, taking about 2 months of 2-4 hours study each day. After completing the associate I thought it'd be silly not to attempt the professional one considering a lot of the knowledge was still fresh.

I know a lot of people feel certifications are a waste of time. For me, it gave me focus time to read and learn about a platform that I use in my everyday job. It allowed me to set time aside to deep dive into services that I thought I knew well, only to realise how little I knew about them (IAM, S3, VPC or EC2!). For me, spending time learning the tools that you work with is very much worth your time, whether that's AWS, GCP, Python, VScode or whatever it is. You won't know the tradeoffs unless you know what options your tooling offers.


## Spark, Delta and DuckDB

This year I've suddenly found myself working a lot with Databricks, working on different use cases such as reverse ETL, data ingestion or testing the SQL warehouse for high volume of read queries. I've also learned a lot more about data warehousing in general and how delta effectively detaches storage and compute to create an effective analytical system based on column storage.

The most exciting platform I've had the pleasure to work with in this space is DuckDB. It is such a good idea that I don't know why no one has come up with it sooner! In fact, my most popular blog post in Medium was about comparing DuckDB to Databricks SQL Warehouse.

## AI Agents

With all the hype around LLMs I've really ignored this topic for a long time. In my mind, any AI Engineering was really making API calls to an LLM, which didn't really interest me much. However, with the new agents, and particularly after starting using Windsurf and then Copilot CLI I started to get curious about agents, so I decided to build my own.

I built a small coding agent using the AWS Bedrock API. I found out that I wasn't that far off, building agents is really an LLM call within a for loop. However it was fun to build it, considering you have to design the tools, and play around with the implementation to get the feedback loop right. I get the impression that the main challenges come from implementing the correct guardrails in these agents than anything else. I also find it unsatisfying that a lot of the AWS services around AI systems are mostly managed black box systems. This is probably the right way to go, but as an engineer it makes me very unsatisfied. I want to tinker and control the infra and systems I build.

Seems like the future is going this way, so now is really the time to upskill in this field.



## Honorable Mentions

Other things that I've learned but that I don't really feel that excited to write about in detail are: graphQL, Connection Pooling, Load Testing or other day to day work stuff.


## Conclusion

This year I feel I've learned a lot of things. Some a lot more useful than others. The process of learning is the fun part, the outcomes of it useful in some cases, but for me, not really the important part.

Happy Learning!
