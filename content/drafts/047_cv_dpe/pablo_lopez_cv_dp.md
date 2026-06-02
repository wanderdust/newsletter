# Pablo Lopez Santori

Edinburgh, UK | pablo.lopez.santori@gmail.com | 07851702981 | [Github](https://github.com/wanderdust) | [Blog](https://medium.com/@pablo.lopez.santori)

---

## Summary

Senior Data Platform Engineer with 5+ years in data and platform engineering, including 3 years in a regulated environment. Specialism in Databricks-first stacks: Spark, Airflow, dbt, and Kubernetes at scale. Available for outside IR35 contracts.

---

## Tech Stack

**Cloud:** AWS (Solutions Architect Professional)
**Compute:** Databricks (Data Engineer Professional), Spark, Trino, Kubernetes (CKAD)
**Warehouse / Storage:** Delta Lake, Snowflake, PostgreSQL, DuckDB
**Orchestration:** Airflow (Astronomer certified), Databricks Workflows, dbt
**Data quality:** Monte Carlo, dbt tests, custom Spark validation
**Infra:** Terraform, CI/CD (Databricks bundles, GitHub Actions), Kong, Docker
**Languages:** Python, SQL
**Governance:** Unity Catalog, PII classification, data retention, medallion architecture

---

## Experience

### FanDuel: Senior Data Engineer
Sep 2025 to present | Edinburgh, UK (remote)

- Led the migration of 50 Salesforce CRM tables to Databricks using CDC via Lakeflow managed pipelines. Built 50 ingestion pipelines, coordinated sign-off with business stakeholders across multiple domains, and worked directly with the Databricks product team to resolve connector issues during implementation.
- Built an agentic pipeline development framework: engineer writes a spec and plan, the LLM implements the pipeline, writes tests, runs it in Airflow and Databricks, and opens a PR for review. Measured 60% reduction in implementation cycle time during testing. Approved by the VP of Data and Directors for rollout to engineers across the data division.
- Authors and maintains 50+ Airflow DAGs orchestrating batch and streaming pipelines on Databricks, following a medallion architecture (landing, foundation, core).
- Implemented a multi-layer data quality framework: dbt schema tests and custom Spark validation at ingestion, Monte Carlo for continuous observability, and Datadog alerting for pipeline health.
- Data estate runs end-to-end CI/CD: dbt and unit tests on every PR, Databricks bundles deployed to staging and production on merge, Airflow DAGs synced automatically, and infrastructure changes applied via Terraform in CI.

### FanDuel: Data Platform Engineer
Sep 2023 to Sep 2025 | Edinburgh, UK (remote)

- Helped design and build the self-service Data API Platform from the ground up, through initial architecture, implementation, and production rollout. The platform serves 50+ engineers across 10+ teams at terabyte scale using Trino, Kubernetes, Aurora PostgreSQL, and Kong.
- Reduced Kubernetes costs by ~40% (£60k/year) by instrumenting resource allocation in Datadog and right-sizing cluster configurations.
- Improved PostgreSQL performance through partitioning strategies, index design, and read/write replica management, reducing critical API query latency to millisecond response times.
- Managed production incidents across all platform failure types: pipeline failures, data quality issues, availability events, and compliance/access issues. Reduced resolution time from hours to minutes by building internal diagnostic tooling. Ran formal postmortems and communicated proactively with stakeholders, escalating P1s to senior leadership.
- Built a reusable Reverse ETL framework from Databricks to Postgres, adopted across multiple teams. Predated managed solutions such as Lakebase.
- Investigated a senior leadership request to adopt GraphQL for the platform. Determined it would require platform decentralisation at significant cost and architectural risk. Presented the analysis and recommended against proceeding.
- Built a reusable load testing framework with Locust to validate API latency requirements under production-level traffic.
- Built platform-wide documentation covering all services, APIs, and runbooks for 50+ engineers across 10+ teams, reducing support load and enabling self-service adoption.
- Implemented PII classification and data retention policies at table and column level across pipelines, operating within a regulated data governance framework.

### Zonda Satellite: MLOps Engineer
Jan 2022 to Sep 2023 | Glasgow, UK (remote)

- Led development of a real-time property similarity API, building the full data pipeline from Snowflake through to a served model via AWS Batch, AWS Lambda, and API Gateway.
- Introduced and built the dbt transformation framework as the first implementation at the organisation, establishing consistent pipeline standards across the MLOps workflow.
- Built a reusable MLOps deployment framework on AWS SageMaker and MLflow, reducing the time to move a model from development to production.
- Introduced Grafana-based monitoring for API performance and pipeline execution, with alerting that improved time to detect and resolve issues.
- Mentored an intern on a generative AI project (GANs and Stable Diffusion for 3D object generation), collaborating with Product to keep delivery on track.

### Zonda Satellite: Machine Learning Engineer
Nov 2020 to Jan 2022 | Glasgow, UK (remote)

- Built an object detection model to track new home construction via satellite imagery using PyTorch, MLflow, AWS Batch, Docker, and Terraform.
- Developed a construction progress prediction model using time series data, KNN, and embeddings; deployed via FastAPI.

---

## Earlier

- **KLU, AI Engineer Consultant (Apr–May 2023):** Fine-tuned and benchmarked Alpaca 7B and 13B for a client. Established model training and deployment standards on AWS SageMaker with clear documentation for handover.
- **UserTesting, Data Science Intern (Jun–Aug 2020):** Built an unsupervised NLP model to flag inconsistent screener responses and shipped a React interface to help QA review cases faster.

---

## Education

- MSc, Artificial Intelligence with Speech and Multimodal Interaction, Heriot Watt University, Edinburgh, 2020
- Degree in Commerce, Complutense University of Madrid, 2016

---

## Certifications

- AWS Certified Solutions Architect Professional
- AWS Certified Solutions Architect Associate
- Certified Kubernetes Application Developer
- Databricks Data Engineer Professional
- Databricks Data Engineer Associate
- Astronomer Certification for Apache Airflow Fundamentals

---

## Speaking and Writing

- Datalab Scotland panel on data engineering and ML trends. Invited speaker. Organised Datalab hackathon hosted at FanDuel.
- Talks on Diffusion Models and Large Language Models for mixed technical and non-technical audiences at EdAI and Pint of Science.
- Maintain a technical blog covering Kubernetes, AWS, database indexing, Reverse ETL, PostgreSQL best practices, and AI.

---

## Patent

- [Co-inventor, Systems and Methods of Property Valuation, Jun 2022](https://patents.justia.com/inventor/pablo-lopez-santori)
