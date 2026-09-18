from fastapi import HTTPException
from ..database.database import connection
from ..schemas.schemas import FinancialRecordAdd, FinancialRecordUpdate, FinancialSummary
import datetime

def get_all_financial_records(farm_id: int):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM financial_records WHERE farm_id = %s ORDER BY date DESC",
            (farm_id,))
        result = cursor.fetchall()

    return result


def add_financial_record(farm_id: int, financial_record: FinancialRecordAdd):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO financial_records(farm_id, type, category, amount, performer, date, info) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *",
                (farm_id,financial_record.type, financial_record.category, financial_record.amount, financial_record.performer, financial_record.date, financial_record.info))
            result = cursor.fetchone()
            connection.commit()

            return result

    except Exception as ex:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding financial record: {str(ex)}")

def get_financial_summary(farm_id: int, date_from: datetime.date, date_to: datetime.date):
    try:
        with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COALESCE(SUM(amount) FILTER (WHERE type = 'przychod'), 0) AS income, " \
                    "COALESCE(SUM(amount) FILTER (WHERE type = 'koszt'), 0) AS costs FROM financial_records WHERE farm_id = %s AND date BETWEEN %s AND %s",
                    (farm_id, date_from, date_to))
                result = cursor.fetchone()
        return result
    except Exception as ex:
        connection.rollback()
        raise HTTPException(status_code=422, detail=f"Invalid date entry, correct: RRRR-MM-DD")

def get_finan_summ_of_income(farm_id: int, date_from: datetime.date, date_to: datetime.date):
    try:
        with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COALESCE(SUM(amount) FILTER (WHERE type = 'przychod'), 0) AS income FROM financial_records WHERE farm_id = %s AND date BETWEEN %s AND %s",
                    (farm_id, date_from, date_to))
                result = cursor.fetchone()
        return result
    except Exception as ex:
        connection.rollback()
        raise HTTPException(status_code=422, detail=f"Invalid date entry, correct: RRRR-MM-DD")

def update_financial_record(farm_id: int, id: int, financial_record: FinancialRecordUpdate):
    financial_data = financial_record.model_dump(exclude_unset=True)

    if not financial_data:
        return {"message": "No financial record fields to update."}

    fields = []
    values = []

    for field, value in financial_data.items():
        fields.append(f"{field} = %s")
        values.append(value)

    values.append(farm_id)
    values.append(id)

    query = f"UPDATE financial_records SET {', '.join(fields)} WHERE farm_id = %s AND id = %s"

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, values)

            if cursor.rowcount == 0:
                connection.rollback()
                raise HTTPException(status_code=404, detail=f"Financial record with ID {id} not found.")
            connection.commit()

    except HTTPException:
        raise

    except Exception as ex:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating financial record: {str(ex)}")

    return {"message": f"Financial record with ID {id} updated successfully."}