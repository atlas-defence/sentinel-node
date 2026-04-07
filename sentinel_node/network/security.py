from __future__ import annotations

import hashlib
import hmac


def sign_bytes(secret: str, body: bytes) -> str:
    if not secret:
        return ""
    mac = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return mac


def verify_bytes(secret: str, body: bytes, signature_hex: str) -> bool:
    if not secret:
        return True
    expected = sign_bytes(secret, body)
    return hmac.compare_digest(expected, signature_hex or "")

