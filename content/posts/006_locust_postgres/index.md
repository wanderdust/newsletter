---
title: 'Load Testing PostgeSQL using Locust'
date: '2025-01-10T15:09:39+01:00'
draft: false
summary: ''
tags: ['postgres', 'test']
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---

I recently needed to run load tests on a PostgreSQL database. Postgres is no question a reliable and scalable database ready for production use cases, but there might be times when you’ll need to confirm it can handle your specific use case. This might be necessary if you’re using a PostgreSQL database hosted by a third party or if you want to check if your current instance size and specs can manage your existing load.

We’ll use [locust](https://locust.io/) to create our test. Locust is a load-testing framework that simulates multiple users interacting with your application at the same time. The code below demonstrates how to implement a custom Postgres client with Locust to send multiple concurrent queries to your PostgreSQL database.

## The code
First we define the Postgres client in `postgres_client.py`

- We use environment variables to define our Postgres connection. Create an `.env` file locally with the required variables and load them using the [python-dotenv](https://pypi.org/project/python-dotenv/) library.
- psycopg2 is used to connect to Postgres. For the purposes of this load test we need to execute multiple concurrent requests, for which we use the [psycogreen](https://pypi.org/project/psycogreen/) library.
- The PostgresClient class has methods to start and close the connections and submit queries. We implement our custom timer to time how long the queries take to execute.

_postgres_client.py_

```python
import os
import time

import psycopg2.pool
import psycopg2.pool
from dotenv import load_dotenv
from locust import events
from psycogreen.gevent import patch_psycopg

load_dotenv()

POSTGRES_DBNAME = os.getenv('POSTGRES_DBNAME')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)

patch_psycopg()
connection_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=200,
    dbname=POSTGRES_DBNAME,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
)

class PostgresClient:
    def __init__(self):
        self.conn = connection_pool.getconn()

    def execute_query(self, query):
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def close_connection(self):
        connection_pool.putconn(self.conn)

    def submit(self, name, query):
        start_time = time.time()
        try:
            res = self.execute_query(query)
            response_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="postgres",
                name=name,
                response_time=response_time,
                response_length=0,
            )
        except Exception as e:
            response_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="postgres",
                name=name,
                response_time=response_time,
                response_length=0,
                exception=e,
            )
            print("error {}".format(e))
```

The next part consists on defining `locustfile.py`

The CustomTaskSet is where you define your queries. Define as many as you’d like for your load test
PostgresUser starts the client and runs the test and also makes sure the connections are closed when the test is terminated.

_locustfile.py_

```python
from pathlib import Path

from locust import TaskSet, task, User
from postgres_client import PostgresClient


class CustomTaskSet(TaskSet):

    @task
    def run_my_query(self):
        sql = Path("sql/my-query.sql").read_text()
        self.client.submit("my-query-name", sql)

    @task
    def run_my_other_query(self):
        sql = Path("sql/my-other-query.sql").read_text()
        self.client.submit("my-other-query-name", sql)

class PostgresUser(User):
    tasks = [CustomTaskSet]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = PostgresClient()
        print("Client connected")

    def on_stop(self):
        self.client.close_connection()
        print("Connection closed")
```

## Running the load test

To start the locust UI run `locust -f locustfile.py`. Ignore the host field and add the number of users and ramp up for your test.

