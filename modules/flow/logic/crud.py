

from typing import List, Dict, Any, Optional
from modules.flow.client import get_sg_client
from homer.utils.logger import get_module_logger

log = get_module_logger("flow.crud.logic")


def create_entity(entity_type: str, data: Dict[str, Any]) -> dict:
    sg = get_sg_client()
    return sg.create(entity_type, data)


def find_entities(entity_type: str, filters: List,
                  fields: Optional[List[str]] = None,
                  order: Optional[List[Dict[str, str]]] = None,
                  limit: int = 0) -> List[dict]:
    sg = get_sg_client()
    return sg.find(entity_type, filters, fields or ["id", "type"], order=order, limit=limit)


def find_one_entity(entity_type: str, filters: List,
                    fields: Optional[List[str]] = None) -> Optional[dict]:
    sg = get_sg_client()
    return sg.find_one(entity_type, filters, fields or ["id", "type"])


def update_entity(entity_type: str, entity_id: int,
                  data: Dict[str, Any],
                  multi_entity_update_modes: Optional[Dict[str, str]] = None) -> dict:
    sg = get_sg_client()
    return sg.update(entity_type, entity_id, data, multi_entity_update_modes)


def delete_entity(entity_type: str, entity_id: int) -> bool:
    sg = get_sg_client()
    return sg.delete(entity_type, entity_id)


def revive_entity(entity_type: str, entity_id: int) -> bool:
    sg = get_sg_client()
    return sg.revive(entity_type, entity_id)


def batch_operations(requests: List[Dict[str, Any]]) -> List[Any]:
    sg = get_sg_client()
    return sg.batch(requests)


def summarize_entity(entity_type: str,
                     filters: List,
                     summary_fields: List[Dict[str, str]],
                     grouping: Optional[List[Dict[str, str]]] = None) -> dict:
    sg = get_sg_client()
    return sg.summarize(entity_type, filters, summary_fields, grouping=grouping)
