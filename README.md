# 🪙 Crypto Analytics Platform

> **P-02** — Pipeline de analytics de criptomonedas con **Polars**, **GCP BigQuery**, **Apache Airflow** y **Terraform**.
> Estado: 🔄 En construcción — Día 0 (Scaffolding)

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)](https://python.org)
[![Polars](https://img.shields.io/badge/Polars-🐻‍❄️-orange)](https://pola.rs)
[![GCP](https://img.shields.io/badge/GCP-BigQuery%20%7C%20GCS-blue?logo=google-cloud)](https://cloud.google.com)
[![Airflow](https://img.shields.io/badge/Airflow-2.x-red?logo=apache-airflow)](https://airflow.apache.org)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-purple?logo=terraform)](https://terraform.io)

---

## 📋 Descripción

Pipeline de datos end-to-end para extracción, transformación y análisis de precios de criptomonedas.

---

## 🏗️ Arquitectura Propuesta

```
APIs Externas (CoinGecko / Binance)
          │
          ▼
  ┌─────────────────┐
  │  Airflow DAG    │  ← Orquestación diaria
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │     Polars      │  ← Transformación in-memory
  └────────┬────────┘
           │
     ┌─────┴──────┐
     ▼            ▼
  ┌──────┐   ┌──────────┐
  │ GCS  │   │BigQuery  │
  │(Raw) │   │  (DWH)   │
  └──────┘   └──────────┘
```

> Arquitectura detallada: [docs/architecture.md](docs/architecture.md)

---

## 🚀 Quickstart

```bash
# 1. Clonar
git clone https://github.com/tu-usuario/crypto-analytics-platform.git
cd crypto-analytics-platform

# 2. Entorno virtual (OBLIGATORIO)
python3 -m venv .venv
source .venv/bin/activate

# 3. Dependencias de desarrollo
pip install -e ".[dev]"

# 4. Variables de entorno
cp .env.example .env
# Editar .env con credenciales reales
```

---

## 📁 Estructura

```
crypto-analytics-platform/
├── .venv/              # Entorno virtual (no en git)
├── .env.example        # Template de variables
├── pyproject.toml      # Dependencias y configuración
├── dags/               # DAGs de Airflow (Issue #4)
├── src/
│   ├── extractors/     # Conectores API (Issue #1)
│   ├── transformers/   # Lógica Polars (Issue #2)
│   ├── loaders/        # GCS + BigQuery (Issue #3)
│   ├── models/         # Pydantic models (Issue #1)
│   └── utils/          # Utilidades compartidas
├── tests/
│   ├── unit/
│   └── integration/
├── infra/              # Terraform (Issue #3)
└── docs/
    ├── architecture.md
    └── issue_0_setup.md
```

---

## 🗺️ Roadmap de Issues

| Issue | Título | Rama |
|-------|--------|------|
| #0 | Setup inicial & scaffolding | `feature/day-0-setup` |
| #1 | Extractor CoinGecko + modelos Pydantic | `feature/issue-1-extractor` |
| #2 | Transformaciones Polars | `feature/issue-2-transform` |
| #3 | BigQuery Loader + Terraform | `feature/issue-3-loader` |
| #4 | DAG Airflow completo + tests | `feature/issue-4-airflow` |
| #5 | GCS Archive resiliente | `feature/issue-5-gcs` |

---

## 🛠️ Stack

| Capa | Tecnología |
|------|-----------|
| Orquestación | Apache Airflow 2.x |
| Transformación | Polars |
| Raw Storage | Google Cloud Storage |
| Analytics DWH | Google BigQuery |
| IaC | Terraform ≥ 1.5 |
| Validación | Pydantic v2 |

---

*Portfolio de Data/AI Engineering — Alejandro Camerlengo*
