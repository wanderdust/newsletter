---
title: 'Interviewing Makes you More Competent at your Job'
date: '2025-10-06T08:01:22+01:00'
draft: false 
summary: ''
tags: ["career", "reflections"]
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---

Interviewing for other jobs in tech can make you a more competent engineer. My premise for this argument is that when you prepare an interview for a new role you need to prepare to answer questions, technical and non-technical, in a domain that is different from your day to day work. This forces you to step out of your daily work and read and think about different domains and technologies. During the interview process you will get an idea of how well you performed, whether that is via self reflection, or feedback from the emloyer. This gives you a pretty good idea of where you are lacking knowledge and a good direction of where to focus next.


This makes the interviewing process a great excercise to do on a regular basis, even when you are happy with your role and are not looking for a move. I find this to be useful at the mid-senior level where I'm currently at, but it may or may not apply at the higher levels. This excercise can be particularly helpful when you find yourself in a role for some time and you take most of the tech for granted, and you don't know where to look for to continue your professional development.

I can share my experience on this. In the last year I've interviewed for a couple of roles, one internally and one externally. In both cases I came out of it having pushed myself to learn new things that I would not have looked into if it wasn't for the interviews.

In the first interview, I was interviewing for a MLOps role. One of the tech interviews involved designing an architecture for a notification system. Before this, I had never really spent much time thinking about designing larger scale systems, thinking about scalability, security, failover etc. To prepare for this interview, I had to open the "Designing Data Intensive Applications" book to refresh on some of the concepts of distributed systems. As part of this learning process, I started to think about the current systems that we built internally, and how these concepts I was learning about apply to the existing infrastructure.

For example, we run Aurora Postgres with Replication as one of the more critical parts of our infrastructure. But I had never stopped to think how replication works. It was there before I arrived in this job, and never really looked into how Postgres scales or handles high availability. Or where Postgres falls in short in our current infrastructure. Most of my job involved connecting to postgres, writing indexes, running queries, but never really thinking about its architecture.

After the interview I got some feedback, where they mentioned I didn't speak enough about scalability, which is why I didn't get the job. This is where I started thinking about the topic more and more. Thinking about the diagram I wrote, where I could have improved it or spoke about tradeoffs. I started to look into Postgres, as a starting point and learned about the idea behind replication and the different types (active-active vs primary-follower). I also looked into how High Availability is achieved, and the tradeoffs to consider to achieve it. I started learning about partitioning and sharding, when it becomes useful, and when it is not.

And the beauty about all of this, is that the same concepts apply to most systems, and not only for databases. The ideas behind how to achieve availability, failover, scalability etc to any system is pretty much the same!

The outcome of this first interview was that I became a lot more aware of the architecture of the systems I work with in my current role, feeling like I could make more informed architectural decisions. This learning process was triggered by the interview.

The second interview I went through, was for an internal role in my existing company. The interview was in the format of trying to debug an issue in AWS, by role playing with the interviewers. In this interview, I had to navigate several AWS services to find what was causing a 503 error in an API. I had to navigate through Route53, Cloudfront, ALB and EC2s. Some of these services I was more familiar with than others, and although I managed to navigate myself to finding out what the issue was, I was unable to answer some basic questions about some of these services. 

Even though I have about 5 years experience in AWS and I felt pretty confident about my knoweledge, the feedback I recieved was that they were looking for someone with more AWS experience. I thought I knew AWS fairly well, and some of these services I had used in the past, however I used them as a means to and end, without ever spending any time understanding how these services work.

One part of the feedback from the interviewer, was to consider doing the AWS Solutions Architect Associate exam. I thought this was a great way to spend my 10% professional development time at work preparing for this, since I was not using it for anything else. While it is true that AWS certifications are mostly a marketing scheme for you adopt AWS and its services, it also exposes you to consider best practices, and to think about developing end to end systems in ways that scale, are secure, are fast, reliable, cost efficient or whatever the question is asking for. Despite having to think in AWS terms, a lot of the concepts such as streaming, decoupling, scalability etc are useful when thinking about system design, independently of whether you are doing it with AWS or not. The worst part is having to learn all the boring managed services that are only relevant within AWS.

The outcome of this interview has been acquiring the AWS certification. I feel a lot more confident in AWS, I know a bunch more services I wasn't aware of, and it's made me more confident about designing "better" systems, making more intelligent decisions about tradeoffs, and how to achieve good levels of security, scalability and reliability in the cloud.

From a personal level, the AWS cert, has made me think outside cloud architecture and want to explore on-prem architectures in more details. I am currently in the process of self hosting my own home lab, with K3s and a home built Network Attached Storage (NAS), which I would never have thought of it it wasn't for this certification.

Interwieving will highlight where you are missing knowledge and motivate you to fill in the gaps, which will make you a more competent at your current job, assuming they don't make you an offer and you leave. So, to keep me on my toes, I will keep applying for jobs every once in a while, even when I'm not strictly looking to leave.


---

_Note: This blog is one of my first attempts at publishing something with minimal edits. I tend to over-edit my writting and I feel like my voice is often lost in the process. This is something I want to continue trying in the future, so hopefully practice makes better. Also, I write my blog in NeoVim, so if anyone has any suggestions about grammar checkers in the terminal, give me shout, because I've not found anything good as of yet._
