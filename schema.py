import datetime
from pydantic import BaseModel, field_validator

class Employee(BaseModel):
    """Класс описывающий сотрудника"""
    staff_id: int
    first_name: str
    last_name: str
    address: str
    birthdate: datetime.date
    
    class Config:
        orm_mode=True
