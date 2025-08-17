---
title: 'Can we use the Databricks SQL Warehouse as an OLAP database?'
date: '2025-08-12T09:42:44+01:00'
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

My team needed to find a way to serve a table from Databricks via an API to integrate in a user facing application. This API was expected to recieve up to 100 requests per second of read operations.

Since the table was already in Databricks, the simplest option would be to create an API and hit the table directly in Databricks.

This investigation explores the feasability of using the SQL warehouse to serve this use case. It shows the performance and cost implications of running a high volume of requests for different query types in the SQL Warehouse.

Enjoy!

## Methodology

This is the methodology used in this investigation

1. Create a baseline. Execute the queries under a low load.

2. Run load test for each of the proposed configurations.

3. Compare baseline to Load tests


## Preparation

For this use case we decided to go for serverless compute because it was the only option that can scale fast enough if there is a spike of requests.

Databricks recommends that for running multiple queries at one time, we should increase number of clusters

> *If you are running multiple queries at a time [serverless], add more clusters for autoscaling. [link](https://docs.databricks.com/aws/en/compute/sql-warehouse/warehouse-behavior#sizing-a-serverless-sql-warehouse)*

Autoscaling only kicks in after queries have been added to the queue. We want to find the right balance between min clusters available vs autoscaling clusters.

> *If the queue is not decreasing quickly enough, autoscaling kicks in to rapidly procure more compute. [link](https://docs.databricks.com/aws/en/compute/sql-warehouse/warehouse-behavior#serverless-autoscaling-and-query-queuing)*


## The queries
These are the queries used for this test. Query B is a simpler query with a GROUP BY clause. Query A is a bit more resource intensive with JOINs and window operations.

{{< details >}}

Query A
```sql
WITH ranked_events AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY created_date DESC) 
    FROM public.analytics.activity_events
    WHERE start_time BETWEEN '2024-11-08' AND '2024-11-10'
        AND user_id = ?
),
deduped_events AS (
    SELECT * FROM ranked_events WHERE row_num = 1
),
formatted_data AS (
    SELECT 
        start_events.reference_id,
        start_events.session_token,
        start_events.product_id,
        end_events.total_amount,
        end_events.net_result
    FROM (
        SELECT * FROM deduped_events WHERE event_type = 'STARTED'
    ) start_events
    LEFT JOIN (
        SELECT * FROM deduped_events WHERE event_type = 'COMPLETED'
    ) end_events
    ON start_events.reference_id = end_events.reference_id
)
SELECT *
FROM formatted_data
ORDER BY reference_id
LIMIT 100 OFFSET 200;
```


Query B 
```sql
WITH aggregated_data AS (
    SELECT
        product_type_id,
        SUM(event_count) AS event_count,
        SUM(total_value) AS total_value,
        SUM(net_amount) AS net_amount,
        SUM(projected_amount) AS projected_amount,
        SUM(tier_a_value) AS tier_a_value,
        SUM(tier_b_value) AS tier_b_value,
        SUM(tier_c_value) AS tier_c_value
    FROM public.analytics.customer_activity_summary
    WHERE
        customer_id = ?
        AND time_period = 'year'
    GROUP BY GROUPING SETS ( (), (product_type_id) )
)
SELECT
    product_type_id,
    event_count,
    total_value,
    net_amount,
    projected_amount,
    tier_a_value,
    tier_b_value,
    tier_c_value
FROM aggregated_data
LIMIT 5000;
```
{{< /details >}}

The load tests are executed using the Locust framework. To ensure realistic results, the [caching](https://docs.databricks.com/aws/en/sql/language-manual/parameters/use_cached_result) is disabled. On top of that, the query parameters are randomised to prevent from submitting the same query multiple times as much as possible.

## Baseline

*The baseline tests the optimal query run time when load is low*

#### Configuration
- **Users**: 2 concurrent users
- **Databricks**: Serverless, Small cluster size, Scaling min 1 to max 2
- **Cost**: $201/day ($6,048/month)

#### Results
*2 users ~ 1.5 requests/s*

| Query Name | p50 (ms) | p95 (ms) | p99 (ms) | max (ms) | avg (ms) |
|------------|----------|----------|----------|----------|----------|
| Query A | 1,400 | 1,900 | 2,300 | 2,730 | 1,489 |
| Query B | 500 | 650 | 1,100 | 1,489 | 526 |

## Load Testing Results

Feel free to skip this section and move directly to the results.

### Load Test #0
*Same configuration as baseline but loading it with 150 concurrent users*

#### Configuration
- **Users**: 150 users
- **Databricks**: Serverless, Small cluster size, Scaling min 1 to max 2
- **Cost**: $201/day ($6,048/month)

#### Results
*150 users ~ 9 requests/s*

| Query Name | p50 (ms) | p95 (ms) | p99 (ms) | max (ms) | avg (ms) |
|------------|----------|----------|----------|----------|----------|
| Query A | 4,300 | 20,000 | 164,000 | 192,000 | 9,943 |
| Query B | 530 | 1,800 | 3,500 | 7,774 | 684 |

{{< details >}}

Databricks SQL warehouse screenshot showing details about the running queries, queued queries and running clusters.

![](./load_test_0.png)

{{< /details >}}


#### Observations
- The databricks queue grows faster than queries can execute, which has a big effect on p95 and p99
- The slower query (Query A) experiences a greater performance degradation under load compared to faster queries, which are less impacted

---

### Load Test #1
*Same configuration as baseline but loading it with 150 concurrent users and increasing the number of max scaling clusters to 10*

#### Configuration
- **Users**: 150 users
- **Databricks**: Serverless, Small cluster size, Scaling min 1 to max 10
- **Cost**: $2,000/day ($60,048/month for 10 clusters running 24/7)

#### Results
*150 users ~ 35 requests/s*

| Query Name | p50 (ms) | p95 (ms) | p99 (ms) | max (ms) | avg (ms) |
|------------|----------|----------|----------|----------|----------|
| Query A | 3,600 | 6,500 | 34,000 | 394,362 | 5,819 |
| Query B | 480 | 650 | 1,100 | 16,348 | 524 |


{{< details >}}
Databricks SQL warehouse screenshot showing details about the running queries, queued queries and running clusters.

![](./load_test_1.png)
{{< /details >}}

#### Key Observations
- When clusters are at the concurrency limit, the queue size grows linearly, eventually stabilising at around 70 queries.
- Autoscaling kicks in within minutes
- During autoscaling, response time (P95) may spike briefly, but stabilizes once the new clusters are active
- P99 is really bad for query A, and not too bad for query B. It implies that the slower query suffers more when the load is high.
- The max value is shockingly bad. This suggest that some of the queued queries remain in the queue for very long times. It seems like databrick's queuing system favours faster queries and punishes slower queries with longer waiting times.


---

### Load Test #2
*Same as load test #1 but adding more users*

#### Configuration
- **Users**: 300 users
- **Databricks**: Serverless, Small cluster size, Scaling min 1 to max 10
- **Cost**: $2,000/day ($60,048/month for 10 clusters running 24/7)

#### Results
*300 users ~ 40 requests/s*

| Query Name | p50 (ms) | p95 (ms) | p99 (ms) | max (ms) | avg (ms) |
|------------|----------|----------|----------|----------|----------|
| Query A | 4,000 | 7,500 | 85,000 | 240,503 | 6,171 |
| Query B | 480 | 760 | 2,300 | 18,760 | 567 |



{{< details >}}
Databricks SQL warehouse screenshot showing details about the running queries, queued queries and running clusters. There are two spikes because I ran the test, then stopped and then ran it again.

![](./load_test_2.png)

{{< /details >}}

#### Key Observations
- Autoscaling is relatively fast. 1 to 10 cluster within 4 minutes  
- P95 is a bit inconsistent (spikes) while autoscaling is happening, then it stabilises
- Queries queue at a linear rate faster than they can execute after ~ 180 users
- P99 is really bad for query A, and not too bad for query B. It implies that the slower query suffers more when the load is high.
- The max value, indicating the worst query execution times are shockingly bad for both queries.


## Results

### The Queue

If you took a look at the SQL warehouse screenshots for each of the tests you will have noticed that they all ended up with a very large queue of queries. This is not good, because it means that in neither of the tests the resources were enough to handle the load, which caused the queries to be queued, and in some cases for very long times (as we will see in the next section).

Let's borrow the screenshot from load test one.

![](./load_test_1.png)

If we take a look at the peak load time when all 10 clusters were running, the peak count of concurrently running queries was 86, and the queue was 77. Almost half the queries were queued, which means that you would expect a delay on queries almost half of the times under that load.


### Query Execution times
Lets take a look at the plotted results. I will take a look at p50 instead of the average because the average will be heavily skewed to those really high max values.

I will also be focusing on the p99, which will give the worst case execution times excluding the outliers. In other words, if we execute the query 100 times, 99 times the execution times will be equal or below the p99 value.

This gives a good indication of what execution times users would expect if we were to implement this in an API.

If we plot the results for each query side by side using the same y axsis, we can barely see the bars for query B. Query A execution times are a lot higher for all experments as compared to query B. But this is expected, because query A was already 2x slower in the baseline, so it makes sense this carries over to the load tests.

![](./p99_results.png)

What I'm interested on finding out is the relative performance for each query. Do both queries degrade the same? To do this I can plot the degradation performance for each query as compared to their baseline.

![](./plot_slowdown_results.png)

So now we can clearly see that query A has a much worse p99 than query B in all load tests. Query A gets 72x worse p99 for load test one as compared to 3x  worse for query B. 

For load test two, query A performs 37x times worse on the p99, as compared to 2.1x worse for query B. This indicates that the slower the query, the worse it scales as we add more load.

I'm going to make an assupmtion here, because I don't have enough data to verify this. There could be two reasons for the degradation to be much worse on the more on the slower queries.

One reason could be that the faster queries rarely end up in the [queue](https://docs.databricks.com/aws/en/compute/sql-warehouse/warehouse-behavior#serverless-autoscaling) and execute straight away.

Reason number two could be that the queue prioritises the faster queries because it is easier to find free available capacity in the cluster for queries that are less resource intensive. The queue does not work in a FIFO format but based on available capacity in the cluster and what query in the queue best fits at the time.

### Cost

Assuming we have all of our clusters running capacity 24/7, running two small serverless clusters [costs](https://www.databricks.com/product/pricing/databricks-sql) $201 per day or $6,048 per month.

Running 10 small serverless clusters [costs](https://www.databricks.com/product/pricing/databricks-sql) $2,000 per day or $60,048 per month.

Of course, it may be the case where you have a small number of clusters running most of the time, and you only need to use the full capacity occassionally. But this should give you a rough idea of what you could be spending.

## Discussion

### Cost vs. Performance Scaling

Running 10 clusters in serverless mode is prohibitively expensive while only handling about 35 requests per second. The relationship between resources and performance shows diminishing returns: a 5x increase in cluster capacity (from 2 to 10) only returned a ~4x increase in throughput (from 9 to 35 req/s). This makes each additional request served progressively more expensive as you scale.

For most API workloads, this cost structure doesn't make sense compared to alternatives like dedicated operational databases, such as PostgreSQL.

Databricks offers managed solutions such as [LakeBase](https://www.databricks.com/product/lakebase) which is a managed Postgres database where you can easily sync data from the warehouse.

### Query Complexity Determines Viability

Not all queries behave the same under load. The tests clearly showed this:
- Simple queries (like Query B) stayed fast even as more users were added. Median latency (p50) barely changed, around 480 ms, across all tests.
- Complex queries (like Query A) slowed down dramatically as load increased. The slowest 1% of queries (p99) went from being twice as slow at baseline to 10–20 times slower under heavy load.

For operational use cases, simple queries might work directly against the data warehouse if you don’t mind the cost. But complex queries quickly become a bottleneck, making the warehouse unsuitable for high-volume, low-latency API workloads.

## Summary

Databricks is an OLAP data lake, where tables is stored in columnar format, which optimised for analytical use cases. The SQL data warehouse is not opitimised for use cases that require a high volume of requests with very low latency. 

This investigation has showed that connecting to Databricks Directily via the SQL Warehouse is not scalable solution to serve a high volume of requests when integrating with downstream applications such as user facing applications.

For this we are better off using an OLTP database like Postgres where we can leverage indexes to make queries really fast and it can scale to thousands of requests per second. It will also be cheaper to run.

I hope you have found this investigation interesting, see you next time.
