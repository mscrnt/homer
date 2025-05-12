#!/usr/bin/env python3

import sys
import subprocess
import threading
import time
import os
import signal
from homer.utils.logger import get_logger

log = get_logger("entrypoint")

def safe_run(description, command):
    log.info(f"📦 Launching: {description} → {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        log.error(f"❌ {description} failed with exit code {e.returncode}")
    except Exception as e:
        log.warning(f"⚠️ Failed to launch {description}: {type(e).__name__} — {e}")

def run_uvicorn():
    safe_run("FastAPI server", [
        "uvicorn", "homer.api.main:app",
        "--host", "0.0.0.0",
        "--port", "4242"
    ])

def run_worker():
    safe_run("Background worker", ["python", "-m", "homer.worker"])

def run_daemon():
    safe_run("MQTT daemon", ["python", "-m", "homer.mqtt_service"])

def run_all_services():
    log.info("🧭 No CLI args provided — starting all available services.")
    threads = []

    for fn in [run_uvicorn, run_worker, run_daemon]:
        thread = threading.Thread(target=fn, daemon=True)
        thread.start()
        threads.append(thread)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log.warning("🛑 Received shutdown signal. Cleaning up...")
        os.killpg(os.getpgid(os.getpid()), signal.SIGTERM)

def run_homer_cli(args):
    log.info(f"🚀 Running HOMER CLI command: homer {' '.join(args)}")
    result = subprocess.run(["homer"] + args)
    sys.exit(result.returncode)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_homer_cli(sys.argv[1:])
    else:
        run_all_services()
