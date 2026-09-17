from fastapi import HTTPException
from ..database import connection
from ..schemas import Crops, CropsAdd, CropsUpdate


def get_all_crops(farm_id: int, field_id: int):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT cr.* FROM crops cr JOIN fields f ON cr.field_id = f.field_id WHERE f.farm_id = %s AND cr.field_id = %s",(farm_id, field_id))
        result = cursor.fetchall()
    return result


def get_crop(farm_id: int, field_id: int, name: str):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT cr.* FROM crops cr JOIN fields f ON cr.field_id = f.field_id WHERE f.farm_id = %s AND cr.field_id = %s AND cr.name = %s", 
            (farm_id, field_id, name))
        result = cursor.fetchall()
        if result is None:
            raise HTTPException(status_code=404, detail=f"Crop with name {name} not found.")
    return result


def add_crop(farm_id: int, field_id: int, crops: CropsAdd):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO crops (field_id, name, type, area, year) SELECT %s, %s, %s, %s, %s WHERE EXISTS ( SELECT 1 FROM fields WHERE field_id = %s AND farm_id = %s) RETURNING *",
                (field_id, crops.name, crops.type, crops.area, crops.year, field_id, farm_id)) 
            result = cursor.fetchone()

            if result is None:
                connection.rollback()
                raise HTTPException(status_code=404,detail=f"Something went wrong.")
            connection.commit()

            return result

    except HTTPException:
        raise

    except Exception as ex:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding crop: {str(ex)}")


def update_crop(farm_id: int, field_id: int, id: int, crops: CropsUpdate):
    crops_data = crops.model_dump(exclude_unset=True)

    if not crops_data:
        return {"message": "No crops to update."}

    fields = []
    values = []

    for crops_name, value in crops_data.items():
        fields.append(f"{crops_name} = %s")
        values.append(value)

    values.append(farm_id)
    values.append(field_id)
    values.append(id)

    query = f"UPDATE crops cr SET {', '.join(fields)} FROM fields f WHERE cr.field_id = f.field_id AND f.farm_id = %s AND cr.field_id = %s AND cr.id = %s"

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, values)

            if cursor.rowcount == 0:
                connection.rollback()
                raise HTTPException(status_code=404, detail=f"Crop with ID {id} not found.")
            connection.commit()

    except HTTPException:
        raise

    except Exception as ex:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating a crop: {str(ex)}")

    return {"message": f"Successfully updated crop with ID {id}."}


def delete_crop(farm_id: int, field_id: int, id: int):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM crops cr USING fields f WHERE cr.field_id = f.field_id AND f.farm_id = %s AND cr.field_id = %s AND cr.id = %s",
                (farm_id, field_id, id))

            if cursor.rowcount == 0:
                connection.rollback()
                raise HTTPException(status_code=404, detail=f"Crop with ID {id} not found.")
            connection.commit()

    except HTTPException:
        raise

    except Exception as ex:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting crop: {str(ex)}")

    return {"message": f"Crop with ID {id} deleted successfully."}
