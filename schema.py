import datetime
from pydantic import BaseModel

class Staff(BaseModel):
    """Класс описывающий сотрудника"""
    staff_id: int | None = None
    first_name: str
    last_name: str
    address: str | None = None
    birthdate: datetime.date | None = None
    
    class Config:
        from_attributes=True
