from fastapi import APIRouter
from ..repositories import repo_farm
from ..schemas.schemas import Farm, FarmCreate, FarmUpdate

farm = APIRouter(prefix="/farm", tags=["Farm"])

@farm.post("/", response_model=FarmCreate)
def create_farm(farm: FarmCreate):
    return repo_farm.create_farm(farm)

@farm.get("/{farm_id}", response_model=Farm)
def get_farm(farm_id: int):
    return repo_farm.get_farm(farm_id)

@farm.get("/", response_model=list[Farm])
def get_all_farms():
    return repo_farm.get_all_farms()  

@farm.patch("/{farm_id}", response_model=dict)
def update_farm(farm_id: int, farm: FarmUpdate):
    return repo_farm.update_farm(farm_id, farm)

@farm.delete("/{farm_id}", response_model=dict)
def delete_farm(farm_id: int):
    return repo_farm.delete_farm(farm_id)
