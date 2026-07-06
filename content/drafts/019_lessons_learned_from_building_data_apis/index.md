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

Over the last 3 years at Fanduel I've been building building highly scalable Data APIs, to enable data access from different data sources with minimal effort. There's been several mistakes made along the way, and many lessons learned. I believe that these lessons learned make up for the foundations to build a good Data API from day one.

Before diving into the lessons, I'll define Data API. A Data API is an API that serves some data to the user. The API backend connects to a database, such as Postgres, Redis or MongoDB, it runs a query based on the API call recived, and it serves that data to the end user.

[Diagram?]

## Lesson 1: Model the Data Before it Arrives
<!-- problem framing → option 1: no modelling (consequences) → option 2: pre-modelled (benefits) → recommendation -->

If you were to take a single takeaway from all of this, is that with Data APIs, the infrastructure is rarely the bottleneck, the Data is.

When we were first building the Data API platform, we made the mistake of not enforcing the pre-modelling of data before it arrives in the database. This meant, for example that rather than doing joins, filters and any other business logic on the table before hand, we were landing the tables directly in Postgres (our database of choice for the API). This meant that every time the API was called, we were running very complex queries in some cases, such as combining tables on the fly, or doing expensive window or filtering operations. This meant that our API SLAs quickly went out the window, depending on the use case.

The reason why went with this approach to start with, was because it was the easier option. It meant very little coordination with the Data Engineering teams in charge of the source Data. We didn't need to bother them with creating the table our API customers needed, and we would add this logic at query time. Over time this became a real issue, because SLAs were not good enough, which meant we needed a better approach.

[Diagram showing slow query]

The solution was very simple, to model the data before it touched Postgres. THis meant that before creating an API endpoint, we would get together with the endpoint consumers and the Data Engineers to define the shape of the data. THe Data Engineers would model the Data in the warehouse before it was landed in Postgres. This involved a lot more planning work across teams, but the end result was that the tables in Postgres were ready to be queried using simple SELECT queries with minimal filters. This meant that we could serve data in ms that previously took 4 to 60 seconds to run.

The biggest challenge with the new approach was when dealing with real time APIs. We had a use case where we were recieving data in real time straight from Kafka, which meant the users could query it sttraight way via the API. This made it very convenient and easy to setup, but as you can imagine, we were recieving raw data that we needed JOIN, clean and filter on the fly on each API call. Over time, we found that the only solution was to use spark in between Kafka and Postgres in order to do some aggretation operations to clean and filter the data. THis meant that the data wasn't available in Postgres as quickly because the transformations added a couple seconds latency. On the other hand, we made up a lot of time by simplifying the tables that landed in the Postgres, making API calls as fast as double digit millisecond. This meant that overall we reduced our SLA form around 5 seconds to 2 seconds to query real time data from when it was produced to it being available for queryiyng.

[Diagram]


## Lesson 2: Index on the Right Columns
<!-- why indexes matter → types of indexes → concrete before/after example (e.g. seconds → milliseconds) -->

Whether your Data is well modelled or not, proper indexes based on query patterns will make the difference going from seconds to milliseconds to run queries. When initally building the MVP, we ran into some performance issues that were quickly solved by using indexes on the right columns.

There are different indexes you can use, such as hash, tree search, and many others depending on the database you use. Learn the best way to combine indexes and what's more efficient in each situation.


## Lesson 3: Partitioning Solves the Write Problem
<!-- the write bottleneck at scale → async index creation as first fix → partitioning by date as second fix → outcome -->

One of our use cases was serving streaming data as soon as it happened using a real time API. This meant several thousand writes per second landing in our Postgres Database.

If you've worked with Postgres, you know that there is only one writer replica available, and if you have write heavy operations, you can be in a bad situation if not managed correctly. And this is what happened to us. One of our tables was recieving thousands or write request per second, on a database that was several Terabytes large. In principle, Postgres is capable of dealing with such a load no problem, assuming you have the right amount of compute, which we did.

The problem was that the table was getting so large, the index creation was becoming slower and slower. The issue with indexes, is that as you add new indexes to your table, some of the existing indexes need to be updated too. If the table grows larger and larger, the index creation process becomes slower and slower.This was an issue, because the slow indexes were preventing the data from being available for read. Also, as the table was getting larger the indexes were getting exponentially slower, to the point where the database could not keep up wich index creation and it went down

The first part of the solution was to partition the database by date. Some of our queries used the date column to filter, so it meant we could effectively redirect users to the right partitions reducing query times. The partitions also meant that we could create indexes on a much smaller table size, which was manageable enough to create the indexes fast enough.

A second improvement we added was to create the indexes asynchronously. By default, Postgres creates indexes synchronously. This means that when you write the data to your database, the data is not available for querying until the index has been created. This makes sense, because it ensures your querys are always fast. With async index creation your data is available to query as soon as it's written, and the index is created in the background without blocking the data from being read. In our case, we made the tradeoff of ensuring data availability over query speed in those cases where a user would query before the index had been created for that row. In practice, this is a very unlikely scenario, but it meant that if we ran again into issues where the index creaition was slowing down, we would at least be able to serve the data without indexes blocking us.


## Lesson 4: Partitioning Has a Cost
<!-- query pattern lock-in pitfall → maintenance overhead (cron jobs) → callback: this was a patch, Lesson 1 was the real fix -->

On the other hand, partitioning brings its onw issues. For example, once you partition by a specific column, you need to ensure that column is a filter on the user queries. If you partition by a column that is not in the filter, it means that when there's a query coming, it is going to have to search arcoss all partitions. This is an issue we encountered, as a new query pattern arrived after our partitions were added, so those queries became rather inefficient. On top of that, when you start partitioning you need to create cron jobs to create and delete new partitions on a schedule. This adds more complexity to the platfrom, and it's worth considering when considering partitions.

One thing to note, is that for our partitioned data use case, partitioning was a patch rather than a solution. A proper fix to our problem would have involded going back to Lesson 1 and ask our users to model the streaming data before it arrived in the database. If that had happened, then we would have had fewer write operations in our database because of better filtered data arriving to the database (instead of the raw data coming straight through) and a lot of these problems woould have gone away.


## Lesson 5: Protect Your Database
<!-- why DBs are fragile → rate limiting → caching (when to use / when not to) -->

The reason we build APIs in front of our Database is not only to do some business logic on the data, but it is to add a layer of protection to our databases. Databases can be very fragile if mis-used. If a user runs an expensive query in a for loop adding lots of load to your database, it can easily bring the database down, bringing down your whele service. This is why good to remember basic stuff like rate limiting and caching where possible.







-----

How to build a robust Data API with Postgres

## Know your Indexes

When you are building a Data API, you need to know the database you are working with. I've worked a lot with Postgres to build Data APIs, and one of the most critical things to make your API queries performant, is to have the correct indexes in your database. Having a good index in your data can be the difference between a query taking seconds to execute to milliseconds.


## Careful with partitions

Partitioning the data can be a great way to optimase how you query your data and how you handle your data. Partitioning can be super useful if you need to regularly drop "old" or stale data from your database. You can easily partition by a key, and simply drop those partitions when it comes to it, rather than having to do complex filter queries and dropping rows individually. Partitioning is more effective.

Partitioning your tables can also be very useful if the queries only need to query a subset of the data. For example, if your queries always filter by date, you may want to partition by the date key, so when a query comes, it can go to the right partition and look at a subset of the data rather than having to scan the whole table. This usually becomes useful when you are dealing with very large tables, and the cost of creating indexes becomes too high, because they take too long to create. Partitioning is a way to make indexes create faster, since indexes in postgres are created at the partition level.

The problem with partitioning is if the query patterns change, and let's say you've partitioned by date, but now the queries pattern has change and we need to filter by user id instead. If your data is partitioned by date, your query may need to look at all partitions individually to find all the user ids. This is very inefficient, because indexes are created at the partition level, so your query does not know which partitions contain a user id or not.

If this happens you will have to think about re-modelling your data to fit this new pattern, which is a lot of work.

Additionally, partitioning in postgres requires constant maintenance. It is not done by default, so you need to create a cron job (internally or externally) that creates new partitions on a daily or weekly basis. This means that there is something else to monitor.

## Use separate replicas for read and write

In postgres you can use replicas to load balance the load. Depending on your use case, you may have a lot of data being written to your database. This could be data arriving to your database via data pipelines, or data being written via API calls. In postgres you can only have one writer, but you can have many read replicas. You want to avoid overwhelming the writer replica as much as possible, so it is a good idea to create one or more replicas to handle the read operations. This will help with load when traffic is high and avoid putting your writer replica under pressure.

Using read replicas is also a good way to load balance requests and ensure you can easily scale if you have a heavy read load in your db.


## Model your data first!

One of our biggest mistakes in the early stages of building data APIs was to not have modelled data before it arrived to the database. In our case this involved planning ahead with different data teams owning the different datasets that needed to be served, and it would not always be modelled to the query patterns that our users needed. THis meant, that when users were making calls to the API, the API was then having to do complex operations, such as joining multiple tables to produce the desired output, which make API response times slow, which made users complain.

If you are building a data API, the best thing you can do is to model your data first, so that when the user hits the API, the API simply needs to do a simple SELECT query because the data is already in the right shape. If you are using indexes effectively, you will get results in single digt milliseconds. SUper fast!

## Real time Data APIs have tradeoffs

There are many different types of Data APIs. The type of APIs I worked with were mainly read only APIs (GET requests), whose purpose was to provide programatic access to applications that were user facing. One such case was building an API to provide real time player information to customer support teams so they can handle support queries and have access to data in real time. For this use case there was a streaming pipeline writing data to postgres, which added user transaction information as soon as it happened, so customer support could have access to it via their Support Interface which called our API.

As I mentioned in the previous post, it is always a good idea to model your data first to ensure your queries are super fast! However, when it comes to to real time considerations you are very likely going to have to tradeoff data freshness vs query speed. In real time applications where you need you data available in your API (database) within a second of the data being produced (ie user transaction), trying to model your data beforehand might take too much time and slow you down. So you may end up putting your raw data in the database. However keep in mind that by doing this you will put this sacrifice on the end user, who will experience slower query times if every time they call the API, it needs to run complex joins and aggregations to get the data in the right shape.

The tradeoff depends on your project, and what works best for your team.


## Rate limiting and Caching.

As with any good data API, make sure you include rate limiting. Databases can be fragile, and one bad user making millions of calls to your API could ovewhelm the database and bring it down. Caching can help with this as well, if the underlying data being returned by the API does not change that often (ie it updates hourly), then you may improve query response speed by caching some of the results. However do not cache responses if your underlying data changes constantly, for example if you work with real time APIs. The same API call, with the same parameters may return different results which include the newest records. You do not want to cache those.


## Self service? Great idea, harder to maintain

One of the API platforms I worked with was a self serving Data API, where internal teams could create their own APIs to access different datasets or different datasources (redshift, Databricks, Postgres etc.). The idea is great, we provide the platform and the connectors to different datasources, and they simply provide the SQL queries to query those datasources. Each SQL query corresponds to an endpoint they own.

The biggest challenge we hit with this appraoch was not owning the underlying data. THis meant that by users creating the queries, they were not always optimised, which meant that when the APIs were slow we would get complaints, and we would have to look into issues such as bad query patterns or lack of indexes in the underlying tables. Self serving is a great idea to programatically give your company access to data, but it means you are not always able to optimise your data as much as if you have full control of it.


## Load testing

In my time building APIs, I used the locust framework to run all sorts of load tests. You want to make sure your APIs and your databases can handle different loads before you put them in production. You may also have spikes of traffic during the year, wether it is black friday if you are an ecommerce company, or sporting events like superbolw if you are in the sports or entertaniment industry. You want to have a platform to ensure your APIs can cope with the level of lead. Start by creating simple tests and eventually devolop a re-usable load testing platform you can re-use whenever you need to teast different levels of load in your API.
