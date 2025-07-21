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

When working with distributed systems you can encounter terminology such as "replicas" or "standby" intstances. Although it can be easy to understand the  difference between them, it can also be easy to confuse them.

## Replicas

Replicas are exact copies of the database, which are used for Horizontal Scaling. 

In a database that uses replication, there's normally a single writer instance, which accepts read and write operations, and optionally one or more reader instances that are read only.

If your database recieves a large volume of read operations, your single writer instance might get overwhelmed with requests. You can alleviate this situation by creating replicas and load balance the requests across instances.

Your replicas can either recieve updates from the primary synchronously or asynchronouly, depending on the application needs.

## Standby instances

A standby instance is an exact clone of your writer instance that gets used in case your current primary fails.  

It is very similar to a replica, except the standby is a writer instance that does not recieve any requests. In case of failover, the standby steps up and starts handling requests. This helps to avoid downtime when your writer instance goes down.

It is a good idea that updates to the standby instance are not async, so there's no data loss if the current primary goes down. The implications of synchronous updates are that writes operations won't be committed (complete) until the update has been recieved by the standby, which adds additional latency to write requests.

Standby instances are used to ensure High Availability in your database or applications. It is normally a good idea to have your standby instance in a different region or data center, to survive regional or data center outages.

## Using them side by side

You can use both features side by side. For example your primary instance is setup to have a standby in a different region, so we can minimise downtime in case of failure.

We can also have replicas to allow for Horizontal Scaling in case your application recieves a large volume or READ operations. Your replicas can be deployed in the same region or data center, or distrubuted across data centers.

If you need low latency replication between instances, it would make sense to have your replicas in the same region. On the other hand, if you have users in different regions, you may want to deploy replicas in different regions to reduce the latency of their requests.

These are the tradeoffs you make when designing your applications.

[Diagram]


## Using your Standby as a read replica

Some database systems are able to combine both Standby and Replicas into a single instance. For example, the standby instance can also act as a read-only replica. If the primary goes down, the replica gets promoted to primary and is able to process write requests.

This is how many modern databases do it, one example is AWS Aurora RDS. It is useful because you save money by re-using the standby for scaling too. Otherwise you still have to pay for the standby instance just for sitting there.




