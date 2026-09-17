from fastapi import HTTPException
from ..database.database import connection
from ..schemas.schemas import Fieldwork, FieldworkAdd, FieldworkUpdate


def get_all_fieldworks(farm_id: int, field_id: int):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT fw.* FROM fieldwork fw JOIN fields f ON fw.field_id = f.field_id WHERE f.farm_id = %s AND fw.field_id = %s",(farm_id, field_id))
        result = cursor.fetchall()
    return result


def get_fieldwork(farm_id: int, field_id: int, type_of_work: str):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT fw.* FROM fieldwork fw JOIN fields f ON fw.field_id = f.field_id WHERE f.farm_id = %s AND fw.field_id = %s AND fw.type_of_work = %s", 
            (farm_id, field_id, type_of_work))
        result = cursor.fetchall()
        if result is None:
            raise HTTPException(status_code=404, detail=f"Fieldwork with ID {id} not found.")
    return result


def add_fieldwork(farm_id: int, field_id: int, fieldwork: FieldworkAdd):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO fieldwork (field_id, type_of_work, method, cost, date) SELECT %s, %s, %s, %s, %s WHERE EXISTS ( SELECT 1 FROM fields WHERE field_id = %s AND farm_id = %s) RETURNING *",
                (field_id, fieldwork.type_of_work, fieldwork.method, fieldwork.cost, fieldwork.date, field_id, farm_id)) 
            result = cursor.fetchone()

            if result is None:
                connection.rollback()
                raise HTTPException(status_code=404,detail=f"Field with ID {field_id} not found in farm {farm_id}.")
            connection.commit()

            return result

    except HTTPException:
        raise

    except Exception as ex:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding fieldwork: {str(ex)}")


def update_fieldwork(farm_id: int, field_id: int, fieldwork_id: int, fieldwork: FieldworkUpdate):
    fieldwork_data = fieldwork.model_dump(exclude_unset=True)

    if not fieldwork_data:
        return {"message": "No fieldwork to update."}

    fields = []
    values = []

    for fieldwork_name, value in fieldwork_data.items():
        fields.append(f"{fieldwork_name} = %s")
        values.append(value)

    values.append(farm_id)
    values.append(field_id)
    values.append(fieldwork_id)

    query = f"UPDATE fieldwork fw SET {', '.join(fields)} FROM fields f WHERE fw.field_id = f.field_id AND f.farm_id = %s AND fw.field_id = %s AND fw.id = %s"

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, values)

            if cursor.rowcount == 0:
                connection.rollback()
                raise HTTPException(status_code=404, detail=f"Fieldwork with ID {fieldwork_id} not found.")
            connection.commit()

    except HTTPException:
        raise

    except Exception as ex:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating fieldwork: {str(ex)}")

    return {"message": f"Successfully updated fieldwork with ID {fieldwork_id}."}


def delete_fieldwork(farm_id: int, field_id: int, id: int):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM fieldwork fw USING fields f WHERE fw.field_id = f.field_id AND f.farm_id = %s AND fw.field_id = %s AND fw.id = %s",
                (farm_id, field_id, id))

            if cursor.rowcount == 0:
                connection.rollback()
                raise HTTPException(status_code=404, detail=f"Fieldwork with ID {id} not found.")
            connection.commit()

    except HTTPException:
        raise

    except Exception as ex:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting fieldwork: {str(ex)}")

    return {"message": f"Fieldwork with ID {id} deleted successfully."}
