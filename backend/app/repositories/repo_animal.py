from fastapi import HTTPException
from ..database.database import connection
from ..schemas.schemas import AnimalCreate, AnimalUpdate



def get_all_animals(farm_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM animals WHERE farm_id = %s", (farm_id,))
        result = cursor.fetchall()

    return result
    
def get_animal(farm_id: int, animal_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM animals WHERE farm_id = %s AND id = %s", (farm_id, animal_id))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail=f"Animal with ID {animal_id} not found.")
        
    return result

def add_animal(farm_id: int, animal: AnimalCreate):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO animals (farm_id, aid_numer, kind, race, utility, sex, date_of_birth) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *",
                (farm_id, animal.aid_numer, animal.kind, animal.race, animal.utility, animal.sex, animal.date_of_birth)
            )
            result = cursor.fetchone()
            connection.commit()

            return result
        
    except Exception as ex:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding animal: {str(ex)}")

def update_animal(farm_id: int, animal_id: int, animal: AnimalUpdate):
    animal_data=animal.model_dump(exclude_unset=True)
    if not animal_data:
        return {"message": "No fields to update."}

    fields = []
    values = []

    for field, value in animal_data.items():
        fields.append(f"{field} = %s")
        values.append(value)

    values.append(farm_id)
    values.append(animal_id)
    query = f"UPDATE animals SET {', '.join(fields)} WHERE farm_id = %s AND id = %s"

    try:
        with connection.cursor() as cursor:
           cursor.execute(query, values)
           connection.commit()

    except HTTPException as http_ex:
        connection.rollback()
        raise
    
    except Exception as ex:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating animal: {str(ex)}")

    return {"message": f"Animal with ID {animal_id} updated successfully."}

def delete_animal(farm_id: int, animal_id: int):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM animals WHERE farm_id = %s AND id = %s", (farm_id, animal_id))
        if cursor.rowcount == 0:
            connection.rollback()
            raise HTTPException(status_code=404, detail=f"Animal with ID {animal_id} not found.")
        connection.commit()
    return {"message": f"Animal with ID {animal_id} deleted successfully."}