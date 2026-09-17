from ..database.database import connection
from fastapi import HTTPException
from ..schemas.schemas import Farm, FarmUpdate, FarmCreate

def create_farm(farm: FarmCreate):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO farm (name, fid_number, position, info) VALUES (%s, %s, %s, %s) RETURNING *",
                (farm.name, farm.fid_number, farm.position, farm.info)
            )
            result = cursor.fetchone()
            connection.commit()

            return result
    except Exception as ex:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating farm: {str(ex)}")

def get_all_farms():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM farm")
        result = cursor.fetchall()
    return result

def get_farm(farm_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM farm WHERE farm_id = %s", (farm_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Farm with ID {farm_id} not found.")
        result = cursor.fetchone()
    return result

def update_farm(farm_id: int, farm: FarmUpdate):
    farm_data = farm.model_dump(exclude_unset=True)
    if not farm_data:
        return {"message": "No fields to update."}

    fields = []
    values = []

    for field_name, value in farm_data.items():
        fields.append(f"{field_name} = %s")
        values.append(value)

    values.append(farm_id)
    query = f"UPDATE farm SET {', '.join(fields)} WHERE farm_id = %s"

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, values)
            connection.commit()
    except Exception as ex:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating farm: {str(ex)}")

    return {"message": f"Farm with ID {farm_id} updated successfully."}

def delete_farm(farm_id: int):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM farm WHERE farm_id = %s", (farm_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Farm with ID {farm_id} not found.")
        connection.commit()
    return {"message": f"Farm with ID {farm_id} deleted successfully."}