from fastapi import HTTPException
from ..database import connection
from ..schemas import Machines, MachineAdd, MachineUpdate



def get_all_machines(farm_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM machines WHERE farm_id = %s", (farm_id,))
        result = cursor.fetchall()

    return result
    
def get_machine(farm_id: int, type: str):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM machines WHERE farm_id = %s AND type = %s", (farm_id, type))
        result = cursor.fetchall()
        if result is None:
            raise HTTPException(status_code=404, detail=f"Machine  with type {type} not found.")
        
    return result

def add_machine(farm_id: int, machine: MachineAdd):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO machines (farm_id, type, name, model, manufacture) VALUES (%s, %s, %s, %s, %s) RETURNING *",
                (farm_id, machine.type, machine.name, machine.model, machine.manufacture)
            )
            result = cursor.fetchone()
            connection.commit()

            return result
        
    except Exception as ex:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding machine{str(ex)}")

def update_machine(farm_id: int, id: int, machine:MachineUpdate):
    machine_data=machine.model_dump(exclude_unset=True)
    if not machine_data:
        return {"message": "No machines to update."}

    fields = []
    values = []

    for field, value in machine_data.items():
        fields.append(f"{field} = %s")
        values.append(value)

    values.append(farm_id)
    values.append(id)
    query = f"UPDATE machines SET {', '.join(fields)} WHERE farm_id = %s AND id = %s"

    try:
        with connection.cursor() as cursor:
           cursor.execute(query, values)
           connection.commit()

    except HTTPException:
        connection.rollback()
        raise
    
    except Exception as ex:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error while updating a machine: {str(ex)}")

    return {"message": f"Machine with ID {id} updated successfully."}

def delete_machine(farm_id: int, id: int):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM machines WHERE farm_id = %s AND id = %s", (farm_id, id))
        if cursor.rowcount == 0:
            connection.rollback()
            raise HTTPException(status_code=404, detail=f"Machine with ID {id} not found.")
        connection.commit()
    return {"message": f"Machine with ID {id} deleted successfully."}