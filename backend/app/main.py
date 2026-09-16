from fastapi import FastAPI
from .routers import router_animals


app = FastAPI()
app.include_router(router_animals.animal)

