from pydantic import BaseModel
import datetime

## FARMS

class Farm(BaseModel):
    farm_id: int
    name: str
    fid_numer: int
    position: str
    info: str

class FarmCreate(BaseModel):
    name: str
    fid_numer: int
    position: str
    info: str

class FarmUpdate(BaseModel):
    name: str | None = None
    fid_numer: int | None = None
    position: str | None = None
    info: str | None = None

## ANIMALS

class Animal(BaseModel):
    id: int
    aid_numer: str
    kind: str
    race: str
    utility: str
    sex: str
    date_of_birth: datetime.date

class AnimalCreate(BaseModel):
    farm_id: int
    aid_numer: str
    kind: str
    race: str
    utility: str
    sex: str
    date_of_birth: datetime.date

class AnimalUpdate(BaseModel):
    aid_numer: str | None = None
    kind: str | None = None
    race: str | None = None
    utility: str | None = None
    sex: str | None = None
    date_of_birth: datetime.date | None = None

##FIELDS

class Field(BaseModel):
    field_id: int
    farm_id: int
    type: str
    position: str
    area: float

class FieldCreate(BaseModel):
    farm_id: int
    type: str
    position: str
    area: float

class FieldUpdate(BaseModel):
    type: str | None = None
    position: str | None = None
    area: float | None = None

## FIELDWORK

class Fieldwork(BaseModel):
    field_id: int   
    id: int
    type_of_work: str
    method: str
    date: datetime.date
    cost: float

class FieldworkAdd(BaseModel):
    type_of_work: str
    method: str
    date: datetime.date
    cost: float

class FieldworkUpdate(BaseModel):
    type_of_work: str | None = None
    method: str | None = None
    date: datetime.date | None = None
    cost: float | None = None

## CROPS

class Crops(BaseModel):
    id: int
    field_id: int
    name: str
    type: str
    area: float
    year: int

class CropsAdd(BaseModel):
    name: str
    type: str
    area: float
    year: int

class CropsUpdate(BaseModel):
    name: str | None = None
    type: str | None = None
    area: float | None = None
    year: int | None = None

## MACHINES

class Machines(BaseModel):
    id: int
    type: str
    name: str
    model: str
    manufacture: int

class MachineAdd(BaseModel):
    type: str
    name: str
    model: str
    manufacture: int

class MachineUpdate(BaseModel):
    type: str | None = None
    name: str | None = None
    model: str | None = None
    manufacture: int | None = None

## FINANCIAL RECORDS

class FinancialRecords(BaseModel):
    id: int
    farm_id: int
    type: str
    category: str
    amount: float
    performer: str
    date: datetime.date
    info: str 


class FinancialRecordAdd(BaseModel):
    type: str
    category: str
    amount: float
    performer: str
    date: datetime.date
    info: str 


class FinancialRecordUpdate(BaseModel):
    type: str | None = None
    category: str | None = None
    amount: float | None = None
    performer: str | None = None
    date: datetime.date | None = None
    info: str | None = None


class FinancialSummary(BaseModel):
    income: float | None = None
    costs: float | None = None