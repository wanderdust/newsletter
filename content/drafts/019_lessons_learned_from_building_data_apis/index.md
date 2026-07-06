---
title: 'Building Performant Data APIs'
date: '2026-07-5T10:41:15+01:00'
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

## Lesson 1: Model the Data Before it arrives

If you were to take a single takeaway from all of this, is that with Data APIs, the infrastructure is rarely the bottleneck, the Data is.

When building a Data API, the software engineering team usually has to work closely with the teams who own the Datasets to get the right Data to the serving Database. In our case we were closely working with Data Engineers who needed to add this data to Postgres. We made the mistake early on to not enforce data modelling before the data was introduced to the database. This meant that at query time, we had to do some complex operations such as heavy filtering and join operations which made our queries extremely slow in some cases.

When building an API platform you have two options. Option 1) You load your data into your Database without prior modelling. This means that there is very litttle work on the Data Side, you add all your tables to the Database and handle the modelling at query time. The benefits of these are many, for example it requires minimal interaction with Data Engineers to model the data, and litttle planning beforehand. If you are building Real time APIs, where you need to be able to query the Data as soon as an even happens, it means you can load your events from Kafka (or Kinesis?) directly into your database and query directly from there. This is a very simple strategy. The biggest downfall of this approach is that your queries at runtime will probably look like monstosuities. Huge SQL queries, JOINining multiple tables, and doing very complex filtering. THis is a huge issue for two reasons: 1, your SLAs will go out the window. Your API will take a very long time to return results. In our case, some of our queries took from 4 to 60 seconds, wihch of course in most cases is unacceptable. Reason 2 is that your Database will suffer if there is are a lot of API requests that need to run expensive operations, which runs the risk of slowing your service. This is not a scalable solution.

[Digarman of SQL queri JOIN + mulitple tables in DB for real time and cold]

The correct approach is to model the data before it arrives in your Database. Whether you are working with Real time APIs or not, the Data in the Database should already be pre-modelled and ready to use. The benefit is that at runtime your queries will look like simple SELECT statements, that are really fast if you are using the correct indexes. THe "dissadvantage" is that you'll need to work closely with the Data Engineers and API consumers to ensure the Data is in the correct shape. It requires better planning across teams, but ensures efficient and Fast APIs.

[Diagram]

## Lesson 2: Know your database (and indexes)

Whether your Data is well modelled or not, proper indexes based on query patterns will make the difference going from seconds to milliseconds to run queries. When initally building the MVP, we ran into some performance issues that were quickly solved by using indexes on the right columns.

There are different indexes you can use, such as hash, tree search, and many others depending on the database you use. Learn the best way to combine indexes and what's more efficient in each situation.


## Lesson 3: Know your database (Partitioning)

Another issue we landed into early on with our Postgres Database was with an API that recieve data directly from Kafka, recieving thousands of write operations per second. While postgres can handle this without many issues, as the tables were getting large, our indexes were getting created very slowly, to the point where they could not keep up with the amount of writes. This meant that even though the data was arriving in time is was taking a very long time to actually be written, because the indexes were taking too long.

The solution was to make the index creation async, which means that the data gets written and it is immediately available, but the index for the newer records are not available straight away. This means sacrificing some speed on queries querying newer data.

The other part of the solution was to partition the tables for tables that had thousands of write operations per second. By partitioning by date, it meant that the indexes were only created on a subset of data, making their creation considerably faster than having to update indexes on tables many terabaytes large. On the other hand, partitioning brings its onw issues. For example, once you partition by a specific column, you need to ensure that column is a filter on the user queries. If you partition by a column that is not in the filter, it means that when there's a query coming, it is going to have to search arcoss all partitions. This is an issue we encountered, as a new query pattern arrived after our partitions were added, so those queries became rather inefficient. On top of that, when you start partitioning you need to create cron jobs to create and delete new partitions on a schedule. This adds more complexity to the platfrom, and it's worth considering when considering partitions.

One thing to note, is that for our partitioned data use case, partitioning was a patch rather than a solution. A proper fix to our problem would have involded going back to Lesson 1 and ask our users to model the streaming data before it arrived in the database. If that had happened, then we would have had fewer write operations in our database because of better filtered data arriving to the database (instead of the raw data coming straight through) and a lot of these problems woould have gone away.


## Lesson 4: Protect your Database

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
