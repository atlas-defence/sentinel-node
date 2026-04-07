from __future__ import annotations

import asyncio
from typing import Optional

import uvicorn

from sentinel_node.api.server import build_app
from sentinel_node.core.config import AppConfig
from sentinel_node.core.modules import Module, load_modules
from sentinel_node.core.processing import ProcessingEngine
from sentinel_node.core.storage import LocalStorage
from sentinel_node.network.sender import PeerSender


class SentinelApp:
    def __init__(self, cfg: AppConfig):
        self._cfg = cfg
        self._modules: list[Module] = load_modules(cfg.modules, node_id=cfg.node_id)
        self._engine = ProcessingEngine(cfg.processing)
        self._storage = LocalStorage(cfg.storage)
        self._sender = PeerSender(cfg.network.peers, shared_secret=cfg.network.shared_secret)
        self._poll_task: Optional[asyncio.Task] = None
        self._api_server: Optional[uvicorn.Server] = None
        self._api_task: Optional[asyncio.Task] = None
        self._stop = asyncio.Event()

    async def start(self) -> None:
        self._storage.start()
        for m in self._modules:
            await m.start()
        if self._cfg.api.enabled:
            await self._start_api()
        self._poll_task = asyncio.create_task(self._poll_loop())

    async def stop(self) -> None:
        self._stop.set()
        if self._poll_task is not None:
            await self._poll_task
        if self._api_server is not None:
            self._api_server.should_exit = True
        if self._api_task is not None:
            await self._api_task
        for m in self._modules:
            await m.stop()
        self._storage.stop()

    async def run_once(self) -> None:
        await self._cycle()

    async def _poll_loop(self) -> None:
        while not self._stop.is_set():
            await self._cycle()
            await asyncio.sleep(1.0)

    async def _cycle(self) -> None:
        samples = []
        for m in self._modules:
            try:
                samples.extend(await m.poll())
            except Exception:
                continue

        filtered = self._engine.filter_samples(samples)
        events = self._engine.detect_events(filtered)

        if filtered:
            await asyncio.to_thread(self._storage.write_samples, filtered)
        if events:
            await asyncio.to_thread(self._storage.write_events, events)
            if self._cfg.network.enabled:
                await asyncio.to_thread(self._sender.send_events, events)

    async def _start_api(self) -> None:
        app = build_app(self._storage, shared_secret=self._cfg.network.shared_secret)
        config = uvicorn.Config(
            app,
            host=self._cfg.api.host,
            port=self._cfg.api.port,
            log_level="info",
        )
        self._api_server = uvicorn.Server(config)
        self._api_task = asyncio.create_task(self._api_server.serve())

