from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import update, select, desc
import json

import models, schema, utils
from database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    print("Вход в метод root()")
    return templates.TemplateResponse("index0.html", {"request": request})

@app.get("/get-staff/", response_class=HTMLResponse)
def get_staff(request: Request, db: Session = Depends(get_db_session), sort_column: str = "staff_id", is_sort_order_asc: bool = True):
    try:
        needed_sort_column = getattr(models.Staff_DB, sort_column)
    except:
        needed_sort_column = models.Staff_DB.staff_id
    
    if is_sort_order_asc:
        staff = db.query(models.Staff_DB).order_by(needed_sort_column).all()
    else:
        staff = db.query(models.Staff_DB).order_by(desc(needed_sort_column)).all()
    return templates.TemplateResponse("table.html", {"request": request, "data": changeDateForShow(staff)})

@app.post("/add")
async def add_employee(employee: schema.Staff, db: Session = Depends(get_db_session)):
    added_employee = models.Staff_DB(
                            first_name=employee.first_name,
                            last_name=employee.last_name,
                            address=employee.address, 
                            birthdate=employee.birthdate)
    print(added_employee)
    db.add(added_employee)
    db.commit()
    db.refresh(added_employee)

@app.post("/delete/{staff_id}")
async def delete_employee(staff_id: int, db:Session = Depends(get_db_session)):
    deleted_employee = db.query(models.Staff_DB).get(staff_id)
    db.delete(deleted_employee)
    db.commit()

@app.get("/get/{staff_id}")
async def get_person(staff_id: int, db: Session = Depends(get_db_session)):
    employee = db.query(models.Staff_DB).get(staff_id)
    empl = jsonable_encoder(employee)
    return empl

@app.post("/update/{staff_id}")
async def update_employee(staff_id: int, employee: schema.Staff, db: Session = Depends(get_db_session)):
    updated_employee: models.Staff_DB = db.query(models.Staff_DB).get(staff_id) # type: ignore
    updated_employee.first_name = employee.first_name
    updated_employee.last_name = employee.last_name
    updated_employee.address = employee.address
    updated_employee.birthdate = employee.birthdate
    db.commit()
    db.refresh(updated_employee)

@app.get("/search")
def search_employee(request: Request, db: Session = Depends(get_db_session), 
                    first_name: str | None = None, 
                    last_name: str | None = None,
                    address: str | None = None,
                    ):
    first_name = f"%{first_name}%"
    last_name = f"%{last_name}%"
    address = f"%{address}%"
    employeeOrStaff = db.query(models.Staff_DB).\
                                filter(models.Staff_DB.first_name.ilike(first_name),\
                                       models.Staff_DB.last_name.ilike(last_name),\
                                        models.Staff_DB.address.ilike(address)).\
                                all()
    
    response = templates.TemplateResponse("tableSearch.html", {"request": request, "searched_staff": changeDateForShow(employeeOrStaff)})
    return response

def changeDateForShow(staff):
    for employee in staff:
        employee.birthdate = employee.birthdate.strftime("%d-%m-%Y")
    return staff
