from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path
from typing import Iterable

from sentinel_node.core.config import StorageConfig
from sentinel_node.core.models import Event, Sample


class LocalStorage:
    def __init__(self, cfg: StorageConfig):
        self._cfg = cfg
        self._db: sqlite3.Connection | None = None
        self._jsonl_fp = None
        self._lock = threading.Lock()

    def _ensure_dirs(self) -> None:
        Path(self._cfg.directory).mkdir(parents=True, exist_ok=True)
        Path(self._cfg.sqlite_path).parent.mkdir(parents=True, exist_ok=True)
        Path(self._cfg.jsonl_path).parent.mkdir(parents=True, exist_ok=True)

    def start(self) -> None:
        self._ensure_dirs()
        # We write from asyncio worker threads; allow cross-thread usage and guard with a lock.
        self._db = sqlite3.connect(self._cfg.sqlite_path, check_same_thread=False)
        with self._lock:
            self._db.execute(
                """
                CREATE TABLE IF NOT EXISTS samples (
                  id TEXT PRIMARY KEY,
                  node_id TEXT,
                  module TEXT,
                  kind TEXT,
                  ts REAL,
                  signal_strength REAL,
                  noise_level REAL,
                  payload_json TEXT
                )
                """
            )
            self._db.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                  id TEXT PRIMARY KEY,
                  node_id TEXT,
                  ts REAL,
                  type TEXT,
                  severity TEXT,
                  source_sample_id TEXT,
                  data_json TEXT
                )
                """
            )
            self._db.commit()
        self._jsonl_fp = open(self._cfg.jsonl_path, "a", encoding="utf-8")

    def stop(self) -> None:
        if self._jsonl_fp is not None:
            self._jsonl_fp.flush()
            self._jsonl_fp.close()
            self._jsonl_fp = None
        if self._db is not None:
            with self._lock:
                self._db.close()
            self._db = None

    def write_samples(self, samples: Iterable[Sample]) -> None:
        if self._db is None:
            raise RuntimeError("Storage not started")
        rows = [
            (
                s.id,
                s.node_id,
                s.module,
                s.kind,
                s.ts,
                s.signal_strength,
                s.noise_level,
                json.dumps(s.payload, separators=(",", ":"), ensure_ascii=False),
            )
            for s in samples
        ]
        with self._lock:
            self._db.executemany(
                """
                INSERT OR REPLACE INTO samples
                (id,node_id,module,kind,ts,signal_strength,noise_level,payload_json)
                VALUES (?,?,?,?,?,?,?,?)
                """,
                rows,
            )
            self._db.commit()

    def write_events(self, events: Iterable[Event]) -> None:
        if self._db is None or self._jsonl_fp is None:
            raise RuntimeError("Storage not started")
        rows = [
            (
                e.id,
                e.node_id,
                e.ts,
                e.type,
                e.severity,
                e.source_sample_id,
                json.dumps(e.data, separators=(",", ":"), ensure_ascii=False),
            )
            for e in events
        ]
        with self._lock:
            self._db.executemany(
                """
                INSERT OR REPLACE INTO events
                (id,node_id,ts,type,severity,source_sample_id,data_json)
                VALUES (?,?,?,?,?,?,?)
                """,
                rows,
            )
            for e in events:
                self._jsonl_fp.write(e.model_dump_json() + "\n")
            self._jsonl_fp.flush()
            self._db.commit()

    def latest_events(self, limit: int = 50) -> list[Event]:
        if self._db is None:
            raise RuntimeError("Storage not started")
        with self._lock:
            cur = self._db.execute(
                "SELECT id,node_id,ts,type,severity,source_sample_id,data_json FROM events ORDER BY ts DESC LIMIT ?",
                (limit,),
            )
            rows = cur.fetchall()

        out: list[Event] = []
        for row in rows:
            data = json.loads(row[6]) if row[6] else {}
            out.append(
                Event(
                    id=row[0],
                    node_id=row[1],
                    ts=row[2],
                    type=row[3],
                    severity=row[4],
                    source_sample_id=row[5],
                    data=data,
                )
            )
        return out

