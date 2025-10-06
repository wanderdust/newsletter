---
title: 'Replicas vs Standby'
date: '2025-10-05T10:11:56+01:00'
draft: false 
summary: ''
tags: ['replication', 'standby', 'databases']
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---

When working with distributed systems you can encounter terminology such as "replicas" or "standby" intstances.

When I first started learning about distrubuted systems, I assumed "replicas" and "standby" were the same thing, but called differently when talking about scaling or high availability. While they can be the same thing, that is not always the case, so I wanted to clarify the concepts in this post.

## Replicas

Replicas are one or more exact copies of the primary instance of your database. Their main purpose is to balance the load. 

In a database that uses replication, there's normally a single writer instance, which accepts both read and write operations, and optionally one or more reader replicas that only accept read operations.

Replication is useful when your database recieves a large volume of read operations and you want to avoid your primary instance from getting overwhelmed with requests. You can leverage read only replicas to load balance the requests.

An important aspect of replication is how the replicas get updated. Replicas keep up to date with the primary instance by recieving frequent updates any time the pirmary instance data is updated. The are two options to go about this: synchronous replication or asynchronous replication.

With synchronous replication the primary instance waits for the replicas to acknowledge the update before getting back to the client. With asynchronous replication, the primary instance sends the updates asynchronouly to the replicas but does not wait for them to acknowledge before getting back to the client.

Which option you use [depends on your application needs](https://wanderdust.github.io/newsletter/posts/011_postgres_replication/#sync-vs-async-replication).

## Standby instances

A standby instance is an exact clone of your **primary** instance. Its main purpose is to take over if the writer instance fails. It waits patiently in the background without recieving any traffic, waiting to take over if the primary instance goes down.

A standby is an instance that **does not recieve any requests**. It is there for the sole purpose of being a backup if the current writer instance fails. When that happens, the standby takes over and starts recieving read and write requests.

This strategy is useful to ensure High Availability of your service. In other words, when you want to avoid downtime when your writer instance goes down. It is normally a good idea to have your standby instance in a different region or data center, to survive regional or data center outages.

In case of a standby, it is a good idea that data updates are recieved synchronously, so there's no data loss if the current primary goes down. The implications of synchronous updates are that writes operations won't be committed (complete) until the update has been recieved by the standby, which adds additional latency to write requests.

## Putting it all together

To summarise, both replicas and stanbyies are exact copies of your primary instance. The main difference is that replicas are used for horizontal scaling to load balance the read traffic, whereas the standby does not recieve any traffic, it just sits there waiting to take over if the primary instance goes down.

In terms of cost, when you add your first replica you are doubling your cost. Adding more replicas can get expensive really fast.

For the standby instance, you also have to pay for hosting, even though it is idle most of the time (even forever). That is the price you pay to ensure high availability.

## Using them together

Both strategies are compatible and used side by side. You can have a primary instance with multiple replicas to load balance, as well as a standby to ensure your database has high availability if the primary goes down.

## Using your Standby as a read replica

Some databases like AWS Aurora, are clever enough to combine stanbies and replicas into the same instance. For example, the standby instance can also act as a read-only replica. When the writer goes down, the replica gets promoted to primary and is able to process write requests. 

## Conclusion

I hope this was a clear explanation of the differences between replicas and standby instances. These strategies are essential to ensure high availability and scalability, and you will see them all around in all types of databases and production systems.
