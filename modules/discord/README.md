Here’s your revised `README.md` for the Discord module, reflecting current progress and clarifying that it's a **work in progress**:

---

````markdown
# 🎬 HOMER Discord Module

The `discord` module is an integration for HOMER that connects to Discord using `discord.py`, enabling CLI and API control of a bot or client instance, scheduled background tasks, and modular command logic via cogs.

> **Status:** 🚧 Work in Progress  
> This module is currently being scaffolded. Core features like intents, CLI launch logic, and cog/task registration are under active development.

---

## 📦 Module Contents

```text
discord/
├── api.py             # (planned) FastAPI routes for control & messaging
├── cli.py             # CLI group for starting bot/client modes
├── client.py          # Defines commands.Bot and discord.Client wrappers
├── config.py          # Environment schema (DISCORD_BOT_TOKEN, etc.)
├── logic/             # Shared logic for CLI/API reuse
│   ├── intents.py         # Builds discord.Intents from env
│   ├── runner.py          # Shared bot/client launcher
│   ├── cogs/              # Modular bot logic (commands, tasks, events)
│   └── tasks/             # Background @tasks.loop definitions
├── requirements.txt   # Python dependencies for Discord bot
├── Dockerfile         # Build script for dockerized usage
├── Makefile           # Build + push targets for this module
└── README.md          # (this file)
````

---

## 🧠 Module Capabilities (WIP)

So far, this module supports:

* ✅ Environment-driven intents (`intents.py`)
* ✅ Shared runner for `commands.Bot` and `discord.Client` (`runner.py`)
* 🧠 Auto-registration for cogs and task loops (in progress)
* 🧠 CLI support for launching bot/client (in progress)
* ⏳ API control routes (planned)

---

## 🔧 Environment Variables

This module expects the following:

| Variable            | Description                               |
| ------------------- | ----------------------------------------- |
| `DISCORD_BOT_TOKEN` | Token for your Discord bot                |
| `DISCORD_MODE`      | `"bot"` or `"client"`                     |
| `DISCORD_INTENTS`   | Comma-separated list of intents to enable |

---

## 💻 CLI Launch Example

```bash
# Run as bot
./homer discord run --mode bot

# Run as raw client
./homer discord run --mode client
```

---

## 🧠 Philosophy

This module follows HOMER’s design goals:

* Modular, testable components (cogs, tasks, CLI)
* Shared logic between CLI and API
* Isolated logic for commands and automation
* Scalable support for hybrid commands, scheduled tasks, and rich events

---

© Mscrnt, LLC – 2025