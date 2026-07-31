# 🪙 Crypto Analytics Platform

> **P-02** — Cryptocurrency analytics pipeline with **Polars**, **GCP BigQuery**, **Apache Airflow**, and **Terraform**.
> Status: ✅ Completed v1.0

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)](https://python.org)
[![Polars](https://img.shields.io/badge/Polars-🐻‍❄️-orange)](https://pola.rs)
[![GCP](https://img.shields.io/badge/GCP-BigQuery%20%7C%20GCS-blue?logo=google-cloud)](https://cloud.google.com)
[![Airflow](https://img.shields.io/badge/Airflow-3.x-red?logo=apache-airflow)](https://airflow.apache.org)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-purple?logo=terraform)](https://terraform.io)

---

## 📋 Description

This project is an automated, end-to-end data pipeline (ETL) built for the daily extraction, transformation, and analysis of cryptocurrency prices and indicators. It is designed with a strong focus on **resilience**, **scalability**, and **high-performance in-memory processing**.

The pipeline orchestrates daily ingestion from public APIs (such as CoinGecko), calculates technical indicators (MACD, RSI, Bollinger Bands) using **Polars**, archives an immutable backup in JSON format on **Google Cloud Storage (GCS)**, and performs the final analytical load into **Google BigQuery**.

---

## 🏗️ Architecture

```mermaid
graph TD
    A[External APIs<br/>CoinGecko] -->|Extract| B(Airflow DAG<br/>TaskFlow API)
    B -->|XCom| C{Transformation<br/>Polars}
    B -.->|Resilient Backup| D[Google Cloud Storage<br/>Raw JSON Archive]
    C -->|Load| E[(BigQuery<br/>Data Warehouse)]
```

> Detailed architecture, ADRs, and technical decisions: [docs/architecture.md](docs/architecture.md)

---

## 🚀 Quickstart (Local Execution)

To run this project in your local environment with unit or integration tests:

```bash
# 1. Clone the repository
git clone https://github.com/your-username/crypto-analytics-platform.git
cd crypto-analytics-platform

# 2. Create and activate the virtual environment (REQUIRED)
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies (including dev)
pip install -e ".[dev]"

# 4. Environment Variables
cp .env.example .env
# Edit .env and configure your GCP_PROJECT_ID and GOOGLE_APPLICATION_CREDENTIALS
```

### Running Airflow Locally
To see the Airflow UI and run the DAG manually:
```bash
airflow standalone
```
*Then open `http://localhost:8080` in your browser.*

---

## 🏆 Milestones Achieved

The project was built in 3 iterative phases using GitFlow:

1. **Phase 1: Extraction & Transformation**
   - HTTP connector for CoinGecko.
   - Robust schema validation using **Pydantic v2**.
   - Transformation engine using **Polars** for lightning-fast financial calculations.

2. **Phase 2: Data Warehouse & Orchestration**
   - Infrastructure as Code (IaC) on GCP using **Terraform**.
   - Implementation of loaders and automatic upserts to BigQuery.
   - DAG design using the modern **Apache Airflow 3.x TaskFlow API**.
   - E2E integration tests using `dag.test()`.

3. **Phase 3: Fallback Archive & Resilience**
   - Resilient `GCSLoader` for raw storage.
   - Comprehensive exception handling and Airflow logging connection (preventing DAG failures due to GCS connection errors).

---

## 📁 Project Structure

```text
crypto-analytics-platform/
├── pyproject.toml      # Dependencies and config
├── src/
│   ├── extractors/     # HTTP Connectors
│   ├── transformers/   # Polars logic
│   ├── loaders/        # GCS and BigQuery loaders
│   ├── models/         # Pydantic models
│   └── dags/           # Airflow DAGs (crypto_daily_pipeline.py)
├── tests/
│   ├── unit/           # DAG Validation, GCSLoader tests
│   └── integration/    # E2E pipeline tests
├── infra/              # Terraform scripts for GCP
└── docs/               # Architecture ADRs and issue logs
```

---

*Data/AI Engineering Portfolio — Alejandro Camerlengo*
