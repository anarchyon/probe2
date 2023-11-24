from sqlalchemy import String, Column, Integer, Date

from database import Base

class Staff(Base):
    __tablename__ = "staff"
    
    staff_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    birthdate = Column(Date)
