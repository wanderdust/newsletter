---
title: 'How to Serverless: Deploy a web application in AWS'
date: '2025-07-24T08:16:09+01:00'
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

- Describe architecture of careernotes.com
- Describe each of the components and why it was chosen
    - Route53, Cloudfront, S3 website, API Gateway, Lambda API, DynamoDB
    - Security - CORS (API), SG in bucket to only allow access from Cloudfront
- Describe the difference between static website and non static - deploy as server or micro service
- Section with CI/CD - GH actions + Cloudformation (SAM)
- Section with pros/cons and tradeoffs - when to choose different compontents
    - Database - Aurora RDS Serverless or Dynamo?
    - Deploy website as a server with EC2 + ASG + Load balancer (or EKS, ECS)?


![architecture](./serverless-webapp.png)
