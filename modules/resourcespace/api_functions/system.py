from ..client import call_api

def get_system_status() -> dict:
    """Get overall system health status (e.g. plugin load, cron, quota, version)."""
    return call_api("get_system_status")


def get_daily_stat_summary(days: int = 30) -> dict:
    """
    Return a summary of daily usage statistics for the past N days.
    
    Max value is 365 (as data only covers current + previous year).
    """
    return call_api("get_daily_stat_summary", {
        "param1": str(days)
    })
