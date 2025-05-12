from ..client import call_api
from typing import Optional

def do_search(
    search: str,
    restypes: str = "",
    order_by: str = "relevance",
    archive: str = "0",
    fetchrows: str = "-1",
    sort: str = "desc",
    offset: int = 0
) -> dict:
    """Perform a basic search for resources."""
    return call_api("do_search", {
        "param1": search,
        "param2": restypes,
        "param3": order_by,
        "param4": archive,
        "param5": fetchrows,
        "param6": sort,
        "param7": str(offset)
    })


def search_get_previews(
    search: str,
    restypes: str = "",
    order_by: str = "relevance",
    archive: int = 0,
    fetchrows: str = "-1",
    sort: str = "desc",
    recent_search_daylimit: str = "",
    getsizes: str = "",
    previewext: str = "jpg"
) -> dict:
    """Perform a search and return results with preview URLs."""
    return call_api("search_get_previews", {
        "param1": search,
        "param2": restypes,
        "param3": order_by,
        "param4": str(archive),
        "param5": fetchrows,
        "param6": sort,
        "param7": recent_search_daylimit,
        "param8": getsizes,
        "param9": previewext
    })
