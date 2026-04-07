from __future__ import annotations

from typing import Iterable

from sentinel_node.core.config import ProcessingConfig
from sentinel_node.core.models import Event, Sample


class ProcessingEngine:
    def __init__(self, cfg: ProcessingConfig):
        self._cfg = cfg

    def filter_samples(self, samples: Iterable[Sample]) -> list[Sample]:
        min_strength = float(self._cfg.filters.get("min_signal_strength", 0.0))
        max_noise = float(self._cfg.filters.get("max_noise_level", 1.0))

        out: list[Sample] = []
        for s in samples:
            if s.signal_strength is not None and s.signal_strength < min_strength:
                continue
            if s.noise_level is not None and s.noise_level > max_noise:
                continue
            out.append(s)
        return out

    def detect_events(self, samples: Iterable[Sample]) -> list[Event]:
        spike_threshold = float(self._cfg.detectors.get("spike_threshold", 0.8))
        events: list[Event] = []

        for s in samples:
            strength = s.signal_strength
            if strength is not None and strength >= spike_threshold:
                events.append(
                    Event(
                        node_id=s.node_id,
                        type=f"{s.module}.spike",
                        severity="medium" if strength < 0.95 else "high",
                        source_sample_id=s.id,
                        data={"kind": s.kind, "signal_strength": strength, "payload": s.payload},
                    )
                )

        return events

