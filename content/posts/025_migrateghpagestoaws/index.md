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
4. Create gh actions (+ trust policy)
5. Create Cloudfront distribution
6. Create Certficates
7. Register Domain (and hosted zone)
8. Create DNS for cloudfront distribution with Route 53


Resources
- GH Actions https://aws.amazon.com/blogs/security/use-iam-roles-to-connect-github-actions-to-actions-in-aws/
- Cloudfront https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/getting-started-cloudfront-overview.html#getting-started-cloudformation-create-s3-www-bucket
