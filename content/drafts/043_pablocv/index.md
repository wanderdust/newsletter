
---
title: 'CV'
date: '2026-02-12T10:58:58Z'
draft: false
summary: ''
tags: []
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---
# Pablo Lopez Santori

Edinburgh, UK | [pablo.lopez.santori@gmail.com](mailto\:pablo.lopez.santori@gmail.com)
| [github.com/wanderdust](https://github.com/wanderdust) | [wanderdust.github.io/newsletter](https://wanderdust.github.io/newsletter/posts/)

## Summary

AI and Machine Learning Engineer with 6+ years of experience building production AI systems, from LLM-powered agents and RAG pipelines through to model training, MLOps, and ML feature platforms. Strong background in AWS, Bedrock, and Kubernetes, with hands-on experience across agentic AI, deep learning, model serving, and operational excellence. Comfortable working across the stack, from data engineering and backend APIs to scalable model deployment and monitoring.

## Experience

### FanDuel: Senior Platform Engineer

Nov 2025 to today | Edinburgh, UK (remote)

- Built and deployed an internal AI Q&A assistant using Amazon Bedrock, AWS Knowledge Base, and a RAG pipeline with document chunking and Elasticsearch-backed retrieval. Applied prompt engineering techniques and Bedrock Guardrails for content safety; used pydantic AI for structured responses and tool definitions. Deployed as a serverless API on AWS Lambda with Amazon API Gateway, documentation hosted on S3.
- Evaluated output quality using an LLM-as-judge framework against a curated Q&A dataset sourced from Slack support threads. Logged traces and API activity to Datadog for observability and alerting; stored conversations in S3 for analysis with Athena. Adopted across multiple platform consumer teams and iteratively improved based on user feedback.
- Architected and implemented the Spec Driven Development Lifecycle, an AI-assisted development framework adopted across all data teams, leveraging LLM-based code generation and review to standardise how pipelines are built and reduce time to deployment.
- Led the first phase of the fraud risk platform, building a batch pipeline to make transaction data available at the ML feature API within 30 minutes. Built a reusable reverse ETL library into PostgreSQL that is now used by multiple engineering teams for similar workloads.
- Contributed to the subsequent real-time fraud risk API backed by Redis and AWS MemoryDB, enabling data science-owned models to score transactions within a second of a transaction occurring.
- Led the platform observability programme, establishing frameworks that define what to monitor, how to monitor it, and how to respond, replacing noisy alerting with actionable signals.
- Drove the Spark Runtime upgrade programme across 100+ pipelines, keeping the platform aligned with LTS releases and eliminating infrastructure debt at scale.
- Led the Salesforce-to-Databricks data migration end to end, partnering with stakeholders to define requirements, document outcomes, and broaden data access for teams that previously had no visibility into that data.

### FanDuel: Platform Engineer

Sep 2023 to Nov 2025 | Edinburgh, UK (remote)

- Reduced Kubernetes infrastructure costs by £60k annually by improving resource monitoring in Datadog, aligning allocated resources to real usage patterns across the cluster.
- Contributed to platform architecture from day one through production rollout, building a self-service API platform on Python, AWS, Terraform, Kubernetes, Kong, Trino and PostgreSQL that serves as the data access layer for ML feature retrieval and latency-sensitive inference workloads.
- Optimised PostgreSQL performance through partitioning strategies, data modelling, index design, and read/write replica management, reducing critical API query latency to millisecond response times. Validated latency requirements under load using a reusable Locust-based performance testing framework.
- Led technical delivery on platform initiatives including a GraphQL API layer and a reverse ETL migration from Databricks to PostgreSQL to serve high-throughput query patterns.
- Reduced time to troubleshoot production incidents from hours to minutes by building internal tooling that gave the team the ability to investigate and recover EKS environments independently.

### Zonda Satellite: Machine Learning Engineer

Nov 2020 to Sep 2023 | Glasgow, UK (remote)

- Built a semantic property search API using LangChain, OpenAI embeddings, Pinecone and Elasticsearch, enabling users to find properties via free-text or image input, with an LLM generating structured search queries from natural language.
- Built and deployed a Stable Diffusion model generating photorealistic facade images from architectural drafts, served via a FastAPI REST API on AWS Lambda.
- Improved construction activity tracking from satellite imagery using MaskRCNN in PyTorch, raising model performance from 0.3 to 0.7 mAP through image augmentation, hyperparameter tuning, ensemble modelling and targeted data labelling. Developed a novel image oversampling technique that raised per-sample prediction accuracy from ~60% to ~90%.
- Built a property valuation model using regression techniques, deployed as a FastAPI service on AWS with full observability and monitoring. Adopted into the core pricing workflow used daily by internal consultants, reducing valuation time from hours to minutes. Co-inventor on a resulting USPTO patent.
- Created a reusable MLOps framework using AWS SageMaker and MLflow to standardise model deployment, with Grafana-based monitoring across model serving APIs and pipelines covering latency, error rates and execution.

### KLU: AI Engineer Contractor

Mar 2023 to Aug 2023 | Remote

- Fine-tuned Alpaca 7B and 13B on a custom dataset using GPU-accelerated distributed training, with an end-to-end MLOps pipeline on AWS (S3, DVC, Weights and Biases, Terraform, SageMaker) for automated versioning, reproducibility and deployment.
- Designed an LLM evaluation framework using GPT-4 as an automated evaluator to benchmark frontier models against each other across tasks, enabling fast and data-driven model selection decisions.


### Earlier

- UserTesting: Data Science Intern, Jun 2020 to Aug 2020. Built an unsupervised NLP model to flag inconsistent screener responses and shipped a small React interface to help QA review cases faster.

## Projects

**Coding Agent** - Built an LLM-powered coding agent from scratch: a CLI tool that autonomously reads, edits, and tests code via a multi-step tool-use loop, similar in design to Claude Code. Built in Python using the Anthropic API and pydantic AI for tool definitions and structured outputs; capable of autonomously adding unit tests to existing functions. [Write-up](https://medium.com/ai-in-plain-english/from-llm-to-agent-building-your-own-coding-agent-867844f3c002)

**Deep Q-Learning - Space Invaders** - Implemented a Deep Q-Network agent in PyTorch to play Space Invaders from raw pixels, using experience replay, target networks, and epsilon-greedy exploration. [GitHub](https://github.com/wanderdust/reinforcement-learning/tree/main/reinforcement_learning/deep_q_learning)

## Education

- MSc, Artificial Intelligence with Speech and Multimodal Interaction, Heriot Watt University, Edinburgh, 2020
- Degree in Commerce, Complutense University of Madrid, 2016

## Patent

- Co-inventor, Systems and Methods of Property Valuation, USPTO, Aug 2022

## Certifications

- AWS Certified Solutions Architect Professional
- AWS Certified Solutions Architect Associate
- Certified Kubernetes Application Developer
- Databricks Certified Data Engineer Professional

## Speaking and Writing

- Datalab Scotland panel on ML trends and platform engineering. Invited speaker. Organised Datalab hackathon hosted at FanDuel.
- Talks on Diffusion Models and Large Language Models for mixed technical and non technical audiences at EdAI and Pint of Science.
- Maintain a technical blog covering Kubernetes, AWS, database indexing, Reverse ETL, PostgreSQL best practices, and AI.

## Skills

ML and AI: PyTorch, scikit-learn, MLflow, AWS SageMaker, LangChain, pydantic AI, Pinecone, LLM fine-tuning, Stable Diffusion, computer vision, FastAPI model serving.

Infra and ops: AWS, Bedrock, Kubernetes, Terraform, CI/CD, performance testing, monitoring and alerting.

Data platforms: Databricks, Trino, Redshift, Postgres, Snowflake, reverse ETL, streaming and batch connectors.

Backend and APIs: Python, FastAPI, Kong, GraphQL, REST, security and performance considerations.

Leadership and strategy: platform roadmaps, cross team alignment, migration planning, stakeholder communication, mentoring and hiring.
