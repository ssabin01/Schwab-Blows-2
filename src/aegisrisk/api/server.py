from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal, Dict, Any

from aegisrisk.pricing.black_scholes import price_greeks
from aegisrisk.pricing.binomial_crr import price as crr_price
from aegisrisk.utils.hashing import sha256_hex


app = FastAPI(title="AegisRisk (bootstrap)")


class Quote(BaseModel):
    S: float = Field(..., gt=0)
    r: float
    q: float
    sigma: float = Field(..., ge=0)
    T: float = Field(..., ge=0)


class PriceRequest(BaseModel):
    quote: Quote
    K: float = Field(..., gt=0)
    right: Literal["C", "P"]
    style: Literal["EUROPEAN", "AMERICAN"] = "EUROPEAN"
    method: Literal["BLACK_SCHOLES", "CRR_BINOMIAL"] = "BLACK_SCHOLES"
    N: int = Field(200, gt=0)


class PriceResponse(BaseModel):
    snapshot_hash: str
    request_hash: str
    result: Dict[str, Any]


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.post("/price", response_model=PriceResponse)
def price_endpoint(req: PriceRequest):
    # Deterministic hashes
    snapshot_hash = sha256_hex(req.quote.model_dump())
    request_hash = sha256_hex(req.model_dump())

    q = req.quote

    if req.method == "BLACK_SCHOLES":
        if req.style != "EUROPEAN":
            raise HTTPException(status_code=400, detail="BLACK_SCHOLES supports EUROPEAN only")
        res = price_greeks(S=q.S, K=req.K, r=q.r, q=q.q, sigma=q.sigma, T=q.T, right=req.right)
        if res.errors:
            raise HTTPException(status_code=422, detail={"errors": res.errors, "warnings": res.warnings})
        out = res.__dict__
    else:
        res = crr_price(S=q.S, K=req.K, r=q.r, q=q.q, sigma=q.sigma, T=q.T, N=req.N, right=req.right, style=req.style)
        if res.errors:
            raise HTTPException(status_code=422, detail={"errors": res.errors, "warnings": res.warnings})
        out = res.__dict__

    return {"snapshot_hash": snapshot_hash, "request_hash": request_hash, "result": out}
