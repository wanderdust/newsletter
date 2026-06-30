
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

Machine Learning Engineer with 6+ years of experience building and deploying production ML systems at scale, across the full lifecycle from model training and data pipelines to cloud infrastructure and inference APIs. Strong background in AWS, Kubernetes and MLOps, with hands-on experience across deep learning, model serving, observability and operational excellence. Comfortable working across the stack, from data engineering and backend APIs to scalable model deployment and monitoring.

## Experience

### FanDuel: Senior Platform Engineer

Nov 2025 to today | Edinburgh, UK (remote)

- Led the first phase of the fraud risk platform, building a batch pipeline to make transaction data available at the ML feature API within 30 minutes. Built a reusable reverse ETL library into PostgreSQL that is now used by multiple engineering teams for similar workloads.
- Contributed to the subsequent real-time fraud risk API backed by Redis and AWS MemoryDB, enabling data science-owned models to score transactions within a second of a transaction occurring.
- Led the platform observability programme, establishing frameworks that define what to monitor, how to monitor it, and how to respond, replacing noisy alerting with actionable signals.
- Architected and implemented the Spec Driven Development Lifecycle, an AI-assisted development framework adopted across all data teams, standardising how pipelines are built and reducing time to deployment.
- Drove the Spark Runtime upgrade programme across 100+ pipelines, keeping the platform aligned with LTS releases and eliminating infrastructure debt at scale.
- Led the Salesforce-to-Databricks data migration end to end, partnering with stakeholders to define requirements, document outcomes, and broaden data access for teams that previously had no visibility into that data.

### FanDuel: Platform Engineer

Sep 2023 to Nov 2025 | Edinburgh, UK (remote)

- Reduced Kubernetes infrastructure costs by £60k annually by improving resource monitoring in Datadog, aligning allocated resources to real usage patterns across the cluster.
- Contributed to platform architecture from day one, from early design decisions through production rollout. Core stack included Python, AWS, Terraform, Kubernetes, Kong, Trino and PostgreSQL.
- Optimised PostgreSQL performance through partitioning strategies, data modelling, index design, and read/write replica management, reducing critical API query latency to millisecond response times.
- Built a reusable performance testing framework using Locust to validate API latency requirements under production-level load, making performance testing a repeatable part of the release process.
- Led technical delivery on platform initiatives including a GraphQL API layer and a reverse ETL migration of operational data from Databricks to PostgreSQL to serve high-throughput query patterns.
- Reduced time to troubleshoot production incidents from hours to minutes by building internal tooling that gave the team the ability to investigate and recover EKS environments independently.
- The API platform serves as the data access layer for ML feature retrieval and model serving, supporting latency-sensitive inference workloads at production scale.

### Zonda Satellite: MLOps Engineer

Jan 2022 to Sep 2023 | Glasgow, UK (remote)

- Built and deployed a Stable Diffusion model that generated photorealistic facade images from hand-drawn architectural drafts, served via a FastAPI REST API on AWS Lambda.
- Built a GAN-based satellite image completion model to generate synthetic training data by filling occluded regions in satellite imagery, used to augment training sets for downstream object detection models.
- Built a semantic property search API using OpenAI embeddings, Pinecone and Elasticsearch that allowed users to find properties via free-text input, using an LLM to generate structured search queries from natural language.
- Built and maintained the feature data pipelines feeding the online model store, automating periodic data updates from Snowflake into MongoDB via AWS Batch to support similarity search models in production.
- Created a reusable MLOps framework using AWS SageMaker and MLflow to standardise model deployment, reducing time from experiment to production.
- Introduced Grafana-based monitoring across model serving APIs and pipelines, covering latency, error rates and execution, replacing reactive debugging with proactive alerting.
- Built agentic pipelines using LangChain and pydantic AI.
- Mentored an intern on a generative AI project using GANs and Stable Diffusion for 3D object synthesis, collaborating closely with Product and stakeholders throughout.

### Zonda Satellite: Machine Learning Engineer

Nov 2020 to Jan 2022 | Glasgow, UK (remote)

- Improved construction activity tracking from satellite imagery using MaskRCNN in PyTorch, raising model performance from 0.3 to 0.7 mAP through a systematic programme of image augmentation, hyperparameter tuning, loss function experimentation, ensemble modelling and targeted data labelling. Eliminated the need to send drivers to construction sites across the USA, saving thousands of dollars in data collection costs.
- Developed a novel image oversampling technique to address overfitting: decomposed training images into 8x8 feature grids and recombined them to generate synthetic samples, raising per-sample prediction accuracy from ~60% to ~90% while producing a simpler, faster model. Experiments tracked and shared across the team using MLflow.
- Built a property valuation model using regression techniques, working closely with subject matter experts to define requirements and iterate on outputs. Deployed as a FastAPI service on AWS with full observability, testing and monitoring. Adopted into the core pricing workflow used daily by internal consultants, reducing valuation time from hours to minutes. The underlying approach was granted a USPTO patent (co-inventor).
- Deployed deep learning models to AWS Batch for offline prediction workloads, with all model repositories containerised using Docker and shipped via CI/CD with Terraform and AWS CodePipeline.

### KLU: MLOps Engineer Contractor

Mar 2023 to Aug 2023 | Remote

- Fine-tuned Alpaca 7B and 13B on a custom dataset using GPU-accelerated distributed training, optimising inference performance for integration with downstream applications.
- Architected an end-to-end MLOps pipeline on AWS integrating S3, DVC, Weights and Biases, Terraform and SageMaker, enabling automated model versioning, reproducibility and deployment.
- Designed an LLM evaluation framework using GPT-4 as an automated evaluator to benchmark frontier models against each other across tasks, enabling fast and data-driven model selection decisions.
- Built agentic AI pipelines using LangChain, pydantic AI and vector databases.
- Documented and standardised the AI infrastructure for handover to in-house engineering teams.


### Earlier

- UserTesting: Data Science Intern, Jun 2020 to Aug 2020. Built an unsupervised NLP model to flag inconsistent screener responses and shipped a small React interface to help QA review cases faster.

## Education

- MSc, Artificial Intelligence with Speech and Multimodal Interaction, Heriot Watt University, Edinburgh, 2020
- Degree in Commerce, Complutense University of Madrid, 2016

## Certifications

- AWS Certified Solutions Architect Professional
- AWS Certified Solutions Architect Associate
- Certified Kubernetes Application Developer
- Databricks Data Engineer Professional
- Databricks Data Engineer Associate
- Astronomer Certification for Apache Airflow Fundamentals

## Speaking and Writing

- Datalab Scotland panel on data engineering and ML trends. Invited speaker. Organised Datalab hackathon hosted at FanDuel.
- Talks on Diffusion Models and Large Language Models for mixed technical and non technical audiences at EdAI and Pint of Science.
- Maintain a technical blog covering Kubernetes, AWS, database indexing, Reverse ETL, PostgreSQL best practices, and AI.

## Patent

- Co inventor, Systems and methods of property valuation, Aug 2022

## Skills

ML and AI: PyTorch, scikit-learn, MLflow, AWS SageMaker, LangChain, pydantic AI, Pinecone, LLM fine-tuning, Stable Diffusion, computer vision, FastAPI model serving.

Infra and ops: AWS, Kubernetes, Terraform, CI/CD, performance testing, monitoring and alerting.

Data platforms: Databricks, Trino, Redshift, Postgres, Snowflake, reverse ETL, streaming and batch connectors.

Backend and APIs: Python, FastAPI, Kong, GraphQL, REST, security and performance considerations.

Leadership and strategy: platform roadmaps, cross team alignment, migration planning, stakeholder communication, mentoring and hiring.
