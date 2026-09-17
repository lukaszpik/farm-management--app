from fastapi import FastAPI
from .routers import router_farm, router_animals, router_fields, router_fieldwork


app = FastAPI()
app.include_router(router_farm.farm)
app.include_router(router_animals.animal)
app.include_router(router_fields.field)
app.include_router(router_fieldwork.fieldwork)





