# 🔧 HOMER Perforce Module

The `perforce` module provides Perforce (Helix Core) integration for HOMER, enabling changelist management, stream operations, and depot synchronization through both CLI and API interfaces.

---

## 📦 Module Contents

```text
perforce/
├── api.py             # FastAPI routes for Perforce operations
├── cli.py             # CLI commands for Perforce integration
├── client.py          # Perforce CLI wrapper and utilities
├── config.py          # Environment configuration schema
├── requirements.txt   # Python dependencies
├── Dockerfile         # Build script with P4 CLI tools
├── Makefile           # Build and deployment targets
└── README.md          # This file
```

---

## 🧠 Module Capabilities

This module provides:

* ✅ Changelist retrieval and analysis
* ✅ Stream listing and management
* ✅ Depot file synchronization
* ✅ Workspace information
* ✅ Search functionality for changelists
* ✅ CLI commands for all Perforce operations
* ✅ FastAPI routes for programmatic access

---

## 💻 CLI Usage

```bash
# Get changelist details
./homer perforce changelist 12345 --output changelist.json

# List recent changelists
./homer perforce changes --user john.doe --max 50

# List streams
./homer perforce streams

# Sync files
./homer perforce sync "//depot/main/..."

# Get workspace info
./homer perforce info

# Check configuration
./homer perforce ping
```

Or with Docker:

```bash
docker run --rm \
  -e P4PORT=ssl:perforce.company.com:1666 \
  -e P4USER=username \
  -e P4CLIENT=workspacename \
  mscrnt/homer:perforce perforce changes --max 10
```

---

## 🌐 API Routes

The `perforce` module exposes the following API routes:

```http
GET  /perforce/ping                    # Health check
GET  /perforce/changelist/{id}         # Get changelist details
GET  /perforce/changelists             # List changelists
GET  /perforce/streams                 # List streams
POST /perforce/sync                    # Sync files
GET  /perforce/info                    # Workspace info
GET  /perforce/search                  # Search changelists
```

Example API usage:

```bash
# Get changelist details
curl http://localhost:4242/perforce/changelist/12345

# List recent changelists
curl "http://localhost:4242/perforce/changelists?user=john.doe&max_results=10"

# Search changelists
curl "http://localhost:4242/perforce/search?query=bugfix&max_results=5"

# Sync files
curl -X POST http://localhost:4242/perforce/sync \
  -H "Content-Type: application/json" \
  -d '{"filespec": "//depot/main/..."}'
```

---

## 🔧 Environment Variables

This module requires the following environment variables:

| Variable   | Description                    | Required |
| ---------- | ------------------------------ | -------- |
| `P4PORT`   | Perforce server port           | Yes      |
| `P4USER`   | Perforce username              | Yes      |
| `P4CLIENT` | Perforce workspace/client name | No       |
| `P4PASSWD` | Perforce password              | No       |
| `P4TRUST`  | Perforce trust settings        | No       |

---

## 🔑 Perforce Setup

To use this module with your Perforce server:

1. Ensure you have access to a Perforce server
2. Set the required environment variables:
   - `P4PORT`: Your Perforce server address (e.g., `ssl:perforce.company.com:1666`)
   - `P4USER`: Your Perforce username
   - `P4CLIENT`: Your workspace name (optional)
3. If using authentication, set `P4PASSWD` or ensure you have a valid ticket

---

## 🚀 Integration Examples

### AI-Powered Changelist Analysis
Combine with OpenAI for intelligent code review:

```bash
# Get changelist and analyze with AI
CHANGELIST=$(./homer perforce changelist 12345 --output /tmp/cl.json)
DESCRIPTION=$(cat /tmp/cl.json | jq -r '.description')
./homer openai sentiment --text "$DESCRIPTION"
./homer openai tags --text "$DESCRIPTION"
```

### Slack Notifications
Send changelist updates to Slack:

```bash
# Monitor new changelists and notify team
LATEST=$(./homer perforce changes --max 1 | head -1)
./homer slack send --channel "#dev-updates" --message "📋 New changelist: $LATEST"
```

### Cross-Module Workflow
Create a complete automation pipeline:

```bash
#!/bin/bash
# Get latest changelist
CL=$(./homer perforce changes --max 1 --output /tmp/latest.json)
CL_ID=$(cat /tmp/latest.json | jq -r '.[0].id')
CL_DESC=$(cat /tmp/latest.json | jq -r '.[0].description')

# Analyze with AI
SUMMARY=$(./homer openai summarize --text "$CL_DESC")
SENTIMENT=$(./homer openai sentiment --text "$CL_DESC")

# Send to Slack
./homer slack send --channel "#code-review" \
  --message "🔧 Changelist $CL_ID Summary: $SUMMARY (Sentiment: $SENTIMENT)"
```

---

## 🐳 Docker Build

```bash
# Build the module image (includes P4 CLI tools)
make build

# Push to registry
make push
```

---

## 🧱 Stack Integration

To include this module in a stack, add to your stack Dockerfile:

```dockerfile
COPY modules/perforce/ /homer/modules/perforce/
RUN pip install -r /homer/modules/perforce/requirements.txt
```

---

## 🎯 Use Cases

* **Code Review Automation**: Analyze changelist descriptions with AI
* **Release Management**: Track changes across streams
* **Notification Systems**: Alert teams about important changes
* **Compliance**: Monitor code changes for audit trails
* **Integration**: Sync Perforce data with other tools

---

## ⚠️ Prerequisites

This module requires:
- Perforce CLI tools (automatically installed in Docker)
- Network access to your Perforce server
- Valid Perforce credentials
- Appropriate permissions for the operations you want to perform

---

© Mscrnt, LLC – 2025