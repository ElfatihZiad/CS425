from fastapi import HTTPException
from repositories import WorkshopRepository, RegistrationRepository
from schemas import RegistrationCreate, RegistrationResponse
from datetime import datetime
from models import Registration

class RegistrationService:

    def __init__(self):
        self.registration_repo = RegistrationRepository()
        self.workshop_repo = WorkshopRepository()

    def get_registration(self, db, workshop_id):
        return self.registration_repo.get_registred_student(db, workshop_id)

    def create_registration(self, db, request: RegistrationCreate):

        current_datetime = datetime.now()

        workshop = self.workshop_repo.find_by_id(db, request.workshop_id)
        if workshop is None:
            raise HTTPException(status_code=404, detail="Workshop Not Found")

        # 1. Reject registration when deadline has passed.

        if workshop.deadline < current_datetime:
            raise HTTPException(status_code=409, detail="Registration Deadline Has Passed")

        # 2. Reject Req when Workshop Has Reachead Maximum Capacity

        registration_count = len(self.registration_repo.get_registred_student(db, workshop.id))
        if registration_count >= workshop.capacity:
            raise HTTPException(status_code=409, detail="Workshop Has Reachead Maximum Capacity")

        registration = Registration(
            student_id = request.student_id,
            student_name = request.student_name,
            student_email = request.student_email,
            workshop_id = request.workshop_id,
            registration_date = current_datetime,
        )

        try:
            self.registration_repo.save(db, registration)
            db.commit()
            db.refresh(registration)

        except Exception:
            db.rollback()
            raise

        return registration


class WorshopService:

    def __init__(self):
        self.workshop_repo = WorkshopRepository()    

    def list_available(self, db):
        return self.workshop_repo.find_available(db)

    def find_by_id(self, db, workshop_id):
        workshop = self.workshop_repo.find_by_id(db, workshop_id)
        if workshop is None:
            raise HTTPException(status_code=404, detail="Workshop Not Found")
        return workshop