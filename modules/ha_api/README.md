# 🏠 HOMER Module: `ha_api`
**Home Assistant Integration for HOMER Automation Framework**

This module connects HOMER to [Home Assistant](https://www.home-assistant.io/) via its REST and WebSocket APIs using the excellent [`HomeAssistant-API`](https://pypi.org/project/HomeAssistant-API/) Python package.

It enables scripting, service control, state inspection, and event listening across your smart home — all through the HOMER CLI and automation workflows.

---

## 🚀 Features

- ✅ Sync + Async client support (REST + WS)
- 🧠 Typed access to `Entity`, `State`, `Domain`, `Service`, and `Event` objects
- 🛠️ CLI for common automation tasks (toggle lights, fire events, read sensors)
- 🖥️ WebSocket event and trigger listeners
- 🧾 Logbook, History, and Config fetchers
- 🧰 Built-in helper commands for smart home debugging
- 🐳 Docker-ready with `.env` support and caching

---

## 📦 Installation

This module is included in your stacked `homer` image when using the `ha_api` variant.

To use it standalone in development:

```bash
pip install HomeAssistant-API
````

---

## ⚙️ Environment Variables

Create a `.env` file in `modules/ha_api/` or pass variables into Docker. Required:

```dotenv
HA_API_URL=http://192.168.69.11:8123/api
HA_API_TOKEN=your_long_lived_access_token

# Optional:
HA_WS_URL=ws://192.168.69.11:8123/api/websocket
HA_ENABLE_CACHE=true
```

An example is generated at:

```
modules/ha_api/.env.example
```

---

## 🧪 CLI Examples

```bash
# Ping the REST API
./homer ha_api ping

# List domains and services
./homer ha_api domain list
./homer ha_api domain services --domain-id light

# Describe a service
./homer ha_api domain describe --domain-id light --service-id turn_on

# Query an entity
./homer ha_api entity state --entity-id light.living_room

# Fire an event
./homer ha_api event fire --event-type custom_event --data '{"foo":"bar"}'
```

See `--help` on any command for details.

---

## 🔧 Helper Commands

To speed up inspection and common queries, the module includes a set of CLI helper commands:

| Command                  | Description                                  |
| ------------------------ | -------------------------------------------- |
| `ha_api ping`            | Ping your Home Assistant instance            |
| `ha_api lights`          | List all `light.*` entities and their states |
| `ha_api domains`         | List available service domains               |
| `ha_api components`      | Show all registered HA components            |
| `ha_api config`          | Print YAML config (name, timezone, version)  |
| `ha_api log`             | Print the HA error log                       |
| `ha_api state ENTITY_ID` | Show state + attributes of a single entity   |

These are especially useful for local testing and debugging.

---

## 🐳 Docker Usage

Run the `ha_api` module with Docker by injecting environment variables:

```bash
docker run --rm -it \
  -e HA_API_URL=http://192.168.69.11:8123/api \
  -e HA_API_TOKEN=your_token \
  mscrnt/homer:ha_api \
  ha_api ping
```

---

## 🧠 Philosophy

This module is part of the [HOMER Automation Framework](../README.md), designed to be:

* **Modular** – drop in/out with minimal config
* **Composable** – works standalone or in `homer-latest` stacks
* **Observable** – CLI logs all actions and errors

---

## 🙌 Acknowledgements

This module wraps the amazing [HomeAssistant-API](https://github.com/GrandMoff100/HomeAssistantAPI) library by [@WixiPi719](https://pypi.org/user/WixiPi719/).

> 📦 [PyPI](https://pypi.org/project/HomeAssistant-API/)
> 🔗 [GitHub](https://github.com/GrandMoff100/HomeAssistantAPI)
> 📖 [Documentation](https://homeassistant-api.readthedocs.io/)