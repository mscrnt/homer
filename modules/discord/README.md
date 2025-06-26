# 🎬 HOMER Discord Module

The `discord` module is an integration for HOMER that connects to Discord using `discord.py`, enabling CLI and API control of a bot or client instance, scheduled background tasks, and modular command logic via cogs.

---

## 📦 Module Contents

```text
discord/
├── __init__.py         # Python package marker
├── api.py              # FastAPI routes for Discord control & messaging
├── cli.py              # CLI group for starting bot/client modes
├── client.py           # Defines commands.Bot and discord.Client wrappers
├── config.py           # Environment schema (DISCORD_BOT_TOKEN, etc.)
├── requirements.txt    # Python dependencies for Discord bot
├── Dockerfile          # Build script for containerized usage
├── Makefile            # Build + push targets for this module
├── README.md           # This file
├── cli_functions/      # CLI helper functions
│   └── __init__.py
├── logic/              # Shared logic for CLI/API reuse
│   ├── __init__.py
│   ├── intents.py      # Builds discord.Intents from env
│   ├── runner.py       # Shared bot/client launcher
│   ├── cogs/           # Modular bot logic (commands, tasks, events)
│   │   ├── __init__.py
│   │   ├── commands.py
│   │   ├── events.py
│   │   └── periodic.py
│   ├── tasks/          # Background @tasks.loop definitions
│   │   ├── __init__.py
│   │   ├── batcher.py
│   │   ├── debug.py
│   │   ├── registry.py
│   │   └── scheduler.py
│   └── utils/          # Discord utilities
│       ├── __init__.py
│       ├── converters.py
│       └── flags.py
└── routes/             # API route implementations
    ├── __init__.py
    ├── bot.py
    └── message.py
```

---

## 🧠 Module Capabilities

This module provides:

* ✅ Environment-driven Discord intents configuration
* ✅ Shared runner for `commands.Bot` and `discord.Client`
* ✅ Auto-registration for cogs and task loops
* ✅ CLI support for launching bot/client
* ✅ FastAPI routes for programmatic Discord control
* ✅ Modular command system via cogs
* ✅ Background task scheduling
* ✅ Event handling and message processing

---

## 🔧 Environment Variables

| Variable                | Description                           | Default     |
| ----------------------- | ------------------------------------- | ----------- |
| `DISCORD_BOT_TOKEN`     | Discord bot token                     | Required    |
| `DISCORD_INTENTS`       | Comma-separated list of intents       | `guilds,messages` |
| `DISCORD_COMMAND_PREFIX`| Bot command prefix                    | `!`         |
| `DISCORD_LOG_LEVEL`     | Discord.py logging level             | `INFO`      |

---

## 💻 CLI Usage

```bash
# Start Discord bot
./homer discord bot

# Start Discord client
./homer discord client

# Check module status
./homer discord ping

# Test connection
./homer discord test-connection
```

Or with Docker:

```bash
docker run --rm -e DISCORD_BOT_TOKEN=your_token \
  mscrnt/homer:discord discord bot
```

---

## 🌐 API Routes

```http
GET  /discord/ping           # Health check
POST /discord/bot/start      # Start bot instance
POST /discord/bot/stop       # Stop bot instance
GET  /discord/bot/status     # Bot status
POST /discord/message/send   # Send message
GET  /discord/guilds         # List guilds
```

Example API usage:

```bash
# Send message
curl -X POST http://localhost:4242/discord/message/send \
  -H "Content-Type: application/json" \
  -d '{"channel_id": "123456789", "content": "Hello Discord!"}'

# Get bot status
curl http://localhost:4242/discord/bot/status
```

---

## 🧪 Development and Testing

```bash
# Validate module structure
make validate-module MODULE=discord

# Test locally
python -m homer.modules.discord.cli ping

# Build and test
make build-module MODULE=discord
```

## 🐳 Docker Build

```bash
# Validate before building (recommended)
make validate-module MODULE=discord

# Build the module image
make build-module MODULE=discord

# Or manually
cd modules/discord
make build

# Push to registry
make push
```

---

## 🤖 Discord Bot Setup

1. Go to https://discord.com/developers/applications
2. Create a new application
3. Go to "Bot" section and create a bot
4. Copy the bot token
5. Set `DISCORD_BOT_TOKEN` environment variable
6. Invite bot to your server with appropriate permissions

---

## 🔄 Integration Examples

### Slack-Discord Bridge
```bash
# Forward Slack messages to Discord
./homer slack listen --channel "#general" | \
./homer discord send --channel "123456789"
```

### Automated Notifications
```bash
# Send build status to Discord
BUILD_STATUS=$(make build 2>&1)
./homer discord send --channel "123456789" --content "🔨 Build Status: $BUILD_STATUS"
```

---

## 🧱 Stack Integration

Include in stack Dockerfile:

```dockerfile
COPY modules/discord/ /homer/modules/discord/
RUN pip install -r /homer/modules/discord/requirements.txt
```

---

## 🎯 Use Cases

* **Team Communication**: Bot for automated notifications
* **Workflow Integration**: Discord updates from CI/CD
* **Community Management**: Automated moderation and responses
* **Event Coordination**: Scheduled announcements and reminders
* **Integration Hub**: Connect Discord with other HOMER modules

---

© Mscrnt, LLC – 2025