from fastapi import APIRouter
from ..repositories import repo_animal
from ..schemas.schemas import Animal, AnimalCreate, AnimalUpdate

animal = APIRouter(prefix="/farms/{farm_id}/animals")


@animal.get("/", response_model=list[Animal])
def get_all_animals(farm_id: int):
    return repo_animal.get_all_animals(farm_id)


@animal.get("/{animal_id}", response_model=Animal)
def get_animal(farm_id: int, animal_id: int):
    return repo_animal.get_animal(farm_id, animal_id)


@animal.post("/", response_model=Animal)
def add_animal(farm_id: int, animal: AnimalCreate):
    return repo_animal.add_animal(farm_id, animal)


@animal.patch("/{animal_id}")
def update_animal(farm_id: int, animal_id: int, animal: AnimalUpdate):
    return repo_animal.update_animal(farm_id, animal_id, animal)


@animal.delete("/{animal_id}")
def delete_animal(farm_id: int, animal_id: int):
    return repo_animal.delete_animal(farm_id, animal_id)