from fastapi import APIRouter, HTTPException, Query
from homer.utils.logger import get_module_logger
from modules.flow.logic import connection as conn_logic

log = get_module_logger("flow-connection")
router = APIRouter()


@router.get("/info")
def get_server_info():
    try:
        return conn_logic.get_server_info()
    except Exception as e:
        log.exception("❌ Failed to fetch server info")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session")
def get_session_token():
    try:
        return {"session_token": conn_logic.get_session_token()}
    except Exception as e:
        log.exception("❌ Failed to get session token")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/authenticate")
def authenticate_human_user(
    user_login: str = Query(...),
    user_password: str = Query(...),
    auth_token: str = Query(None)
):
    try:
        return conn_logic.authenticate_user(user_login, user_password, auth_token)
    except Exception as e:
        log.exception("❌ Human user authentication failed")
        raise HTTPException(status_code=500, detail=str(e))
