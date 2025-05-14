from typing import Any, Literal, Optional, Union
from pydantic import Field
from homeassistant_api import (
    ErrorResponse as HAErrorResponse,
    PingResponse as HAPingResponse,
    EventResponse as HAEventResponse,
    ResultResponse as HAResultResponse,
)
from homeassistant_api.models.websocket import (
    FiredEvent,
    FiredTrigger,
    TemplateEvent,
)

from homer.utils.logger import get_module_logger

log = get_module_logger("ha_api.response")

# ──────────────────────────────────────────────────────────────────────────────
# ❌ ErrorResponse
# ──────────────────────────────────────────────────────────────────────────────

class ErrorResponse(HAErrorResponse):
    """
    ❌ WebSocket error response from Home Assistant.
    Indicates failure of a command.
    """
    type: Literal["result"]
    success: Literal[False]
    id: int
    error: dict[str, Any]

    def describe(self) -> str:
        return f"❌ Error [{self.error.get('code')}]: {self.error.get('message')}"


# ──────────────────────────────────────────────────────────────────────────────
# 🟡 PingResponse
# ──────────────────────────────────────────────────────────────────────────────

class PingResponse(HAPingResponse):
    """
    🟡 WebSocket ping/pong response for latency checks.
    """
    type: Literal["pong"]
    id: int
    start: int
    end: Optional[int] = None

    def get_latency_ms(self) -> Optional[float]:
        if self.end is not None:
            return self.end - self.start
        return None


# ──────────────────────────────────────────────────────────────────────────────
# 📡 EventResponse
# ──────────────────────────────────────────────────────────────────────────────

class EventResponse(HAEventResponse):
    """
    📡 Fired event response from Home Assistant WebSocket.
    Can be a normal event, a trigger, or a rendered template.
    """
    type: Literal["event"]
    id: int
    event: Union[FiredEvent, FiredTrigger, TemplateEvent]

    def summary(self) -> str:
        if isinstance(self.event, FiredEvent):
            return f"📨 Event '{self.event.event_type}' from {self.event.origin} at {self.event.time_fired}"
        elif isinstance(self.event, FiredTrigger):
            return f"⚡ Trigger event with vars: {self.event.variables}"
        elif isinstance(self.event, TemplateEvent):
            return f"🧪 Template rendered: {self.event.result}"
        return "🌀 Unknown event response."


# ──────────────────────────────────────────────────────────────────────────────
# ✅ ResultResponse
# ──────────────────────────────────────────────────────────────────────────────

class ResultResponse(HAResultResponse):
    """
    ✅ Generic WebSocket result response from Home Assistant.
    """
    type: Literal["result"]
    success: Literal[True]
    id: int
    result: Optional[Any]

    def describe(self) -> str:
        return f"✅ Result [{self.id}]: {self.result if self.result is not None else 'No payload'}"
