from __future__ import annotations

import time
import uuid
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, Field


class Sample(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    node_id: str
    module: str
    kind: str
    ts: float = Field(default_factory=lambda: time.time())
    payload: Dict[str, Any] = Field(default_factory=dict)
    signal_strength: Optional[float] = None
    noise_level: Optional[float] = None


class Event(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    node_id: str
    ts: float = Field(default_factory=lambda: time.time())
    type: str
    severity: Literal["low", "medium", "high"] = "low"
    source_sample_id: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)
