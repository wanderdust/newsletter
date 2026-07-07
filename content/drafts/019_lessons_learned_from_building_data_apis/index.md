---
title: 'Building Performant Data APIs'
date: '2026-07-05T10:41:15+01:00'
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

Over the last 3 years at I've spent a lot of time building highly scalable Data APIs, to enable teams data access from different data sources with minimal effort. There's been several mistakes made along the way, and many lessons learned. I believe that these lessons learned here will make up for strong foundations to build performant Data APIs from day one.

Before diving into the lessons, I'll define Data API.

A Data API is an API service that serves some data to the user. The API backend connects to a database, such as Postgres, Redis or MongoDB, it runs a query based on the API call recived, and it serves that data to the end user.

![Data API](./Data_api.png)

Simple, right?

## Lesson 1: Model the Data Before it Arrives

If you were to take a single takeaway from all of this, is that with Data APIs, the infrastructure is rarely the bottleneck, the Data is.

When we were first building the Data API platform, we made the mistake of not enforcing the pre-modelling of data before it arrives in the database. This meant, for example that rather than doing joins, filters and any other business logic on the table before hand, we were landing the tables directly in Postgres (our database of choice for the API). This meant that every time the API was called, we were running very complex queries in some cases, such as combining tables on the fly, or doing expensive window or filtering operations. This meant that our API SLAs quickly went out the window, depending on the use case.

The reason why went with this approach to start with, was because it was the easier option. It meant very little coordination with the Data Engineering teams in charge of the source Data. We didn't need to bother them with creating the table our API customers needed, and we would add this logic at query time. Over time this became a real issue, because SLAs were not good enough, which meant we needed a better approach.

![API with no modelling](./api_no_modelling.png)

The solution was very simple, to model the data before it touched Postgres. THis meant that before creating an API endpoint, we would get together with the endpoint consumers and the Data Engineers to define the shape of the data. THe Data Engineers would model the Data in the warehouse before it was landed in Postgres. This involved a lot more planning work across teams, but the end result was that the tables in Postgres were ready to be queried using simple SELECT queries with minimal filters. This meant that we could serve data in ms that previously took 4 to 60 seconds to run.

The biggest challenge with the new approach was when dealing with large volumes of real-time data. We had a use case where we were receiving thousands of events per second directly into our system, which meant we needed to make that data queryable via the API as quickly as possible. Rather than landing raw data and doing complex joins and filters at query time, we modeled the data upstream before it arrived in Postgres. This meant the tables in Postgres were clean and simple to query, enabling us to serve that real-time data with minimal latency.

![API with modelling](./api_with_modelling.png)


## Lesson 2: Index on the Right Columns
<!-- why indexes matter → types of indexes → concrete before/after example (e.g. seconds → milliseconds) -->

Indexes matter a lot. Anyone who has ever worked with a database knows this. If you are new, then an index makes the difference between a query taking 4 seconds or taking 100 milliseconds. Indexes are the mechanismn in your database to "bookmark" your data, so that rather than doing a full search of your database every time you are looking for something, you can easily point your query in the right direction.

Without going into too much detail, we were able to reduce the latency of some of the more complex queries from 4 seconds to 100 milliseconds by indexing the right columns based on the query patterns. It is important to know your database well to know which indexes are useful for different situations. Some scenarios will require hash indexes (such as user ids) vs tree search (date ranges) vs other options available in each individual database. There is also a benefit to using composite indexes vs individual indexes. All of this knowledge comes when you know your database well to make the right decisions for each scenario.


## Lesson 3: Partitioning Solves the Write Problem
<!-- the write bottleneck at scale → async index creation as first fix → partitioning by date as second fix → outcome -->

One of our use cases was serving streaming data as soon as it happened using a real time API. This meant several thousand writes per second landing in our Postgres Database.

If you've worked with Postgres, you know that there is only one writer replica available, and if you have write heavy operations, you can be in a bad situation if not managed correctly. And this is what happened to us. One of our tables was recieving thousands or write request per second, on a database that was several Terabytes large. In principle, Postgres is capable of dealing with such a load no problem, assuming you have the right amount of compute, which we did.

The problem was that the table was getting so large, the index creation was becoming slower and slower. The issue with indexes, is that as you add new indexes to your table, some of the existing indexes need to be updated too. If the table grows larger and larger, the index creation process becomes slower and slower.This was an issue, because the slow indexes were preventing the data from being available for read. Also, as the table was getting larger the indexes were getting exponentially slower, to the point where the database could not keep up wich index creation and it went down

The first part of the solution was to partition the database by date. Some of our queries used the date column to filter, so it meant we could effectively redirect users to the right partitions reducing query times. The partitions also meant that we could create indexes on a much smaller table size, which was manageable enough to create the indexes fast enough.

A second improvement we added was to create the indexes asynchronously. By default, Postgres creates indexes synchronously. This means that when you write the data to your database, the data is not available for querying until the index has been created. This makes sense, because it ensures your querys are always fast. With async index creation your data is available to query as soon as it's written, and the index is created in the background without blocking the data from being read. In our case, we made the tradeoff of ensuring data availability over query speed in those cases where a user would query before the index had been created for that row. In practice, this is a very unlikely scenario, but it meant that if we ran again into issues where the index creaition was slowing down, we would at least be able to serve the data without indexes blocking us.


## Lesson 4: Partitioning Has a Cost
<!-- query pattern lock-in pitfall → maintenance overhead (cron jobs) → callback: this was a patch, Lesson 1 was the real fix -->

Partitioning solved one of our biggest problems with large growing tables. However, it's important to understand the ongoing costs.

In theory, partitioning is a great way to split your data into smaller tables, potentially making querying more efficient and dropping older tables very easy.

In reality, partitioning adds a lot of overhead to your system. For example, in postgres you have to manage your partition creationg. This means setting up a cron job to run every x amount of seconds/hours/days to create the new partitions ahead of time. A partition is essentially an empty table you need to create before you can add your data to it. Managing this cron job can be a real pain, and the logic can get complex really fast. This cron job suddenly becomes one of the most critical jobs in your system, because if it fails and you don't create/drop partitions in time, then you can be in real trouble. So you want to ensure it has the correct visibility and alerting systems so that your team can be aware of issues early on.

The other problem with partitioning is when query patterns change. For example, we partitioned by date, and this was originally a good idea because some of the queries in the API filtered by date, which meant we could effectively use partitioning to reduce the amount of data needed to be queried, potentially making query times faster.

Over time, new use cases arrived that queried the same data, which didn't use date as a filter query. Our ANALYZE queries revealed that all partitions were being scanned for these queries. Because indexes are created at the partition level, it meant that scanning all partitions is slower than scanning a single table. Our decision to partition helped us with some queries, but made other queries worse.

Undoing any partitioning can be very hard and take a lot of effort to do, which is why it needs to be carefully considered as the right option.

The lesson here is that partitioning was a necessary solution for our write problem at the time. However, in hindsight, the real fix would have been to go back to Lesson 1: better data modelling before the data landed in our database. If we had modelled the data correctly upstream, we would have written less data in the first place, potentially avoiding the need to partition altogether. That would have saved us a lot of operational overhead.


## Closing thoughts

Data APIs are all about the Data. If your data is well modelled and it has the correct indexes, you'll have a very performant API and you'll save yourself a lot of issues down the line. In our case, a lot of our challenges could have been easily solved by getting this right the first time.


{{< outro >}}
