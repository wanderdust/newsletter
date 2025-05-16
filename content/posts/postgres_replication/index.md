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

# Leader-Follower replication strategy

A replica consists of a full copy of the database. There are two types of replicas, we have leaders and followers.

The leader or primary replica is used for writing operations to the database. Any write operation needs to go through the writer replica. It can also be used for reading. 

The follower or reader replicas can only be used for reading the data. Whenever the data is written to the primary replica, it also sends the data changes to the writers.

In Postgres, by default, there is only one leader but there can be more than one followers. When a write operation comes through it must go through the writer, which then updates the reader replicas. Read operations can go to any replica.

(Diagram here)

Each replica runs on its own compute instance, which means it can be useful for load balancing if we have a high load of read and writes. Reads can be spread across all the replicas, however the writes must always go through the writer. Since postgres leverages vertical scaling, a high volume of writes can lead to bottlenecks in the primary replica.

(Diagram here)

# Updating the replicas

An important aspect of a replicated system is whether the replication process happens synchronously or asynchronously. 

With synchronous replication, when the primary is updated, the transaction is not marked as complete until all the replicas have acknowledged the update. The main advantage is that all the users will always get the same data, no matter which replica they are looking at. The downside is that write operations will be slower, since we need to wait until all replicas acknowledge having recieved the update. Communication between replicas goes through the network, which means that if we have networking issues the write operation can be very slow. In the worst case, if one of the reader replicas is down, we will need to get until is reboots, which could take a very long time.

Slow writes will block further writes, which can cause issues if we deal with a high volume of transactions.

(diagram)

Asynchronous replication does not wait for the replicas to acknoweledge the updates. As soon as the update happens in the primary replica, it returns a succesufl answer to the client. The replicas are then updated synchronously. The main advantage of this approach is that the primary does not have to wait, meaning that writes are a lot faster. This can be required for transactional systems with a high volume of writes. The main dowsnside is that users querying the same data, could potentially be getting outdated results. For example, if a user queries the primary and another user queries the follower replica, the second user might be looking at outdadet results.

(diagram)

Asynchronous communication is used when synchronous would be too slow.

# Read After Write Consistency

What happens in the scenario where one user writes some data, and then tries to read that data. If the read operation happens on a reader replica that has not yet been updated, the user would not see the update leading to confusion.

(diagram)

There are different ways to solve for this problem, one of them using synchronous updates. Another solution could be to always read for the primary replica where this situation can become an issue. For example, in a web application, the user profile and settings are only read by one user, so any updates to these pages should be reflected immediately, so in this case it would make sense to read from the primary.

This is fine if we do it for only a subset of our read operations, but if we find ourselves reading from the primary replica too much, we lose the advantange of read only replicas.



# Replication Logs

https://www.postgresql.org/docs/current/wal-intro.html (Write ahead Logs WAL)

Replication happens by writing the changes to a log file and seniding it to the replicas to implement. Any time a write operation occurs (INSERT, UPDATE, DELETE), the data changes (not the satetements themselves) are logged at the binary level. The logs are then pushed to the replicas to apply. As you can see, we don’t record the SQL statements that get executed, but rather the changes at the disk level.

Block 0xA1B2C3 changed from 0xXYZ to 0x123

If any of the replicas goes down, it can look at the logs, and replay all the changes from the last log it recorded to become up to date with the primary.

Handling Failover

If writer fails, there you can’t write until it comes back. You can promote readers to become writers (I think this is not natively supported). Some challenges associated with this such keeping state to let the old primary know it is no longer a primary to avoid data loss.

If reader fails, we still have availability

Bringing replicas up to speed when failover or reboot 

One of the main advantages of replicated systems is the ability to handle situations where one or more of the replicas go down, and being able to still serve requests to the user from the remaining replicas. 

This is also known as availability, which means that if part of the system goes down, you are still capable of serving data to the user. Replicated systems also ensure there is no data loss when some of the replicas go down.

If you remember from the previous section, all the writes in postgres have to go through the primary replica which creates a single point of failure for write operations. If the primary goes down, we will no longer be able to serve write requests. Users will only be able to run read operations from the read only replicas.

There are different ways to approach this problem. Postgres does not provide the functionality to identify and handle failures on the primary. So the default behaviour if the primary fails would be that users are unable to write until the primary is back online, but it will be able to serve read operations from the replicas.

A possible approach to handle such sutiuations is to have a standby server that can take over the primary duties while it goes down. For example, one of the follower replicas could be promoted to a leader when the primary fails. However, this adds additional complexity to our system. If the primary server fails and the standby server becomes the new primary, and then the old primary restarts, you must have a mechanism for informing the old primary that it is no longer the primary. This is necessary to avoid situations where both systems think they are the primary, which will lead to confusion and ultimately data loss.

PostgreSQL does not provide the functionality to identify a failure on the primary and deal with it, for this we’d need to use a third party tool.



# Multi Leader Replication

There is another option to still be able to serve write operations even when the primary goes down. We can use a multi-leader replication approach, although this is not offered in Postgres by default.

In the multi-leader approach, we have multiple replicas that can handle writes, instead of a single one. This approach removes the single point of failure of having a single primary replica, so if one goes down, you can still serve write requests without any downtime (High Availability). It allows you to have your database distributed across different regions, to ensure it will still work even if one of your regions go down.

(diagram)

The downside of this approach is the added complexity of having two or more primary replicas. In this situation, when a user runs a write operation, we don’t only need to update the followers, but also the other primaries need to be updated as well to reflect the new state of the data.

In this situation, we can encounter situations where two users write at the same time to different primary replicas, where the replicas have not had time to update each other with update. In this case it would create an inconsistency which would need to be resolved. One way could be to only run the transaction that happens first, and cancel the other one. However, this is not a good solution, since we may have already acknowledged to the user that the transaction was succesful, so cancelling after that would be confusing and a bad user interface.

(diagram)

Another solution, would be to wait until the other primaries have recieved the update before we can write to it, essentially synchronously updating the other primaries. The problem is that networking speed becomes your bottleneck here. Also, if one of the primaries goes down, you need to have a method to skip the sync so that it doesn’t get stuck waiting for the other primaries to come back up, because you’d be losing the advantages of having multiple primaries.

Some tools that offer this are: …

---
## My Newsletter

I send out an email every so often about cool stuff I'm building or working on.

{{< subscribe >}}
