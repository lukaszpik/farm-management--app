from fastapi import APIRouter
from ..repositories import repo_animal
from ..schemas import Animal, AnimalCreate,  AnimalUpdate

animal = APIRouter(prefix="/animals")

@animal.get("/", response_model=list[Animal])
def get_all_animals():
    return repo_animal.get_all_animals()

@animal.get("/{animal_id}", response_model=Animal)
def get_animal(animal_id: int):
    return repo_animal.get_animal(animal_id)

@animal.post("/", response_model=Animal)
def add_animal(animal: AnimalCreate):
    return repo_animal.add_animal(animal)

@animal.patch("/{animal_id}", response_model=AnimalUpdate)
def update_animal(animal_id: int, animal: AnimalUpdate):
    return repo_animal.update_animal(animal_id, animal)

@animal.delete("/{animal_id}")
def delete_animal(animal_id: int):
    return repo_animal.delete_animal(animal_id)

