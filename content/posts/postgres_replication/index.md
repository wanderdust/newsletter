---
title: 'Postgres Replication'
date: '2025-05-16T13:14:57+01:00'
draft: true 
summary: ''
tags: ['postgres']
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---


(Add an intro here)

# Leader-Follower replication strategy

A replica consists of a full copy of the database. There are two types: leaders and followers.

The leader or primary replica is used for writing operations to the database. All write operations need to go through the writer replica.

The follower or reader replicas can only be used for reading the data. Whenever the data is written to the primary replica, it also sends the data changes to the followers.

In Postgres, by default, there is only one leader but there can be more than one follower. When a write operation comes through, it is redirected to the writer, which then updates the reader replicas. Read operations can go to any replica, including the primary.

(Diagram here)

Each replica runs on its own compute instance, which means it can be useful for load balancing if we have a high load of read operations. On the other hand, writes must always go through the leader replica. Since postgres leverages vertical scaling, a high volume of writes can lead to bottlenecks in the primary replica.

(Diagram here)

# Updating the replicas

An important aspect of a replicated system is whether the replication process happens synchronously or asynchronously. 

With synchronous replication, when the leader is updated with a write operation, the transaction is not marked as complete until all the replicas have acknowledged the update. The main advantage is that all replicas will always be synced with up-to-date data. Multiple users, querying different replicas will always get the same results. The downside is that write operations will be slower, since we need to wait until all replicas have acknowledged the update. Communication between replicas goes through the network, which means that if we have networking issues the write operation can be slow. In the worst case, if one of the reader replicas is down, we will need to get until is reboots, which could take a long time.

Slow writes will block further writes, which can cause issues if we deal with a high volume of write operations.

(diagram)

Asynchronous replication does not wait for the replicas to acknoweledge the updates. As soon as the update happens in the primary replica, it returns a succesful answer to the client. The replicas are then updated synchronously. The main advantage of this approach is that the primary does not have to wait, meaning that writes are a lot faster. This can be required for transactional systems with a high volume of writes. The main dowsnside is that users querying the same data, could potentially be getting outdated results. For example, if a user queries the primary and another user queries the follower replica, the second user might be looking at outdadet results.

(diagram)

Long story short, asynchronous communication is used when synchronous would be too slow. Postgres supports both types of replication strategies, using asynchronous by default.

# Read After Write Consistency

What happens in the scenario where one user writes some data, and then immediately tries to read that data? If the read operation happens on a reader replica that has not yet been updated, the user would not see the update leading to confusion.

(diagram)

There are different ways to solve for this problem, one of them using synchronous updates.

Another solution could be to always read from the leader replica where this situation can become an issue. For example, in a web application, the user profile and settings are only read by one user, so any updates to these pages should be reflected immediately. In this case it would make sense send all read operations of the user profile to the the leader replica. This can be a good solution if we do it for only a subset of our read operations, but if we find ourselves reading from the leader replica too much, we lose the advantage of having follower replicas.


# Replication Logs
Replication is the process of replicating the data from the leader replica into the followers. Replication happens by writing the changes to a log file and sending it to the replicas to implement those same changes. Any time a write operation occurs (INSERT, UPDATE, DELETE), the underlying data changes are logged. The logs are then pushed to the replicas to apply. As you can see, we don’t record the SQL statements that get executed, but rather the changes at the disk (binary) level.

```bash
Block 0xA1B2C3 changed from 0xXYZ to 0x123
```

If any of the replicas goes down, it can look at the logs, and replay all the changes from the last log it recorded to become up to date with the leader.

# Handling Failover

One of the main advantages of replicated systems is the ability to handle situations where one or more of the replicas go down, and being able to still serve requests to the user from the remaining replicas. 

This is also known as availability, which means that if part of the system goes down, you are still capable of serving data to the user. Replicated systems also ensure there is no data loss when some of the replicas go down.

If you remember from the previous section, all the writes in postgres have to go through the primary replica, which creates a single point of failure for write operations. If the primary goes down, we will no longer be able to serve write requests. Users will only be able to run read operations from the read only replicas.

There are different ways to approach this problem. Postgres does not provide the functionality to identify and handle failures on the leader. So the default behaviour if the leader fails would be that users are unable to run write operations until the leader is back online. Users will still be able to run read operations from the follower replicas.

A possible approach to handle such sutiuations is to have a standby server that can take over the leader duties when it goes down. For example, one of the follower replicas could be promoted to a leader when the current leader fails. However, this adds additional complexity to our system. If the primary server fails and the standby server becomes the new leader, and then the old leader restarts, you must have a mechanism for informing the old leader that it is no longer in charge. This is necessary to avoid situations where both systems think they are the leader, which will lead to confusion and ultimately data loss.

Postgres does not provide out of the box functionality to identify a failure on the leader and deal with it, for this we’d need to use a third party tool.


# Multi Leader Replication

There is another option to still be able to serve write operations even when the leader goes down. We can use a multi-leader replication approach, although this is also not available by default.

In the multi-leader approach, we have multiple replicas that can handle writes instead of just a single one. This approach removes the single point of failure of having a single leader replica, so if one goes down, you can still serve write requests without any downtime (High Availability). It allows you to have your database distributed across different regions, to ensure it will still work even in the case of an outage.

(diagram)

The downside of this approach is the added complexity of having two or more leader replicas. In this situation, when a user runs a write operation, we don’t only need to update the followers, but also the other leaders.

We can encounter situations where two users write on the same data, at the same time on different leader replicas, where the replicas have not had time to update each other with update. This would create an inconsistency because both transactions have written on the same data, which would create a conflict for the leader when trying to update the other leader. One solution could be to only keep the transaction that happens first, and cancel the other one. However, it is not a good solution to acknowledge a transaction to the user, and then cancelling it. This would be a bad interface that would lead to confusion and data inconsistencies. 

(diagram)

Another solution, would be to wait until the other leaders have recieved the update before we can write to it, essentially synchronously updating the other leaders. The problem is that networking speed becomes your bottleneck here. Also, if one of the primaries goes down, you need to have a method to skip the sync so that it doesn’t get stuck waiting for the other primaries to come back up, otherwise you’d be losing the advantages of having multiple primaries.

---
## My Newsletter

I send out an email every so often about cool stuff I'm building or working on.

{{< subscribe >}}
