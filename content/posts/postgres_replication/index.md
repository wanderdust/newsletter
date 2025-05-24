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

Replication refers to having copies of your data, so if your database goes down, you still have a backup to prevent data loss. In this post I give an overview of how Postgres handles replication. One thing to note is that a lot of the strategies mentioned in this blog are not only applicable to postgres, in fact, they are common techniques used across many database systems.

# Leader-Follower replication strategy

This is the most common strategy for replication across databases, and the one used by Postgres as well. In the Leader-Follower strategy there are two types of replicas: leaders and followers.

The leader replica is in charge of the write operations to the database. All write operations can only go through the leader replica.

The follower replicas keep an up-to-date copy of the data in the leader. Whenever any data is written to the leader, the updates are propagated to the followers so they can stay up to date. Follower replicas can only do read operations.

In Postgres, there is one leader but we can have more than one follower. When a write operation comes through, it is goes to the leader, which then updates the follower replicas. Read operations can go to any replica, including the leader.

(Diagram here)

This strategy brings several benefits. To begin with, if one of our replicas goes down, we still have a copy of the data in the remaning replicas, which means there is no data loss. Another benefit of having replicas in different nodes is that we can load balance the read operations across the replicas.

(Diagram here)

On the other hand, if the leader happens to go down, we will be unable to handle write operations since the followers can only do reads. We'll discuss strategies on how to handle failover in the next section.

# Handling Failover

One of the main advantages of replicated systems is the ability to serve requests, even when one or more of the replicas go down.

This is also known as availability, which means that if part of the system goes down, the database is still capable of serving data to the user.

If you remember from the previous section, all the writes have to go through the leader replica, which creates a single point of failure for write operations. If the leader goes down, we will no longer be able to serve write requests. Users will only be able to run read operations from the follower replicas. Which means write operations won't be availabe until the leader comes back up.

A possible approach to handle such situations is to promote a follower to become the leader when the current leader fails. This is how systems like dynamoDB or Kafka handle these situations, but it is not part of Postgres by default. There are third party tools that can be used to implement this functionality, but it adds an additional layer of complexity to your system. For example, if the leader fails and a follower becomes the new leader, and then the old leader comes back to life, we must have a mechanism for informing the old leader that it is no longer in charge. This is necessary to avoid situations where both systems think they are the leader, which will lead to confusion and ultimately data loss.

# Sync vs Async replication

An important aspect of a replicated system is whether the replication process happens synchronously or asynchronously. 

With synchronous replication, when the leader is updated with a write operation, the transaction is not marked as complete until all the replicas have been updated as well.

The main advantage of synchronous replication is that all replicas will always be synced with up-to-date data. Multiple users, querying different replicas will always get the same results.

The downside is that write operations will be slower, since we need to wait until all replicas have been updated. Communication between replicas goes through the network, which means that if we have networking issues the write operation can be slow. In the worst case, if one of the reader replicas is down, we will need to get until is reboots, which could take a long time.

Slow writes will block further writes, which can cause issues if we deal with a high volume of write operations.

(diagram)

Asynchronous replication does not wait for the replicas to acknoweledge the updates. As soon as the update happens in the leader replica, it returns a succesful answer to the client. The replicas are then updated asynchronously.

The main advantage of this approach is that the leader does not have to wait, meaning that writes are a lot faster. This is a common requirement for transactional systems with a high volume of writes.

The main dowsnside is that users querying the same data, could potentially be getting outdated results. For example, if a user writes to the leader and another user queries a follower replica, the second user might be looking at outdated results.

(diagram)

Long story short, asynchronous replication is used when synchronous would be too slow. Postgres supports both types of replication strategies, using asynchronous by default.

# Read After Write Consistency

What happens in the scenario where one user writes some data, and then immediately after tries to read that data from a follower replica?

If we are using asynchronous replication, there could be a situation where the user reads data from the follower before it's had the chance to update. In this case they would see outdated data. In some situations, this can lead to confusion.

(diagram)

For example, in a social media site, when a user updates their profile image, it should immediately reflect that change to the user, otherwise they may think the change has not taken effect. In this case, what we could do is to always read user profile information from the leader replica to ensure the user is always seeing the latest changes.

Reading from the leader can be a good solution for edge cases like this one. But if we find ourselves reading from the leader for too much, we could end up putting too much strain on that single replica, losing the benefit of load balancing across the followers.

(diagram)

In other situations, users seeing outdated data might not be a problem at all. In the same example as before, this user's friends will not care if for some time they see an outdated profile image for that user.

# Updating the replicas

So far we've seen different strategies to work with our replicated Postgres database. But we still have no idea how the replication process happens.

When the leader recieves a write operation, the operation is first _logged_ into a log or file. Only after it has been logged, the database actually updates the data and acknoweldges the operation to the user. The log contains a sequential list of operations that the followers can use to keep their data up-to-date. 

The reason for logging the operation before updating the actual data is so that the transaction gets recorded first in case of the replica (leader or follower) goes down. That way if there is a failover and the database needs to restart, it can simply look at the logs and pick up from where it left off.

There are different ways to write the logs. One way is to log the actual SQL statements, and then run those statements in order in the replicas. The main advantage of this, is that the logs are very intuitive and easy to read. The problem is when we have non determinstic operations, we have no way of consistently replicating it across the replicas.

For example, this statement wild insert different results each time it gets executed.
```sql
INSERT INTO table (col1)
VALUES (FLOOR(RAND() * 100));
```

Another method is to log the data changes rather than the statements themselves. For example, we run the SQL statement in memory first and observe how the data will change, and then we record this change to the log. Only after the log has been written we update the data itself. Using this method we can replicate the data consistently even for non deterministic operations because the statement is only ran once, and then the data changes are applied equally across replicas. In this case the log might look like this:

```bash
Block 0xA1B2C3 changed from 0xXYZ to 0x123
```

If any of the replicas goes down, as it restarts, it can look at the logs and replay all the changes from where it left off to become up to date with the leader.

# Multi Leader Replication

There is another option to still be able to serve write operations even when the leader goes down. We can use a multi-leader replication approach, although this is also not available by default in Postgres.

In the multi-leader approach, we have multiple replicas that can handle writes instead of just a single one. This approach removes the single point of failure of having a single leader replica, so if one goes down, you can still serve write requests without any downtime (High Availability). It allows you to have your database distributed across different regions, to ensure it will still work even in the case of an outage.

(diagram)

The downside of this approach is the added complexity of having two or more leader replicas. In this situation, when a user runs a write operation, we don’t only need to update the followers, but also the other leaders.

We can encounter situations where two users write on the same data, at the same time on different leader replicas, where the replicas have not had time to update each other with update. This would create an inconsistency because both transactions have written on the same data, which would create a conflict for the leader when trying to update the other leader. One solution could be to only keep the transaction that happens first, and cancel the other one. However, it is not a good solution to acknowledge a transaction to the user, and then cancelling it. This would be a bad interface that would lead to confusion and data inconsistencies. 

(diagram)

Another solution, would be to wait until the other leaders have recieved the update before we can write to it, essentially synchronously updating the other leaders. The problem is that networking speed becomes your bottleneck here. Also, if one of the primaries goes down, you need to have a method to skip the sync so that it doesn’t get stuck waiting for the other primaries to come back up, otherwise you’d be losing the advantages of having multiple primaries.

# Conclusion

???

---
## My Newsletter

I send out an email every so often about cool stuff I'm building or working on.

{{< subscribe >}}
