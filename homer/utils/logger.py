# base/utils/logger.py


import os
import logging
import inspect
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler

DEFAULT_UNIFIED_LOGFILE = "logs/homer.log"
DEFAULT_LOG_LEVEL = os.environ.get("HOMER_LOG_LEVEL", "DEBUG")

def get_logger(name="HOMER", logfile=None, level=None, max_bytes=5 * 1024 * 1024, backup_count=5):
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # Already configured

    level = level or DEFAULT_LOG_LEVEL
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)

    logger.setLevel(level)

    # 🎛 Rich Console Handler
    console_handler = RichHandler(
        rich_tracebacks=True,
        markup=True,
        show_time=True,
        show_level=True,
        show_path=False,
    )
    logger.addHandler(console_handler)

    # 🛡 Try to set up file logging
    log_dir = os.getenv("HOMER_LOG_DIR", "logs")
    try:
        os.makedirs(log_dir, exist_ok=True)
    except PermissionError:
        fallback_log_dir = "/tmp/homer-logs"
        try:
            os.makedirs(fallback_log_dir, exist_ok=True)
            log_dir = fallback_log_dir
        except Exception:
            logger.warning(f"⚠️ File logging disabled: unable to create {log_dir} or fallback.")
            return logger  # Console-only fallback

    # 📁 Per-module log file
    logfile = logfile or os.path.join(log_dir, f"{name.lower()}.log")
    file_handler = RotatingFileHandler(logfile, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
    file_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # 📁 Unified HOMER log
    if name != "HOMER":
        unified_path = os.path.join(log_dir, "homer.log")
        unified_handler = RotatingFileHandler(unified_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
        unified_handler.setFormatter(file_formatter)
        logger.addHandler(unified_handler)

    return logger

def get_module_logger(logfile=None, level=None):
    """
    Shortcut for getting a logger based on the caller's module name.
    """
    frame = inspect.stack()[1]
    module_name = frame.frame.f_globals.get("__name__", "unknown")
    return get_logger(name=module_name, logfile=logfile, level=level)


def log_with_caller(level: str, message: str):
    stack = inspect.stack()

    callee = stack[1]
    callee_func = callee.function
    callee_module = callee.frame.f_globals.get("__name__", "unknown")

    # Find first non-wrapper caller
    caller_func = "unknown"
    caller_module = "unknown"
    for frame in stack[2:]:
        if frame.function not in {"wrapper", "inner", "<lambda>"}:
            caller_func = frame.function
            caller_module = frame.frame.f_globals.get("__name__", "unknown")
            break

    logger = get_logger(callee_module)
    full_message = (
        f"{message} ← {callee_module}.{callee_func} "
        f"→ called by {caller_module}.{caller_func}"
    )
    getattr(logger, level.lower())(full_message)


def set_global_log_level(level: str):
    """Dynamically change logging level across all loggers."""
    resolved_level = getattr(logging, level.upper(), logging.INFO)
    logging.getLogger().setLevel(resolved_level)
    for name in logging.root.manager.loggerDict:
        logging.getLogger(name).setLevel(resolved_level)
    log_with_caller("info", f"🔧 Global log level set to {level.upper()}")
