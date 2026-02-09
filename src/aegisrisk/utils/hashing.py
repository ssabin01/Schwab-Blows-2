from __future__ import annotations

import dataclasses
import hashlib
import json
import math
from typing import Any


def _canonicalize(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj):
        return _canonicalize(dataclasses.asdict(obj))

    if obj is None or isinstance(obj, (str, int, bool)):
        return obj

    if isinstance(obj, float):
        if not math.isfinite(obj):
            raise ValueError("Non-finite float encountered (NaN/Inf). Hashing is fail-closed.")
        return obj

    if isinstance(obj, (list, tuple)):
        return [_canonicalize(x) for x in obj]

    if isinstance(obj, dict):
        out = {}
        for k in sorted(obj.keys(), key=lambda x: str(x)):
            out[str(k)] = _canonicalize(obj[k])
        return out

    return str(obj)


def stable_json_bytes(obj: Any) -> bytes:
    canon = _canonicalize(obj)
    s = json.dumps(canon, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return s.encode("utf-8")


def sha256_hex(obj: Any) -> str:
    return hashlib.sha256(stable_json_bytes(obj)).hexdigest()
