from datetime import datetime

from pydantic import BaseModel


class PriceRecord(BaseModel):
    coin_id: str
    symbol: str
    name: str
    current_price: float
    market_cap: float
    total_volume: float
    price_change_24h: float | None
    fetched_at: datetime
