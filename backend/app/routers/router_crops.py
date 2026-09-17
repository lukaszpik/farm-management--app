from fastapi import APIRouter
from ..repositories import repo_crops
from ..schemas import Crops, CropsUpdate, CropsAdd

crops = APIRouter(prefix="/farms/{farm_id}/fields/{field_id}/crops")

@crops.get("/", response_model=list[Crops])
def get_all_crops(farm_id: int, field_id: int):
    return repo_crops.get_all_crops(farm_id, field_id)

@crops.get("/{name}", response_model=list[Crops])
def get_crop(farm_id: int, field_id: int, name: str):
    return repo_crops.get_crop(farm_id, field_id, name)

@crops.post("/", response_model=CropsAdd)
def add_crop(farm_id: int, field_id: int, crop: CropsAdd):
    return repo_crops.add_crop(farm_id, field_id, crop)

@crops.patch("/{id}", response_model=CropsUpdate)
def update_crop(farm_id: int, field_id: int, id:int, crop: CropsUpdate):
    return repo_crops.update_crop(farm_id, field_id, id, crop)

@crops.delete("/{id}")
def delete_field(farm_id: int, field_id: int, id: int):
    return repo_crops.delete_crop(farm_id, field_id, id)