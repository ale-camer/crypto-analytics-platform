import polars as pl

from src.models.price_record import PriceRecord


class PriceTransformer:
    def add_technical_indicators(self, df: pl.DataFrame) -> pl.DataFrame:
        if df.is_empty():
            return df.with_columns(
                [
                    pl.lit(None).cast(pl.Float64).alias("macd"),
                    pl.lit(None).cast(pl.Float64).alias("macd_signal"),
                    pl.lit(None).cast(pl.Float64).alias("bb_upper"),
                    pl.lit(None).cast(pl.Float64).alias("bb_lower"),
                    pl.lit(None).cast(pl.Float64).alias("rsi_14"),
                ]
            )

        df = df.sort("fetched_at")

        # MACD: EMA(12) - EMA(26), Signal: EMA(9)
        ema_12 = pl.col("current_price").ewm_mean(span=12, min_samples=12, ignore_nulls=True)
        ema_26 = pl.col("current_price").ewm_mean(span=26, min_samples=26, ignore_nulls=True)
        macd = ema_12 - ema_26
        macd_signal = macd.ewm_mean(span=9, min_samples=9, ignore_nulls=True)

        # Bollinger Bands: SMA 20 +/- (2 * STD 20)
        sma_20 = pl.col("current_price").rolling_mean(window_size=20)
        std_20 = pl.col("current_price").rolling_std(window_size=20)
        bb_upper = sma_20 + (std_20 * 2)
        bb_lower = sma_20 - (std_20 * 2)

        # RSI (14)
        delta = pl.col("current_price").diff()
        gain = pl.when(delta > 0).then(delta).when(delta <= 0).then(0).otherwise(None)
        loss = pl.when(delta < 0).then(-delta).when(delta >= 0).then(0).otherwise(None)
        avg_gain = gain.ewm_mean(span=14, min_samples=14, ignore_nulls=True)
        avg_loss = loss.ewm_mean(span=14, min_samples=14, ignore_nulls=True)
        rs = avg_gain / avg_loss
        rsi_14 = 100 - (100 / (1 + rs))

        return df.with_columns(
            [
                macd.over("coin_id").alias("macd"),
                macd_signal.over("coin_id").alias("macd_signal"),
                bb_upper.over("coin_id").alias("bb_upper"),
                bb_lower.over("coin_id").alias("bb_lower"),
                rsi_14.over("coin_id").alias("rsi_14"),
            ]
        )

    def transform(self, records: list[PriceRecord]) -> pl.DataFrame:
        if not records:
            df = pl.DataFrame(
                schema={
                    "coin_id": pl.String,
                    "symbol": pl.String,
                    "name": pl.String,
                    "current_price": pl.Float64,
                    "market_cap": pl.Float64,
                    "total_volume": pl.Float64,
                    "price_change_24h": pl.Float64,
                    "fetched_at": pl.Datetime("us"),
                }
            )
            return self.add_technical_indicators(df)

        data = [r.model_dump() for r in records]
        df = pl.DataFrame(data)
        return self.add_technical_indicators(df)
