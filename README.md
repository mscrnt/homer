![HOMER Logo](./assets/homer-4.png)

# 🧠 HOMER

**Hub for Orchestrating Metadata, Events, and Resources**

**HOMER** is a modular Python + Docker automation framework designed to manage metadata, events, and resource workflows across diverse platforms. It provides a unified CLI and FastAPI interface for seamless integration with systems like GitHub, Confluence, Jira, ResourceSpace, and more.

Built for **modularity**, **composability**, and **security**, HOMER enables teams to orchestrate complex workflows while maintaining structured logging and isolated secrets.

---

## 🚀 Project Goals

### ✅ MVP

* Build a `homer-base` image with:

  * Shared CLI, FastAPI, config loader, and structured logging
* Modular layers:

  * `github`: GitHub automation
  * `atlassian`: Confluence + Jira support
  * `resourcespace`: DAM sync and ingestion
* Composable Docker stacks defined in `stacks/`
* Support CLI tooling, FastAPI services, and webhook triggers

### 🛠️ Future Capabilities

* Add modules for Slack, Teams, Notion, and Miro
* Enable cron-based or event-driven automation
* Support chatbot-style archive queries
* Maintain structured logs and secure secrets injection

---

## 🧱 Architecture Overview

HOMER is **layered and declarative**:

* 🧩 **Modules** — Located under `modules/`; copied into `homer/modules/` at build
* 🧱 **Stacks** — Layered task images built from `stacks/`; copied into `homer/stacks/`
* 💻 **CLI** — Powered by `Click` + `@register_cli(...)`
* ⚡ **FastAPI** — Auto-registers with `@register_api(...)`
* 🎯 **Entrypoint** — Smart detection of CLI, API, or daemon mode via `entrypoint.py`

---

## 📁 Folder Structure

```text
.
├── build_and_push_all.sh             # Build script for base/modules/stacks
├── README.md
├── Dockerfile                        # Base image (homer-base)
├── homer/
│   ├── api/                          # FastAPI core
│   ├── modules/                      # Populated at build
│   ├── stacks/                       # Populated at build
│   ├── utils/                        # Logging, config, decorators
│   ├── cli_registry.py               # CLI registration logic
│   ├── entrypoint.py                 # CLI/API launcher
│   ├── homer                         # CLI runner script
│   ├── Makefile                      # Make targets for builds
│   ├── requirements.txt              # Base dependencies
│   └── .env.example                  # Base-level env vars
├── modules/                          # Source modules (copied into image)
│   ├── github/
│   ├── atlassian/
│   ├── resourcespace/
│   ├── netbox/
│   ├── ha_api/
│   └── flow/
├── stacks/                           # Stack Dockerfiles
│   ├── github-atlassian/
│   └── homer-latest/                # Dynamically generated with all modules
├── examples/
│   ├── modules/                      # Module template
│   │   └── Dockerfile
│   └── stacks/                       # Stack template
│       └── Dockerfile
```

> `homer/modules/` and `homer/stacks/` are empty in the repo and **populated dynamically during Docker build**.

---

## 🧠 Dynamic CLI + API Registration

HOMER uses decorators for auto-registration:

```python
# cli.py
@register_cli("example")
@click.group()
def cli(): ...

# api.py
@register_api
class ExampleAPI(HomerAPI): ...
```

Each module should expose a CLI command group and (optionally) an API handler.

---

## 🐳 Docker Image Design

All modules and stacks are built from the same base:

```dockerfile
FROM mscrnt/homer:base
```

Resulting images are tagged as:

```
mscrnt/homer:<module>
mscrnt/homer:<stack>
```

The final `homer:latest` image includes **all available modules**.

---

## 🏗️ Building and Publishing Images

Use the provided script to build everything:

```bash
./build_and_push_all.sh
```

This script will:

* Build `mscrnt/homer:base`
* Build each module in `modules/`
* Create a combined `homer:latest` image with all modules
* Build all defined stacks except `homer-latest`
* Push all images to the registry

---

## 💻 CLI Usage

```bash
# Local CLI
./homer <module> <command> [args]

# Docker CLI
docker run --rm \
  -e HOMER_ENV=production \
  mscrnt/homer:<module> <module> <command>
```

---

## 🌐 API Usage

```bash
# Generic health check
curl http://localhost:4242/<module>/ping
```

---

## 🔐 Base Environment Variables

These base variables apply to all builds:

| Variable      | Description                                                |
| ------------- | ---------------------------------------------------------- |
| `HOMER_ENV`   | Runtime environment (default: `development`)               |
| `LOG_LEVEL`   | Logging level (`INFO`, `DEBUG`, etc.)                      |
| `CONFIG_PATH` | Path to shared config file (default: `config/config.yaml`) |

> Module-specific environment variables are documented within each module's README.

---

## 🧩 Available Modules

| Module          | Description                              |
| --------------- | ---------------------------------------- |
| `github`        | GitHub repo automation and syncing       |
| `atlassian`     | Confluence + Jira integration            |
| `resourcespace` | DAM metadata automation                  |
| `ha_api`        | Home Assistant integration               |
| `netbox`        | NetBox DCIM/IPAM connector               |
| `flow`          | Automation routing and conditional logic |

---

## 🧪 Creating a New Module

To scaffold your own module:

```bash
cp -r examples/modules modules/<your_module>
```

Each module should contain:

```text
cli.py
api.py
client.py
config.py
requirements.txt
Dockerfile
Makefile
README.md
```

You must define either a CLI or API entrypoint (or both) using the provided decorator patterns.

---

## 🧠 HOMER Philosophy

* **Modular** – Each module is self-contained and independently testable
* **Composable** – Stack modules as needed into tailored automation images
* **Transparent** – Logs everything with full context and structure
* **Secure** – No secrets in code; use `.env` or CI secrets
* **Extensible** – Add CLI, API, and daemon tasks easily across any platform

---

© Mscrnt, LLC – 2025