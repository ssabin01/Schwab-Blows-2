import unittest
from aegisrisk.pricing.binomial_crr import price


class TestCRRInvariants(unittest.TestCase):
    def test_am_1_call_no_div_equals_euro(self):
        euro = price(S=100, K=100, r=0.05, q=0.0, sigma=0.20, T=30/365, N=200, right="C", style="EUROPEAN")
        amer = price(S=100, K=100, r=0.05, q=0.0, sigma=0.20, T=30/365, N=200, right="C", style="AMERICAN")
        self.assertEqual(euro.errors, [])
        self.assertEqual(amer.errors, [])
        self.assertAlmostEqual(euro.price, amer.price, places=3)
        self.assertAlmostEqual(euro.price, 2.4905182527, places=6)
        self.assertAlmostEqual(amer.price, 2.4905182527, places=6)

    def test_am_2_put_american_ge_euro(self):
        euro = price(S=100, K=100, r=0.05, q=0.0, sigma=0.20, T=30/365, N=200, right="P", style="EUROPEAN")
        amer = price(S=100, K=100, r=0.05, q=0.0, sigma=0.20, T=30/365, N=200, right="P", style="AMERICAN")
        self.assertEqual(euro.errors, [])
        self.assertEqual(amer.errors, [])
        self.assertGreaterEqual(amer.price, euro.price)
        self.assertAlmostEqual(euro.price, 2.0804026291, places=6)
        self.assertAlmostEqual(amer.price, 2.1115903094, places=6)


if __name__ == "__main__":
    unittest.main()
