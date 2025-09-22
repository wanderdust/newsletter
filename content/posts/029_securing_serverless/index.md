---
title: 'How to Stop Your Serverless App from Running Up a $100k Bill Overnight'
date: '2025-09-18T20:04:11+01:00'
draft: true 
summary: 'Practical strategies to protect your serverless applications from runaway AWS bills, including caching, rate limiting, WAF rules, and DynamoDB safeguards.'
tags: ['aws', 'serverless', 'security']
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---



## Introduction

One of the best things about serverless is how easy it is to get started. You don’t need to worry about infrastructure, scaling groups, or servers. You just deploy and go.

It’s also incredibly cheap for small projects or apps with modest traffic. Hosting a static site on S3 and wiring it up with CloudFront? A few dollars a month. Adding Lambda, API Gateway, and DynamoDB? Still pennies for small workloads.

But here’s the catch: the same magic that lets your app scale smoothly from 0 to a few dozen requests can also scale into thousands of requests if someone decides to run a DDoS attack, or even just accidentally spams your endpoint. Without guardrails, [you can end up with an eye-watering AWS bill](https://serverlesshorrors.com/all/firebase-100k/).

This post walks through a sample serverless setup and highlights some best practices to keep your costs predictable and your application safe.

## The application

For the purpose of this blog post I'll use a classic example of a serverless architecture I used for a hobby project.

![serverless diagram](./serverless_app_diagram.png)

The purpose of the application was a note taking app for career progress, where you would regularly keep track of career achievements so that you could refer to them later in time and not forget any of the work done. In this application you could create, edit and delete notes. 

The website was created using React and hosted in an S3 bucket. The API logic to create notes was hosted in a lambda function, fronted by an API Gateway. For the database layer I used Dynamodb. All of these are serverless services.

## Securing the components

In this section we take a look at each of the components, and see how we can secure them to prevent spending a lot of money when there is unusually high traffic, or when a bad actor tries a Denial of Service attack.

### S3 Buckets

S3 is a very cheap way to host static websites or webapps, for example those you build with React. One thing that is easy to forget is that S3 charges you for egress costs. This means that every time someone accesses the website, you will pay for all of the media that needs to be loaded in the user's browser. If you have larger files, like HD images, music or videos [this can get expensive very fast](https://old.reddit.com/r/webdev/comments/1b14bty/netlify_just_sent_me_a_104k_bill_for_a_simple/).

The easiest way to save yourself trouble is to cache any content that does not change very often, like static images or videos.

[**Caching with CloudFront**](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/getting-started-secure-static-website-cloudformation-template.html): Cloudfront caches content at edge in locations all over the world. Every request that CloudFront serves directly is one less request hitting your S3 bucket. This reduces S3 read costs and, more importantly, avoids unnecessary data transfer charges.

**Restrict Direct Access to S3**: Add an [Origin Access Control (OAC)](https://aws.amazon.com/blogs/networking-and-content-delivery/amazon-cloudfront-introduces-origin-access-control-oac/) to your bucket, so content can only be accessed via CloudFront. This prevents people from bypassing caching and hammering your bucket directly.


[**AWS Web Application Firewall**](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-web-awswaf.html): AWS WAF are a set of rules you add to protect Cloudfront from unwanted traffic, such as blocking specific IPs. AWS has sets of predefined rules that are easy to setup and can come in handy.

### API Gateway

An API Gateway sits in front of your APIs and handles authentication, security, and routing, so you don’t need to build that logic into your application code. This separation makes microservices easier to maintain. AWS's API Gateway can be used as a first layer of security to protect your backend from unnecessary calls.

[**Enable Rate Limiting**](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html): Use API Gateway’s rate limiting features to stop anyone from spamming your API. With rate limitting you can set a maximum number of calls that can be made to your API within a window of time, for example add a limit of 100 requests per second. Anything beyond that recieves a 429 error. Rate limitting can be set globally, per endpoint or per user.

[**Add Authentication**](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html): Don’t expose your API to the entire internet without checks. At minimum, validate JWTs (e.g., Cognito, Auth0). This ensures requests come from valid clients that have authenticated to your application.

[**Use Caching**](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html): Cache frequent read requests in API Gateway. If your data changes infrequently, set longer cache times so repeated calls are served at the gateway instead of hitting your backend.

[**Lock Down CORS**](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-cors.html): Only allow requests from your known frontend domain(s). This prevents random websites from abusing your API in browser contexts.

[**AWS Web Application Firewall**](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-control-access-aws-waf.html): AWS WAF are a set of rules you add in front of your API Gateway to help you reduce unwanted traffic, such as blocking specific IPs. AWS has sets of predefined rules that are easy to setup and can come in handy.


### Lambda

Lambda is one of the most versatile AWS services, it can serve as the backend for your APIs as well as many other workloads. The problem is that each AWS account has a hard limit of 1,000 concurrent Lambda executions. If your application uses them all, other services or functions in your account may be left without capacity.

[**Set Reserved Concurrency**](https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html): The solution is to configure reserved concurrency for critical functions. This caps the maximum number of concurrent executions, giving you predictable costs and preventing downstream services (like DynamoDB) from being overwhelmed. It also guarantees that other Lambda functions in your account still have room to run, even during heavy load. Ensure the frontend code retries API calls using exponential backoff in case the API call fails.


### DynamoDB

DynamoDB is a low latency key value database for unstructured data. It comes with serverless and provisioned options. Serverless is the more expensive mode, but it comes at the benefit of out of the box autoscaling and not having to pay for provisioned infrastructure. The other side of the coin is that you run into more cost when the traffic is high.

[**Use DAX for Caching**](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html): Consider using DynamoDB Accelerator (DAX) to cache repeated queries. By serving cached responses, you cut costs and improve latency.

[**Apply Resource-Based Policies**](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/access-control-resource-based.html): Restrict DynamoDB access to just your Lambda functions. This ensures nobody can hit your tables directly.

## Conclusion

Serverless is powerful because it lets you move fast without managing infrastructure. The tradeoff is that the same flexibility can lead to unpredictable costs if you do not set guardrails. By adding caching with CloudFront, setting limits in API Gateway and Lambda, restricting access to DynamoDB, and protecting your endpoints with WAF, you turn unlimited scaling into scaling that you control.

It is much better to build these protections in from the start than to discover them after a surprising AWS bill. With the right setup your apps will stay reliable, secure, and affordable even if traffic suddenly spikes.

If you want more real-world examples of what happens when these guardrails aren’t in place, check out [serverlesshorrors.com](https://serverlesshorrors.com/).
