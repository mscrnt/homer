

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from homer.utils.logger import get_module_logger, log_with_caller

log = get_module_logger()

# ──────────────────────────────────────────────────────────────────────────────
# 🔐 Base config defaults
# ──────────────────────────────────────────────────────────────────────────────

DEFAULTS = {
    "HOMER_ENV": "development",
    "LOG_LEVEL": "INFO",
    "CONFIG_PATH": "config/config.yaml",
}

# ──────────────────────────────────────────────────────────────────────────────
# 📦 Load base .env config
# ──────────────────────────────────────────────────────────────────────────────

ENV_PATH = Path(os.getenv("DOTENV_PATH", "/homer/.env"))
load_dotenv(dotenv_path=ENV_PATH)
log.debug(f"📄 Loaded base .env from: {ENV_PATH}")

# ──────────────────────────────────────────────────────────────────────────────
# 📦 Module env registry
# ──────────────────────────────────────────────────────────────────────────────

_module_registry: dict[str, dict] = {}

def register_module_env(name: str, *, env_path: str, schema_cls: type[BaseModel] | None = None):
    _module_registry[name] = {
        "env_path": env_path,
        "schema": schema_cls,
    }
    return lambda obj: obj

def load_registered_module_envs():
    for name, entry in _module_registry.items():
        path = Path(entry["env_path"])
        if not path.exists():
            log.warning(f"⚠️ Missing .env for module '{name}' at {path}")
            continue
        load_dotenv(dotenv_path=path, override=True)
        log.info(f"📥 Loaded .env for module: {name} ({path})")

def validate_registered_module_configs():
    for name, entry in _module_registry.items():
        schema = entry.get("schema")
        if not schema:
            continue
        try:
            schema(**os.environ)
            log.info(f"✅ Validated config for module: {name}")
        except ValidationError as e:
            log.error(f"❌ Validation failed for '{name}':\n{e}")
            raise SystemExit(1)

# ──────────────────────────────────────────────────────────────────────────────
# 📄 Load optional YAML config
# ──────────────────────────────────────────────────────────────────────────────

def _load_yaml_config(path):
    if not os.path.exists(path):
        log_with_caller("warning", f"YAML config not found at {path}. Skipping.")
        return {}
    try:
        with open(path, "r") as f:
            log.debug(f"📑 Loading YAML config from {path}")
            return yaml.safe_load(f) or {}
    except Exception as e:
        log_with_caller("warning", f"⚠️ Failed to load YAML: {e}")
        return {}

# ──────────────────────────────────────────────────────────────────────────────
# 🧠 Smart-cast .env values
# ──────────────────────────────────────────────────────────────────────────────

def _smart_cast(value):
    if isinstance(value, str):
        if value.lower() in ("true", "yes"):
            return True
        if value.lower() in ("false", "no"):
            return False
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            return value
    return value

# ──────────────────────────────────────────────────────────────────────────────
# 🔧 Load and merge env + yaml + defaults
# ──────────────────────────────────────────────────────────────────────────────

def load_raw_config():
    # ✅ Ensure module envs are loaded before resolving config
    load_registered_module_envs()

    config_path = os.getenv("CONFIG_PATH", DEFAULTS["CONFIG_PATH"])
    yaml_config = _load_yaml_config(config_path)

    merged = dict(DEFAULTS)
    merged.update({k: v for k, v in yaml_config.items() if v is not None})
    for key in os.environ:
        merged[key] = os.environ[key]

    merged = {k: _smart_cast(v) for k, v in merged.items()}

    redacted = {
        k: "[REDACTED]" if any(secret in k for secret in ("TOKEN", "KEY", "PASSWORD")) else v
        for k, v in merged.items()
    }
    log.debug(f"🔧 Final merged config: {redacted}")
    return merged

# ──────────────────────────────────────────────────────────────────────────────
# 📐 Structured core config with validation
# ──────────────────────────────────────────────────────────────────────────────

class HomerConfig(BaseModel):
    HOMER_ENV: str = DEFAULTS["HOMER_ENV"]
    LOG_LEVEL: str = DEFAULTS["LOG_LEVEL"]
    CONFIG_PATH: str = DEFAULTS["CONFIG_PATH"]

# ──────────────────────────────────────────────────────────────────────────────
# 🧪 Runtime config access
# ──────────────────────────────────────────────────────────────────────────────

def load_config() -> HomerConfig:
    # ✅ Always validate module envs before building structured config
    validate_registered_module_configs()

    raw = load_raw_config()
    try:
        return HomerConfig(**raw)
    except ValidationError as e:
        log_with_caller("error", "❌ Config validation failed")
        log.error(e)
        raise SystemExit(1)

# ──────────────────────────────────────────────────────────────────────────────
# 🧾 .env example generator
# ──────────────────────────────────────────────────────────────────────────────

def write_env_example(schema: type[BaseModel], path: Path, include_base: bool = True):
    """Generate a .env.example file from a Pydantic schema, optionally including base config."""
    from collections import OrderedDict

    fields = OrderedDict()

    if include_base:
        for field, info in HomerConfig.model_fields.items():
            fields[field] = info

    for field, info in schema.model_fields.items():
        fields[field] = info

    lines = []
    for field, info in fields.items():
        comment = "# required" if info.is_required() else "# optional"
        default = info.default if info.default is not None else ""
        lines.append(f"{field}={default} {comment}")

    path.write_text("\n".join(lines) + "\n")
    log.info(f"📝 Wrote .env.example to {path}")
 