# Sentinel Node

Edge node software for collecting, processing, and sharing sensor and signal data.

**Read this in other languages:** [Türkçe](README.tr.md)

---

## Overview

Sentinel Node is a lightweight edge software designed to run on distributed devices and act as a data collection and processing unit within the Atlas Defence ecosystem. It gathers input from sensors and signal sources, processes data locally, and shares structured outputs with other nodes or central systems.

The goal is to enable decentralized, scalable, and resilient monitoring networks using simple, modular components.

---

## Features

- Multi-source data collection (RF, environmental, audio, custom sensors)
- Local processing and filtering
- Real-time event generation
- Lightweight and resource-efficient
- Modular plugin system
- Secure data transmission between nodes
- Works offline / intermittent connectivity support

---

## Architecture

```

[ Sensors / Inputs ]
(RF / Audio / Env / Custom)
↓
Data Ingestion Layer
↓
Processing Engine
(Filtering / Detection)
↓
Event & Data Layer
↓
Output (API / Network / Storage)

````

---

## Supported Hardware

- Raspberry Pi (recommended)
- Linux-based edge devices
- ESP32 (experimental integration)
- SDR devices (RTL-SDR, HackRF)
- USB / GPIO sensors

---

## Getting Started

### Requirements

- Linux (Ubuntu / Debian preferred)
- Python 3.10+
- Optional: SDR drivers, sensor libraries

### Install

```bash
git clone https://github.com/atlas-defence/sentinel-node.git
cd sentinel-node
pip install -r requirements.txt
```

### Run

```bash
copy config.example.yaml config.yaml
python main.py --config config.yaml
```

---

## Configuration

Configuration is handled via simple JSON/YAML files:

```json
{
  "node_id": "node-001",
  "modules": ["rf", "audio"],
  "output": "local"
}
```

---

## Modules

* `rf/` — RF signal ingestion and processing
* `audio/` — sound-based detection
* `env/` — environmental sensors
* `core/` — processing engine
* `network/` — node-to-node communication

---

## API

When enabled in config (default), the node runs a small HTTP API:

- `GET /health`
- `GET /events?limit=50`
- `POST /ingest` (peer-to-peer event ingestion; optional `X-Sentinel-Signature` HMAC)

---

## Notes

- The built-in `rf`, `audio`, and `env` modules in this repo are **working placeholders** (they generate synthetic samples). Replace them with real sensor/SDR integrations as needed.
- To add external plugins, set `modules` to include `your_package.your_module:create`.

## Use Cases

* Distributed sensor networks
* Signal monitoring systems
* Environmental data collection
* Edge AI experimentation
* Decentralized security systems

---

## Philosophy

Sentinel Node is designed to be:

* **Simple** — easy to deploy and understand
* **Modular** — extend with custom sensors
* **Decentralized** — no single point of failure
* **Open** — fully transparent and hackable

---

## Contributing

Contributions are welcome. Open issues or submit pull requests to improve modules or add new integrations.

---

## License

MIT License
