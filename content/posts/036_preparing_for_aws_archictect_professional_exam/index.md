---
title: 'Preparing for the AWS Architech Professional Exam'
date: '2025-11-12T12:06:38Z'
draft: false
summary: ''
tags: ['aws', 'certification']
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---

I have passed the AWS Architect Professional exam with a score of 791/1000!

## Preparing for the AWS exam

I have recently completed the AWS Architect Associate Exam, and I thought the Professional would be a nice next step considering all the prep work I had done. I took about three months between passing the Associate and taking the Professional exam.

For the Associate exam I spent a lot of hours each day going through the course content, writing notes and doing the practice exams multiple times, this time I didn't have the luxury of time. I had to do all of the studying during work hours, where I could only spend about an hour a day (sometimes more, sometimes less), 4 days a week.

At first, I started watching the famous courses from Udemy, but they were quite long, so I stopped quite early and jumped into the practice exams straight away. I knew my exams results would suck, but I used this approach as a way to force me find my knowledge gaps and use the documentation to fill them up.

I also have access to AWS Skill Builder through my work. This was very useful for the self-guided labs on some of the services I had never used, such as Kinesis, VPC Flow Logs, AWS Systems Manager or Deploying an Active Directory in EC2. There were a lot more labs that I wish I had done, but I had to weight the decision between endless studying and taking the exam.

I did a total of 5 practice exams, 3 from Udemy and 2 from Skill bulider. Two of these exams were 20 questions only, so really I've only done 3 full exams. I did all of these exams in practice mode, answering a few questions each day.

These are my scores in the order I took them:
- Udemy 20 sample question practice exam: 73%
- Udemy 75 questions practice exam: 52%
- Udemy 75 questions practice exam 2: 55%
- Skill Builder 20 sample question exam: 90% score
- Skill Bulider 75 questions practice exam: 78%

Based on my Udemy scores I was definitely not ready to take the AWS exam. However, I reviewed every single wrong question carefully to better understand why. Some services I covered in more depth than others.

The most useful resources for learning have been the AWS documentation, the Skill Bulider Labs, and the ChatGPT voice assistant to discuss back and forth topics that weren't very clear in my mind. It was useful to say my understanding of a service out loud, in my own words, and the assistant would clarify the parts I was misunderstanding.

Going to the exam you should have done as many practice tests as you can possibly fit. One reason is because they test you on a lot of topics you may not know about, and it forces you to look it up. The second reason is because is because it gives you plenty of practice in reading long questions to quickly understand what it is asking of you. For the exam, you need to read and process 75 dense questions back to back, the more you practice, the better you get at question comprehension.

## The Exam

It took me about 3 hours an 10 minutes to complete the exam (I had an 30 extra minutes for having English as a second language). The questions are all scenario based and require you to carefully read what's asking of you. Without counting the extra time, on average you get 2 and a half minutes to answer each question. Some were easier than others, so I tried no to overthink the ones the "easier" ones to make sure I had a bit more time to spend on harder and longer ones.

In a lot of cases, multiple answers seemed perfectly reasonable, so you really need to look for clues in the question to see what they are asking of you. Question lenghts can be quite long more often than not, so you need to get good at finding the relevant bits and ignoring the fluff.

Most of the exam felt like educated guess work. I was only very confident about a handful of questions. During the exam you can flag questions to revise later on, I flagged a couple but didn't bother revising at the end. I had 20 minutes to spare at the end which I could have used to revise, but after 3 hours sitting the exam I just wanted to be finished with it. I either I knew the answer or not, and once I gave my best guess I didn't think revising was going to make things any better.


## I Need to pee

This might sound like something very silly, but when I did the AWS Architect Associate Exam, I had the urge to pee half way through the exam, which made answering the last 35 questions very uncomfortable.

This time I had a strategy to not eat or drink anything at least 2 hours before the exam. The exam is 3 hours long (longer if you count the check in process), so make sure you prepare for this sort of thing. You don't want to be distracted because your bodily functions have other priorities.

Alternatively, you can go to a testing center where they will let you use the toilet, but who can be bothered when you have the option to do it at home.

## Mock Exams vs the Real exam

This is something that I wanted to know but I could not really find good answers online. I found the Udemy practice exams to be slightly harder than the real exam. I felt like many of the Udemy practice questions asked about specific details of services that are buried deep in the AWS documentation. In the real exam there are not that many questions that test you on this sort of thing (maybe a few). It makes the Udemy exams a bit annoying and frustrating, but nevertheless it makes for a good learning resource, forcing you to read deep in the docs. As shown above, I barely got over 50% in the practice exams, but still managed to pass the AWS exam.

In the actual exam, there were maybe one or two questions that were almost exactly the same as the practice exams. The rest were either similar topics or very different.

The Skill Builder sample exams are a bit more in-line with the real exam. For both my exams — Associate and Professional — I took the practice test the week before, and the results were more or less in line with what I got in the real exam. I would still say that the actual exam is slightly more challenging, so don't rely too much on this. On the other hand, the 20 sample question practice is either too easy or too hard, but good practice non the less. I found the 20 sample question practice for the Professional certification to be more in line with Associate questions than with Professional questions. And the opposite for the Associate one.

## Exam topics

The exam topics were focused mainly on these areas:
- Migration use cases (Application Migration Service, Migration Hub, AWS DataSync)
- Lots of AWS organisations questions for different services or use cases
- Database questions mostly about RDS (not Aurora) and disaster recovery. Make sure you know well if RDS supports multi-region vs multi-AZ, upgrading replicas to primary etc.
- Backups (AWS Backups etc)
- Lots of tagging questions to ensure tagging consistency in the org with SCPs
- Questions on Networking with Direct Connect, Transit Gateways, VPC, Encryption at edge, Route53
- Lots of questions involving VPC endpoints for various use cases
- Different scenarios about best approach for using different types of EC2/ECS autoscaling, Load Balancing etc
- Varied questions about accessing S3 buckets, Encryption Keys etc
- Lots of ECS related questions with Fargate vs EC2, permissions
- IAM questions for cross acount access of resources
- Some questions about best strategies for cost saving using a mix of reserved instances and other instances
- No ML questions about HPC or Machine Learning or placement groups!

## Difference between Professional and Associate

The Associate covers a wider range of services, with more high level use cases where you need to select the right service. The AWS Professional handles more specific use cases with more subtle differences between responses. It requires more in-depth knowledge about AWS services as well as general knowledge about deployng scalable and secure applications. There is a lot of focus on AWS Organisations, Security and Cost.

For example, where the Associate exam might have a questions about EC2 costs, where the obvious answer might be to use reserved instances, the Professional exam might give you 2 or 3 options where reserved instances is mentioned but with different lenghts (1 year, 3 years) mixed up with other instance types for the use case. You need to carefully understand the business use case to pick the right scenario.

The Professional exam will also expect you to know more about the same services that you learn about in the Associate exam. For example, you are not just expected to know what the transit gateway is used for, but you need to know how to use it in advanced scenarios for using with a centralised VPC for shared resources with private link or VPC isolation using separate route tables.

## Is it worth it?

I guess that depends on each of you. For me, the reason for taking the exam to really prove myself that I was capable. A few months ago I had this strange idea that these sort of certifications were beyond my knowledge or capabilities. Now that I have it, I don't really feel much different, but perhaps I do feel more confident about being called an "expert" in AWS.
