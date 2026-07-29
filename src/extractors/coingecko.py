from datetime import datetime, timezone

import httpx

from src.models.price_record import PriceRecord


class CoinGeckoExtractor:
    def __init__(
        self, base_url: str = "https://api.coingecko.com/api/v3", vs_currency: str = "usd"
    ):
        self.base_url = base_url
        self.vs_currency = vs_currency

    def fetch(self, coins: list[str]) -> list[PriceRecord]:
        url = f"{self.base_url}/coins/markets"
        params = {
            "vs_currency": self.vs_currency,
            "ids": ",".join(coins),
        }
        headers = {"User-Agent": "crypto-analytics-platform/0.1.0"}

        with httpx.Client() as client:
            response = client.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

        records = []
        now = datetime.now(timezone.utc)
        for item in data:
            record = PriceRecord(
                coin_id=item["id"],
                symbol=item["symbol"],
                name=item["name"],
                current_price=float(item["current_price"]),
                market_cap=float(item["market_cap"]),
                total_volume=float(item["total_volume"]),
                price_change_24h=float(item["price_change_24h"])
                if item.get("price_change_24h") is not None
                else None,
                fetched_at=now,
            )
            records.append(record)

        return records
