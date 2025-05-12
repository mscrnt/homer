![HOMER Logo](./assets/homer-4.png)

# 🧠 HOMER  
**Hub for Orchestrating Metadata, Events, and Resources**

**HOMER** is a modular Python + Docker automation framework built for managing metadata, events, and resources across multiple platforms. It provides a unified CLI and FastAPI interface for seamless integration with various services like GitHub, Atlassian (Confluence + Jira), and ResourceSpace.
It is designed to be extensible, allowing for easy addition of new modules and stacks as needed.
It is built with a focus on modularity, composability, and security, ensuring that all logs are structured and secrets are kept isolated.

---

## 🚀 Project Goals

### ✅ MVP
- Build `homer-base` image with:
  - Shared CLI, FastAPI, config loader, and logging
- Modular layers:
  - `github`: GitHub automation
  - `atlassian`: Confluence + Jira support
  - `resourcespace`: DAM automation, metadata sync
- Composable Docker images via `stacks/`
- Support CLI tooling, FastAPI service mode, and webhooks

### 🛠️ Future Capabilities
- Add support for Slack, Teams, Notion, Miro
- Support cron-based + webhook triggers
- Enable chatbot-style archive queries
- Keep secrets isolated and logs fully structured

---

## 🧱 Architecture Overview

HOMER is layered and declarative:

- 🧩 **Modules** — `modules/github`, `modules/atlassian`, `modules/resourcespace`, etc.
- 🧱 **Stacks** — e.g. `homer-github-atlassian`, combining modules
- 💻 **CLI** — Powered by `Click` and `@register_cli(...)`
- ⚡ **FastAPI** — Auto-detects and mounts all registered module APIs
- 🎯 **Entrypoint** — Smart detection: CLI vs API/daemon

---

## 📁 Folder Structure

```text
homer/
├── homer/                         
│   ├── api/                       # FastAPI + dynamic loading
│   ├── utils/                     # Logger, config, HTTP client
│   ├── modules/                  
│   │   ├── github/              # GitHub sync
│   │   ├── atlassian/             # Confluence + Jira
│   │   └── resourcespace/         # DAM tools via ResourceSpace
│   ├── stacks/                   # Stack-specific logic (e.g. GitHub + Jira sync)
│   ├── cli_registry.py           # CLI decorator system
│   ├── entrypoint.py             # Entry router (CLI, daemon, etc)
│   └── homer                     # CLI script
├── modules/                      # Dockerfiles for composed modules
├── stacks/                       # Dockerfiles for composed stacks
├── requirements.txt
├── Dockerfile                    # Base image
└── assets/
````

## 🧠 Dynamic CLI + API Registration

### CLI Modules

```python
# modules/resourcespace/cli.py
@register_cli("resourcespace")
@click.group()
def cli(): ...
```

### FastAPI Modules

```python
# modules/resourcespace/api.py
@register_api
class ResourceSpaceAPI(HomerAPI): ...
```

---

## 🐳 Entrypoint Behavior

`entrypoint.py` smartly switches modes:

| Behavior                  | Example                                           |
| ------------------------- | ------------------------------------------------- |
| 🧠 Run CLI                | `docker run homer-base github fetch --repo ...` |
| 🚀 Serve FastAPI          | `docker run -p 4242:4242 homer-base`              |
| 🔄 Launch workers/daemons | *(future release)*                                |

---

## 📦 Stack Docker Example

### `stacks/homer-github-atlassian/Dockerfile`

```Dockerfile
FROM homer-base

USER root

# Install Python deps
COPY modules/github/requirements.txt /tmp/github.txt
COPY modules/atlassian/requirements.txt /tmp/atlassian.txt
RUN pip install --no-cache-dir -r /tmp/github.txt -r /tmp/atlassian.txt

# Copy modules and stack code
COPY modules/github/ /homer/modules/github/
COPY modules/atlassian/ /homer/modules/atlassian/
COPY stacks/homer-github-atlassian/ /homer/stacks/homer-github-atlassian/

USER homer
```

```bash
docker build -t homer-github-atlassian -f stacks/homer-github-atlassian/Dockerfile .
```

---

## 💻 CLI Usage

```bash
# ResourceSpace CLI examples
./homer resourcespace resource get-resource-info --id 123
./homer resourcespace metadata update-field --resource-id 123 --field-id 12 --value "Production Ready"
./homer resourcespace collection create-collection --name "Upload Bucket"

# Stack-based command
./homer docsync sync-docs --repo sfd/docs

# Docker CLI
docker run --rm \
  -e RS_API_URL=http://10.130.48.193 \
  -e RS_API_USER=admin \
  -e RS_API_KEY=b0f9c323f... \
  homer-resourcespace resourcespace system get-system-status
```

---

## 🌐 API Examples

### Health check

```bash
curl http://localhost:4242/resourcespace/ping
```

---

## 🔐 Environment Variables

| Key                    | Description                |
| ---------------------- | -------------------------- |
| `GH_TOKEN`             | GitHub token               |
| `REPO_URL`             | Target repo URL (for automation)      |
| `CONFLUENCE_API_TOKEN` | Confluence API token       |
| `CONFLUENCE_SPACE_KEY` | Space key                  |
| `CONFLUENCE_API_URL`   | Optional override for Confluence API  |
| `JIRA_API_TOKEN`       | Jira token                 |
| `JIRA_PROJECT_KEY`     | Jira project key                      |
| `RS_API_URL`           | ResourceSpace API base URL |
| `RS_API_USER`          | ResourceSpace username     |
| `RS_API_KEY`           | ResourceSpace private key  |

---

## 🧩 Available Modules

| Module          | Description                                |
| --------------- | ------------------------------------------ |
| `github`        | GitHub sync: markdown, workflows, metadata |
| `atlassian`     | Confluence + Jira metadata publishing      |
| `resourcespace` | DAM workflows: resources, metadata, search |
| `slack`         | *(Planned)* Slack alerts + automation      |
| `miro`          | *(Planned)* Whiteboard + planning sync     |

---

## 🧠 HOMER Philosophy

* **Modular** – Add/remove CLI/API modules independently
* **Composable** – Stack Dockerfiles to bundle workflows
* **Transparent** – All logs are structured per module
* **Secure** – Secrets via `.env` or environment only
* **Extensible** – CLI + API + workers in one architecture

---

© Mscrnt, LLC – 2025

