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
├── build_and_push_all.sh             # Build script with validation
├── Makefile                          # Project-wide build targets
├── README.md
├── VALIDATION_REPORT.md              # Validation system documentation
├── .github/
│   └── workflows/
│       └── validate-and-build.yml    # CI/CD with validation
├── scripts/                          # Validation and automation scripts
│   ├── validate-module.sh            # Module structure validation
│   ├── validate-stack.sh             # Stack validation
│   ├── fix-module-structure.sh       # Auto-fix common issues
│   ├── pre-build-check.sh            # Comprehensive validation
│   ├── validate-all.sh               # Legacy validation
│   └── README.md                     # Scripts documentation
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
│   ├── atlassian/                    # Confluence + Jira integration
│   ├── discord/                      # Discord bot integration
│   ├── flow/                         # Automation routing and logic
│   ├── github/                       # GitHub automation
│   ├── ha_api/                       # Home Assistant integration
│   ├── netbox/                       # NetBox DCIM/IPAM connector
│   ├── openai/                       # OpenAI API integration
│   ├── perforce/                     # Perforce version control
│   ├── resourcespace/                # DAM metadata automation
│   ├── slack/                        # Slack integration
│   └── syncsketch/                   # Creative review workflows
├── stacks/                           # Composable Docker stacks
│   ├── github-atlassian/             # GitHub + Atlassian workflow
│   ├── perforce-openai/              # AI-powered code analysis
│   ├── slack-syncsketch/             # Creative workflow notifications
│   └── homer-latest/                 # Auto-generated all-modules stack
├── examples/
│   ├── modules/                      # Module template and documentation
│   └── stacks/                       # Stack template and documentation
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

### Quick Start

Use the Makefile for validated builds:

```bash
# Validate and build everything (recommended)
make build

# Just validate without building
make validate

# Validate with auto-fixes
make validate-fix

# Build specific module
make build-module MODULE=openai

# Build specific stack
make build-stack STACK=perforce-openai
```

### Advanced Building

Use the build script directly:

```bash
# Build with validation (default)
./build_and_push_all.sh

# Skip validation (not recommended)
./build_and_push_all.sh --no-validate
```

### Validation First (Recommended)

Before building, run validation to catch issues:

```bash
# Quick validation
./scripts/pre-build-check.sh

# Validation with auto-fixes
./scripts/pre-build-check.sh --fix

# Validate specific component
./scripts/validate-module.sh modules/openai
./scripts/validate-stack.sh stacks/perforce-openai
```

The build process will:

* **Validate** all modules and stacks
* **Auto-fix** common issues (with `--fix` flag)
* **Build** `mscrnt/homer:base`
* **Build** each module in `modules/`
* **Create** a combined `homer:latest` image with all modules
* **Build** all defined stacks
* **Push** all images to the registry

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

| Module          | Description                              | Status |
| --------------- | ---------------------------------------- | ------ |
| `atlassian`     | Confluence + Jira integration            | ✅ Ready |
| `discord`       | Discord bot and webhook integration      | ✅ Ready |
| `flow`          | Automation routing and conditional logic | ✅ Ready |
| `github`        | GitHub repo automation and syncing       | ✅ Ready |
| `ha_api`        | Home Assistant integration               | ✅ Ready |
| `netbox`        | NetBox DCIM/IPAM connector               | ✅ Ready |
| `openai`        | OpenAI API integration for AI workflows  | ✅ Ready |
| `perforce`      | Perforce version control integration     | ✅ Ready |
| `resourcespace` | DAM metadata automation                  | ✅ Ready |
| `slack`         | Slack messaging and workflow integration | ✅ Ready |
| `syncsketch`    | Creative review and collaboration tools  | ✅ Ready |

## 🧱 Available Stacks

| Stack               | Modules              | Description                        | Status |
| ------------------- | -------------------- | ---------------------------------- | ------ |
| `github-atlassian`  | github + atlassian   | Development workflow automation    | ✅ Ready |
| `perforce-openai`   | perforce + openai    | AI-powered code analysis           | ✅ Ready |
| `slack-syncsketch`  | slack + syncsketch    | Creative workflow notifications    | ✅ Ready |
| `homer-latest`      | all modules          | Complete HOMER installation       | ✅ Auto-generated |

---

## 🧪 Creating a New Module

### 1. Scaffold from Template

```bash
# Copy the example module
cp -r examples/modules modules/<your_module>

# Fix structure and validate
./scripts/fix-module-structure.sh modules/<your_module>
make validate-module MODULE=<your_module>
```

### 2. Required Files

Each module must contain:

```text
├── __init__.py                 # Python package marker
├── api.py                      # FastAPI routes with @register_api
├── cli.py                      # CLI commands with @register_cli
├── client.py                   # API client/wrapper logic
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container build instructions
├── Makefile                    # Build targets
├── README.md                   # Module documentation
├── cli_functions/              # CLI helper functions
│   └── __init__.py
├── logic/                      # Core business logic
│   └── __init__.py
└── routes/                     # API route implementations
    └── __init__.py
```

### 3. Development Workflow

```bash
# 1. Create module structure
make validate-module MODULE=<your_module>

# 2. Implement functionality
# Edit api.py, cli.py, client.py, etc.

# 3. Test locally
make build-module MODULE=<your_module>

# 4. Validate before commit
make validate-fix
```

### 4. Required Decorators

You must use these decorators for auto-registration:

```python
# cli.py
@register_cli("your_module")
@click.group()
def cli():
    """Your module CLI"""
    pass

# api.py  
@register_api
class YourModuleAPI(HomerAPI):
    """Your module API"""
    
    def get(self, path: str = "/ping"):
        return {"status": "ok", "module": "your_module"}
```

---

## 🔍 Validation & CI/CD

HOMER includes comprehensive validation to prevent build failures and ensure consistency:

### Validation Tools

- **`scripts/validate-module.sh`** - Validates individual module structure
- **`scripts/validate-stack.sh`** - Validates stack configuration  
- **`scripts/fix-module-structure.sh`** - Auto-fixes common issues
- **`scripts/pre-build-check.sh`** - Comprehensive validation with auto-fix

### GitHub Actions

Automated CI/CD pipeline at `.github/workflows/validate-and-build.yml`:

1. **Validates** all modules and stacks
2. **Auto-fixes** issues when possible
3. **Builds** base image, modules, and stacks in parallel
4. **Pushes** images to registry (main branch only)

### Pre-commit Validation

Prevent issues before they reach CI:

```bash
# Quick check
make validate

# Fix and validate
make validate-fix

# Check specific component
make validate-module MODULE=openai
```

### Common Validations

- ✅ Required files and directories present
- ✅ Python decorators (`@register_cli`, `@register_api`)
- ✅ Dockerfile best practices (layer caching, security)
- ✅ Dependencies properly declared
- ✅ Module/stack integration compatibility

---

## 🧠 HOMER Philosophy

* **Modular** – Each module is self-contained and independently testable
* **Composable** – Stack modules as needed into tailored automation images
* **Transparent** – Logs everything with full context and structure
* **Secure** – No secrets in code; use `.env` or CI secrets
* **Extensible** – Add CLI, API, and daemon tasks easily across any platform

---

© Mscrnt, LLC – 2025