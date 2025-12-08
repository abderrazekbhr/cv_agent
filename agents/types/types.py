from typing import Optional
from pydantic import BaseModel,Date, field_validator, EmailStr
from datetime import datetime
from enum import Enum

class Sex(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class Treatment(BaseModel):
    name:str
    description:str
    side_effects:list[str]
    date:datetime
    cost:float
    
class Disease(BaseModel):
    name: str
    description: str
    symptoms: list[str]
    treatment: list[Treatment]
    prevention: list[str]
    cure_probability: float


class UserInfo(BaseModel):
    full_name: str
    age: int
    sex: Sex
    email: EmailStr
    phone: str
    city: str
    country: str
    chronic_disease:list[Disease]=[]
    symptom:list[str]=[]
    allergy:list[str]=[]
    actual_treatement:list[Treatment]=[]
    
    
    @field_validator('phone')
    def validate_phone(cls, v: str) -> bool:
        if v.startswith('+'):
            return v[1:].isdigit()
        else:
            return v.isdigit()




    