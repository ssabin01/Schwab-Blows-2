import unittest
from fastapi.testclient import TestClient

from aegisrisk.api.server import app

client = TestClient(app)


class TestAPIPrice(unittest.TestCase):
    def test_health(self):
        r = client.get("/healthz")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["ok"], True)

    def test_price_deterministic_hashes(self):
        payload = {
            "quote": {"S": 100, "r": 0.05, "q": 0.0, "sigma": 0.20, "T": 30/365},
            "K": 100,
            "right": "C",
            "style": "EUROPEAN",
            "method": "BLACK_SCHOLES",
            "N": 200
        }
        r1 = client.post("/price", json=payload)
        r2 = client.post("/price", json=payload)
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r2.status_code, 200)
        j1, j2 = r1.json(), r2.json()
        self.assertEqual(j1["snapshot_hash"], j2["snapshot_hash"])
        self.assertEqual(j1["request_hash"], j2["request_hash"])
        self.assertAlmostEqual(j1["result"]["price"], 2.4933768194, places=6)

    def test_price_rejects_american_bs(self):
        payload = {
            "quote": {"S": 100, "r": 0.05, "q": 0.0, "sigma": 0.20, "T": 30/365},
            "K": 100,
            "right": "C",
            "style": "AMERICAN",
            "method": "BLACK_SCHOLES",
            "N": 200
        }
        r = client.post("/price", json=payload)
        self.assertEqual(r.status_code, 400)


if __name__ == "__main__":
    unittest.main()
