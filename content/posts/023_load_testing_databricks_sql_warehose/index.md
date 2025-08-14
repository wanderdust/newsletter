---
title: '023_load_testing_databricks_sql_warehose'
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

We needed to fetch data from the data warehouse to integrate in dowsnstream applications via an API. The API would recieve dozens up to hundreds of requests per second.

Data Warehouses are not designed to serve operational use cases such as this one. However this is no reason not to run this experiment to understand to what point this is true. It may be the case that for smaller workloads the data warehouse can serve these use cases, minimasing operational overhead of having to setup a downstream operational store such as Postgres to serve this data.

After all, Databricks separates storage from compute, so we can hit the warehouse as hard as we want without worrying about bringing the Warehouse down right?

In this blog post I run a load test into Databricks SQL Warehouse to better understand performance and cost under different levels of load.

Enjoy!

## Methodology

Steps

1. Create a baseline. Execute the queries under a low load.

2. Run load test for each of the proposed configurations.

3. Compare baseline to other Load tests

4. Select most cost/efficient solution

**Considerations**

Databricks recommends that for running multiple queries at one time, we should increase number of clusters

> If you are running multiple queries at a time [serverless], add more clusters for autoscaling. [link](https://docs.databricks.com/aws/en/compute/sql-warehouse/warehouse-behavior#sizing-a-serverless-sql-warehouse)

Autoscaling only kicks in after queries have been added to the queue. We want to find the right balance between min clusters available vs autoscaling clusters.

> If the queue is not decreasing quickly enough, autoscaling kicks in to rapidly procure more compute. [link](https://docs.databricks.com/aws/en/compute/sql-warehouse/warehouse-behavior#serverless-autoscaling-and-query-queuing)

## Choosing the compute

For this use case we decided to go for serverless compute because it was the only option that could scale fast enough if there is a spike of requests. The idea is test whether we can put the data warehouse behind an API layer to directly handle operational requests.

## The queries
THese are the queries used for this test. Query B is a simpler query with a GROUP BY clause. Query A is a bit more resource intensive with JOINs.


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
        AND time_period = 'lifetime'
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

The load tests are executed using the Locust framework. We use different load configurations for each test.

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


![](./load_test_0.png)

#### Key Observations
- The databricks queue grows faster than queries can execute, which has a big effect on p95 and p99
- Slower queries experience a greater performance degradation under load compared to faster queries, which are less impacted

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


![](./load_test_1.png)


#### Key Observations
- When clusters are exhausted, the queue grows linearly but at a slower rate, eventually stabilising around 70
- New clusters are added relatively quickly during autoscaling (within a few minutes)
- During autoscaling, response time (P95) may spike briefly, but stabilizes once the new clusters are active
- This is a very expensive configuration.
- P99 is really bad for query A, and not too bad for query B. It implies that the slower query suffers more when the load is high.
- THe max value, indicating the worst query execution times are shockingly bad for both queries.


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


![](./load_test_2.png)

#### Key Observations
- Autoscaling is relatively fast. 1 to 10 cluster within 4 minutes
- P95 is a bit inconsistent (spikes) while autoscaling is happening, then it stabilises
- Queries queue at a linear rate faster than they can execute after ~ 180 users
- P99 is really bad for query A, and not too bad for query B. It implies that the slower query suffers more when the load is high.
- THe max value, indicating the worst query execution times are shockingly bad for both queries.

## Discussion

### Cost vs. Performance Scaling

Running 10 clusters in serverless mode is prohibitively expensive while only handling about 35 requests per second. More concerning is that the relationship between resources and performance shows diminishing returns: a 5x increase in cluster capacity (from 2 to 10) only yielded a ~4x increase in throughput (from 9 to 35 req/s). This makes each additional request served progressively more expensive as you scale.

For most API workloads, this cost structure simply doesn't make sense compared to alternatives like dedicated operational databases.

Databricks offers managed solutions such as LakeBase or Online tables so you don't have to manage reverse ETL pipelines going from the warehouse to the operational database.

### Query Complexity Determines Viability

The tests showed a disparity in how different query types perform under load. Simple queries like Query B maintained reasonable performance even as concurrency increased, with p50 latency remaining stable around 480ms across all tests. Complex queries like Query A, however, degraded non-linearly. At baseline the performance gap for p99 was roughly 2x worse, but under load this worsened to 10-21x in p99 times.

This suggests that data warehouses might actually be viable for certain simple operational queries if cost isn't the primary concern. It becomes unsuitable for more complex operations when serving for API use cases. The complexity of your query workload becomes the determining factor in whether this architecture could work.

## Summary

We came into this blog post knowing this was not going to work out. If everyone says OLAP databeses are not good for OLTP use cases it is probably for a reason. However, I hope you found it interesting getting a bit more of an insight into how the databricks SQL warehouse behaves under such load.

It never hurts to try things for yourself, even if they are bound to fail. You may learn something on the way.
