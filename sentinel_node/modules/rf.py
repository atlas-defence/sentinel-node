from __future__ import annotations

import random
import time

from sentinel_node.core.models import Sample


class RfModule:
    name = "rf"

    def __init__(self, node_id: str):
        self._node_id = node_id

    async def start(self) -> None:
        return None

    async def stop(self) -> None:
        return None

    async def poll(self) -> list[Sample]:
        # Placeholder: simulate a "signal" with SNR-like fields.
        freq_mhz = 433.0 + random.random() * 2.0
        strength = random.random()
        noise_level = random.random()
        bandwidth_khz = 12.5 if random.random() < 0.7 else 25.0

        return [
            Sample(
                node_id=self._node_id,
                module=self.name,
                kind="rf",
                ts=time.time(),
                payload={
                    "freq_mhz": round(freq_mhz, 4),
                    "bandwidth_khz": bandwidth_khz,
                },
                signal_strength=strength,
                noise_level=noise_level,
            )
        ]


def create(node_id: str) -> RfModule:
    return RfModule(node_id=node_id)

