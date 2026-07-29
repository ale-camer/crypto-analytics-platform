from unittest.mock import MagicMock, patch

import httpx
import pytest

from src.extractors.coingecko import CoinGeckoExtractor
from src.models.price_record import PriceRecord


@patch("httpx.Client.get")
def test_fetch_returns_price_records(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "current_price": 60000.0,
            "market_cap": 1e12,
            "total_volume": 5e10,
            "price_change_24h": 1.5,
        }
    ]
    mock_get.return_value = mock_response

    extractor = CoinGeckoExtractor()
    records = extractor.fetch(["bitcoin"])

    assert len(records) == 1
    assert isinstance(records[0], PriceRecord)
    assert records[0].coin_id == "bitcoin"
    assert records[0].current_price == 60000.0


@patch("httpx.Client.get")
def test_fetch_handles_null_price_change(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "current_price": 60000.0,
            "market_cap": 1e12,
            "total_volume": 5e10,
            "price_change_24h": None,
        }
    ]
    mock_get.return_value = mock_response

    extractor = CoinGeckoExtractor()
    records = extractor.fetch(["bitcoin"])

    assert len(records) == 1
    assert records[0].price_change_24h is None


@patch("httpx.Client.get")
def test_fetch_raises_on_http_error(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "429 Too Many Requests",
        request=MagicMock(),
        response=MagicMock(status_code=429),
    )
    mock_get.return_value = mock_response

    extractor = CoinGeckoExtractor()
    with pytest.raises(httpx.HTTPStatusError):
        extractor.fetch(["bitcoin"])
