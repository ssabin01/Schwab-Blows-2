from __future__ import annotations

import dataclasses
import math
from typing import Literal, List

Right = Literal["C", "P"]


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


@dataclasses.dataclass(frozen=True)
class BSResult:
    price: float
    delta: float
    gamma: float
    vega: float
    theta_day: float
    warnings: List[str]
    errors: List[str]
    method: str = "BLACK_SCHOLES"
    day_count: str = "ACT/365F"
    theta_units: str = "PER_CALENDAR_DAY"
    vega_units: str = "PER_1.00_VOL"


def price_greeks(
    *,
    S: float,
    K: float,
    r: float,
    q: float,
    sigma: float,
    T: float,
    right: Right,
) -> BSResult:
    warnings: List[str] = []
    errors: List[str] = []

    if not (S > 0 and K > 0):
        return BSResult(0.0, 0.0, 0.0, 0.0, 0.0, warnings, ["S and K must be > 0"])
    if T < 0:
        return BSResult(0.0, 0.0, 0.0, 0.0, 0.0, warnings, ["T must be >= 0"])
    if sigma < 0:
        return BSResult(0.0, 0.0, 0.0, 0.0, 0.0, warnings, ["sigma must be >= 0"])

    if T == 0.0:
        intrinsic = max(0.0, S - K) if right == "C" else max(0.0, K - S)
        warnings.append("T==0: returning intrinsic value; greeks set to 0.")
        return BSResult(intrinsic, 0.0, 0.0, 0.0, 0.0, warnings, errors)

    if sigma == 0.0:
        return BSResult(0.0, 0.0, 0.0, 0.0, 0.0, warnings, ["sigma==0 not supported (explicit error)"])

    sqrtT = math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / (sigma * sqrtT)
    d2 = d1 - sigma * sqrtT

    disc_q = math.exp(-q * T)
    disc_r = math.exp(-r * T)
    Nd1 = _norm_cdf(d1)
    Nd2 = _norm_cdf(d2)
    n_d1 = _norm_pdf(d1)

    if right == "C":
        price = S * disc_q * Nd1 - K * disc_r * Nd2
        delta = disc_q * Nd1
        theta_year = -(S * disc_q * n_d1 * sigma) / (2.0 * sqrtT) + q * S * disc_q * Nd1 - r * K * disc_r * Nd2
    elif right == "P":
        price = K * disc_r * _norm_cdf(-d2) - S * disc_q * _norm_cdf(-d1)
        delta = disc_q * (Nd1 - 1.0)
        theta_year = -(S * disc_q * n_d1 * sigma) / (2.0 * sqrtT) - q * S * disc_q * _norm_cdf(-d1) + r * K * disc_r * _norm_cdf(-d2)
    else:
        return BSResult(0.0, 0.0, 0.0, 0.0, 0.0, warnings, ["right must be 'C' or 'P'"])

    gamma = disc_q * n_d1 / (S * sigma * sqrtT)
    vega = S * disc_q * n_d1 * sqrtT
    theta_day = theta_year / 365.0

    for name, val in [("price", price), ("delta", delta), ("gamma", gamma), ("vega", vega), ("theta_day", theta_day)]:
        if not math.isfinite(val):
            errors.append(f"Non-finite {name} computed")

    if errors:
        return BSResult(0.0, 0.0, 0.0, 0.0, 0.0, warnings, errors)

    return BSResult(price, delta, gamma, vega, theta_day, warnings, errors)
