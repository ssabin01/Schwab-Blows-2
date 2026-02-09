import unittest
from aegisrisk.pricing.black_scholes import price_greeks


class TestBlackScholesGoldens(unittest.TestCase):
    def test_bs_1_atm_30d(self):
        res_c = price_greeks(S=100, K=100, r=0.05, q=0.0, sigma=0.20, T=30/365, right="C")
        res_p = price_greeks(S=100, K=100, r=0.05, q=0.0, sigma=0.20, T=30/365, right="P")
        self.assertEqual(res_c.errors, [])
        self.assertEqual(res_p.errors, [])
        self.assertAlmostEqual(res_c.price, 2.4933768194, places=6)
        self.assertAlmostEqual(res_p.price, 2.0832611958, places=6)
        self.assertAlmostEqual(res_c.delta, 0.5399635456, places=6)
        self.assertAlmostEqual(res_p.delta, -0.4600364544, places=6)
        self.assertAlmostEqual(res_c.gamma, 0.0692276405, places=6)
        self.assertAlmostEqual(res_c.vega, 11.3798861044, places=6)
        self.assertAlmostEqual(res_c.theta_day, -0.0449881561, places=6)
        self.assertAlmostEqual(res_p.theta_day, -0.0313457062, places=6)

    def test_bs_2_otm_call_div_0_5y(self):
        res_c = price_greeks(S=100, K=110, r=0.03, q=0.01, sigma=0.25, T=0.5, right="C")
        res_p = price_greeks(S=100, K=110, r=0.03, q=0.01, sigma=0.25, T=0.5, right="P")
        self.assertEqual(res_c.errors, [])
        self.assertEqual(res_p.errors, [])
        self.assertAlmostEqual(res_c.price, 3.7230100452, places=6)
        self.assertAlmostEqual(res_p.price, 12.5840754823, places=6)
        self.assertAlmostEqual(res_c.delta, 0.3449878381, places=6)
        self.assertAlmostEqual(res_p.delta, -0.6500246411, places=6)
        self.assertAlmostEqual(res_c.gamma, 0.0207764082, places=6)
        self.assertAlmostEqual(res_c.vega, 25.9705102708, places=6)
        self.assertAlmostEqual(res_c.theta_day, -0.0193723642, places=6)
        self.assertAlmostEqual(res_p.theta_day, -0.0131919343, places=6)


if __name__ == "__main__":
    unittest.main()
