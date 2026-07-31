# System Architecture — Crypto Analytics Platform

This document records the architectural design, technical decisions, and component structure of the cryptocurrency analytics pipeline.

---

## 1. Extraction Layer and Data Models

### 1.1 HTTP Extractor (`src/extractors/coingecko.py`)
The extraction layer is responsible for querying the public CoinGecko REST API and obtaining real-time market metrics.

* **Client**: `httpx.Client` is used to make HTTP requests in a clean and configurable way.
* **Endpoint**: `GET /api/v3/coins/markets`
* **Parameters**:
  * `vs_currency`: Reference currency (default `"usd"`).
  * `ids`: Comma-separated list of cryptocurrency identifiers (e.g., `"bitcoin,ethereum"`).
* **Headers**: A custom `User-Agent` (`crypto-analytics-platform/0.1.0`) is sent to avoid blocks due to basic rate-limiting.
* **Resilience**: HTTP exceptions are captured using `response.raise_for_status()`.

### 1.2 Validation Model (`src/models/price_record.py`)
Guarantees the integrity of the extracted data before being processed by subsequent layers of the pipeline.

* **Library**: `pydantic` (v2).
* **Schema**:
  * `coin_id` (`str`): Unique asset identifier (e.g., `"bitcoin"`).
  * `symbol` (`str`): Lowercase ticker symbol (e.g., `"btc"`).
  * `name` (`str`): Full asset name.
  * `current_price` (`float`): Current price in the reference currency.
  * `market_cap` (`float`): Market capitalization.
  * `total_volume` (`float`): Total volume traded in 24h.
  * `price_change_24h` (`float | None`): 24-hour percentage variation (optional/nullable field).
  * `fetched_at` (`datetime`): Exact timestamp of the extraction (in UTC timezone).

---

## 2. Transformation Layer

### 2.1 Polars Transformer (`src/transformers/price_transformer.py`)
Converts validated `PriceRecord` instances into structured analytical DataFrames.

* **Engine**: Polars (used for high-performance, memory-efficient data processing).
* **Technical Indicators**: Calculates indicators using native Polars expressions (`ewm_mean`, `rolling_mean`, `rolling_std`).
  * `macd` & `macd_signal`
  * `bb_upper` & `bb_lower` (Bollinger Bands)
  * `rsi_14`
* **Handling Missing Data**: Gracefully handles missing historical data (yielding nulls) without crashing the pipeline when only a few records exist.

---

## 3. Storage and Data Warehouse Layer

### 3.1 BigQuery Analytics (`src/loaders/bigquery_loader.py`)
The final destination for all transformed analytical records.

* **Mode**: Upsert (Update/Insert) based on the asset ID and timestamp to prevent duplicate records.
* **Schema Evolution**: Handled externally via Terraform IaC (`infra/`).
* **Format**: Polars DataFrames are converted natively via PyArrow before being loaded into BigQuery for maximum I/O performance.

### 3.2 GCS Fallback Archive (`src/loaders/gcs_loader.py`)
An immutable raw data lake storing the exact JSON payloads obtained from the Extractors.

* **Resilience**: Designed to **never** raise exceptions on failure (network issues, missing credentials, bucket absence). Instead, it logs a warning via the Airflow logger and returns a boolean status, allowing the downstream BigQuery analytical load to continue unharmed.

---

## 4. Orchestration Layer (Apache Airflow)

### 4.1 Daily Pipeline DAG (`src/dags/crypto_daily_pipeline.py`)
* **Framework**: Airflow 3.x using the modern **TaskFlow API** (`@task` decorators).
* **State Management**: Uses native **XComs** implicitly to pass data between the extraction, GCS loading, and transformation layers.
* **Topology**:
  1. `extract_market_data`
  2. `load_raw_to_gcs` (Resilient branch)
  3. `transform_market_data`
  4. `load_transformed_to_bigquery`

---

## 5. Architectural Decision Records (ADRs)

### ADR-001: Selection of Synchronous HTTP Client (`httpx`)
* **Status**: Approved.
* **Context**: Data needs to be extracted periodically from Airflow.
* **Decision**: Use synchronous `httpx.Client` instead of `asyncio`/`aiohttp`.
* **Consequences**: Simplifies extraction code within Airflow operators without adding the overhead of asynchronous event loops for small batch requests.

### ADR-002: Strict Schema Validation with Pydantic v2
* **Status**: Approved.
* **Context**: External API data can change or contain unexpected nulls.
* **Decision**: Map the JSON response immediately to Pydantic `PriceRecord` models.
* **Consequences**: Prevents propagation of corrupt data to the transformation and storage layers (BigQuery/GCS).

### ADR-003: Selection of Polars over Pandas for Data Transformation
* **Status**: Approved.
* **Context**: The pipeline requires high-speed calculations for technical indicators across multiple cryptocurrency time-series.
* **Decision**: Adopt Polars due to its Rust-based engine, multi-threading capabilities, and strict schema enforcement.
* **Consequences**: Significantly faster execution times and lower memory footprint compared to Pandas, but requires adopting the Polars Expression API syntax.

### ADR-004: TaskFlow API and XComs for Data Passing
* **Status**: Approved.
* **Context**: Passing large amounts of data between tasks was traditionally an anti-pattern in Airflow.
* **Decision**: Use Airflow's TaskFlow API to implicitly pass dictionaries between `extract` and `transform` tasks.
* **Consequences**: Simplifies DAG syntax drastically compared to classic `PythonOperator`. Since our crypto payloads are small (<1MB JSONs), default XCom limits are not a bottleneck.

### ADR-005: Optional Resiliency for GCS Archive
* **Status**: Approved.
* **Decision**: The GCS raw archive is a "nice-to-have" historical backup, while BigQuery is the critical path. Therefore, `GCSLoader` must catch all exceptions and degrade gracefully instead of failing the DAG run.
