import json
from pathlib import Path
from typing import Any, Dict

import yaml
from pydantic import BaseModel, Field


class ProcessingConfig(BaseModel):
    filters: Dict[str, float] = Field(default_factory=dict)
    detectors: Dict[str, float] = Field(default_factory=dict)


class StorageConfig(BaseModel):
    directory: str = "data"
    sqlite_path: str = "data/sentinel.sqlite3"
    jsonl_path: str = "data/events.jsonl"


class ApiConfig(BaseModel):
    enabled: bool = True
    host: str = "127.0.0.1"
    port: int = 8787


class NetworkConfig(BaseModel):
    enabled: bool = False
    peers: list[str] = Field(default_factory=list)
    shared_secret: str = ""


class AppConfig(BaseModel):
    node_id: str = "node-001"
    modules: list[str] = Field(default_factory=lambda: ["env"])
    processing: ProcessingConfig = Field(default_factory=ProcessingConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
    api: ApiConfig = Field(default_factory=ApiConfig)
    network: NetworkConfig = Field(default_factory=NetworkConfig)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_config(path: Path) -> AppConfig:
    if not path.exists():
        raise FileNotFoundError(
            f"Config file not found: {path}. Create one from config.example.yaml."
        )

    raw = _read_text(path)
    suffix = path.suffix.lower()
    data: Dict[str, Any]

    if suffix in (".yaml", ".yml"):
        data = yaml.safe_load(raw) or {}
    elif suffix == ".json":
        data = json.loads(raw)
    else:
        # Try YAML first, then JSON.
        try:
            data = yaml.safe_load(raw) or {}
        except Exception:
            data = json.loads(raw)

    return AppConfig.model_validate(data)
