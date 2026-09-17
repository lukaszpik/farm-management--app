from fastapi import HTTPException
from ..database import connection
from ..schemas import Fieldwork, FieldworkCreate, FieldworkUpdate

def get_all_fieldworks(farm_id: int, field_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM fieldworks WHERE farm_id = %s AND field_id = %s", (farm_id, field_id))
        result = cursor.fetchall()

    return result

def get_fieldwork(farm_id: int, field_id: int, type_of_fieldwork: str):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM fieldworks WHERE farm_id = %s AND field_id = %s AND type_of_fieldwork = %s", (farm_id, field_id, type_of_fieldwork))
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail=f"Fieldwork with ID {type_of_fieldwork} not found.")
        
    return result

def add_fieldwork(farm_id: int, field_id: int, fieldwork: Fieldwork):
    with connection.cursor() as cursor:
        cursor.execute(
                       