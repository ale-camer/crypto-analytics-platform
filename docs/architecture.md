# Arquitectura del Sistema — Crypto Analytics Platform

Este documento registra el diseño arquitectónico, decisiones técnicas y la estructura de componentes del pipeline de analítica de criptomonedas.

---

## 1. Capa de Extracción y Modelos de Datos

### 1.1 Extractor HTTP (`src/extractors/coingecko.py`)
La capa de extracción es responsable de consultar la API REST pública de CoinGecko y obtener métricas de mercado en tiempo real.

* **Cliente**: Se utiliza `httpx.Client` para realizar peticiones HTTP de forma limpia y configurable.
* **Endpoint**: `GET /api/v3/coins/markets`
* **Parámetros**:
  * `vs_currency`: Moneda de referencia (por defecto `"usd"`).
  * `ids`: Lista de identificadores de criptomonedas separados por comas (ej. `"bitcoin,ethereum"`).
* **Headers**: Se envía un `User-Agent` personalizado (`crypto-analytics-platform/0.1.0`) para evitar bloqueos por rate-limiting básico.
* **Resiliencia**: Captura de excepciones HTTP mediante `response.raise_for_status()`.

### 1.2 Modelo de Validación (`src/models/price_record.py`)
Garantiza la integridad de los datos extraídos antes de ser procesados por las capas subsecuentes del pipeline.

* **Librería**: `pydantic` (v2).
* **Esquema**:
  * `coin_id` (`str`): Identificador único del activo (ej: `"bitcoin"`).
  * `symbol` (`str`): Símbolo de cotización en minúsculas (ej: `"btc"`).
  * `name` (`str`): Nombre completo del activo.
  * `current_price` (`float`): Precio actual en la moneda de referencia.
  * `market_cap` (`float`): Capitalización de mercado.
  * `total_volume` (`float`): Volumen total negociado en 24h.
  * `price_change_24h` (`float | None`): Variación porcentual en 24 horas (campo opcional/nulo).
  * `fetched_at` (`datetime`): Estampa de tiempo exacta de la extracción (en zona horaria UTC).

---

## 2. Registro de Decisiones de Arquitectura (ADRs)

### ADR-001: Selección de Client HTTP Síncrono (`httpx`)
* **Estado**: Aprobado.
* **Contexto**: Se requiere extraer datos periódicamente desde Airflow.
* **Decisión**: Usar `httpx.Client` síncrono en lugar de `asyncio`/`aiohttp`.
* **Consecuencias**: Simplifica el código de extracción dentro de los operadores de Airflow sin añadir sobrecarga de event loops asíncronos para peticiones batch pequeñas.

### ADR-002: Validación Estricta de Esquemas con Pydantic v2
* **Estado**: Aprobado.
* **Contexto**: Los datos de APIs externas pueden cambiar o contener nulos inesperados.
* **Decisión**: Mapear la respuesta JSON inmediatamente a modelos Pydantic `PriceRecord`.
* **Consecuencias**: Evita la propagación de datos corruptos a las capas de transformación y almacenamiento (BigQuery/GCS).
