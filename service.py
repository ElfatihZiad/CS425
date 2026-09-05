from fastapi import HTTPException
from database import get_db
from repositories import WorkshopRepository, RegistrationRepository
from schemas import RegistrationCreate, RegistrationResponse
from datetime import datetime
from models import Registration

class RegistrationService:

    def __init__(self):
        self.registration_repo = RegistrationRepository()

    def get_registration(self, workshop_id):
        return self.registration_repo.get_registred_student(workshop_id)

    def create_registration(self, db, request: RegistrationCreate):

        current_datetime = datetime.now()

        # 1. Reject registration when deadline has passed.

        if request.registartion_deadline < current_datetime:
            raise HTTPException(status_code=409, detail="Registration Deadline Has Passed")

        # 2. Reject Req when Workshop Has Reachead Maximum Capacity

        registration_count = len(self.registration_repo.get_registred_student(get_db(), request.id))
        if registration_count >= request.capacity:
            raise HTTPException(status_code=404, detail="Workshop Has Reachead Maximum Capacity")

        registration = Registration(
            student_id = request.student_id,
            student_name = request.student_name,
            workshop_id = request.workshop_id,
            registration_date = current_datetime,
        )

        try:
            self.registration_repo.save(db, registration)
            self.commit()
            self.refresh(registration)

        except Exception:
            db.rollback()
            raise

        return registration


class WorshopService:

    def __init__(self):
        self.workshop_repo = WorkshopRepository()    

    def list_available(self, db):
        return self.workshop_repo.find_available(db)