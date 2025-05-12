#!/usr/bin/env python3

# github.github_client



import os
import time
import requests
from collections import deque
from github import Github, GithubException
from homer.utils.logger import get_module_logger

logger = get_module_logger("github-client")

# ──────────────────────────────────────────────────────────────────────────────
# 🔐 GitHub Auth
# ──────────────────────────────────────────────────────────────────────────────

def get_github_client() -> Github:
    token = os.environ.get("GH_TOKEN")
    if not token:
        raise RuntimeError("❌ GH_TOKEN is not set in environment.")
    return Github(token)

# ──────────────────────────────────────────────────────────────────────────────
# 📁 Repo Info
# ──────────────────────────────────────────────────────────────────────────────

def get_repo_info(repo_full_name: str):
    client = get_github_client()
    try:
        return client.get_repo(repo_full_name)
    except GithubException as e:
        logger.error(f"❌ Failed to fetch repo info: {e}")
        raise

# ──────────────────────────────────────────────────────────────────────────────
# 🌿 Branches
# ──────────────────────────────────────────────────────────────────────────────

def list_branches(repo_full_name: str):
    repo = get_repo_info(repo_full_name)
    try:
        return repo.get_branches()
    except GithubException as e:
        logger.error(f"❌ Failed to list branches: {e}")
        return []

# ──────────────────────────────────────────────────────────────────────────────
# 🔃 Pull Requests
# ──────────────────────────────────────────────────────────────────────────────

def list_pull_requests(repo_full_name: str, state: str = "open"):
    repo = get_repo_info(repo_full_name)
    try:
        return repo.get_pulls(state=state)
    except GithubException as e:
        logger.error(f"❌ Failed to list PRs: {e}")
        return []

# ──────────────────────────────────────────────────────────────────────────────
# 🐛 Issues
# ──────────────────────────────────────────────────────────────────────────────

def create_issue(repo_full_name: str, title: str, body: str = ""):
    repo = get_repo_info(repo_full_name)
    try:
        return repo.create_issue(title=title, body=body)
    except GithubException as e:
        logger.error(f"❌ Failed to create issue: {e}")
        raise

# ──────────────────────────────────────────────────────────────────────────────
# 📄 Markdown Files (with ETag support)
# ──────────────────────────────────────────────────────────────────────────────

def get_repo_markdown_files(repo_full_name: str, branch: str = "main", etag: str = None):
    """
    Return a list of markdown files from the specified GitHub repo and branch.
    Uses conditional GET with ETag when available.
    """
    token = os.getenv("GH_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "Github-Agent"
    }
    if etag:
        headers["If-None-Match"] = etag

    url = f"https://api.github.com/repos/{repo_full_name}/contents/?ref={branch}"
    logger.info(f"🌐 Fetching contents from GitHub: {url}")

    try:
        resp = requests.get(url, headers=headers)
    except Exception as e:
        logger.error(f"❌ HTTP error while fetching repo contents: {e}")
        return []

    if resp.status_code == 304:
        logger.info("⏩ No changes detected (ETag matched).")
        return []

    if not resp.ok:
        logger.error(f"❌ GitHub API error: {resp.status_code} - {resp.text}")
        return []

    new_etag = resp.headers.get("ETag")
    data = resp.json()

    md_files = [item for item in data if item["name"].lower().endswith(".md")]

    logger.info(f"📄 Found {len(md_files)} Markdown files. New ETag: {new_etag}")
    return md_files

# ──────────────────────────────────────────────────────────────────────────────
# 🔁 Delivery ID Cache (Replay Protection)
# ──────────────────────────────────────────────────────────────────────────────

_delivery_cache = set()
_delivery_queue = deque()
_MAX_CACHE_SIZE = 500
_CACHE_EXPIRY_SECONDS = 3600  # 1 hour

def store_delivery_id(delivery_id: str):
    now = time.time()
    if delivery_id not in _delivery_cache:
        _delivery_cache.add(delivery_id)
        _delivery_queue.append((delivery_id, now))
        if len(_delivery_queue) > _MAX_CACHE_SIZE:
            _trim_delivery_cache()
        logger.debug(f"🧾 Stored delivery ID: {delivery_id}")

def is_duplicate_delivery_id(delivery_id: str) -> bool:
    return delivery_id in _delivery_cache

def _trim_delivery_cache():
    now = time.time()
    while _delivery_queue and (now - _delivery_queue[0][1]) > _CACHE_EXPIRY_SECONDS:
        old_id, _ = _delivery_queue.popleft()
        _delivery_cache.discard(old_id)
        logger.debug(f"🧹 Expired delivery ID: {old_id}")

# ──────────────────────────────────────────────────────────────────────────────
# 🔌 Hookable Event Dispatch System
# ──────────────────────────────────────────────────────────────────────────────

# Internal callback registry
_event_hooks = {
    "push": [],
    "pull_request": [],
    "issues": []
}

def register_hook(event_type: str, callback):
    """
    Register a callback for a GitHub event.
    Example event types: "push", "pull_request", "issues"
    """
    if event_type not in _event_hooks:
        raise ValueError(f"❌ Unsupported event type: {event_type}")
    _event_hooks[event_type].append(callback)
    logger.debug(f"✅ Registered hook for {event_type}: {callback.__name__}")

def dispatch_event(event_type: str, payload: dict):
    """
    Dispatch a GitHub webhook event to registered handlers.
    """
    hooks = _event_hooks.get(event_type, [])
    if not hooks:
        logger.info(f"📭 No handlers registered for: {event_type}")
        return

    logger.info(f"📨 Dispatching '{event_type}' to {len(hooks)} hook(s)")
    for hook in hooks:
        try:
            hook(payload)
        except Exception as e:
            logger.exception(f"❌ Error in {hook.__name__}: {e}")
