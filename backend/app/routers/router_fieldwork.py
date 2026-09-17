from fastapi import APIRouter
from ..repositories import repo_fieldwork
from ..schemas.schemas import Fieldwork, FieldworkAdd, FieldworkUpdate

fieldwork = APIRouter(prefix="/farms/{farm_id}/fields/{field_id}/fieldworks")

@fieldwork.get("/", response_model=list[Fieldwork])
def get_all_fieldworks(farm_id: int, field_id: int):
    return repo_fieldwork.get_all_fieldworks(farm_id, field_id)

@fieldwork.get("/{fieldwork_id}", response_model=list[Fieldwork])
def get_fieldwork(farm_id: int, field_id: int, type_of_work: str):
    return repo_fieldwork.get_fieldwork(farm_id, field_id, type_of_work)

@fieldwork.post("/", response_model=Fieldwork)
def add_fieldwork(farm_id: int, field_id: int, fieldwork: FieldworkAdd):
    return repo_fieldwork.add_fieldwork(farm_id, field_id, fieldwork)

@fieldwork.patch("/{fieldwork_id}", response_model=FieldworkUpdate)
def update_fieldwork(farm_id: int, field_id: int, fieldwork_id, fieldwork: FieldworkUpdate):
    return repo_fieldwork.update_fieldwork(farm_id, field_id, fieldwork_id, fieldwork)

@fieldwork.delete("/{id}")
def delete_fieldwork(farm_id: int, field_id: int, id: int):
    return repo_fieldwork.delete_fieldwork(farm_id, field_id, id)




