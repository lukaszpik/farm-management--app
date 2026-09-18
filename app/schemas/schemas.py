from pydantic import BaseModel, Field as PField
from typing import Literal
import datetime

## FARMS

class Farm(BaseModel):
    farm_id: int
    name: str = PField(min_length=1)
    fid_numer: int = PField(gt=0)
    position: str = PField(min_length=3)
    info: str 

class FarmCreate(BaseModel):
    name: str = PField(min_length=1)
    fid_numer: int = PField(gt=0)
    position: str = PField(min_length=3)
    info: str

class FarmUpdate(BaseModel):
    name: str | None = PField(default=None, min_length=1)
    fid_numer: int | None = PField(default=None, gt=0)
    position: str | None = None
    info: str | None = None

## ANIMALS

class Animal(BaseModel):
    id: int
    aid_numer: str = PField(min_length=3)
    kind: str
    race: str = PField(min_length=2)
    utility: str
    sex: str
    date_of_birth: datetime.date

class AnimalCreate(BaseModel):
    farm_id: int = PField(gt=0)
    aid_numer: str = PField(min_length=3)
    kind: str
    race: str = PField(min_length=2)
    utility: str
    sex: str
    date_of_birth: datetime.date

class AnimalUpdate(BaseModel):
    aid_numer: str | None = PField(default=None, min_length=3)
    kind: str | None = None
    race: str | None = PField(default=None, min_length=2)
    utility: str | None = None
    sex: str | None = None
    date_of_birth: datetime.date | None = None

##FIELDS

class Field(BaseModel):
    field_id: int 
    farm_id: int = PField(gt=0)
    type: str
    position: str
    area: float = PField(gt=0)

class FieldCreate(BaseModel):
    farm_id: int 
    type: str
    position: str 
    area: float = PField(gt=0)

class FieldUpdate(BaseModel):
    type: str
    position: str | None = None
    area: float | None = PField(default=None, gt=0)

## FIELDWORK

class Fieldwork(BaseModel):
    field_id: int = PField(gt=0)
    id: int
    type_of_work: str 
    method: str 
    date: datetime.date
    cost: float = PField(gt=0)

class FieldworkAdd(BaseModel):
    type_of_work: str 
    method: str 
    date: datetime.date
    cost: float = PField(gt=0)

class FieldworkUpdate(BaseModel):
    type_of_work: str | None = None
    method: str | None = None
    date: datetime.date | None = None
    cost: float | None = PField(default=None,gt=0)

## CROPS

class Crops(BaseModel):
    id: int
    field_id: int
    name: str = PField(min_length=3)
    type: str = PField(min_length=3)
    area: float = PField(gt=0)
    year: int = PField(gt=1900)

class CropsAdd(BaseModel):
    name: str = PField(min_length=3)
    type: str = PField(min_length=3)
    area: float = PField(gt=0)
    year: int = PField(gt=1900)

class CropsUpdate(BaseModel):
    name: str | None = PField(default=None, min_length=3)
    type: str | None = PField(default=None, min_length=3)
    area: float | None = PField(default=None, gt=0)
    year: int | None = PField(default=None, gt=1900)

## MACHINES

class Machines(BaseModel):
    id: int
    type: str = PField(min_length=3) 
    name: str = PField(min_length=3)
    model: str = PField(min_length=3)
    manufacture: int = PField(gt=1900)

class MachineAdd(BaseModel):
    type: str = PField(min_length=3) 
    name: str = PField(min_length=3)
    model: str = PField(min_length=3)
    manufacture: int = PField(gt=1900)

class MachineUpdate(BaseModel):
    type: str | None = PField(default=None, min_length=3)
    name: str | None = PField(default=None, min_length=3)
    model: str | None = PField(default=None, min_length=3)
    manufacture: int | None = PField(default=None, gt=1900)

## FINANCIAL RECORDS

class FinancialRecords(BaseModel):
    id: int
    farm_id: int
    type: Literal["przychod", "koszt"]
    category: str 
    amount: float = PField(gt=0)
    performer: str
    date: datetime.date
    info: str 


class FinancialRecordAdd(BaseModel):
    type: Literal["przychod", "koszt"]
    category: str
    amount: float = PField(gt=0)
    performer: str
    date: datetime.date
    info: str 


class FinancialRecordUpdate(BaseModel):
    type: Literal["przychod", "koszt"] | None = None
    category: str | None = None
    amount: float | None = PField(default=None, gt=0)
    performer: str | None = None
    date: datetime.date | None = None
    info: str | None = None


class FinancialSummary(BaseModel):
    income: float | None = None
    costs: float | None = None