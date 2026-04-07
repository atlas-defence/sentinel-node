from __future__ import annotations

import random
import time

from sentinel_node.core.models import Sample


class EnvModule:
    name = "env"

    def __init__(self, node_id: str):
        self._node_id = node_id

    async def start(self) -> None:
        return None

    async def stop(self) -> None:
        return None

    async def poll(self) -> list[Sample]:
        # Placeholder "sensor" producing plausible environmental readings.
        temperature_c = 18 + random.random() * 10
        humidity = 0.35 + random.random() * 0.45
        noise_level = random.random()
        strength = max(0.0, min(1.0, 1.0 - noise_level))

        return [
            Sample(
                node_id=self._node_id,
                module=self.name,
                kind="environment",
                ts=time.time(),
                payload={"temperature_c": round(temperature_c, 2), "humidity": round(humidity, 3)},
                signal_strength=strength,
                noise_level=noise_level,
            )
        ]


def create(node_id: str) -> EnvModule:
    return EnvModule(node_id=node_id)

