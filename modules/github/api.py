# modules/github/api.py

from fastapi import Request, Header
from homer.api.core import HomerAPI, register_api
from homer.utils.logger import get_module_logger
from .github_client import (
    dispatch_event,
    is_duplicate_delivery_id,
    store_delivery_id,
)
from typing import Optional

log = get_module_logger("github-api")

@register_api
class GithubAPI(HomerAPI):
    def __init__(self):
        super().__init__(prefix="/webhook")

    def register_routes(self):
        @self.router.post("/github")
        async def github_webhook(
            payload: dict,
            request: Request,
            x_github_event: Optional[str] = Header(None),
            x_github_delivery: Optional[str] = Header(None),
        ):
            # 🛡️ Replay protection
            if x_github_delivery and is_duplicate_delivery_id(x_github_delivery):
                log.warning(f"🚨 Duplicate delivery ID: {x_github_delivery}")
                return {"status": "duplicate", "delivery_id": x_github_delivery}

            store_delivery_id(x_github_delivery)
            log.info(f"📦 Webhook received: event={x_github_event}, delivery={x_github_delivery}")

            # 🧠 Dispatch to event hooks (if registered)
            if x_github_event in {"push", "pull_request", "issues"}:
                dispatch_event(x_github_event, payload)
            else:
                log.info(f"⚠️ Unsupported GitHub event: {x_github_event}")

            return {
                "status": "accepted",
                "event": x_github_event,
                "delivery_id": x_github_delivery,
            }
