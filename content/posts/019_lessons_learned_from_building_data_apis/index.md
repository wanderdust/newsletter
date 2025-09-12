---
title: 'Lessons Learned from building Data APIs'
date: '2025-08-02T10:41:15+01:00'
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

GOAL: Lessons from a Retired Self-Serve Data API
TARGET AUDIENCE: General Audience interested in data applications
# Lessons from a Self Service Data API

Over the past 2 years I've been building a self serving data API platform. Different teams in the org needed programmatic access the the data in the warehouse. There was no standardised way to access the data, which meant each time teams would need to figure out how to build APIs from scratch with. There were no set best practices, or reusability across teams.

There was a need for a solution, which is where this platform was born. THe platform was a plug and play where users defined the datasource and a SQL query and an API was created for them with authentication, authorisation, rate limiting, caching, pagination etc.

I've worked in this platform since the very beggining, having contributed to shape it what it is today. After two years I am moving to a new team, and I thought it would be a good time to reflect on the platform and collect some of the lessons learned.

## Users should only be able to serve data from modelled tables

Self serving can be a double edge sword. On the one hand, it gives users freedom to build their own APIs without the bottleneck of the platform team having to be involved so we can focus on developing new features. On the other hand, without the correct guardrails, users will create APIs over raw, unmodelled data. By unmoddeled, it either means tables that require complex and expensive queries to find the information you need, or tables without the correct indexes or partitions to ensure queries are fast.

This can be an issue for two reasons. First, slow APIs create poor API experiences. When working with APIs, the users usually expect sub-second latency. If the API call takes over 10s because it's querying an unmoddeled table, it will make everyone unhappy. Secondly, an unmoddelled table will add more load to the database every time it is queried because it needs to do a lot of heavy lifting execute the query. If the load is high it will consume a lot of resources, adding additional cost for needing to scale. 

This was a lesson learned early on, and one which became very hard to backtrack. Once the APIs querying these tables were "locked in" and serving business use cases, it was hard to go back and ask the users to do the extra work to model the source tables further.

## Ensuring performance comes at the cost of Freedom

This one is a continuation of the previous lesson. Our APIs allowed users to define the SQL query that was getting executed every time the endpoint was hit. Nothing would stop the users from defining very complex queries with JOINs or other queries that were not making use of the existing indexes already created on the tables.

APIs are expected to be performant, and a SQL query can make or break the API. Rather than allowing users the freedom to provide parametrised queries, we could have removed that completely and only allow users to query by primary key, where select page limit and the columns they want. This way we could have easily created indexes on the tables on a known column, and have a simple and standard select query hardcoded in the background for all APIs. An added benefit of this approach is that it forces users to model the tables to fit the API.

Alternatively, if being able to create your own SQL is a requirement for more complex business use cases, I've seen companies like Tinybird enforce a 10s timeout. Any queries hitting that threshold gets killed. This could have also been a suitable and less rigid solution.

## Perfect architectures don't exist 

This was one of the lessons that I found most dissapointing as an engineer. I had always imagined software platforms to have been built using the perfect desing patters and perfect architectures. In the real world, business use cases require to add new "patches" or features to accomodate for things like "last minute data protection requirements", regulatory needs or simply new business needs that were not orignally anticipated. More and more you start moving away from that "clean" architecture. What you can focus on, is to try and build a great platform that users really want to use, and that solves a real business need, which takes me to the next lesson.

## It's up to you to build a good user experience

Something is very clear to me now, a platform that serves a real business need does not mean that it is a platform that users will want to use. If you are not careful, you can end up building a platform that leadership loves, but the developers to use.

User experience should not be neglected. By this I mean not only the user interface (config, cli, website), but also things like documentation or the ability to test APIs easily and quickly.

The tricky thing is, that as long as the platform is doing its job, no one is going to come asking for better UI/UX features. Asking users directly is a good way, although I found that the can tend to try and be nice to you. It can be hard to setup a good round of questions to gather valuable feedbock.

A better approach is to spot the user complaints. Sometimes this can be in Slack or in a Zoom meeting. For example, a user was once complaining that to test a change in the API it took about 10 minutes for the changes to be deployed to the dev environment. Unfortunately I won't be around for long enough to improve that experience.

## Bonus: To build a scalabe Self Serving data API, you need a managed reverse ETL Solution

As I mentioned at the beggining of the post, the goal of the API is enable users to create APIs that need to query data from the Warehouse. In order to achieve this in a scalable and performant manner, the data had to be moved from Databricks into a Postgres Database, also known as the "Operational Store".

Although we provided a template for how to create both streaming and batch pipelines to move the data across, this was an extra step required for the users who wanted to create an API, which usually needed to involve additional teams. This process was very slow and not scalable, because each data pipeline required to go through a PR review process. 

In order to build a scalable data API, a managed solution is needed to move data from the warehouse into the operational Store with minimal user interaction, perhaps a few clicks here and there. This soultion should be able to create the necessary indexes and roles on the operational store to ensure good performance. Databricks already offers some similar solutions for this such as "online tables" or their new product "Lakebase", which can be useful if you are already using Databricks.

## Summary

I have shared some of the lessons learned from working on a self serving Data API platform. Although I've only spoken about the things I would have liked to improve, I also feel incredibly proud of the platform, and I believe that many things were done well, thanks to being part of an excellent team. Hopefully some of these lessons can help the someone build the next Data API.
