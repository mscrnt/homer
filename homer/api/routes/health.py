# homer/api/routes/health.py

import os
from fastapi import APIRouter
from utils.logger import get_module_logger
from homer.api.loader import discover_module_apis

log = get_module_logger()
router = APIRouter()

REQUIRED_ENV_VARS = [
    "GH_TOKEN",
    "REPO_URL",
    "CONFLUENCE_API_TOKEN",
    "CONFLUENCE_SPACE_KEY",
    "JIRA_API_TOKEN",
    "JIRA_PROJECT_KEY",
    "SLACK_WEBHOOK_URL",  # Optional, still checked
]

@router.get("/health", tags=["System"])
def health_check():
    log.debug("🫀 Health check requested")

    loaded_apis = discover_module_apis()
    env_status = {
        var: "present" if os.getenv(var) else "missing"
        for var in REQUIRED_ENV_VARS
    }

    health_info = {
        "status": "ok",
        "message": "HOMER API is alive",
        "modules_loaded": len(loaded_apis),
        "env_vars": env_status,
    }

    log.info(f"✅ Health check status: {health_info}")
    return health_info
