from __future__ import annotations

import json
from typing import Iterable

import requests

from sentinel_node.core.models import Event
from sentinel_node.network.security import sign_bytes


class PeerSender:
    def __init__(self, peers: list[str], shared_secret: str = "", timeout_s: float = 5.0):
        self._peers = peers
        self._secret = shared_secret or ""
        self._timeout_s = timeout_s

    def send_events(self, events: Iterable[Event]) -> None:
        if not self._peers:
            return
        payload = {"events": [e.model_dump() for e in events]}
        body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        sig = sign_bytes(self._secret, body)

        headers = {"Content-Type": "application/json"}
        if sig:
            headers["X-Sentinel-Signature"] = sig

        for peer in self._peers:
            try:
                requests.post(
                    peer.rstrip("/") + "/ingest",
                    data=body,
                    headers=headers,
                    timeout=self._timeout_s,
                )
            except Exception:
                # Best-effort; node may be offline.
                continue

