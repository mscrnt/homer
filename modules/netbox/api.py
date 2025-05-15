from fastapi import HTTPException
from homer.api.core import HomerAPI, register_api
from homer.utils.logger import get_module_logger

# Route modules (with routers exposed)
from modules.netbox.routes.dcim import devices, interfaces, racks
from modules.netbox.routes.ipam import ip_addresses, prefixes
from modules.netbox.routes.tenancy import tenants

log = get_module_logger("netbox-api")


@register_api
class NetboxAPI(HomerAPI):
    def __init__(self):
        super().__init__(prefix="/netbox")

    def register_routes(self):
        @self.router.get("/ping")
        async def ping():
            """Quick NetBox health check."""
            try:
                from modules.netbox.client import get_netbox_client
                nb = get_netbox_client()
                return {"status": "ok", "version": nb.version}
            except HTTPException as e:
                return {"status": "error", "message": e.detail}
            except Exception as e:
                log.exception("❌ NetBox ping failed")
                return {"status": "error", "message": str(e)}

        # Grouped route registration
        self.router.include_router(devices.router, prefix="/devices", tags=["dcim"])
        self.router.include_router(interfaces.router, prefix="/interfaces", tags=["dcim"])
        self.router.include_router(racks.router, prefix="/racks", tags=["dcim"])
        self.router.include_router(ip_addresses.router, prefix="/ip-addresses", tags=["ipam"])
        self.router.include_router(prefixes.router, prefix="/prefixes", tags=["ipam"])
        self.router.include_router(tenants.router, prefix="/tenants", tags=["tenancy"])
