# Open-Source Modern Data Stack Pipeline

## 📖 Project Overview
This project is an end-to-end batch data pipeline built entirely with free, open-source tools running locally via Docker. It takes raw e-commerce data, stores it in a local data lake, loads it into a data warehouse, and transforms it into analytics-ready tables.

**Dataset:** [Olist Brazilian E-Commerce Dataset (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

---

## 🛠️ The Tech Stack
* **Docker Compose:** Containerizes and runs all services locally.
* **Apache Airflow:** Orchestrates the entire pipeline (scheduling and running tasks).
* **MinIO:** An open-source, S3-compatible object store acting as our Data Lake (Bronze Layer).
* **PostgreSQL:** Acts as our local Data Warehouse (Silver & Gold Layers).
* **dbt-core:** Handles data transformation, converting raw tables into a clean star schema.

---

## 🗺️ Step-by-Step Implementation Plan

### Step 1: Infrastructure Setup (Day 1)
Instead of installing these tools directly on your OS, you will use a single `docker-compose.yml` file to spin them up simultaneously.
* **Goal:** Have Airflow (webserver & scheduler), a Postgres database, and a MinIO server running locally.

### Step 2: Ingestion to Data Lake (Day 1)
You will write your first Airflow DAG (Directed Acyclic Graph) in Python.
* **Goal:** The DAG downloads the Olist CSV files and uploads them into a MinIO bucket (e.g., a bucket named `raw-data`).

### Step 3: Loading into the Warehouse (Day 2)
You will write a second Airflow DAG (or add tasks to the first one).
* **Goal:** Airflow reads the CSV files from MinIO and inserts the data into raw tables inside your PostgreSQL database. This mimics the EL (Extract & Load) part of ELT.

### Step 4: Data Transformation with dbt (Day 2 - 3)
You will initialize a `dbt` project that connects to your PostgreSQL database.
* **Goal:** Write SQL `SELECT` statements in dbt to clean the data and organize it into a Star Schema (e.g., `fact_orders`, `dim_customers`, `dim_products`). dbt will automatically handle the creation of these tables/views in Postgres.

---

## 🤖 How to Build This Fast (AI Prompting Guide)

Since you are using AI to speed up development, here is how you should prompt your AI model step-by-step to avoid getting overwhelmed:

1. **Prompt 1 (Infra):** *"Write a `docker-compose.yml` file that spins up Apache Airflow, MinIO, and a PostgreSQL database. Include all necessary environment variables and volumes."*
2. **Prompt 2 (Ingestion):** *"Write an Airflow DAG in Python that takes a local folder of CSV files and uploads them to a MinIO bucket using the `S3Hook`."*
3. **Prompt 3 (Loading):** *"Write an Airflow task that reads CSV files from MinIO and uses pandas or psycopg2 to insert the data into raw PostgreSQL tables."*
4. **Prompt 4 (dbt):** *"I have raw tables in Postgres for customers, orders, and payments. Give me the dbt SQL models to transform this into a Star Schema."*

---

## 🎯 Why This Will Look Great on Your CV
Once finished, you can add bullet points like this to your resume:
* *Architected a local ELT Modern Data Stack using Docker, orchestrating data pipelines with Apache Airflow.*
* *Engineered a Medallion architecture, migrating data from a MinIO object store to a PostgreSQL data warehouse.*
* *Transformed raw relational data into an analytics-optimized Star Schema using dbt (data build tool), enforcing data quality and modular SQL design.*
