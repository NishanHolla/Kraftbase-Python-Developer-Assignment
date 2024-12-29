from sqlalchemy.orm import Session
from . import models, schemas
from ..core.security import get_password_hash

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
    db_form = models.Form(
        title=form.title,
        description=form.description,
        owner_id=user_id
    )
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return db_form

def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
