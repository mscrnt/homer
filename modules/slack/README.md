# 💬 HOMER Slack Module

The `slack` module provides Slack integration for HOMER, enabling message sending, channel management, and Slack workspace interaction through both CLI and API interfaces.

---

## 📦 Module Contents

```text
slack/
├── api.py             # FastAPI routes for Slack operations
├── cli.py             # CLI commands for Slack integration
├── client.py          # Slack SDK wrapper and utilities
├── config.py          # Environment configuration schema
├── requirements.txt   # Python dependencies
├── Dockerfile         # Build script for containerization
├── Makefile           # Build and deployment targets
└── README.md          # This file
```

---

## 🧠 Module Capabilities

This module provides:

* ✅ Send messages to Slack channels
* ✅ List available channels
* ✅ Get channel information
* ✅ CLI commands for Slack operations
* ✅ FastAPI routes for programmatic access
* ✅ Environment-based configuration

---

## 💻 CLI Usage

```bash
# Send a message to a channel
./homer slack send --channel "#general" --message "Hello from HOMER!"

# List available channels
./homer slack channels

# Check module configuration
./homer slack ping
```

Or with Docker:

```bash
docker run --rm -e SLACK_BOT_TOKEN=your_token \
  mscrnt/homer:slack slack send --channel "#general" --message "Hello!"
```

---

## 🌐 API Routes

The `slack` module exposes the following API routes:

```http
GET  /slack/ping              # Health check
POST /slack/send              # Send message to channel
GET  /slack/channels          # List all channels
GET  /slack/channels/{id}     # Get channel information
```

Example API usage:

```bash
# Send a message
curl -X POST http://localhost:4242/slack/send \
  -H "Content-Type: application/json" \
  -d '{"channel": "#general", "text": "Hello from API!"}'

# List channels
curl http://localhost:4242/slack/channels
```

---

## 🔧 Environment Variables

This module requires the following environment variables:

| Variable               | Description                    | Required |
| ---------------------- | ------------------------------ | -------- |
| `SLACK_BOT_TOKEN`      | Slack bot token (xoxb-...)     | Yes      |
| `SLACK_APP_TOKEN`      | Slack app token (xapp-...)     | No       |
| `SLACK_SIGNING_SECRET` | Slack signing secret           | No       |
| `SLACK_DEFAULT_CHANNEL`| Default channel for operations | No       |

---

## 🔑 Slack App Setup

To use this module, you need to create a Slack app:

1. Go to https://api.slack.com/apps
2. Create a new app "From scratch"
3. Configure OAuth & Permissions:
   - Add bot token scopes: `chat:write`, `channels:read`, `groups:read`
4. Install the app to your workspace
5. Copy the "Bot User OAuth Token" (starts with `xoxb-`)

---

## 🐳 Docker Build

```bash
# Build the module image
make build

# Push to registry
make push
```

---

## 🧱 Stack Integration

To include this module in a stack, add to your stack Dockerfile:

```dockerfile
COPY modules/slack/ /homer/modules/slack/
RUN pip install -r /homer/modules/slack/requirements.txt
```

---

© Mscrnt, LLC – 2025