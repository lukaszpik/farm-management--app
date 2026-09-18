from fastapi import APIRouter
from ..schemas.schemas import FinancialRecords, FinancialSummary, FinancialRecordUpdate, FinancialRecordAdd
from ..repositories import repo_finances
import datetime

finances = APIRouter(prefix="/farms/{farm_id}/finances", tags=["Finances"])

@finances.get("/", response_model=list[FinancialRecords])
def get_all_financial_records(farm_id: int):
    return repo_finances.get_all_financial_records(farm_id)

@finances.post("/", response_model=FinancialRecordAdd)
def add_financial_record(farm_id: int, finance: FinancialRecordAdd):
    return repo_finances.add_financial_record(farm_id, finance)

@finances.get("/summary", response_model=FinancialSummary)
def get_financial_summary(farm_id: int, date_from: datetime.date, date_to: datetime.date):
    return repo_finances.get_financial_summary(farm_id, date_from, date_to)

@finances.get("/income", response_model=FinancialSummary)
def get_finan_summ_of_income(farm_id: int, date_from: datetime.date, date_to: datetime.date):
    return repo_finances.get_finan_summ_of_income(farm_id, date_from, date_to)

@finances.patch("/", response_model=FinancialRecordUpdate)
def update_financial_record(farm_id: int, id: int, financial_record: FinancialRecordUpdate):
    return repo_finances.update_financial_record(farm_id, id, financial_record)