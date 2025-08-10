---
title: '019_building_a_self_service_data_api'
date: '2025-08-02T10:41:15+01:00'
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

GOAL: Lessons from a Retired Self-Serve Data API
TARGET AUDIENCE: General Audience interested in data applications
# Lessons from a Self Service Data API

Over the past 2 years I've been building a self serving data API platform. Different teams in the org needed programmatic access the the data in the warehouse. There was no standardised way to access the data, which meant each time teams would need to figure out how to build APIs from scratch with. There were no set best practices, or reusability across teams.

There was a need for a solution, which is where this platform was born. THe platform was a plug and play where users defined the datasource and a SQL query and an API was created for them with authentication, authorisation, rate limiting, caching, pagination etc.

I've worked in this platform since the very beggining, having contributed to shape it what it is today. After two years I am moving to a new team, and I thought it would be a good time to reflect on the platform and collect some of the lessons learned.

## Users should only be able to serve data from modelled tables

Self serving can be a double edge sword. On the one hand, it gives users freedom to build their own APIs without the bottleneck of the platform team having to be involved so we can focus on developing new features. On the other hand, without the correct guardrails, users will create APIs over raw, unmodelled data. By unmoddeled, it either means tables that require complex and expensive queries to find the information you need, or tables without the correct indexes or partitions to ensure queries are fast.

This can be an issue for two reasons. First, slow APIs create poor API experiences. When working with APIs, the users usually expect sub-second latency. If the API call takes over 10s because it's querying an unmoddeled table, it will make everyone unhappy. Secondly, an unmoddelled table will add more load to the database every time it is queried because it needs to do a lot of heavy lifting execute the query. If the load is high it will consume a lot of resources, adding additional cost for needing to scale. 

This was a lesson learned early on, and one which became very hard to backtrack. Once the APIs querying these tables were "locked in" and serving business use cases, it was hard to go back and ask the users to do the extra work to model the source tables further.

## Ensuring performance comes at the cost of Freedom

This one is a continuation of the previous lesson. Our APIs allowed users to define the SQL query that was getting executed every time the endpoint was hit. Nothing would stop the users from defining very complex queries with JOINs or other queries that were not making use of the existing indexes already created on the tables.

APIs are expected to be performant, and a SQL query can make or break the API. Rather than allowing users the freedom to provide parametrised queries, we could have removed that completely and only allow users to query by primary key, where select page limit and the columns they want. This way we could have easily created indexes on the tables on a known column, and have a simple and standard select query hardcoded in the background for all APIs. An added benefit of this approach is that it forces users to model the tables to fit the API.

Alternatively, if being able to create your own SQL is a requirement for more complex business use cases, I've seen companies like Tinybird enforce a 10s timeout. Any queries hitting that threshold gets killed. This could have also been a suitable and less rigid solution.

## Perfect architectures don't exist 

This was one of the lessons that I found most dissapointing as an engineer. I had always imagined software platforms to have been built using the perfect desing patters and perfect architectures. In the real world, business use cases require to add new "patches" or features to accomodate for things like "last minute data protection requirements", regulatory needs or simply new business needs that were not orignally anticipated. More and more you start moving away from that "clean" architecture. What you can focus on, is to try and build a great platform that users really want to use, and that solves a real business need, which takes me to the next lesson.

## It's up to you to build a good user experience

Something is very clear to me now, a platform that serves a real business need does not mean that it is a platform that users will want to use. If you are not careful, you can end up building a platform that leadership loves, but the developers to use.

User experience should not be neglected. By this I mean not only the user interface (config, cli, website), but also things like documentation or the ability to test APIs easily and quickly.

The tricky thing is, that as long as the platform is doing its job, no one is going to come asking for better UI/UX features. Asking users directly is a good way, although I found that the can tend to try and be nice to you. It can be hard to setup a good round of questions to gather valuable feedbock.

A better approach is to spot the user complaints. Sometimes this can be in Slack or in a Zoom meeting. For example, a user was once complaining that to test a change in the API it took about 10 minutes for the changes to be deployed to the dev environment. Unfortunately I won't be around for long enough to improve that experience.

## Bonus: To build a scalabe Self Serving data API, you need a managed reverse ETL Solution

As I mentioned at the beggining of the post, the goal of the API is enable users to create APIs that need to query data from the Warehouse. In order to achieve this in a scalable and performant manner, the data had to be moved from Databricks into a Postgres Database, also known as the "Operational Store".

Although we provided a template for how to create both streaming and batch pipelines to move the data across, this was an extra step required for the users who wanted to create an API, which usually needed to involve additional teams. This process was very slow and not scalable, because each data pipeline required to go through a PR review process. 

In order to build a scalable data API, a managed solution is needed to move data from the warehouse into the operational Store with minimal user interaction, perhaps a few clicks here and there. This soultion should be able to create the necessary indexes and roles on the operational store to ensure good performance. Databricks already offers some similar solutions for this such as "online tables" or their new product "Lakebase", which can be useful if you are already using Databricks.

## Summary

I have shared some of the lessons learned from working on a self serving Data API platform. Although I've only spoken about the things I would have liked to improve, I also feel incredibly proud of the platform, and I believe that many things were done well, thanks to being part of an excellent team. Hopefully some of these lessons can help the someone build the next Data API.



-----

Once the data arrives in the warehouse it is only the first step. To get value from your data it needs to be easily accessible by different parts of the business. In some cases, the data warehouse is the single source of truth with all the data, in others the data may be scattered across different data sources - Redshift, Databricks, Postgres, you name it. 

One of the ways to make data accessible to the rest of the business is to make it accessible via APIs. In this blog post, I describe an architecture where users can create their own APIs to access the data they need using a centralised platform.

## The Problem

We have data entering the organisation from different data sources. We have setup our ingestion pipelines with streaming, and our batch operations to model the data in the warehouse. But once the data arrives in the warehouse we have no easy way of consuming this data.

Every time a team needs to access data they need to figure out: where the data lives, authentication, authorisation, rate limiting and how to access the data in a secure and performant manner. The teams that need this data might not be API experts, so they do not know best practices. 

In short, every time a team needs to access data for their platform or frontend, they need to figure this all out. There are no standards or reusability across teams.

### A Self Serve Data API Platform

We can build an API platform where users can easily create APIs to access the data they need. Users can define some parameters such as the data source, auth method, the query and the parameters. With this information, the platform creates an API ready to go, so users don't need to worry about the low level stuff such as: rate limiting, caching, setting up Auth, creating secure access to the data sources, ensuring performance, or maintaning architecture.


#### Why APIs?

Why use an API layer rather than connecting to the database directly?

APIs are well understood by developers. They are easily integrated into other applications. Also, adding an API layer helps us standardise access even if we have multiple data sources in the backend.

With APIs we can also easily define data contracts via OAS specifications. The users can easily understand what are the data inputs, and know what to expect in return. It is well defined.

An APIs layer also give us additional levels of security to protect the database from being hit directly by the user, thanks to caching, rate limiting and authentication.

#### Why Self Serve?

The goal of this platform is to provide standardised and secure access to data to everyone in the organisation. The goal is to go from Data to API in with as little friction as possible.

Self serving enables the end users (Users of the API) to define their own endpoins, without needing intervention from the Platform team for specific use cases. Users can indpedently create APIs without the platform team becoming a bottleneck. This also frees the platform team to be able to keep working on the plattform to develop new features.


## How it works

(High level overview of how the platform works!)


## The Platform

[Diagram] - 

API Gateway - API (ensuring consistency) - online store - Warehouse

### Components

#### API Gateway

The API Gateway gives us the ability to create an interface between the users and the APIs. THe API gateway gives us the ability to create multiple APIs (microservices) under a single URL. It helps us by detaching the backend from the users, so we can add, update, or remove the backend APIs with no changes to end user.

API gateways also help us by removing some of the logic from the API microservices. The API gateway gives us athentication, rate limiting, endpoint based routing and many other features.

#### The Facades

The Facades are the interface that connects the user to the datasources. The facade is an API that connects to the different backends, executes a query and returns the results. If we have multiple data sources that our platform can connect to, we can have a single facade that redirects to each data source depending on the request. For example, we can have a header `x-data-source: postgres` that indicates the data source to redirect to, and write some logic in the facade to redirect to the correct datasource at runtime.

Alternatively, we can have 1 facade for each data source (ie Postgres Facade for Postgres requests, Redis Facade for redis requests), where each facade acts as a connector to a data source. In this case, the API gateway is in charge of redirecting each request to the correct facade. This can be defined once when creating the API, and the API Gateway will automatically redirect to the correct facade.

In AWS API Gateway, the redirection may look like this:

```hcl
resource "aws_api_gateway_rest_api" "example" {
  body = jsonencode({
    openapi = "3.0.1"
    info = {
      title   = "example"
      version = "1.0"
    }
    paths = {
      "/transactions" = {
        get = {
          x-amazon-apigateway-integration = {
            httpMethod           = "GET"
            payloadFormatVersion = "1.0"
            type                 = "HTTP_PROXY"
            uri                  = "https://redis-facade.com/users"
          }
        }
      }
      "/users" = {
        get = {
          x-amazon-apigateway-integration = {
            httpMethod           = "GET"
            payloadFormatVersion = "1.0"
            type                 = "HTTP_PROXY"
            uri                  = "https://postgres-facade.com/items"
          }
        }
      }
    }
  })
}
```

I prefer the latter approach because this way users don't need to remember to pass additional headers or parameters to connect to the right resource. They can simply define this at API creating time and it will automatically use the right facade.

The goal of the facades is to standardise the way that requests come in, and the format of the response coming out.

Different datasources return different response formats. We can use the facades to transform the data and return a unified schema. Another important aspect is to ensure error format and error codes are standardised across data sources.

```json
{
  "data": [{"col1": "val1", "col2": "val2"}],
  "error": []
}
```

Since we are handling endpoints at the API gateway level, we can define the facade as a dummy API whose job is simply trannforming the requests and the results.

```python

@app.get("/")
def read_root(request):
  db_connection = client.connect()
  # Get the query corresponding to the endpoint
  query = get_query(request.url.path)

  # Execute query and gather results
  data = db_connection.execute_query()
  db_connection.close()

  # Transform the results to standardised format and return
  return {"data": transformed_results(data)}
```

#### Data Sources

The data source is what the facades connect to. For this platform we can have one or more data sources that users can connect to, and its up to the users to decide what datasource they want to connect to when definining the API. We'll go into more detail about the data in a later section.

### Deploying the components

Let's recap all the components.
1. We have an API Gateway. THe API Gateway is where the routes are defined. The API gateway knows how to route each request to the correct backend. The API gateway gives us other features like caching, and authentication.
2. The Facades. One facade connects to a single data source. The job of the facade is to standardise requests, response formats and error messages. From the point of view of the user, it is a single API no matter the database in the backend.
3. The datasources. These probably already exist in our org, and we will be connecting the platform to each of them.

We only need to deploy 2 components for this platform, the API Gateway and the Facade API servers.

For the API Gateway we can use AWS API Gateway, Kong or any other provider. AWS API Gateway is a good simple solution, since it is serverless so we don't have to worry about maintaining infrastructure.

THe second component we need to deploy is the facades. The facades can be written in any languague of your choice (python, Java, Go etc). The important element is to ensure each facade can scale. If we expect a high load of calls to the APIs, we can create multiple instances running and place them behing a load balancer. We then point the API Gateway to the load balancer DNS.

We have multiple options for deploying the infrastucture. Using Docker containers to deploy our application is great to ensure we are developing and deploying using a consistent environment. We have a few options, such as Kubernetes (eg EKS) or ECS. ECS is a good choice for this use case, unless you have existing knoweldge of Kubernetes. ECS is easier to use 

[final diagram]

Now we have the platform running. Lets take a look at how users define the APIs, and how the endpoints are dynamically created.


## Self Serving

Now that we have defined the infrastructure, we can look at how the users create and deploy new APIs.

### Config Files - OAS Specs, API Gateway Config, SQL queries

The config file is where the users define their APIs. The config file is where the user defines the endpoint, the data source, the query to run and API Gateway behaviour such as authentication and caching.


```yaml
metadata:
  name: users
  description: Get all active users

routes:
  /users:
    datasource: operational_store # Postgres
    query: "SELECT id, name FROM op_store.myschema.users WHERE active = :active"
    methods: [GET]
    params:
      - name: active
        type: bool
    auth:
      secret_path: aws::secret/my-secret
    caching:
      enabled: true
      ttl: 100ms

```

### Generating the IaC form the Config

We need to create a component that is capable of taking a configuration file and generating all of the different resources we need, this can be created using your programming language of choice and can be deployed either as a library, a script or a cli.

The Compontent takes the config file as an input and generates the resources that need to be deployed. In this case, the config file will generate the resources required to deploy the user endpoins, in this case it is the API Gateway config with the new endpoint (or endpoint modifications), and the SQL query that the endpoint will execute.


[Diagram of how defs component creates resaurces (OAS, terraform etc)]

#### API Gateway

The firs thing we need to generate from the config file is the API gateway configuration. Most API gateways providers allow us to create resources from an OAS template. 

In this case, every time a new definition is created, updated or deleted, we can create an OAS template that we use to update our resources. 


```json
{
  "openapi": "3.0.1",
  "info": {
    "title": "Self-Service Data API",
    "description": "API for accessing business data",
    "version": "1.0.0"
  },
  "paths": {
    "/users": {
      "get": {
        "summary": "Get all users",
        "parameters": [
          {
            "name": "department",
            "in": "query",
            "schema": { "type": "string" },
            "description": "Filter by department"
          }
        ],
        "responses": {
          "200": {
            "description": "Successful response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": { "$ref": "#/components/schemas/User" }
                }
              }
            }
          }
        },
        "x-amazon-apigateway-integration": {
          "uri": "arn:aws:apigateway:${region}:lambda:path/2015-03-31/functions/${lambda_arn}/invocations",
          "type": "aws_proxy",
          "httpMethod": "POST"
        }
      }
    }
  },
  "components": {
    "schemas": {
      "User": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "name": { "type": "string" },
          "email": { "type": "string" },
          "department": { "type": "string" }
        }
      }
    }
  }
}
```

We can deploy the OAS template to the API gateway via terraform templates.

```hcl
resource "aws_api_gateway_rest_api" "data_api" {
  name        = "self-service-data-api"
  description = "API for accessing business data"
  body        = file("${path.module}/openapi.json")

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_stage" "prod" {
  deployment_id = aws_api_gateway_deployment.api_deployment.id
  rest_api_id  = aws_api_gateway_rest_api.data_api.id
  stage_name   = "prod"

  # Cache configuration
  cache_cluster_enabled = true
  cache_cluster_size    = "0.5" # 0.5GB cache

  # Method cache settings
  variables = {
    "cacheEnabled" = "true"
  }
}

resource "aws_api_gateway_method_settings" "all" {
  rest_api_id = aws_api_gateway_rest_api.data_api.id
  stage_name  = aws_api_gateway_stage.prod.stage_name
  method_path = "*/*"

  settings {
    metrics_enabled      = true
    logging_level        = "INFO"
    data_trace_enabled   = true
    caching_enabled      = true
    cache_ttl_in_seconds = 300 # 5 minutes
  }
}

resource "aws_api_gateway_deployment" "api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.data_api.id

  triggers = {
    # Redeploy when the OAS spec changes
    openapi_sha = sha1(file("${path.module}/openapi.json"))
  }

  lifecycle {
    create_before_destroy = true
  }
}
```


### Deployment process

Now we have the terraform files required to delpoy the API Gateway as well as the SQL query that we want each endpoint to execute. 

The deployment process for the API Gateway is as follows

1. THe config generation component looks at the API config and generates the terraform + OAS resources
2. The terraform is applied to create or update the API Gateway
3. THe endpoint is created in the API Gateway which points to the correct Facade.

Depending on how we build this platform, this process can be integrated as a CI/CD pipeiline (if users define these definitions in a github repo), or we can create a cli that handles this process.



#### SQL queries

The final step is ensuring each endpoint will execute the query that the user has defined. However, if you rememeber the API facade is already running, and we don't want to redeploy the server every time a user wants to add or update an endpoint.

What we can do instead is to upload the SQL queries to an S3 bucket. THe facade can have a running process running every few seconds that checks for any new SQL queries, and loads them into the facade. All of this can happen asynchronously without having to redeploy the server.

If we remember the facade code it was a wildcard endpoint that routes all requests to the database. When a request comes in, we can use the endpoint name to load the correct SQL query at runtime.


```python
# Async process that loads the queries into memory
queries = async cron_query_loader(s3_bucket_path="s3:://my-path", reload_time="30s")

@app.get("/")
def read_root(request):
  db_connection = client.connect()
  # Get the query corresponding to the endpoint
  query = get_query(request.url.path)

  # Execute query and gather results
  data = db_connection.execute_query()
  db_connection.close()

  # Transform the results to standardised format and return
  return {"data": transformed_results(data)}
```

And with this we have a fully functioning platform that creates API endpoints based on user configs.


## The Data

The good news is that we have a fully functioning data api platform: users can create APIs to access the data they need using a config file and deploying it via CI/CD. 

The bad news? That is the easy part. Whether the Data API platform can be succesful depends on how we handle the data before it's served.

For example, when a user is defining the query for a new API, nothing is stopping them from writing something like this

```sql
--- Very SLOW query with joins, deduplication etc
```

To begin with, running such a query can take a long time, from seconds to minutes depending on the data source, the compute, the amount of data and how the data is modelled. From an API perspective, waiting more than a few seconds for a response creates a very poor experience. Especially if such API is integrated in user facing applications.

Another problem is the resources such a query consumes. Usually, slow queries are slow because they need to scan a lot of data, usually because of inefficient queries or badly modelled data (ie no indexes). The database can end up consuming a lot of resources because of this, and could bring the database down if the load is high, and the database is not capable of scaling.

Long running queries can sometimes create blocks on other queries, meanining that other queries might not be able to execute until the long running has terminated, which creates a very poor user experence.

### Modelling

The good news, is that there is a solution: Data modelling. For a data api platform to work the data in the database needs to be properly modelled. This means that rather than trying to run expensive queries at runtime, we model this data beforehand so that the API can do a simple SELECT query of the data we need. We can achieve this by running a series of premodelling steps with tools such as dbt, where we have different stages of modelling, such as the medallion architecture. ALternatively we can use materialised views which refresh on a cadence acceptable for our API.

[Diagram Showcasing modelling - ie medallion process]

```sql
--- Example query with simple SELECT
```

The second part is ensuring that the database has the correct indexes to ensure the database can efficiently find the data is looking for. For example, if we are searching some data by user id, by adding an index on the `user_id` the database can easily find the user id rather than having to do a full table scan, which can be expensive (link blog post about indexes).

So users creating APIs need to be aware of the data before creating an API. It is very important that there exists coordination between the data teams preparing the data for the business use case, and the teams creating and integrating their APIs into their own platforms to ensure SLAs are met.

### Choosing the right Database

Not every database is suitable for every task. Data Warehouses (OLAP) are optimised for analytical queries. The data is stored in column format, which is optimised for spaced on disk, as well as for selecting data based on columns, rather than rows.

On the other hand, OLTP databases such as postgres are opitimsed to serve thousands of requests per second, when the use case is small queries returning fewer rows. They can leverage indexes to make querying fast.

If you have data in the Data Warehouse, you might be tempted to connect your API diretcly to it. THis can be a valid use case, depending on the situation, however this approach has some risks.

Modern data warehouses such as Snowflake or Databricks separate compute from the data, which means you can hit the warehouse as hard as you can, which won't bring the warehouse down, you can scale compute independently of storage. However this is not the case for some data warehouses such as Redshift: if you connect an API dircetly to Redshift, an increase load of requests from the API could eventually bring the whole cluster down. This won't only affect your API going down, but systems in the company that depend on redshift. As you can imagine this is not a sustainable way of creating APIs.

The second issue, which I've already mentioned, is that the data warehouse is not optimised to serve a high volume of small transactions with very low SLAs. They are meant for analytical use cases. OLTP databases such as Postgres or DynamoDB are better suited for API use cases.

To ensure the APIs can handle a high volume of queries with slow SLAs, we need to move the data from the Warehouse to an OLTP database (of your choice) and connect the API to it. This means adding an extra step to the API creating process, however it will ensure high quality and high performance APIs.

THis process is called Reverse ETL, and there are multiple ways to do it. I've recently written a blog on how to use spark to move data from Databricks Delta into Postgres. However, you can use other methods, such as third party vedors (hightouch) or custom implementations such as using EMR, Lamdbas etc.

### Summary

As we have seen in this section, the API creating process is not only about defining the data source and the query and start hitting the endpoint. It requires careful consideration about how the data is modelled and served to the APIs. The Data Platform should provide suitable solutions for the different use cases that the platform may have. For example, Postgres may be a suitable solution to move data from the Warehouse so it's ready to be queried at scale. For other use cases, such as real time data, other solutions such as Redis may be more suitable.

## Federation and Hot & Cold data
### Hot & Cold Data

In some cases, we need to serve data in real time - for example, if we are monitoring for fraudulent logins into a user account, we need to act very quickly from when the fraudulent user logs in to taking an action to block the account, particularly for platform where there is money involved. In these use cases we may choose to bypass the warehouse completely and send the data directly 

We used trino ... 

But you can also combine both your hot data and cold data into a single operational store (ie Postgres) and combine queries that way.




## Lessons Learned

### Local Testing - Database Modelling Access control

### Data strategy


### Data modelling is the most important element

### Designing User Interfaces is hard
Getting feedback sometimes happens by accident as side comments or remarks. Checking for feedbakc often is impartont

### Solving for 90% of problems
In our case solving for long running queries caused issues. If we colud cut queries running over 10s, it would have made our lifes easier. However business needs sometimes require these exceptions that complicate platform design.
