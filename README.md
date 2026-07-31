# 🪙 Crypto Analytics Platform

> **P-02** — Pipeline de analytics de criptomonedas con **Polars**, **GCP BigQuery**, **Apache Airflow** y **Terraform**.
> Estado: ✅ Finalizado v1.0

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)](https://python.org)
[![Polars](https://img.shields.io/badge/Polars-🐻‍❄️-orange)](https://pola.rs)
[![GCP](https://img.shields.io/badge/GCP-BigQuery%20%7C%20GCS-blue?logo=google-cloud)](https://cloud.google.com)
[![Airflow](https://img.shields.io/badge/Airflow-3.x-red?logo=apache-airflow)](https://airflow.apache.org)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-purple?logo=terraform)](https://terraform.io)

---

## 📋 Descripción

Este proyecto es un pipeline de datos (ETL) automatizado, end-to-end, construido para la extracción, transformación y análisis diario de precios e indicadores de criptomonedas. Está diseñado con un enfoque fuerte en **resiliencia**, **escalabilidad** y **procesamiento en memoria de alto rendimiento**.

El pipeline orquesta diariamente la ingesta desde APIs públicas (como CoinGecko), calcula indicadores técnicos (MACD, RSI, Bandas de Bollinger) utilizando **Polars**, archiva un backup inmutable en formato JSON en **Google Cloud Storage (GCS)**, y realiza el volcado analítico final en **Google BigQuery**.

---

## 🏗️ Arquitectura

```mermaid
graph TD
    A[APIs Externas<br/>CoinGecko] -->|Extract| B(Airflow DAG<br/>TaskFlow API)
    B -->|XCom| C{Transformación<br/>Polars}
    B -.->|Backup Resiliente| D[Google Cloud Storage<br/>Raw JSON Archive]
    C -->|Load| E[(BigQuery<br/>Data Warehouse)]
```

> Arquitectura detallada, ADRs y decisiones técnicas: [docs/architecture.md](docs/architecture.md)

---

## 🚀 Quickstart (Ejecución Local)

Para ejecutar este proyecto en tu entorno local con pruebas unitarias o de integración:

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/crypto-analytics-platform.git
cd crypto-analytics-platform

# 2. Crear y activar el entorno virtual (OBLIGATORIO)
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar las dependencias (incluyendo de desarrollo)
pip install -e ".[dev]"

# 4. Variables de entorno
cp .env.example .env
# Editá .env y configurá tu GCP_PROJECT_ID y GOOGLE_APPLICATION_CREDENTIALS
```

Para probar el pipeline completo (mockeado sin base de datos local):
```bash
pytest tests/integration/test_pipeline_e2e.py -v
```

---

## 🏆 Milestones Logrados

El proyecto fue construido en 3 fases iterativas utilizando GitFlow:

1. **Fase 1: Extracción y Transformación**
   - Creación del conector HTTP a CoinGecko.
   - Validación robusta de esquemas de datos usando **Pydantic v2**.
   - Motor de transformación con **Polars** para cálculos financieros ultrarrápidos.

2. **Fase 2: Data Warehouse & Orquestación**
   - Infraestructura como código (IaC) en GCP mediante **Terraform**.
   - Implementación de loaders y upserts automáticos hacia BigQuery.
   - Diseño del DAG utilizando la moderna **TaskFlow API de Apache Airflow 3.x**.
   - Implementación de E2E integration tests usando `dag.test()`.

3. **Fase 3: Fallback Archive & Resiliencia**
   - Creación de un `GCSLoader` resiliente para el almacenamiento crudo.
   - Manejo exhaustivo de excepciones y conexión con el sistema de *Logging* de Airflow (evitando caídas del DAG ante errores de conexión GCS).

---

## 📁 Estructura Principal

```text
crypto-analytics-platform/
├── pyproject.toml      # Dependencias y configuración
├── src/
│   ├── extractors/     # Conectores HTTP a APIs
│   ├── transformers/   # Lógica Polars
│   ├── loaders/        # Loaders GCS y BigQuery
│   ├── models/         # Pydantic models
│   └── dags/           # DAGs de Airflow (crypto_daily_pipeline.py)
├── tests/
│   ├── unit/           # DAG Validation, GCSLoader tests
│   └── integration/    # E2E pipeline tests
├── infra/              # Terraform para GCP
└── docs/               # Architecture ADRs y bitácoras
```

---

*Portfolio de Data/AI Engineering — Alejandro Camerlengo*
