from __future__ import annotations

import asyncio
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel

from sentinel_node.core.models import Event
from sentinel_node.core.storage import LocalStorage
from sentinel_node.network.security import verify_bytes


class IngestBody(BaseModel):
    events: list[dict[str, Any]]


def build_app(storage: LocalStorage, shared_secret: str = "") -> FastAPI:
    app = FastAPI(title="Sentinel Node API", version="0.1.0")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/events")
    async def events(limit: int = 50) -> list[dict[str, Any]]:
        return [e.model_dump() for e in storage.latest_events(limit=limit)]

    @app.post("/ingest")
    async def ingest(
        request: Request,
        body: IngestBody,
        x_sentinel_signature: str | None = Header(default=None),
    ) -> dict[str, Any]:
        raw = await request.body()
        if not verify_bytes(shared_secret or "", raw, x_sentinel_signature or ""):
            raise HTTPException(status_code=401, detail="invalid signature")

        events = [Event.model_validate(e) for e in body.events]
        # Write synchronously in a thread to avoid blocking the event loop.
        await asyncio.to_thread(storage.write_events, events)
        return {"ok": True, "ingested": len(events)}

    return app

