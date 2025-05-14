# 🎬 HOMER Flow Module (ShotGrid API)

The `flow` module integrates HOMER with [ShotGrid (formerly Shotgun)](https://www.autodesk.com/products/shotgrid/overview), enabling automation of asset, task, and metadata workflows using the ShotGrid Python API.

This module is named **Flow** in reference to production pipelines, shot flow, and asset tracking across animation, VFX, and game workflows.

---

## 🔧 Features

* ✅ ShotGrid connection test (ping)
* 📁 Project discovery (list, lookup by name or ID)
* 🛠️ Full CRUD support for any entity (create, find, update, delete, revive)
* 🔍 Schema inspection (entity types, field definitions)
* 📂 Playlist, Shot, Task, Version management
* 🧠 Activity & automation endpoint support (via API)
* 🧪 CLI and API co-exist under a unified module

---

## 📦 Dependencies

The module installs [ShotGrid Python API v3.8.1](https://github.com/shotgunsoftware/python-api/tree/v3.8.1) directly from GitHub to preserve compatibility.

```text
git+https://github.com/shotgunsoftware/python-api.git@v3.8.1
```

✅ Python 3.10 required

---

## 🐳 Docker Support

This module is part of the HOMER Docker stack and includes:

* Git client for Python API installation
* ShotGrid CLI + FastAPI support
* Can be built independently or as part of `mscrnt/homer:latest`

---

## 🚀 Usage

### CLI

All commands are namespaced under the `flow` group:

```bash
docker run --rm -it \
  -e SG_SITE=https://your-team.shotgrid.autodesk.com \
  -e SG_SCRIPT_NAME=your_script \
  -e SG_API_KEY=your_key \
  mscrnt/homer:flow flow --help
```

#### Core Commands

```bash
flow ping                          # Check ShotGrid connection
flow crud find ...                # Generic entity queries
flow crud find-one ...            # Find a single entity
flow crud create ...              # Create an entity
flow crud update ...              # Modify entity fields
flow crud delete ...              # Soft delete
flow crud revive ...              # Revive deleted
flow crud summarize ...           # Aggregate stats
```

#### Tools

```bash
flow tools list-projects                             # List all projects
flow tools get-project-id --name "Solo Leveling"     # Look up a project ID by name
flow tools get-project-name --id 122                 # Look up project name from ID
```

#### Schema

```bash
flow schema entities               # List entity types
flow schema fields --entity Shot   # List fields for entity type
```

---

## 📡 API

All routes are registered under `/flow` via FastAPI when running the server:

```bash
docker run --rm -p 8080:8080 mscrnt/homer:flow serve-api
```

Then visit:

```
http://localhost:8080/docs
```

Example endpoints:

* `GET /flow/ping`
* `GET /flow/schema/entities`
* `GET /flow/schema/{entity}/fields`
* `GET /flow/tools/projects`
* `GET /flow/tools/project-id?name=Overwatch`
* `GET /flow/tools/project-name?id=122`

---

## 🧩 Module Tree

```
modules/flow/
├── cli.py                       # Registers main flow CLI group
├── client.py                    # ShotGrid connection
├── config.py                    # Env loader + validation
├── logic/                       # Business logic for all features
│   ├── actions.py
│   ├── crud.py
│   ├── schema.py
│   ├── tools.py
│   └── ...
├── cli_functions/               # CLI entrypoints per command group
├── routes/                      # FastAPI routers for each area
├── requirements.txt
└── README.md
```

---

## 🔐 Environment Variables

| Variable         | Description                 |
| ---------------- | --------------------------- |
| `SG_SITE`        | Your ShotGrid site URL      |
| `SG_SCRIPT_NAME` | Script user name            |
| `SG_API_KEY`     | API key for the script user |

You can use `.env` to supply these automatically for local testing.

---

## 🧠 Roadmap

| Feature                    | Status        |
| -------------------------- | ------------- |
| ShotGrid CLI               | ✅ Complete    |
| API endpoints              | ✅ Complete    |
| Playlist + Task automation | ⏳ In Progress |
| FastAPI webhook support    | 🔜 Planned    |

---

## 🤝 Contributing

This module is essential for connecting HOMER to studio pipeline tools. Feel free to submit issues or feature suggestions via Github.
