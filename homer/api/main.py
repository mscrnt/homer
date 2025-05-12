# homer/api/main.py

from fastapi import FastAPI
from homer.api.routes.health import router as health_router
from homer.api.loader import discover_module_apis

app = FastAPI(title="HOMER Modular API")

# Core routes
app.include_router(health_router)

# Dynamically load and mount all HomerAPI subclasses
for module_api in discover_module_apis():
    app.include_router(module_api.router)
