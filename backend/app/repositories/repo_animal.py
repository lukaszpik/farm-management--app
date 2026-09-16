from fastapi import APIRouter
from ..database import connection
from ..schemas import Animal, AnimalCreate

animalRouter = APIRouter(prefix="/animals")

@animalRouter.get("/", response_model=Animal)
def get_all_animals():
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, aid_numer, kind, race, utility, sex, date_of_birth FROM animals")
        result = cursor.fetchall()
    return result
    

@animalRouter.get("/animal/{animal_id}", response_model=Animal)
def get_animal(animal_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, aid_numer, kind, race, utility, sex, date_of_birth FROM animals WHERE id = %s", (animal_id,))
        result = cursor.fetchone()
    return result

@animalRouter.post("/", response_model=AnimalCreate)
def add_animal(animal: AnimalCreate):
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO animals (aid_numer, kind, race, utility, sex, date_of_birth) VALUES (%s, %s, %s, %s, %s, %s)",
            (animal.aid_numer, animal.kind, animal.race, animal.utility, animal.sex, animal.date_of_birth)
        )
        connection.commit()
        result = cursor.fetchone()
    return result

@animalRouter.delete("/{animal_id}")
def delete_animal(animal_id: int):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM animals WHERE id = %s", (animal_id,))
        if cursor.rowcount == 0:
            connection.rollback()
            raise HTTPException(status_code=404, detail=f"Animal with ID {animal_id} not found.")
        connection.commit()
    return {"message": f"Animal with ID {animal_id} deleted successfully."}