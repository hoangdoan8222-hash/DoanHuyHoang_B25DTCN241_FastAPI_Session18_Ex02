from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_code = Column(String(20), unique=True)
    full_name = Column(String(100))
    email = Column(String(100), unique=True)
    status = Column(String(20), default="ACTIVE")

    registrations = relationship("Registration", back_populates="student")


class Workshop(Base):
    __tablename__ = "workshops"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(255))
    maximum_participants = Column(Integer)
    status = Column(String(20), default="OPEN")
    start_time = Column(DateTime)

    registrations = relationship("Registration", back_populates="workshop")


class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    workshop_id = Column(Integer, ForeignKey("workshops.id"))
    registered_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="REGISTERED")

    student = relationship("Student", back_populates="registrations")
    workshop = relationship("Workshop", back_populates="registrations")