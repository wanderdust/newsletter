---
title: 'Building a GraphQL API with AWS AppSync and PostgreSQL Aurora'
date: '2025-08-05T14:46:48+01:00'
draft: false 
summary: ''
tags: ["aws", "serverless", "postgres"]
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---

## Introduction

This is a guide to myself if I need to deploy an Appsync App in the future. Appsync is a Serverless AWS offering for implementing GraphQL APIs. It integrates nicely with Aurora and DynamoDB. Other integrations are done via Lambdas.

## Architecture Overview

Compontents

1. **AWS AppSync**: The managed GraphQL service that processes API requests
2. **Aurora PostgreSQL**: Serverless relational database for data storage
3. **AWS Secrets Manager**: Securely stores database credentials
4. **AWS IAM**: Manages permissions between services
5. **AWS CloudWatch**: Handles logging and monitoring

The flow of a request is:
1. Client sends a GraphQL query to AppSync endpoint
2. AppSync processes the request using resolver templates
3. Resolver connects to Aurora PostgreSQL via RDS Data API
4. Aurora executes the SQL query and returns results
5. AppSync transforms the data and responds to the client

## Setting Up AWS AppSync with Terraform

Let's start by setting up our AWS AppSync API using Terraform. We'll create a module that encapsulates all the necessary resources:

```hcl
# AppSync API
resource "aws_appsync_graphql_api" "appsync_api" {
  name                = "${var.deploy_environment}-appsync-data-api"
  authentication_type = "API_KEY" # Use IAM ROLE for production use cases

  log_config {
    cloudwatch_logs_role_arn = aws_iam_role.appsync_logs.arn
    field_log_level          = "INFO"
  }

  schema = file("${path.module}/schema/schema.graphql")
}

resource "aws_appsync_api_key" "test_key" {
  api_id  = aws_appsync_graphql_api.appsync_api.id
  expires = timeadd(timestamp(), "336h") # 14 days, for production use IAM auth instead
}
```

This creates our GraphQL API with API key authentication. For production environments, you should consider using IAM authentication instead. The API also has logging configured to send logs to CloudWatch.

### Configuring Aurora PostgreSQL Connection

Next, we need to configure the connection between AppSync and our Aurora PostgreSQL database:

```hcl
# AppSync datasource for Aurora PostgreSQL
resource "aws_appsync_datasource" "postgres_datasource" {
  api_id           = aws_appsync_graphql_api.appsync_api.id
  name             = "data_api_rds"
  service_role_arn = aws_iam_role.appsync_datasource_role.arn
  type             = "RELATIONAL_DATABASE"

  relational_database_config {
    http_endpoint_config {
      aws_secret_store_arn  = aws_secretsmanager_secret.rds_credentials.arn
      database_name         = var.rds_database_name
      db_cluster_identifier = var.rds_cluster_arn
    }
  }
}
```

Here we're creating a datasource of type `RELATIONAL_DATABASE` that connects to our Aurora PostgreSQL cluster through the RDS Data API. The connection uses credentials stored in AWS Secrets Manager and references the Aurora cluster ARN.

### Securing Database Credentials

Security is paramount when dealing with database credentials. We use AWS Secrets Manager to securely store and rotate our credentials:

```hcl
# Secrets Manager for RDS credentials
resource "aws_secretsmanager_secret" "rds_credentials" {
  name = "${var.deploy_environment}/appsync/data-api"
}

resource "aws_secretsmanager_secret_version" "rds_credentials" {
  secret_id = aws_secretsmanager_secret.rds_credentials.id
  secret_string = jsonencode({
    username = var.rds_appsync_username
    password = var.rds_db_password
  })
}
```

### IAM Roles and Permissions

To ensure proper security and access control, we need to create IAM roles and policies for AppSync to interact with other AWS services:

```hcl
# IAM role for AppSync datasource
resource "aws_iam_role" "appsync_datasource_role" {
  name = "${var.deploy_environment}-appsync-datasource-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "appsync.amazonaws.com"
        }
      }
    ]
  })
}

# IAM policy for RDS access
resource "aws_iam_role_policy" "appsync_datasource_policy" {
  name = "${var.deploy_environment}-appsync-datasource-policy"
  role = aws_iam_role.appsync_datasource_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "rds-data:ExecuteStatement",
          "rds-data:BatchExecuteStatement",
          "rds-data:BeginTransaction",
          "rds-data:CommitTransaction",
          "rds-data:RollbackTransaction"
        ]
        Resource = [var.rds_cluster_arn]
      },
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = [aws_secretsmanager_secret.rds_credentials.arn]
      }
    ]
  })
}
```

These resources establish the necessary permissions for AppSync to:
1. Execute SQL statements against our Aurora PostgreSQL database
2. Retrieve database credentials from Secrets Manager

### Defining the GraphQL Schema

The GraphQL schema defines the API contract between clients and your service. Here's our schema:

```graphql
type Query {
    getTransactions(provider: String!): [Transaction!]!
}

type Transaction {
    transaction_id: String!
    amount: String!
}
```

This simple schema defines a single query to retrieve transactions filtered by provider, returning an array of Transaction objects.

### Implementing Resolvers with VTL Templates

Resolvers are the connective tissue that translate between GraphQL operations and your data sources. AWS AppSync uses Apache Velocity Template Language (VTL) for resolver mapping templates:

#### Request Mapping Template

```json
{
  "version": "2018-05-29",
  "statements": [
    $util.toJson(
      "SELECT table.\"transaction\" 
              table.\"amount\"
       FROM mytable.purchases AS table
       WHERE table.provider = :provider"
    )
  ],
  "variableMap": {
    ":provider": $util.toJson($ctx.arguments.provider)
  }
}
```

This template takes the `provider` argument from the GraphQL query and constructs a SQL query to fetch transactions matching that provider. Note how we're using parameter binding (`:provider`) to prevent SQL injection attacks.

#### Response Mapping Template

```
$utils.toJson($utils.rds.toJsonObject($ctx.result)[0])
```

This template handles error conditions and transforms the RDS Data API response into the JSON structure expected by GraphQL. The `$utils.rds.toJsonObject()` utility function helps parse the RDS response into a format that can be returned to the client.

### Connecting the Resolver to the Schema

Finally, we connect our resolver to the appropriate field in our GraphQL schema:

```hcl
resource "aws_appsync_resolver" "get_transactions" {
  api_id      = aws_appsync_graphql_api.appsync_api.id
  type        = "Query"
  field       = "getTransactions"
  data_source = aws_appsync_datasource.postgres_datasource.name

  request_template  = file("${path.module}/resolvers/Query/getTransactions.req.vtl")
  response_template = file("${path.module}/resolvers/Query/getTransactions.res.vtl")
}
```

This configures the resolver to use our request and response templates when handling the `getTransactions` query.

### Using the AppSync Module

To use our AppSync module in a larger infrastructure, we simply include it as follows:

```hcl
module "appsync" {
  count  = var.deploy_environment == "dataproduction" ? 0 : 1
  source = "./modules/appsync"

  deploy_environment   = var.deploy_environment
  account_id           = var.account_id
  rds_cluster_arn      = module.data_api_rds.data_api_arn
  rds_database_name    = var.rds_database_name
  rds_appsync_username = var.rds_appsync_username
  rds_db_password      = var.data_api_db_password
}
```

Note that in this example, we're conditionally deploying the AppSync API based on the deployment environment.

## Testing the GraphQL API

Once deployed, you can test your API using the AWS AppSync console or any GraphQL client like Apollo Client or Postman. Here's a sample query:

```graphql
query GetTransactions {
  getTransactions(provider: "myprovider") {
    transaction_id
    amount
    
  }
}
```

## Conclusion

In this guide, we've built a robust GraphQL API using AWS AppSync connected to Aurora PostgreSQL.
