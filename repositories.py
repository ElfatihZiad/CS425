
from models import Workshop, Registration

class WorkshopRepository:

    def find_by_id(self, db, workshop_id):
        return(
            db.query(Workshop)
            .filter(Workshop.id == workshop_id)
            .first()
        )

    def find_available(self, db):
        return(
            db.query(Workshop)
            .all()
        )

class RegistrationRepository:

    def save(self, db, reg: Registration):

        db.add(reg)
        return reg

    def get_registred_student(self, db, workshop_id):
        return(
            db.query(Registration)
            .filter(Registration.workshop_id == workshop_id)
            .all()
        )
