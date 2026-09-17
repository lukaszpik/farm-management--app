from ..database import connection
from fastapi import HTTPException
from ..schemas import Field, FieldUpdate, FieldCreate

def get_all_fields(farm_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM fields WHERE farm_id = %s",  (farm_id))
        result = cursor.fetchall()
    return result

def get_field(farm_id: int, field_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM fields WHERE farm_id = %s AND field_id = %s", (farm_id, field_id))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Field with ID {field_id} not found.")
        result = cursor.fetchone()
    return result

def add_field(farm_id: int, field: FieldCreate):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO fields (farm_id, type, position, area) VALUES (%s, %s, %s, %s) RETURNING *",
                (farm_id, field.type, field.position, field.area)
            )
            result = cursor.fetchone()
            connection.commit()

            return result
    except Exception as ex:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding field: {str(ex)}")

def update_field(farm_id: int, field_id: int, field: FieldUpdate):
    field_data = field.model_dump(exclude_unset=True)
    if not field_data:
        return {"message": "No fields to update."}

    fields = []
    values = []

    for field_name, value in field_data.items():
        fields.append(f"{field_name} = %s")
        values.append(value)

    values.append(field_id)
    values.append(farm_id)
    query = f"UPDATE fields SET {', '.join(fields)} WHERE farm_id = %s AND field_id = %s"

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, values)
            connection.commit()
    except Exception as ex:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating field: {str(ex)}")

    return {"message": f"Field with ID {field_id} from Farm {farm_id} updated successfully."}

def delete_field(farm_id: int, field_id: int):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM fields WHERE farm_id = %s AND field_id = %s", (farm_id, field_id))
        connection.commit()
    return {"message": f"Field with ID {field_id} from Farm {farm_id} deleted successfully."}
    