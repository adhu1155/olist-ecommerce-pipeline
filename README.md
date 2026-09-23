# Olist E-Commerce ELT Pipeline

This repository contains an end-to-end batch data pipeline that processes the Olist Brazilian E-Commerce dataset. I built this to demonstrate a modern, containerized ELT workflow running entirely locally.

## Architecture

The pipeline implements a Medallion architecture (Bronze, Silver, Gold) using the ELT pattern:

1. **Extraction/Load (Bronze):** Raw CSVs are ingested into a local MinIO object storage bucket.
2. **Load (Silver):** Data is extracted from MinIO and loaded into raw PostgreSQL tables.
3. **Transformation (Gold):** `dbt` handles the in-database transformations, converting the raw relational tables into a dimensional Star Schema (Fact & Dimension tables).

All task scheduling and execution is orchestrated via Apache Airflow.

## Tech Stack
- **Apache Airflow:** Orchestration
- **MinIO:** Data Lake / Object Storage
- **PostgreSQL:** Data Warehouse
- **dbt-core:** Data Transformation & Testing
- **Docker Compose:** Local Infrastructure

## Local Setup

### 1. Prerequisites
- Docker and Docker Compose
- The Olist dataset from Kaggle. Extract the CSV files and place them directly in the `/data` directory at the root of this project.

### 2. Infrastructure
Bring up the entire stack using docker-compose:
```bash
docker-compose up -d
```
This will spin up Postgres (mapped to port 5433 on the host), MinIO, and the Airflow webserver/scheduler.

### 3. Running the Pipeline
- Navigate to the Airflow UI at `http://localhost:8080` (admin/admin).
- Unpause and trigger the DAGs in this sequence:
  1. `ingest_to_minio`
  2. `load_to_postgres`
  3. `dbt_transform`

Once completed, you can connect to the local PostgreSQL instance on port `5433` (user: `airflow`, db: `warehouse`) to query the analytics-ready Star Schema (`fact_orders`, `dim_products`, etc.).

## Teardown
To spin down the cluster and preserve data:
```bash
docker-compose down
```
To completely wipe the containers and associated volumes:
```bash
docker-compose down -v
```
