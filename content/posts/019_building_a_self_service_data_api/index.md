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

Once the data arrives in the warehouse it is only the first step. To get value from your data it needs to be easily accessible by different parts of the business. In some cases, the data warehouse is the single source of truth with all the data, in others the data may be scattered across different data sources - Redshift, Databricks, Postgres, you name it. 

One of the ways to make data accessible to the rest of the business is to make it accessible via APIs. In this blog post, I describe an architecture where users can create their own APIs to access the data they need using a centralised platform.

## The Problem

We have data entering the organisation from different data sources. We have setup our ingestion pipelines with streaming, and our batch operations to model the data in the warehouse. But once the data arrives in the warehouse we have no easy way of consuming this data.

Every time a team needs to access data they need to figure out: where the data lives, authentication, authorisation, rate limiting and how to access the data in a secure and performant manner. The teams that need this data might not be API experts, so they do not know best practices. 

In short, every time a team needs to access data for their platform or frontend, they need to figure this all out. There are no standards or reusability across teams.

## The Solution

We can build an API platform where users can easily create APIs to access the data they need. Users can define some parameters such as the data source, auth method, the query and the parameters. With this information, the platform creates an API ready to go, so users don't need to worry about the low level stuff such as: rate limiting, caching, setting up Auth, creating secure access to the data sources, ensuring performance, or maintaning architecture.


## 10000 ft Architecture

[Diagram] - 

API Gateway - API (ensuring consistency) - online store - Warehouse


## The Components

### API Gateway

The API Gateway gives us the ability to create an interface between the users and the APIs. THe API gateway gives us the ability to create multiple APIs (microservices) under a single URL. It helps us by detaching the backend from the users, so we can add, update, or remove the backend APIs with no changes to end user.

API gateways also help us by removing some of the logic from the API microservices. The API gateway gives us athentication, rate limiting, endpoint based routing and many other features.

### The Facades

The Facades are the interface that connects the user to the datasources. The facade is an API that connects to the different backends, executes a query and returns the results. We can have a single facade to connect to the differnt data sources and route based on the endpoint, or we can have different facades to handle different datasources and have the API gateway route based on the endpoint or headers.

The goal of the facades is to standardise the way that requests come in, and the format of the response coming out.

If we are connecting to multiple data sources we need to ensure the requests from the user point of view are all the same no matter the source of the data. We want to make sure we standardise the way endpoints are named, how query parameters and path parameters are passed, and the methods that are used. If we are building a read only Data API, we might want to standardise access via GET requests only.

Different datasources return different response formats. We can use the facades to transform the data and return a unified schema. Another important aspect is to ensure error format and error codes are standardised across data sources.

```json
{
  "data": [{"col1": "val1", "col2": "val2"}],
  "error": []
}

```

### Data Sources

This is where the data lives. The APIs connect to the data sources to gather the data and return the results. The data sources can be the data warehouse, or an operational data store.

Different data sources will satisfy different different business needs. We have the option to connect the API directly to the data warehouse use cases where the API is expected to have low load, and SLA is high (10+ seconds). However, hitting the warehouse directly is not reccommended for the following reasons
- Warehouses are optimised for querying by column, now by row. Querying the warehouse for queries where we are interested in grabbing a handful of rows will be a lot slower than if we used an OLTP database like Posttgres.
- Warehouses compute is not opitmised for a high volume of transactions. You may end up in a situation where queries get queued, and you'll also have to spend a lot more on compute than using OLT alternatives.
- Some warehouses like Redshift, don't have a separate compute and storage. Hitting the warehouse repetaadly with non optimised queries can bring the whole warehouse down

When creating Data APIs, a better solution is to move the data from the warehouse into an operational data store, such as Postgres. Postgres is designed to handle use cases with thousands of requests per second. It uses indexes to improve query performance and it has horizontal and vertical scalability to handle different levels of load.

We can use reverse ETL to move the data from the Warehouse into Postgres, and solve all the problems mentioned abave.

## Creating APIs - User Journey

Now that we have defined the components, we can look at how the users interact with the platform to create APIs.

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
    auth_required: true # Define user/pass via env variables
    caching:
      enabled: true
      ttl: 100ms


```

### Generating Resources

We need to create a component that is capable of taking a configuration file and generating all of the different resources we need.


[Diagram of how defs component]

#### API Gateway

The firs thing we need to generate from the config file is the API gateway configuration. Most API gateways providers allow us to create resources from an OAS template. 

In this case, every time a new definition is created, updated or deleted, we can create an OAS template that we use to update our resources.


```json
OAS example here
```


### Deployments 


## Challenges

### Self Service - No control over queries


### Data Modelling


### Local Testing - Database Modelling Access control


### Versioning


### Hot & Cold Data

In some cases, we need to serve data in real time - for example, if we are monitoring for fraudulent logins into a user account, we need to act very quickly from when the fraudulent user logs in to taking an action to block the account, particularly for platform where there is money involved. In these use cases we may choose to bypass the warehouse completely and send the data directly 
