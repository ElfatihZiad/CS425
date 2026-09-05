from datetime import date, time, datetime
from pydantic import BaseModel, ConfigDict

class RegistrationCreate(BaseModel):

    student_id: str
    student_email: str
    workshop_id: int
    registration_date: date

class RegistrationResponse(BaseModel):
    id: int
    student_id: str
    student_email: str
    workshop_id: int
    registration_date: date

    model_config = ConfigDict(from_attributes=True)

class WorkshopResponse(BaseModel):
    id: str
    title: str
    desc: str
    workshop_date: date
    workshop_time: time
    venue: str
    capacity: int
    registration_deadline: datetime