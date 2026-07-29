from datetime import datetime, timezone

import polars as pl

from src.models.price_record import PriceRecord
from src.transformers.price_transformer import PriceTransformer


def test_transform_creates_dataframe():
    record = PriceRecord(
        coin_id="bitcoin",
        symbol="btc",
        name="Bitcoin",
        current_price=60000.0,
        market_cap=1e12,
        total_volume=5e10,
        price_change_24h=1.5,
        fetched_at=datetime.now(timezone.utc),
    )
    transformer = PriceTransformer()
    df = transformer.transform([record])

    assert isinstance(df, pl.DataFrame)
    assert df.height == 1
    assert "coin_id" in df.columns
    assert df["coin_id"][0] == "bitcoin"
    assert df["current_price"][0] == 60000.0


def test_transform_empty_list():
    transformer = PriceTransformer()
    df = transformer.transform([])

    assert isinstance(df, pl.DataFrame)
    assert df.height == 0
    assert "coin_id" in df.columns
