---
title: 'Securing Your Serverless Application (Before It Costs You Thousands)'
date: '2025-09-18T20:04:11+01:00'
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



## Introduction

One of the best things about serverless is how easy it is to get started. You don’t need to worry about infrastructure, scaling groups, or servers—you just deploy and go.

It’s also incredibly cheap for small projects or apps with modest traffic. Hosting a static site on S3 and wiring it up with CloudFront? A few dollars a month. Adding Lambda, API Gateway, and DynamoDB? Still pennies for small workloads.

But here’s the catch: the same magic that lets your app scale smoothly from 0 to hundreds of requests can also scale into thousands of requests if someone decides to run a DDoS attack—or even just accidentally spams your endpoint. Without guardrails, you can end up with an eye-watering AWS bill.

This post walks through a sample serverless setup (S3 + CloudFront, API Gateway + Lambda, DynamoDB) and highlights some best practices to keep your costs predictable and your application safe.

## The application

For the purpose of this blog post I'll use an example of a serverless architecture I bulit for a hobby project. This architecture is very common in AWS, but it is not without risks if you don't secure it properly.

![serverless diagram]()

The purpose of the application was a note taking app for career progress, where you would regularly keep track of career achievements so that you could refer to them later in time and not forget any of the work done. In this application you could create, edit and delete notes. 

The website was created using react and hosted in an S3 bucket. The API logic to edit,create and delete notes was hosted in a lambda function, fronted by an API Gateway. For the database layer I used Dynamodb. All of these services are serverless.

## Securing the components

In this section we take a look at each of the components, and see how we can secure them to prevent spending a lot of money when there is unusually high traffic, or when a bad actor tries a Denial of Service attack.

### S3 Buckets

S3 is a very cheap way to host static websites or webapps, for example those you build with React. One thing that is easy to forget is that S3 charges you for "egress" costs. This means that every time someone accesses the website, you will pay for all of the media that needs to be loaded in the user's browser. If you have larger files, like HD images or videos this can get expensive very fast.

The easiest way to save yourself trouble is to cache any content that does not change very often, like images, videos etc. In AWS the best way is to use Cloudfront as a Content Delivery Network.

**Caching with CloudFront**: Cloudfront caches content at edge in locations all over the world. Every request that CloudFront serves directly is one less request hitting your S3 bucket. This reduces S3 read costs and, more importantly, avoids unnecessary data transfer charges.

**Restrict Direct Access to S3**: Add a bucket policy so only CloudFront can access your files. This prevents people from bypassing caching and hammering your bucket directly.

⸻

### API Gateway

An API Gateway sits in front of your APIs and handles authentication, security, and routing, so you don’t need to build that logic into your application code. This separation makes microservices easier to maintain. AWS's API Gateway can be used as a first layer of security to protect your backend from unnecessary calls.

**Enable Rate Limiting**: Use API Gateway’s rate limiting features to stop anyone from spamming your API. With rate limitting you can set a maximum number of calls that can be made to your API within a window of time, for example add a limit of 100 requests per second. Anything beyond that recieves a 429 error.

**Add Authentication**: Don’t expose your API to the entire internet without checks. At minimum, validate JWTs (e.g., Cognito, Auth0). This ensures requests come from valid clients that have authenticated to your application.

**Use Caching**: Cache frequent read requests in API Gateway. If your data changes infrequently, set longer cache times so repeated calls are served at the gateway instead of hitting your backend.

**Lock Down CORS**: Only allow requests from your known frontend domain(s). This prevents random websites from abusing your API in browser contexts.

⸻

### Lambda

Lambda is one of the most versatile AWS services, it can serve as the backend for your APIs as well as many other workloads. The problem is that each AWS account has a hard limit of 1,000 concurrent Lambda executions. If your application uses them all, other services or functions in your account may be left without capacity.

**Set Reserved Concurrency**
The solution is to configure reserved concurrency for critical functions. This caps the maximum number of concurrent executions, giving you predictable costs and preventing downstream services (like DynamoDB) from being overwhelmed. It also guarantees that other Lambda functions in your account still have room to run, even during heavy load.


⸻

### DynamoDB
**Use DAX for Caching**
DynamoDB Accelerator (DAX) helps reduce repeated queries. By serving cached responses, you cut costs and improve latency.

**Apply Resource-Based Policies**
Restrict DynamoDB access to just your Lambda functions. This ensures nobody can hit your tables directly.

⸻

## Conclusion

Serverless gives you power and flexibility with minimal effort—but that same ease of scaling can backfire if you’re not careful. By putting guardrails in place across S3, CloudFront, API Gateway, Lambda, and DynamoDB, you can prevent an innocent project (or a malicious attacker) from running up thousands in AWS costs.

Think of these controls as your seatbelt. You might not always need them—but you’ll be glad they’re there when something goes wrong.
