from datetime import date, time, datetime
from pydantic import BaseModel, ConfigDict

class RegistrationCreate(BaseModel):

    student_id: str
    student_name: str
    student_email: str
    workshop_id: int

class RegistrationResponse(BaseModel):
    id: int
    student_id: str
    student_name: str
    student_email: str
    workshop_id: int
    registration_date: date

    model_config = ConfigDict(from_attributes=True)

class WorkshopResponse(BaseModel):
    id: int
    title: str
    description: str
    date: date
    time: time
    venue: str
    capacity: int
    deadline: datetime

    model_config = ConfigDict(from_attributes=True)
