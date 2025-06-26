# 🎬 HOMER Example Module

The `example` module is a simple demonstration of how to create a module for HOMER. It includes CLI and API components, showing how to register commands, routes, configuration, and logic in a standard, reusable format.

You can use this as a template for your own module's `README.md`.

---

## 📦 Module Contents

```text
example/
├── api.py             # FastAPI routes registered with @register_api
├── cli.py             # CLI group registered with @register_cli
├── client.py          # Shared request logic (e.g., wrappers, helpers)
├── config.py          # Default config loader and structure
├── logic/             # Internal Python logic and workflows
│   └── example_logic.py
├── requirements.txt   # Python dependencies for this module
├── Dockerfile         # Build script for dockerized usage
├── Makefile           # Build + push target for this module
└── README.md          # (this file)
````

---

## 🧠 Module Capabilities

This module demonstrates:

* ✅ CLI command group with subcommands
* ✅ FastAPI route registration
* ✅ Typed config loading and defaults
* ✅ Isolated logic functions
* ✅ Docker-ready for stack composition

---

## 💻 CLI Usage

Once built or included in a stack, you can run the CLI via:

```bash
./homer example ping
```

Or with Docker:

```bash
docker run --rm mscrnt/homer:example example ping
```

---

## 🌐 API Routes

The `example` module exposes the following API routes:

```http
GET /example/ping     # Returns a status JSON
```

You can test the route locally using:

```bash
curl http://localhost:4242/example/ping
```

---

## 🔧 Environment Variables

This module supports the following optional env vars:

| Variable          | Description                        | Default  |
| ----------------- | ---------------------------------- | -------- |
| `EXAMPLE_MODE`    | Controls response behavior         | `"demo"` |
| `EXAMPLE_TIMEOUT` | Max wait time for operations (sec) | `"5"`    |

> These should be added to your `.env` or passed as `-e` flags in Docker.

---

## 🔌 CLI Registration

```python
# cli.py
@register_cli("example")
@click.group()
def cli():
    "Example CLI group for HOMER"
    ...

@cli.command("ping")
def ping():
    click.echo("pong 🏓")
```

---

## 🚀 API Registration

```python
# api.py
@register_api
class ExampleAPI(HomerAPI):
    @get("/ping")
    def ping(self):
        return {"status": "ok", "module": "example"}
```

---

## 🧪 Local Testing

```bash
# Validate module structure
make validate-module MODULE=example

# Run CLI manually
python homer/homer example ping

# Run API locally
uvicorn homer.api.main:app --reload

# Build and test
make build-module MODULE=example
```

---

## 🐳 Docker Build

Best practice Dockerfile pattern:

```dockerfile
# Dockerfile
FROM mscrnt/homer:base

USER root

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (for better layer caching)
COPY modules/example/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy module code
COPY modules/example/ /homer/modules/example/

USER homer
```

To build and validate:

```bash
# Validate first (recommended)
make validate-module MODULE=example

# Build
make build-module MODULE=example

# Or manually
docker build -t mscrnt/homer:example .
```

---

## 📁 Integration Notes

When included in a stack, this module will be mounted to:

```text
/homer/modules/example/
```

It will be auto-registered on both CLI and API layers by HOMER’s `entrypoint.py`.

---

## 🧱 Stack Inclusion

To use this module in a stack:

1. Add the module’s folder under `modules/`
2. Modify your stack Dockerfile:

```dockerfile
COPY modules/example/ /homer/modules/example/
```

3. Install dependencies:

```dockerfile
RUN pip install -r /homer/modules/example/requirements.txt
```

---

## 🧠 Philosophy

This module is minimal on purpose — a template to build real functionality from. Use this pattern to:

* Create isolated, testable integrations
* Provide CLI + API access to the same logic
* Extend HOMER without modifying core files

---

© Mscrnt, LLC – 2025
