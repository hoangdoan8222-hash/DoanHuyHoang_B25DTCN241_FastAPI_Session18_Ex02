from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from models import Student, Workshop, Registration
from schemas import StudentCreate, WorkshopCreate, RegistrationCreate


def create_student_service(data: StudentCreate, db: Session):
    check = db.query(Student).filter(
        (Student.student_code == data.student_code) |
        (Student.email == data.email)
    ).first()

    if check:
        raise HTTPException(status_code=400, detail="Student already exists")

    student = Student(**data.model_dump())

    db.add(student)
    db.commit()
    db.refresh(student)

    return student


def get_students_service(db: Session):
    return db.query(Student).all()


def create_workshop_service(data: WorkshopCreate, db:Session):

    workshop = Workshop(**data.model_dump())

    db.add(workshop)
    db.commit()
    db.refresh(workshop)

    return workshop


def get_workshops_service(db: Session):
    return db.query(Workshop).all()


def get_workshop_service(id:int, db:Session):

    workshop = db.query(Workshop).filter(
        Workshop.id == id
    ).first()

    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")

    return workshop


def register_workshop_service(data: RegistrationCreate, db: Session):

    student = db.query(Student).filter(
        Student.id == data.student_id
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if student.status != "ACTIVE":
        raise HTTPException(status_code=400, detail="Student inactive")

    workshop = db.query(Workshop).filter(
        Workshop.id == data.workshop_id
    ).first()

    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")

    if workshop.status != "OPEN":
        raise HTTPException(status_code=400, detail="Workshop closed")

    if workshop.start_time <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Workshop already started")

    check = db.query(Registration).filter(
        Registration.student_id == data.student_id,
        Registration.workshop_id == data.workshop_id,
        Registration.status == "REGISTERED"
    ).first()

    if check:
        raise HTTPException(status_code=400, detail="Already registered")

    total = db.query(Registration).filter(
        Registration.workshop_id == data.workshop_id,
        Registration.status == "REGISTERED"
    ).count()

    if total >= workshop.maximum_participants:
        raise HTTPException(status_code=400, detail="Workshop is full")

    registration = Registration(
        student_id=data.student_id,
        workshop_id=data.workshop_id
    )

    db.add(registration)
    db.commit()
    db.refresh(registration)

    return registration


def get_student_workshops_service(student_id:int, db:Session):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    workshops = []

    for registration in student.registrations:
        if registration.status == "REGISTERED":
            workshops.append({
                "id": registration.workshop.id,
                "title": registration.workshop.title
            })

    return {
        "student_id": student.id,
        "full_name": student.full_name,
        "workshops": workshops
    }


def get_workshop_students_service(workshop_id:int, db:Session):

    workshop = db.query(Workshop).filter(
        Workshop.id == workshop_id
    ).first()

    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")

    students = []

    for registration in workshop.registrations:
        if registration.status == "REGISTERED":
            students.append({
                "id": registration.student.id,
                "full_name": registration.student.full_name
            })

    return {
        "workshop_id": workshop.id,
        "title": workshop.title,
        "students": students
    }


def cancel_registration_service(id:int, db:Session):

    registration = db.query(Registration).filter(
        Registration.id == id
    ).first()

    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    registration.status = "CANCELLED"

    db.commit()

    return {"message": "Registration cancelled"}