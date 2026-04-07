from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Iterable, Protocol

from sentinel_node.core.models import Sample


class Module(Protocol):
    name: str

    async def start(self) -> None: ...
    async def stop(self) -> None: ...
    async def poll(self) -> list[Sample]: ...


@dataclass(frozen=True)
class ModuleSpec:
    name: str
    import_path: str
    factory: str = "create"


BUILTIN_MODULES: dict[str, ModuleSpec] = {
    "rf": ModuleSpec(name="rf", import_path="sentinel_node.modules.rf"),
    "audio": ModuleSpec(name="audio", import_path="sentinel_node.modules.audio"),
    "env": ModuleSpec(name="env", import_path="sentinel_node.modules.env"),
}


def load_modules(names: Iterable[str], node_id: str) -> list[Module]:
    loaded: list[Module] = []
    for n in names:
        spec = BUILTIN_MODULES.get(n)
        if spec is None:
            # Allow external plugins via fully-qualified import path:
            # modules: ["package.module:factory"]
            if ":" in n:
                import_path, factory = n.split(":", 1)
                spec = ModuleSpec(name=import_path.rsplit(".", 1)[-1], import_path=import_path, factory=factory)
            else:
                raise ValueError(
                    f"Unknown module '{n}'. Known: {sorted(BUILTIN_MODULES)} or use 'pkg.mod:factory'."
                )

        mod = importlib.import_module(spec.import_path)
        create = getattr(mod, spec.factory, None)
        if create is None:
            raise AttributeError(
                f"Module '{spec.name}' missing factory '{spec.factory}' in {spec.import_path}"
            )
        inst = create(node_id=node_id)
        loaded.append(inst)
    return loaded

