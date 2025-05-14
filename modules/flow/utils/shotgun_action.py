

import urllib.parse
from typing import Dict, List, Optional, Tuple
from homer.utils.logger import get_module_logger

log = get_module_logger("flow-ami")

class ShotgunAction:
    def __init__(self, url: str):
        log.debug(f"Parsing AMI URL: {url}")
        self.url = url
        self.protocol, self.action, self.params = self._parse_url(url)

        self.entity_type: str = self.params.get("entity_type")

        self.project: Optional[Dict] = None
        if "project_id" in self.params:
            self.project = {
                "id": int(self.params["project_id"]),
                "name": self.params.get("project_name", "")
            }

        self.columns: List[str] = self.params.get("cols", [])
        self.column_display_names: List[str] = self.params.get("column_display_names", [])

        self.ids: List[int] = self._split_int_list(self.params.get("ids"))
        self.ids_filter = self._convert_ids_to_filter(self.ids)

        self.selected_ids: List[int] = self._split_int_list(self.params.get("selected_ids"))
        self.selected_ids_filter = self._convert_ids_to_filter(self.selected_ids)

        self.sort = None
        if "sort_column" in self.params:
            self.sort = {
                "column": self.params["sort_column"],
                "direction": self.params.get("sort_direction", "asc")
            }

        self.title: str = self.params.get("title", "")
        self.user: Dict = {
            "id": int(self.params.get("user_id", 0)),
            "login": self.params.get("user_login", "")
        }
        self.session_uuid: str = self.params.get("session_uuid", "")

    def _split_int_list(self, value: Optional[str]) -> List[int]:
        if value:
            return [int(v) for v in value.split(",") if v.isdigit()]
        return []

    def _convert_ids_to_filter(self, ids: List[int]) -> List[List]:
        filters = [["id", "is", i] for i in ids]
        log.debug(f"Parsed filters: {filters}")
        return filters

    def _parse_url(self, url: str) -> Tuple[str, str, Dict]:
        # Parse protocol and path
        protocol, path = url.split(":", 1)
        action, query_string = path.lstrip("/").split("?", 1)

        raw_params = urllib.parse.parse_qs(query_string)
        params = {}

        # Normalize multi-value fields
        for key, value in raw_params.items():
            if key in ("cols", "column_display_names"):
                params[key] = value
            else:
                params[key] = value[0] if len(value) == 1 else value

        return protocol, action, params
