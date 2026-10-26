CREATE OR REPLACE VIEW `gen-lang-client-0887473308.crypto_market_data.vw_p02_crypto_health` AS
SELECT 
    coin_id,
    symbol,
    COUNT(1) AS total_records,
    MIN(DATE(fetched_at)) AS first_seen_date,
    MAX(DATE(fetched_at)) AS last_seen_date,
    DATE_DIFF(CURRENT_DATE(), MAX(DATE(fetched_at)), DAY) AS days_since_last_fetch,
    COUNTIF(current_price IS NULL OR current_price <= 0) AS invalid_price_count,
    COUNTIF(total_volume IS NULL OR total_volume < 0) AS invalid_volume_count,
    COUNTIF(rsi_14 IS NULL) AS missing_rsi_count,
    CASE 
        WHEN DATE_DIFF(CURRENT_DATE(), MAX(DATE(fetched_at)), DAY) <= 1 
         AND COUNTIF(current_price IS NULL OR current_price <= 0) = 0 
        THEN 1 
        ELSE 0 
    END AS is_healthy
FROM `gen-lang-client-0887473308.crypto_market_data.prices`
GROUP BY coin_id, symbol;
