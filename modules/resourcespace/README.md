# 📁 HOMER ResourceSpace Module

This module provides CLI and API support for interacting with a [ResourceSpace](https://www.resourcespace.com/) server, allowing you to automate tasks related to digital asset management including resources, metadata, collections, and more.

> 🔐 This module is used internally by Blizzard’s Archive Team to orchestrate asset workflows across ResourceSpace and integrate with external systems like GitHub, Confluence, and Jira.

---

## 🚀 Features

- Full CLI access to ResourceSpace via the HOMER CLI
- Upload resources from local files or URLs
- Manage metadata fields and options
- Search resources and preview images
- Manage user collections and featured collections
- System diagnostics (status, usage stats)
- Modular and composable for CI/CD or daemonized use

---

## 🧪 Example Usage

```bash
docker run --rm -it \
  -e RS_API_URL=https://10.130.48.193 \
  -e RS_API_USER=admin \
  -e RS_API_KEY=<your-secret-key> \
  homer-resourcespace:latest \
  resourcespace system get-system-status
```

---

## 📦 CLI Commands

### Resource Commands

* `get-resource-info` — Get top-level data for a resource
* `create-resource` — Create a new resource
* `upload-resource-file` — Upload a local file
* `upload-resource-by-url` — Upload from URL
* `upload-resource-preview` — Upload a preview image
* `delete-resource` — Delete a resource
* `get-resource-metadata` — Get full field data
* `get-related-resources`, `get-resource-log`, etc.

### Collection Commands

* `get-user-collections`
* `create-collection`, `delete-collection`
* `add-resource-to-collection`, `remove-resource-from-collection`
* `search-public-collections`, `get-featured`

### Metadata Commands

* `get-field-options`, `get-field-nodes`, `get-node-id`
* `add-resource-nodes`, `add-resource-nodes-multi`
* `update-field`, `set-node`, `create-field`

### User Commands

* `get-users`, `login`, `check-permission`
* `mark-email-invalid`, `get-users-by-permission`

### System Commands

* `get-system-status` — Confirm server health and quotas
* `get-daily-stats` — Show usage summaries (e.g. uploads, views)

### Search Commands

* `search-resources` — Perform standard search
* `search-resources-with-previews` — Include thumbnails/scr/pre URLs

---

## 🔧 Environment Variables

| Variable      | Description                        |
| ------------- | ---------------------------------- |
| `RS_URL`      | Base URL of your ResourceSpace     |
| `RS_API_USER` | ResourceSpace username             |
| `RS_API_KEY`  | Private API key for the user       |

---

## 🧩 Modular Design

This module registers itself using `@register_cli("resourcespace")` and extends the HOMER CLI core. It can be stacked with other modules (e.g., github, atlassian) for compound workflows.

---

## 📂 Location

```text
modules/
└── resourcespace/
    ├── cli.py                # CLI entrypoint
    ├── client.py             # API signing + multipart support
    └── api_functions/
        ├── resource.py
        ├── collection.py
        ├── metadata.py
        ├── system.py
        ├── user.py
        ├── message.py
        └── search.py
```

---

## ✅ Verifying Connection

You can validate your setup using:

```bash
resourcespace system get-system-status
```

This ensures your credentials and URL are working properly.

---

## 📜 License

This module is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the LICENSE file for details.
```

