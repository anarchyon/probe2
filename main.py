from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session

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
def root(request: Request, db: Session = Depends(get_db_session)):
    staff = db.query(models.Staff).order_by(models.Staff.staff_id).all()
    for employee in staff:
        employee.birthdate = employee.birthdate.strftime("%d-%m-%Y")
    return templates.TemplateResponse("index.html",{"request": request, "data": staff})

@app.post("/add", response_class=HTMLResponse)
async def add_employee(db: Session = Depends(get_db_session), 
                 first_name = Form(...),
                 last_name = Form(...),
                 address = Form(...),
                 birthdate = Form(...)
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
    response = RedirectResponse("/", status_code=303)
    return response

# @app.get("/get-staff")
# def get_staff():
#     connection = make_db_connection()
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM staff ORDER BY staff_id")
#     result = cursor.fetchall()
#     json_data = []
#     for row in result:
#         json_data.append(dict(zip([column[0] for column in cursor.description], row)))
#     cursor.close()
#     connection.close()
#     return json_data


# @app.get("/get-person/{last_name}")
# def get_person(last_name: str):
#     connection = make_db_connection()
#     cursor = connection.cursor()
#     cursor.execute(f"SELECT * FROM staff WHERE last_name = '{last_name}'")
#     result = cursor.fetchall()
#     json_data = []
#     for row in result:
#         json_data.append(dict(zip([column[0] for column in cursor.description], row)))
#     cursor.close()
#     connection.close()
#     return json_data

# @app.post("/add-person")
# def add_person(parameters: Employee):
#     person_dict = {}
#     person_dict['Имя'] = parameters.first_name
#     person_dict['Фамилия'] = parameters.last_name
#     person_dict['Адрес'] = parameters.address
#     person_dict['Год рождения'] = parameters.birthdate