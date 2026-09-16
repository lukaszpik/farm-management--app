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
    aid_numer: str
    kind: str
    race: str
    utility: str
    sex: str
    date_of_birth: date