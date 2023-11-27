from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import update
import json

import models, schema
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
    return templates.TemplateResponse("index0.html", {"request": request})

@app.get("/get-staff", response_class=HTMLResponse)
def get_staff(request: Request, db: Session = Depends(get_db_session)):
    staff = db.query(models.Staff).order_by(models.Staff.staff_id).all()
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
async def get_person(request: Request, staff_id: int, db: Session = Depends(get_db_session)):
    employee = db.query(models.Staff).get(staff_id)
    empl = jsonable_encoder(employee)
    return empl

@app.post("/update/{staff_id}")
async def update_employee(staff_id: int, db: Session = Depends(get_db_session),
                            first_name = Form(...),
                            last_name = Form(...),
                            address = Form(...),
                            birthdate = Form(...),
                            ):
    updated_employee = db.query(models.Staff).get(staff_id)
    updated_employee.first_name = first_name
    updated_employee.last_name = last_name
    updated_employee.address = address
    updated_employee.birthdate = birthdate
    db.commit()
    db.refresh(updated_employee)
    response = RedirectResponse("/get-staff", status_code=303)
    return response
