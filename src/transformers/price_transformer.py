import polars as pl

from src.models.price_record import PriceRecord


class PriceTransformer:
    def transform(self, records: list[PriceRecord]) -> pl.DataFrame:
        if not records:
            return pl.DataFrame(
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

        data = [r.model_dump() for r in records]
        return pl.DataFrame(data)
