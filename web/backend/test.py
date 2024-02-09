from sqlalchemy.orm import Session
from sqlalchemy import func

import models, schemas, crud

def get_school(db: Session, school_id: int):
    return db.query(models.School).filter(models.School.id == school_id).first()

#test query school by name