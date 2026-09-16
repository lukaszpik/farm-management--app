from fastapi import APIRouter
from ..repositories import repo_animal
from ..schemas import Animal, AnimalCreate

animal = APIRouter(prefix="/animals")

@animal.get("/", response_model=list[Animal])
def get_all_animals():
    return repo_animal.get_all_animals()
