from fastapi import APIRouter
from ..repositories import repo_fields
from ..schemas.schemas import Field, FieldCreate, FieldUpdate

field = APIRouter(prefix="/farms/{farm_id}/fields")

@field.get("/", response_model=list[Field])
def get_all_fields(farm_id: int):
    return repo_fields.get_all_fields(farm_id)

@field.get("/{field_id}", response_model=Field)
def get_field(farm_id: int, field_id: int):
    return repo_fields.get_field(farm_id, field_id)

@field.post("/", response_model=Field)
def add_field(farm_id: int, field: FieldCreate):
    return repo_fields.add_field(farm_id, field)

@field.patch("/{type_of_work}", response_model=Field)
def update_field(farm_id: int, field_id: int, field: FieldUpdate):
    return repo_fields.update_field(farm_id, field_id, field)

@field.delete("/{field_id}")
def delete_field(farm_id: int, field_id: int):
    return repo_fields.delete_field(farm_id, field_id)