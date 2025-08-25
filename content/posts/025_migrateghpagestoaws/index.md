---
title: '025_migrateghpagestoaws'
date: '2025-08-24T08:15:32+01:00'
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

1. Setup in gh pages
2. I wanted to migrate to have more flexibility - multiple subdomains 
3. Create Bucket
    - I have a hugo blog post with multiple index.html files. So I needed to create an S3 website rather than being able to use a private S3 bucket that only allows access to cloudfront
    - In the s3 bucket I add a policy where only GET requests are allowed (because it is public)
4. Create gh actions (+ trust policy)
5. Create Cloudfront distribution
6. Create Certficates
    - How to troubleshoot certificates when it does not create. Use email approach?
7. Register Domain (and hosted zone)
8. Create DNS for cloudfront distribution with Route 53
    - You need to have domains defined in the cloudfront distribution for the alias to appear. Ohterwise it wont appear as an opiton. 
    - To be able to have "domains" you need the ACM certificate.


Resources
- GH Actions https://aws.amazon.com/blogs/security/use-iam-roles-to-connect-github-actions-to-actions-in-aws/
- Cloudfront https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/getting-started-cloudfront-overview.html#getting-started-cloudformation-create-s3-www-bucket
