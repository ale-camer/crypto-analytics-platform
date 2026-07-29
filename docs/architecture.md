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

## 2. Architectural Decision Records (ADRs)

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
