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
    field_id: int | None = None
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