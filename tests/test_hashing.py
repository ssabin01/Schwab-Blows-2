import unittest
from aegisrisk.utils.hashing import sha256_hex


class TestHashing(unittest.TestCase):
    def test_hash_deterministic_for_key_order(self):
        a = {"x": 1, "y": {"b": 2, "a": 3}}
        b = {"y": {"a": 3, "b": 2}, "x": 1}
        self.assertEqual(sha256_hex(a), sha256_hex(b))

    def test_hash_fail_closed_nan(self):
        with self.assertRaises(ValueError):
            sha256_hex({"x": float("nan")})


if __name__ == "__main__":
    unittest.main()
