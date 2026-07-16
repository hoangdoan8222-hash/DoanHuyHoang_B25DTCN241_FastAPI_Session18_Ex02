from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from database import Base, engine, get_db

from schemas import (
    StudentCreate,
    StudentResponse,
    WorkshopCreate,
    WorkshopResponse,
    RegistrationCreate,
    RegistrationResponse,
    StudentWorkshopResponse,
    WorkshopStudentResponse
)

from services import (
    create_student_service,
    get_students_service,
    create_workshop_service,
    get_workshops_service,
    get_workshop_service,
    register_workshop_service,
    get_student_workshops_service,
    get_workshop_students_service,
    cancel_registration_service
)

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Workshop Management API"}


# ================= STUDENT =================

@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    return create_student_service(student, db)


@app.get(
    "/students",
    response_model=list[StudentResponse]
)
def get_students(db: Session = Depends(get_db)):
    return get_students_service(db)


# ================= WORKSHOP =================

@app.post(
    "/workshops",
    response_model=WorkshopResponse,
    status_code=status.HTTP_201_CREATED
)
def create_workshop(
    workshop: WorkshopCreate,
    db: Session = Depends(get_db)
):
    return create_workshop_service(workshop, db)


@app.get(
    "/workshops",
    response_model=list[WorkshopResponse]
)
def get_workshops(db: Session = Depends(get_db)):
    return get_workshops_service(db)


@app.get(
    "/workshops/{id}",
    response_model=WorkshopResponse
)
def get_workshop(
    id: int,
    db: Session = Depends(get_db)
):
    return get_workshop_service(id, db)


# ================= REGISTRATION =================

@app.post(
    "/registrations",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED
)
def register_workshop(
    registration: RegistrationCreate,
    db: Session = Depends(get_db)
):
    return register_workshop_service(registration, db)


@app.delete("/registrations/{id}")
def cancel_registration(
    id: int,
    db: Session = Depends(get_db)
):
    return cancel_registration_service(id, db)


# ================= QUERY =================

@app.get(
    "/students/{id}/workshops",
    response_model=StudentWorkshopResponse
)
def get_student_workshops(
    id: int,
    db: Session = Depends(get_db)
):
    return get_student_workshops_service(id, db)


@app.get(
    "/workshops/{id}/students",
    response_model=WorkshopStudentResponse
)
def get_workshop_students(
    id: int,
    db: Session = Depends(get_db)
):
    return get_workshop_students_service(id, db)