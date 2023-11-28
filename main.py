from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import update, desc
import json

import models, schema, utils
from database import SessionLocal, engine

app = FastAPI()

sort_params = utils.SortParams()

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
def get_staff(request: Request, db: Session = Depends(get_db_session), order: str = "staff_id"):
    print("Вход в метод get_staff()")
    try:
        needed_sort_column = getattr(models.Staff, order)
    except:
        needed_sort_column = models.Staff.staff_id
    print(f"needed_sort_column - {needed_sort_column}")
    
    if sort_params.sort_column != needed_sort_column: # type: ignore
        sort_params.sort_column = needed_sort_column
        sort_params.is_sort_asc = True
    elif sort_params.is_sort_asc:
        sort_params.is_sort_asc = False
    else:
        sort_params.is_sort_asc = True
    
    print(f"sort_params.sort_column - {sort_params.sort_column}")
    print(sort_params.is_sort_asc)
    
    if sort_params.is_sort_asc:
        staff = db.query(models.Staff).order_by(sort_params.sort_column).all()
    else:
        staff = db.query(models.Staff).order_by(desc(sort_params.sort_column)).all()
    for employee in staff:
        employee.birthdate = employee.birthdate.strftime("%d-%m-%Y")
    return templates.TemplateResponse("index.html", {"request": request, "data": staff})

@app.post("/add")
async def add_employee(db: Session = Depends(get_db_session), 
                 first_name = Form(...),
                 last_name = Form(...),
                 address = Form(...),
                 birthdate = Form(...),
                 ):
    employee = models.Staff(
                        first_name = first_name,
                        last_name = last_name,
                        address = address,
                        birthdate = birthdate
                        )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    response = RedirectResponse("/get-staff", status_code=303)
    return response

@app.post("/delete/{staff_id}")
async def delete_employee(staff_id: int, db:Session = Depends(get_db_session)):
    deleted_employee = db.query(models.Staff).get(staff_id)
    db.delete(deleted_employee)
    db.commit()
    response = RedirectResponse("/get-staff", status_code=303)
    return response

@app.get("/get/{staff_id}")
async def get_person(staff_id: int, db: Session = Depends(get_db_session)):
    employee = db.query(models.Staff).get(staff_id)
    empl = jsonable_encoder(employee)
    print(empl)
    return empl

@app.post("/update/{staff_id}")
async def update_employee(staff_id: int, db: Session = Depends(get_db_session),
                            first_name = Form(...),
                            last_name = Form(...),
                            address = Form(...),
                            birthdate = Form(...),
                            ):
    updated_employee: models.Staff = db.query(models.Staff).get(staff_id) # type: ignore
    updated_employee.first_name = first_name
    updated_employee.last_name = last_name
    updated_employee.address = address
    updated_employee.birthdate = birthdate
    db.commit()
    db.refresh(updated_employee)
    response = RedirectResponse("/get-staff", status_code=303)
    return response
