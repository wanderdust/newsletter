---
title: '016_postgres_ha_vs_scalability'
date: '2025-07-21T10:11:56+01:00'
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

When working with distributed systems you can encounter terminology such as "replicas" or "standby" intstances.

When I first started learning about distrubuted systems, I assumed "replicas" and "standby" were the same thing, but called differently when talking about scaling or high availability. While they can be the same thing, that is not always the case, so I wanted to clarify the concepts in this post.

## Replicas

Replicas are exact copies of the database. Their main purpose is to balance the load. 

In a database that uses replication, there's normally a single writer instance, which accepts both read and write operations, and optionally one or more reader replicas that only accept read operations.

Replication is useful when your database recieves a large volume of read operations and you want to avoid your writer instance from getting overwhelmed with requests. You can leverage read only replicas to load balance the requests.

An important aspect of replication is how the replicas get updated. Replicas keep up to date with the writer instance by recieving frequent updates any time the writer instance data is updated. The are two options to go about this.

The updates can be synchronous - where the writer instance waits for the replicas to acknowledge the update before getting back to the client - or asynchronouly - where the writer instance sends the updates asynchronouly to the replicas but does not wait for them to acknowledge before getting back to the client. Which option you use depends on your application needs.

## Standby instances

A standby instance is an exact clone of your **writer** instance. Its main purpose is to take over if the writer instance fails.

A standby is an instance that **does not recieve any requests**. It is there for the sole purpose of being a backup if the current writer instance fails. When that happens, the standby takes over and starts recieving read and write requests.

This strategy is useful to ensure High Availability of your service, In other words, when you want to avoid downtime when your writer instance goes down. It is normally a good idea to have your standby instance in a different region or data center, to survive regional or data center outages.

In case of a standby, it is a good idea that updates are recieved synchronously, so there's no data loss if the current primary goes down. The implications of synchronous updates are that writes operations won't be committed (complete) until the update has been recieved by the standby, which adds additional latency to write requests.

## Standby vs Replicas

Both replication and standby are exact copies of your database, but they serve different purposes. The main difference is that replicas are (normally) read only instances used for horizontally scaling your applications whereas a standby is a writer instance that sits "idle" and in only used when failover happens.


## Using them together

Both strategies are compatible and used side by side. You can have a database with multiple replicas, as well as a standby to protect yourself from failover.


## Using your Standby as a read replica

Some database systems are able to combine both Standby and Replicas into a single instance. For example, the standby instance can also act as a read-only replica. When the writer goes down, the replica gets promoted to primary and is able to process write requests.

This is how many modern databases do it, one example is AWS Aurora RDS (other??). It is useful because you save money by re-using the standby for scaling too. 




