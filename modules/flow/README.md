# 🎬 HOMER Flow Module (ShotGrid API)

The `flow` module integrates HOMER with [ShotGrid (formerly Shotgun)](https://www.autodesk.com/products/shotgrid/overview), enabling automation of asset, task, and metadata workflows using the ShotGrid Python API.

This module is named **Flow** in reference to production pipelines, shot flow, and asset tracking across animation/VFX/game pipelines.

---

## 🔧 Features

- Connect to ShotGrid via API Script
- Automate asset/task sync or metadata extraction
- Compose into full HOMER stacks (e.g., `flow-resourcespace`)
- CLI-ready with support for FastAPI endpoints (optional)

---

## 📦 Dependencies

The module installs [ShotGrid Python API v3.8.1](https://github.com/shotgunsoftware/python-api/tree/v3.8.1) directly from GitHub to preserve compatibility and vendored files.

Installed via:

```text
git+https://github.com/shotgunsoftware/python-api.git@v3.8.1
````

**Note:** Python 3.10 is required due to ShotGrid compatibility limits.

---

## 🐳 Dockerfile

This module builds on `homer:base` and includes:

* Git client for pulling the API repo
* ShotGrid API installed via `requirements.txt`

---

## 🚀 Usage

### CLI (Coming Soon)


### API (Coming Soon)

FastAPI endpoints for Flow module will be available in a future release.

---

## 🧪 Example CLI Entry Point

```python
@click.group()
def flow():
    """Flow (ShotGrid) module commands."""
    pass

@flow.command()
@click.option("--site", required=True)
@click.option("--script-name", required=True)
@click.option("--api-key", required=True)
def ping(site, script_name, api_key):
    from shotgun_api3 import Shotgun
    sg = Shotgun(site, script_name, api_key)
    click.echo(f"✅ Connected to ShotGrid {sg.server_info.get('version')}")
```

---

## 🧩 Integration Plan

| Feature                  | Status        |
| ------------------------ | ------------- |
| ShotGrid Connection Test | ✅ Done        |
| Asset Pull + Sync        | ⏳ In Progress |
| Task/Shot Status Ingest  | ⏳ Planned     |
| FastAPI Interface        | ⏳ Planned     |

---

## 📁 Files

```
modules/
└── flow/
    ├── cli.py                  # Command-line entry
    ├── client.py               # ShotGrid wrapper (optional)
    ├── README.md               # This file
    └── requirements.txt        # API dependency
```

---

## 🔐 Env Vars (if needed)

| Variable         | Description                 |
| ---------------- | --------------------------- |
| `SG_SITE`        | ShotGrid site URL           |
| `SG_SCRIPT_NAME` | Script name for API access  |
| `SG_API_KEY`     | API key for the script user |
