import datetime
from pydantic import BaseModel

class Staff(BaseModel):
    """Класс описывающий сотрудника"""
    staff_id: int
    first_name: str
    last_name: str
    address: str
    birthdate: datetime.date
    
    class Config:
        from_attributes=True
