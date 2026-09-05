from sqlalchemy import Column, Integer, String, Date, Time, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Workshop(Base):
    __tablename__ = "workshop"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    venue = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    deadline = Column(DateTime, nullable=False)

    registrations = relationship("Registration", back_populates="workshop")


class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True)
    student_id = Column(String, nullable=False)
    student_name = Column(String, nullable=False)
    student_email = Column(String, nullable=False)
    registration_date = Column(Date, nullable=False)

    workshop_id = Column(
        Integer,
        ForeignKey("workshop.id"),
        nullable=False
    )

    workshop = relationship("Workshop", back_populates="registrations")