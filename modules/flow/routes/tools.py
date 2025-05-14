#!/usr/bin/env python3



from fastapi import APIRouter, Query, HTTPException
from typing import List
from homer.utils.logger import get_module_logger
from modules.flow.logic import tools as tools_logic

log = get_module_logger("flow.tools.api")
router = APIRouter()


@router.get("/projects", summary="List accessible ShotGrid projects")
def list_projects(fields: List[str] = Query(default=["id", "name"])):
    """
    Return a list of ShotGrid projects visible to the current API user.
    """
    try:
        return tools_logic.list_projects(fields)
    except Exception as e:
        log.exception("❌ Failed to fetch ShotGrid projects")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/project-id", summary="Get ShotGrid project ID from name")
def get_project_id(name: str, fields: List[str] = Query(default=["id", "name"])):
    """
    Return the ID of a ShotGrid project based on its name.
    """
    try:
        result = tools_logic.find_project_by_name(name, fields)
        if result:
            return {"id": result["id"], "name": result["name"]}
        raise HTTPException(status_code=404, detail="Project not found")
    except Exception as e:
        log.exception("❌ Failed to find project by name")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/project-name", summary="Get ShotGrid project name from ID")
def get_project_name(id: int, fields: List[str] = Query(default=["id", "name"])):
    """
    Return the name of a ShotGrid project based on its ID.
    """
    try:
        result = tools_logic.find_project_by_id(id, fields)
        if result:
            return {"id": result["id"], "name": result["name"]}
        raise HTTPException(status_code=404, detail="Project not found")
    except Exception as e:
        log.exception("❌ Failed to find project by ID")
        raise HTTPException(status_code=500, detail=str(e))
