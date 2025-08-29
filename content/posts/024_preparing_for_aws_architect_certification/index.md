---
title: '024_preparing_for_aws_architect_certification'
date: '2025-08-12T13:34:53+01:00'
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

- THe worst part is having to learn a million different services that sound the same or do similar things (AWS WAF, AWS Firewall Manager).


---

I have recently passed the AWS Architect Associate Exam with a score of 848! This is a very tricky certification which covers a lot of AWS services, so I wanted to write about my experience preparing for the exam.

## Background

I have about 5 years of experience with AWS, on and off. I have worked mostly with RDS, Lambda, EC2s and a few other services here and there. 

## Preparation

To prepare for the exam I took the famous course by Stephane Mareek. I have to say that it is a very lenghty course, 27 hours I think, and it covers quite a lot of content. THe course basically touches any service that may appear in the exam, so I definetely reccommend doing a run throught it, because there were a lot of services that I either did not know of or I knew some features but not all.

It took me about a month of preparation. Some days I'd study only an hour or less, others I'd spend a few hours.

Initially I started taking notes of every single service, and I even drew a mind map with all the AWS services covered in the exam. 

![](./knowledge_map.png)

I now know this is the best way to approach the learning, because all the services that you are not familiar with just mix up in your head.

The best way is to do hands on if you can, and try the services yourself. This is the only way that things will stick in your brain for good.

I remember a quote from someone, that said something like "If I can't implement it, I don't understand it". 

However, this might not be possible for all of us, and in fact some services like VPNs, AWS organisations etc are not the kinds of things that you setup on your personal AWS account. 

My reccommendation then is to buy the other course with the preparation exams, which has 5 practice exams of similar difficulty to the real exam. By going through the questions you realise all the gaps that you have in the different services, and then you can go and read about it in more detail in the documentation.

The exam will test you on little details like "[KMS keys on bucket level or object level](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-key.html)" that the course may not cover.


## Exam day

On the exam day you'll need to check in 30 mins before the exam. The check in process can take a good 20 mins, even more if you do not have the secure browser software already installed.

You will be recorded throughout the whole session, and you will be asked to show some pictures of your desk and your room. 

Thankfully they don't make you get rid of any books in the room like in the Kubernetes exam, as long as they are not within arms reach. I was also able to run the exam with my dogs walking around, so that was nice.

## Exam Topics

Some of the exam topics that I remember. This list does not inculde all

- AWS Recycle Bin for accidental deletes and retention  
- AWS Backups  
- Elastic Disaster Recovery  
- VPC Endpoints (Interface vs Gateway)  
- EC2, ASG, and ALBs  
- EBS (which option is best)  
- CloudFront and S3 Buckets (use OAC)  
- Global Accelerator (for UDP connections)  
- Kinesis, SQS, SNS, Firehose, Athena  
- S3 and KMS Keys (Bucket Keys, Object Keys)  
- S3 Replication  
- EFS, and EFS to access S3 as a file system with Lustre  
- Cross-Account EFS access
- RDS, Aurora and Database Migrations  
- WAF, AWS Config, GuardDuty  
- AWS Organisations and SCPs  
- Resource-based vs IAM-based Policies  
- Troubleshooting IAM Policies  
- Cognito  
- Questions on PTR and OTR (at least 2) 


## Is the certification worth it

Only if you want it to be.

I have read a lot of stories about people getting the certification without having touched AWS in their life. People get the certification for different reasons of course, but I don't think this has many benefits in practical terms beyond making your CV look nicer.

I believe the best way to approach this, is to have some hands on experience in AWS before attempting the certification. 

For example, I was familiar with autoscaling and load balancing from working with kubernetes, and I also had some previous experience with EC2s. With the certification I've learned so much about how to build services in AWS using Route53, CDN, ELBs, EC2, ASGs as well as the different database options.

Thanks to certification I was able to explore some of these services in depth, that I would otherwise not have done. So now I feel a lot more confident designing end to end architectures in AWS for different use cases.

## What's Next?

It has been a bit intense preparing for this exam. There is a huge amount of content to cover. But it would be silly not to try and and attepmt the Architect Proffessional certification next now that all the knowledge is fresh, so that's the next plan. But we'll see.

If you are interested in getting this certification, feel free to message me on [Linkedin](https://www.linkedin.com/in/lopezsantoripablo/) and I'll be happy to answer any questions.

Have a nice day!
