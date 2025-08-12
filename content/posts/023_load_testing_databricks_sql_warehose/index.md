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

query-1 (v3-crui)
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

query2 (v1-round)
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

## The baseline
Databricks Config:
- Type: Serverless
- Cluster Size: Small
- Scaling: min 1, max 2
- Cost: $201/day or $6,048/month

Load: 
- 2 concurrent requests per second

Results

| Query Name | p50 (ms) | p95 (ms) | p99 (ms) | max (ms) | avg |
|------------|----------|----------|----------|----------|-----|
| v1-round | 1,400 | 1,900 | 2,300 | 2,730 | 1,489 |
| v3-crui-statsbyentity | 500 | 650 | 1,100 | 1,489 | 526 |


