from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine, get_db
from models import Registration, Workshop
from schemas import RegistrationResponse, RegistrationCreate, WorkshopResponse
from service import RegistrationService, WorshopService

from datetime import date, time, datetime

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Campus Workshop Registration System")

registration_service = RegistrationService()
workshop_service = WorshopService()


@app.get("/workshops", response_model=list[WorkshopResponse])
def list_available(db: Session = Depends(get_db)):
    return workshop_service.list_available(db)

@app.get("/workshops/{workshop_id}", response_model=WorkshopResponse)
def get_workshop(workshop_id: int, db: Session = Depends(get_db)):
    return workshop_service.find_by_id(db, workshop_id)

@app.post("/registrations", response_model=RegistrationResponse, status_code=201)
def create_registration(request: RegistrationCreate, db: Session = Depends(get_db)):
    return registration_service.create_registration(db, request)


@app.get("/registrations/{workshop_id}", response_model=list[RegistrationResponse])
def get_registred_student(workshop_id: int, db: Session = Depends(get_db)):
    return registration_service.get_registration(db, workshop_id)



# ---------- demo seed data ----------


def seed_data():
    db = SessionLocal()
    try:
        if db.query(Workshop).count() == 0:
            db.add_all(
                [
                    Workshop(title="Spring Boot Essentials", description="REST APIS", date=date(2026, 9, 2), time=time(12,12,12), venue="Room A101", capacity=30, deadline = datetime(2026, 10, 10, 2,0,0)),
                    Workshop(title="Software Engineering", description="...", date=date(2026, 9, 2), time=time(12,12,12), venue="Room B202", capacity=25, deadline = datetime(2026, 10, 10, 2,0,0)),
                    Workshop(title="Machine Learning", description="...", date=date(2026, 9, 2), time=time(12,12,12), venue="Lab C303", capacity=20, deadline = datetime(2026, 10, 10, 2,0,0)),

                ]
            )
            db.commit()
    finally:
        db.close()


seed_data()