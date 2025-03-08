import unittest
import os
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app  # Assuming the main app instance is defined in app.main
from app.services.cryptocurrencies_service import CryptoCurrenciesService
client = TestClient(app)
os.chdir("../")
class TestCryptoCurrenciesIntegration(unittest.TestCase):
    def test_query_physical_currencies(self):
        response = client.get("/crypto-currencies/query_physical_currencies")
        self.assertEqual(response.status_code, 200)
        result=response.json()
        self.assertEqual(
            result['err_code'],
            0
        )

    def test_query_digital_currencies(self):
        response = client.get("/crypto-currencies/query_digital_currencies")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(
            result['err_code'],
            0
        )

    def test_query_exchange_rate(self):
        response = client.get("/crypto-currencies/exchange-rate/query?from_currency=BTC&to_currency=USD")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(
            result['err_code'],
            0
        )
    def test_get_fx_daily(self):
        response = client.get("/crypto-currencies/fx-daily?from_symbol=EUR&to_symbol=USD")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(
            result['err_code'],
            0
        )
    def test_get_fx_weekly(self):
        response = client.get("/crypto-currencies/fx-weekly?from_symbol=EUR&to_symbol=USD")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(
            result['err_code'],
            0
        )

    def test_get_fx_monthly(self):
        response = client.get("/crypto-currencies/fx-monthly?from_symbol=EUR&to_symbol=USD")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(
            result['err_code'],
            0
        )


if __name__ == "__main__":
    unittest.main()

