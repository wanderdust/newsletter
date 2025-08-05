---
title: '020_real_time_data_api_with_cdc'
date: '2025-08-04T20:45:17+01:00'
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
Goal: End to end streaming - from data gathering with Kafka to Serving the data via APIs.
Target Audience: Data Engineers

Outline
- Sending transaction Data to Kafka via SDK (dummy API)
- Streaming transformations with Delta Tables - combine 2 tables - Create an example where we have inserts
- Reverse ETL into PostgreSQL
- API

---
Intro here

## What are our requirements?

Before we start implementing, we need to understand our requirements:
- We collect transaction metrics from the front end APIs
- We need to make this data available within 1 minute to customer support teams to be able to see this info in real time to handle support

## Design the pipeline

![](./diagram.png)

To meet these requirements, we'll use Delta's Change Data Feed to track row-level changes in our transaction data. This gives us several advantages:

1. We only move the data that has changed, not the entire dataset.
2. We capture all operations: inserts, updates, and deletes.
3. We can run the pipeline at any frequency, processing changes in near real-time.

The pipeline will have three main components:
- A streaming job that reads changes from Delta and writes to PostgreSQL
- A properly indexed PostgreSQL database optimized for fast reads
- A FastAPI service that provides a clean interface to the data

## Data Collection (kafka)


## Data Transformations (Delta)


## Reverse ETL (spark)

Now to the juicy bit. Let's start with enabling Change Data Feed in our source Delta table:

```sql
ALTER TABLE
  transactions
SET TBLPROPERTIES
  (delta.enableChangeDataFeed = true)
```

Once enabled, we can view changes using:

```sql
SELECT * FROM table_changes('transactions', 1);
```

This returns all row changes since version 1, with additional metadata columns:
- `_change_type`: The operation type (insert, update_preimage, update_postimage, delete)
- `_commit_version`: The table version when the change happened
- `_commit_timestamp`: When the change was committed

Here's what a simple output might look like:

![](./cdc_example.png)

Next, we need to write a function that processes these changes and handles deduplication. When running CDC jobs, the same row might appear multiple times if it was updated several times:

```python
def get_latest_cdc_record(df, primary_key):
  window_spec = Window.partitionBy(primary_key).orderBy(
    col("_commit_version").desc()
  )
  
  df_dedup = (
    df.filter("_change_type != 'update_preimage'")
      .withColumn("row_num", row_number().over(window_spec))
      .filter(col("row_num") == 1)
      .drop("row_num")
  )
  return df_dedup
```

This function:
1. Groups records by the primary key
2. Orders them by commit version (descending)
3. Takes only the first record (latest version) for each key
4. Filters out the "before" images of updates

Now we need a function to write these changes to PostgreSQL:

```python
def write_to_postgres(df, batch_id):
  # Skip empty batches
  if df.isEmpty():
    return
    
  # Deduplicate to get latest version
  df = get_latest_cdc_record(df, "transaction_id")
  
  # Process the batch
  with psycopg.connect(
    host="postgres-host",
    dbname="transactions_db",
    user="postgres_user",
    password="postgres_password"
  ) as conn:
    with conn.cursor() as cur:
      # Handle inserts and updates
      for row in df.filter("_change_type != 'delete'").collect():
        query = """
        MERGE INTO transactions AS target
        USING (VALUES (%s, %s, %s, %s, %s)) AS source 
          (transaction_id, user_id, amount, status, timestamp)
        ON target.transaction_id = source.transaction_id
        WHEN MATCHED THEN
          UPDATE SET 
            user_id = source.user_id,
            amount = source.amount,
            status = source.status,
            timestamp = source.timestamp
        WHEN NOT MATCHED THEN
          INSERT (transaction_id, user_id, amount, status, timestamp)
          VALUES (source.transaction_id, source.user_id, source.amount, 
                  source.status, source.timestamp)
        """
        cur.execute(query, (
          row.transaction_id,
          row.user_id, 
          row.amount,
          row.status,
          row.timestamp
        ))
      
      # Handle deletes
      delete_ids = [row.transaction_id 
                   for row in df.filter("_change_type = 'delete'").collect()]
      if delete_ids:
        cur.execute(
          "DELETE FROM transactions WHERE transaction_id = ANY(%s)", 
          (delete_ids,)
        )
      
      conn.commit()
```

This function:
1. Deduplicates records to get the latest version of each row
2. Uses PostgreSQL's `INSERT ... ON CONFLICT ... DO UPDATE` syntax for upserts
3. Handles deletes separately
4. Commits all changes in a single transaction

Now we can set up the streaming job:

```python
# Create the streaming job
streaming_query = (
  spark.readStream
    .format("delta")
    .option("readChangeFeed", "true")
    .table("transactions")
    .writeStream
    .foreachBatch(write_to_postgres)
    .option("checkpointLocation", "/mnt/checkpoints/transactions_cdc")
    .start()
)
```

This job:
- Reads the change feed from the Delta table
- Uses our `write_to_postgres` function to upsert data
- Tracks progress using a checkpoint

## Creating Indexes in PostgreSQL

To ensure fast query performance, we need to add appropriate indexes to our PostgreSQL table:

```sql
-- Primary key
ALTER TABLE transactions ADD PRIMARY KEY (transaction_id);

-- Index for user_id lookups (most common query pattern)
CREATE INDEX idx_user_id ON transactions (user_id);

-- Composite index for filtering by user_id and timestamp
CREATE INDEX idx_user_timestamp ON transactions (user_id, timestamp DESC);
```

These indexes will make our queries lightning-fast, especially the ones filtering by user ID and sorting by timestamp.

## Building the API

Now let's create a simple FastAPI application to expose this data:

```python
import logging
from fastapi import FastAPI
from psycopg_pool import AsyncConnectionPool

# Set up connection pool
pool = AsyncConnectionPool(
  "host=postgres-host dbname=transactions_db user=postgres_user password=postgres_password",
  min_size=5,
  max_size=20
)

app = FastAPI(title="Transactions API")

@app.on_event("startup")
async def startup():
  await pool.open()

@app.on_event("shutdown")
async def shutdown():
  await pool.close()

@app.get("/transactions/user/{user_id}")
async def get_user_transactions(
  user_id: str,
  limit: int = 100,
  offset: int = 0
):
  query = """
  SELECT transaction_id, user_id, amount, status, timestamp
  FROM transactions
  WHERE user_id = %s
  ORDER BY timestamp DESC
  LIMIT %s OFFSET %s
  """
  
  async with pool.connection() as conn:
    async with conn.cursor() as cur:
      await cur.execute(query, (user_id, limit, offset))
      rows = await cur.fetchall()
      return {"transactions": rows}
```

This API:
- Sets up a connection pool for efficient database access
- Defines an endpoint to query transactions by user ID
- Uses parameterized queries to prevent SQL injection
- Returns the results as JSON

## Putting it all together

With all these pieces in place, we now have a complete solution:
1. Capture all events with Kafka
2. Send the events to DBX
...
5. Serve the data in near Real time via APIs

This architecture gives us several benefits:
- Low-latency access to transaction data
- Reduced load on the data warehouse
- Support for real-time operational use cases
- Separation of analytical and operational workloads

## Conclusion

We've built a near real-time API using Change Data Capture and streaming to make warehouse data available with sub-second latency. By combining Delta's CDC capabilities with PostgreSQL's indexing and FastAPI's performance, we've created a solution that meets the needs of our customer support team.

The same pattern can be applied to many other use cases where real-time access to warehouse data is needed, such as personalization, fraud detection, or inventory management.

We can also apply this pattern to move data into any database, such as Redis or DynamoDB.
