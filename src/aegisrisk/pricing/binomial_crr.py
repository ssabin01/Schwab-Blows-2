from __future__ import annotations

import dataclasses
import math
from typing import Literal, List

Right = Literal["C", "P"]
Style = Literal["EUROPEAN", "AMERICAN"]


@dataclasses.dataclass(frozen=True)
class CRRResult:
    price: float
    warnings: List[str]
    errors: List[str]
    method: str = "CRR_BINOMIAL"


def price(
    *,
    S: float,
    K: float,
    r: float,
    q: float,
    sigma: float,
    T: float,
    N: int,
    right: Right,
    style: Style,
) -> CRRResult:
    warnings: List[str] = []
    errors: List[str] = []

    if not (S > 0 and K > 0):
        return CRRResult(0.0, warnings, ["S and K must be > 0"])
    if T < 0:
        return CRRResult(0.0, warnings, ["T must be >= 0"])
    if sigma < 0:
        return CRRResult(0.0, warnings, ["sigma must be >= 0"])
    if N <= 0:
        return CRRResult(0.0, warnings, ["N must be > 0"])
    if T == 0.0:
        intrinsic = max(0.0, S - K) if right == "C" else max(0.0, K - S)
        warnings.append("T==0: returning intrinsic value.")
        return CRRResult(intrinsic, warnings, errors)
    if sigma == 0.0:
        return CRRResult(0.0, warnings, ["sigma==0 not supported (explicit error)"])

    dt = T / float(N)
    u = math.exp(sigma * math.sqrt(dt))
    d = 1.0 / u
    disc = math.exp(-r * dt)
    a = math.exp((r - q) * dt)
    p = (a - d) / (u - d)

    if not (0.0 <= p <= 1.0):
        return CRRResult(0.0, warnings, ["Invalid risk-neutral probability p; check inputs."])

    prices = [S * (u ** j) * (d ** (N - j)) for j in range(N + 1)]
    if right == "C":
        values = [max(0.0, s - K) for s in prices]
    else:
        values = [max(0.0, K - s) for s in prices]

    american = style == "AMERICAN"
    for i in range(N - 1, -1, -1):
        new_vals = []
        for j in range(i + 1):
            cont = disc * (p * values[j + 1] + (1.0 - p) * values[j])
            if american:
                s = S * (u ** j) * (d ** (i - j))
                exer = max(0.0, s - K) if right == "C" else max(0.0, K - s)
                new_vals.append(max(cont, exer))
            else:
                new_vals.append(cont)
        values = new_vals

    out = values[0]
    if not math.isfinite(out):
        return CRRResult(0.0, warnings, ["Non-finite price computed"])
    return CRRResult(out, warnings, errors)
