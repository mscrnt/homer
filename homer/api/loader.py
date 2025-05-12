# homer/api/loader.py

import importlib
import os
from homer.api.core import get_registered_apis
from homer.utils.logger import get_module_logger

log = get_module_logger()

def discover_module_apis():
    modules_path = "/homer/modules"
    log.info(f"🔍 Scanning modules in: {modules_path}")

    if not os.path.exists(modules_path):
        log.warning(f"⚠️ Module path not found: {modules_path}")
        return []

    for mod in os.listdir(modules_path):
        mod_api_path = f"modules.{mod}.api"
        try:
            log.debug(f"📦 Attempting to import: {mod_api_path}")
            importlib.import_module(mod_api_path)
        except ModuleNotFoundError:
            log.debug(f"⛔ No API found in module: {mod}")
        except Exception as e:
            log.warning(f"❌ Failed to load module API: {mod_api_path} — {type(e).__name__}: {e}")

    apis = get_registered_apis()
    log.info(f"🧩 Discovered {len(apis)} API module(s).")
    return apis
