from __future__ import annotations

import random
import time

from sentinel_node.core.models import Sample


class AudioModule:
    name = "audio"

    def __init__(self, node_id: str):
        self._node_id = node_id

    async def start(self) -> None:
        return None

    async def stop(self) -> None:
        return None

    async def poll(self) -> list[Sample]:
        # Placeholder: simulate a normalized loudness + a crude "event" marker.
        loudness = random.random()
        noise_level = min(1.0, 0.2 + random.random() * 0.9)
        strength = max(0.0, min(1.0, loudness * (1.0 - (noise_level * 0.3))))
        label = "impulse" if loudness > 0.85 else "ambient"

        return [
            Sample(
                node_id=self._node_id,
                module=self.name,
                kind="audio",
                ts=time.time(),
                payload={"loudness": round(loudness, 3), "label": label},
                signal_strength=strength,
                noise_level=noise_level,
            )
        ]


def create(node_id: str) -> AudioModule:
    return AudioModule(node_id=node_id)

