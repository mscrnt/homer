# 🧠 HOMER Netbox Module (Netbox API)

The `netbox` module integrates HOMER with [NetBox](https://netbox.readthedocs.io/en/stable/), enabling automation of network, asset, and infrastructure metadata using the NetBox API.

This module is named **Netbox** in reference to network management, IP address management (IPAM), and data center infrastructure management (DCIM) workflows.

---

## 🔧 Features

* ✅ NetBox server connection test (`ping`)
* 📦 Inventory management for devices, racks, interfaces
* 🌐 IP address and prefix allocation and tracking
* 🏷️ Tenancy support for multitenant infrastructure
* 🛠️ Full CRUD support for all entities
* ⚙️ Choice lookup for valid status, roles, and more
* 🧪 CLI and REST API powered by FastAPI under a unified module

---

## 📦 Dependencies

This module uses [`pynetbox`](https://github.com/netbox-community/pynetbox), the official NetBox Python API client.

```text
pynetbox>=7.3.0
````

✅ Python 3.10+ required

---

## 🐳 Docker Support

This module can be used standalone or included in a HOMER stack image:

* Base: Python 3.11-slim
* Includes NetBox CLI + FastAPI support
* Supports `.env`-driven config for NetBox token and base URL

---

## 🚀 Usage

### CLI

All commands are namespaced under the `netbox` CLI group:

```bash
docker run --rm -it \
  -e NETBOX_API_URL=https://netbox.example.com \
  -e NETBOX_TOKEN=abc123 \
  homer:netbox netbox --help
```

#### Core Commands

```bash
netbox ping                               # Server connection test
netbox dcim.devices list                  # List all devices
netbox dcim.racks create --file rack.json # Create rack from JSON
netbox ipam.prefixes delete --filter ...  # Delete prefixes by query
```

#### Examples

```bash
netbox ipam.prefixes create --file new_prefixes.json
netbox tenancy.tenants list
netbox dcim.interfaces update --file patch.json
```

---

## 📡 API

When the HOMER API is running, Netbox endpoints are exposed under `/netbox`.

```bash
docker run -p 8080:8080 homer:netbox serve-api
```

Browse live docs at:

```
http://localhost:8080/docs
```

### Example Endpoints

* `GET /netbox/ping`
* `GET /netbox/devices`
* `GET /netbox/prefixes/search?q=10.0`
* `POST /netbox/tenants`
* `PATCH /netbox/interfaces/{id}`
* `DELETE /netbox/racks?ids=1&ids=2&ids=3`

---

## 🧩 Module Tree

```
modules/netbox/
├── cli.py                           # CLI entrypoint
├── client.py                        # NetBox connection wrapper
├── cli_functions/
│   ├── dcim/
│   │   ├── devices.py
│   │   ├── interfaces.py
│   │   └── racks.py
│   ├── ipam/
│   │   ├── ip_addresses.py
│   │   └── prefixes.py
│   ├── tenancy/
│   │   └── tenants.py
│   └── utils.py
├── routes/
│   ├── dcim/
│   │   ├── devices.py
│   │   ├── interfaces.py
│   │   └── racks.py
│   ├── ipam/
│   │   ├── ip_addresses.py
│   │   └── prefixes.py
│   ├── tenancy/
│   │   └── tenants.py
│   └── utils.py
└── README.md
```

---

## 🔐 Environment Variables

| Variable         | Description                                   |
| ---------------- | --------------------------------------------- |
| `NETBOX_API_URL` | NetBox base URL (e.g. `https://netbox.local`) |
| `NETBOX_TOKEN`   | API token with access to objects              |

---

## 🧠 Roadmap

| Feature                        | Status     |
| ------------------------------ | ---------- |
| DCIM CRUD via API              | ✅ Complete |
| IPAM prefix + address support  | ✅ Complete |
| Tenancy endpoints              | ✅ Complete |
| Choice lookup per model        | ✅ Complete |
| API filtering, deletion, patch | ✅ Complete |
| Slack/webhook integration      | 🔜 Planned |

---

## 📚 References

* [NetBox Documentation](https://netbox.readthedocs.io/)
* [pynetbox GitHub](https://github.com/netbox-community/pynetbox)
* [FastAPI Docs](https://fastapi.tiangolo.com/)
* [HOMER Framework](../README.md)

