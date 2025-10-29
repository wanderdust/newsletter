---
title: '032_slowly_changing_dimensions'
date: '2025-10-29T08:11:11Z'
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

Slowly changing dimensions, what a confusing name. This is the sort of term I've been hearing for a while now, but never really bothered to properly look up what it actually means. As it turns out, all at is, is whether you decide to maintain historical data in your tables by appending new rows when a change happens, or you decide to update in place instead.

Over the last few weeks I've had to work on a migration project, I needed to create an ELT pipeline to move data from an outside CRM system into Databricks. After working on the project for a few weeks, and once the pipeline was more or less in place, a new question came up. Do we want our data in databricks to keep track of changes in the source table? Or do we simply want to update any changes in place?

Let me show you an example.

Let's say my source table in the CRM system keeps track of user information, their name, last name, country, address and favorite colour. When building the ELT pipeline, we maintain an exact copy of the source table in our warehouse.

![Example Tables](./scd_intro.png)

But what happens when the data in the source updates? We have two options: we can update our destination data in place, which means we can update the destination rows that have changed in place; or for every change we can add a new row with the changes, and keeping the original row intact.

Let's see an example of implementing option one, where we update in place. This is also known as the Slowly Changing Dimension 1 (Don't ask me why). In this example, the destination table is an exact copy of the source table.

![SCD1](./scd_1.png)

The main disadvantage of this approach is that you don't keep track of the data history. We won't know that Fred Anderson used to live in Mexico, and now lives in the Bahamas. The question here is whether keeping track of this historical data makes sense for us. If this is not useful, then this approach is absolutely fine. If keeping track of history is useful, then we can do this by appending new changes rather than updating data in place. This is what is know as the Slowly Changing Dimension 2 (again, don't ask me why).

![SCD2](./scd_2.png)

In this other approach we append a new row every time there is an update in the source table. See how we have added two additional metadata columns `_start_at` and `_end_at`, which we need to keep track of when this change was introduced, and when it was "overriden" by a new change.

One of the biggest dissadvantages of the history tracking approach is that our data will keep growing forever. If there are a lot of changes in the source table, the table in our warehuse will get large very fast, making it more expensive to maintain. On the other hand when we update in place, the table size will be as large as the source table, but of course you lose all the history. These are the tradeoffs you need to keep in mind.


## Downstream

Let's say we care about history, so the destination table in our warehouse gets a new row appended every time there is a change at the source table. Once the table is in the warehouse we can use the [ medallion architecture](https://www.databricks.com/glossary/medallion-architecture) as a framework to clean our data.

For example, is this data going to be used by analysts who don't care about the history? Well, we create a new table that takes our source table and removes any duplicates to maintain only the latest records. In the process we may as well want to do some data cleaning jobs, such as formatting dates, removing whitespaces, column naming standarisation or whatever other cleanup we want to do.

On the other hand, the machine learning team might want to build a model on this data, for which they want to have the historical data. In this case they can access the raw data directly to train their machine learning models.

Finally, we may have some other use case, where the marketing team wants to see user information combined with behavioural user data that is tracked in a different table in the warehouse. Following the medallion architecture, we can take our cleaned table and combine it with this other table to create a final table ready for the marketing department to use.

![Warehouse Example](./scd_warehouse.png)

These are made up examples of how the data may be used in the company that showcase how the same data may be useful for different teams. Keeping the historical data depends on your use case, and whether this is something that may be useful to you. It is important to keep in mind that while it may not be useful now, it may be useful in the future, so sometimes it is better to be safe than sorry. After all, dumping all your data is what the data warehouse is for. Just keep an eye on your S3 storage costs.
