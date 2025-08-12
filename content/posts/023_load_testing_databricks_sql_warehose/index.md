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

I needed to fetch data from the data warehouse to integrate in dowsnstream applications via an API. The API would recieve dozens up to hundreds of requests per second.

I run a load test to understand the performance and cost implications of hitting Databricks diretcly via the SQL warehouse.

## Methodology

Steps

1. Create a baseline

2. Load test for each of the proposed configurations 

3. Compare to baseline and to other load tests

4. Select most cost/efficient solution

**Considerations**

Databricks recommends that for running multiple queries at one time, we should increase number of clusters

> If you are running multiple queries at a time [serverless], add more clusters for autoscaling. [link](https://docs.databricks.com/aws/en/compute/sql-warehouse/warehouse-behavior#sizing-a-serverless-sql-warehouse)

Autoscaling only kicks in after queries have been added to the queue. We want to find the right balance between min clusters available vs autoscaling clusters.

> If the queue is not decreasing quickly enough, autoscaling kicks in to rapidly procure more compute. [link](https://docs.databricks.com/aws/en/compute/sql-warehouse/warehouse-behavior#serverless-autoscaling-and-query-queuing)


## The queries

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

## Databricks Load Testing Results

### Baseline Test
*Optimal query run time when load is low*

#### Configuration
- **Users**: 2 users
- **Databricks**: Serverless, Small cluster size, Scaling min 1 to max 2
- **Cost**: $201/day ($6,048/month)

#### Results
*2 users ~ 1.5 requests/s*

| Query Name | p50 (ms) | p95 (ms) | p99 (ms) | max (ms) | avg (ms) |
|------------|----------|----------|----------|----------|----------|
| Query A | 1,400 | 1,900 | 2,300 | 2,730 | 1,489 |
| Query B | 500 | 650 | 1,100 | 1,489 | 526 |


---

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
- Queue grows faster than queries can execute, which has a big effect on p95 and p99
- Slower queries experience a greater performance degradation under load compared to faster queries, which are less impacted

---

### Load Test #1
*Increasing the number of max scaling clusters to 10*

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
- New clusters are added relatively quickly during autoscaling
- During autoscaling, response time (P95) may spike briefly, but stabilizes once the new clusters are active

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

## Results

