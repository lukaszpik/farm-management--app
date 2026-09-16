from pydantic import BaseModel
from datetime import date

class Animal(BaseModel):
    id: int
    aid_numer: str
    kind: str
    race: str
    utility: str
    sex: str
    date_of_birth: date

class AnimalCreate(BaseModel):
    farm_id: int
    aid_numer: str
    kind: str
    race: str
    utility: str
    sex: str
    date_of_birth: date

class AnimalUpdate(BaseModel):
    aid_numer: str | None = None
    kind: str | None = None
    race: str | None = None
    utility: str | None = None
    sex: str | None = None
    date_of_birth: date | None = None