from sqlalchemy.orm import Session
from . import models, schemas
from ..core.security import get_password_hash
from datetime import datetime

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_form(db: Session, form: schemas.FormCreate, user_id: int):
    try:
        print("Creating form with title:", form.title)
        db_form = models.Form(
            title=form.title,
            description=form.description,
            owner_id=user_id,
            created_at=datetime.utcnow()  # Manually set the created_at timestamp
        )
        db.add(db_form)
        db.commit()
        db.refresh(db_form)
        print("Form created:", db_form)
        return db_form
    except Exception as e:
        print("Error in create_form function:", e)
        db.rollback()  # Rollback the transaction in case of error
        raise



def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
