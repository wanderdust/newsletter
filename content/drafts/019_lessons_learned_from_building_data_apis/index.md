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

---

While working at Fanduel I have spent nearly two years building Data Apis to enable different teams to access data programatically from different data sources. When I say Data Api, I am referring to APIs whose purpose is to serve data from a data source, such as Database, a Data Warehouse.

Data APIs are important because they give your applications access to the data they need in a secure and scalable way. When you build an API in front of your database, you are adding an additional layer of security to protect both your data and your database. It protects your Database infrastructure from going down from potential mis-use of the clients, as well as only giving access to the clients to the data they need, enforcing Least Priviledge access best practices. On top of that, APIs can help you optimise the speed and efficiency to which your data is queried.

These are some of the lessons I've learned, which I'll carry with me when building new APIs from scratch.

## Your API is only as fast as your queries

If your query is slow, your API response will be slow. If I had to take asnigle lesson from building good Data APIs, it would be that the most essential thing is that the data in the Database needs to be precomputed. What this means, is that when I'm querying the database from the API, it should always be a simple SELECT query, which will always be fast, and it is super easy to optimise.

On the other hand, if you run queries with complex transforms logic or JOINs, you can expect your API responses to be slow. You may be thinking this is very obvious, however this can easily happen when you add your data in your database before thinking about the use case. When your use caso comes, you may find yourseld having to join data from different tables te get the data you need. Which can end up in disaster.

The right approach is to understand the use case first, and do your transformations before you land your tables in the database. 

## Real time is hard

Having said all that in the previous section, this can become a challenge when building Real Time APIs. When I say Real Time, I mean APIs in which the data is accessible within a second or less of it being produced. For example, a bank may want to build an fraud API in which they can query any transactions as soon as they occor so that can catch fraudulent transactions in real time. In such use cases, transforming the data before landing it to the database can add some latency to how soon a transaction is ready to be queried, which depending on the use case, it may be critical to have it as soon as possible.

In this case , there is a tradeoff between transforming your data before you land it in your database, vs transforming your data on the fly when a client queries the data. Here is about considering the risk of slower arrivinng data vs the risk of scaling an API where data is pre-computed on the fly.

This should only really be an issue when working with real time APIs. If you don't have real time considerations, data should always be precomputed.

## Know your indexes

Learn the database you are working with, and make use of whatever indexes it can offer. Understand which indexes work better for different situations. Understand whether you should use composite indexes vs single column indexes. The difference between a query taking 3 seconds and 20ms can be a well placed index. It is not that hard.

## Partitions are hard to maintain

I worked mainly with Postgres. In Postgres you can use partitions, in which you split the your large tables into smaller chunks which can be benefitial for things like making it easy to drop tables, reducing the amount of data your query reads if the data is contained in a single partition, and making indexes faster to create because they operate on a single partition rather than on the whole table.

The problem with partitions, is that they are hard to maintain. You need to have a separate process, such a cron job to create new partitions, as well as dropping old partitions if that's something you need to do. THis is the sort of thing that ends up growing arms and legs, and can become hard to maintain.

At the same time, partitions come in handy when queries filter by the partition key. But query patterns change over time, and you may find yourself in a situation where you are not using the partition key in your query filter, which means you need to scan accross many partitions making your queries potentially really slow. Remembre, that when working with partitions in postgres, and many simiilar databases, indexes are created at the partition level not at the table level, so you can end up with very inefficient queries later down the line.

Partitions are great, but make sure you understand the risks of partitioning too early, the cost of maintenance, and the potential for query patterns to change down the line.

## Self serving = slow queries






















-----
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
