---
title: '057_deploy_open_weights_llm_api'
date: '2026-11-09T08:56:30Z'
draft: true
summary: ''
# Valid tags: ai, aws, career, certifications, data-engineering, kubernetes, postgres, reflections, security, serverless, testing, tooling
tags: []
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---

Structure of the blog post

1) Intro: why it makes sense to deploy open weights - (open models are very capable, your data stays within the company)

2) The hardware: RTX, ubuntu server etc, othes specs

3) The LLM: Qwen 4B with tools, llama.cpp API server

4) THe deployment: Kubernetes with K3s, the specs, what the url looks like with the service

5) Calling the deployed model: What it looks like, OPENAPI specs, stateless models, what streaming looks like

6) Hardware conmuption/performance, memory, GPU, idle resources etc

7) Calling the model via PI harness from my laptop to use as coding agent.

8) Commentary on scalability for real prod envs (lots of GPU required, KEDA for proper autoscaling needs), monitoring
