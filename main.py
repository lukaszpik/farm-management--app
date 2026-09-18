from fastapi import FastAPI
from app.routers import router_animals, router_crops, router_farm, router_fields, router_fieldwork, router_finances
from app.routers import router_machines
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI(
    title="Farm Management API",
    description="API for managing farms, animals, fields, crops, machines and finances.",
    version="v1.0.0",
    docs_url=None
)


BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(
        directory=BASE_DIR / "app" / "static"
    ),
    name="static"
)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Farm Management API",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="/static/ui.css"
    )

app.include_router(router_farm.farm)
app.include_router(router_animals.animal)
app.include_router(router_fields.field)
app.include_router(router_fieldwork.fieldwork)
app.include_router(router_crops.crops)
app.include_router(router_machines.machines)
app.include_router(router_finances.finances)




