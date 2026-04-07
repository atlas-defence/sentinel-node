import argparse
import asyncio
import signal
from pathlib import Path

from sentinel_node.core.app import SentinelApp
from sentinel_node.core.config import load_config


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Sentinel Node edge runtime")
    p.add_argument(
        "--config",
        default="config.yaml",
        help="Path to JSON/YAML config (default: config.yaml)",
    )
    p.add_argument(
        "--once",
        action="store_true",
        help="Run one ingestion/process cycle then exit",
    )
    return p.parse_args()


async def _run() -> int:
    args = parse_args()
    config_path = Path(args.config)
    cfg = load_config(config_path)

    app = SentinelApp(cfg)
    await app.start()

    if args.once:
        await app.run_once()
        await app.stop()
        return 0

    stop_event = asyncio.Event()

    def _request_stop() -> None:
        stop_event.set()

    try:
        signal.signal(signal.SIGINT, lambda *_: _request_stop())
        signal.signal(signal.SIGTERM, lambda *_: _request_stop())
    except Exception:
        # Some platforms/environments may not support SIGTERM handlers.
        pass

    await stop_event.wait()
    await app.stop()
    return 0


def main() -> None:
    raise SystemExit(asyncio.run(_run()))


if __name__ == "__main__":
    main()
