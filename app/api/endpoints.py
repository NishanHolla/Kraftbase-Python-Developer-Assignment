# app/api/endpoints.py

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi_login import LoginManager
from app.core.config import settings
from ..core import security
from ..db import schemas, models, session, functions
from typing import List
from jose import jwt, JWTError
from datetime import datetime, timedelta

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize LoginManager
SECRET = settings.secret_key
print("Initializing LoginManager with SECRET:", SECRET)  # Debugging print
manager = LoginManager(SECRET, token_url='/auth/login')

# Define and register the user_loader callback
@manager.user_loader
def load_user(email: str):
    print("user_loader called with email:", email)  # Debugging print
    db = session.SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
    finally:
        db.close()
    print("Loaded user:", user)  # Debugging print
    return user

def get_user_with_db(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()

# User Registration Endpoint
@router.post("/auth/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = functions.create_user(db, user)
    return new_user

@router.post("/auth/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Set token expiration to 2 hours
    access_token_expires = timedelta(hours=2)
    access_token = security.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token }


# User Logout Endpoint (example using cookie-based sessions)
@router.post("/auth/logout")
def logout_user(response: Response):
    response.delete_cookie(key="access_token")
    return {"msg": "Successfully logged out"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/forms/create", response_model=schemas.Form)
def create_form(
    form: schemas.FormCreate, 
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        print("Form data:", form)
        print("User details:", user)
        db_form = functions.create_form(db, form, user.id)
        print("Form created:", db_form)
        print("Form created_at:", db_form.created_at)  # Debugging print
        return db_form
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    except Exception as e:
        print("Error creating form:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Delete a Form Endpoint
@router.delete("/forms/delete/{form_id}", response_model=schemas.Form)
def delete_form(form_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        db_form = db.query(models.Form).filter(models.Form.id == form_id, models.Form.owner_id == user.id).first()
        if not db_form:
            raise HTTPException(status_code=404, detail="Form not found or not authorized")

        db.delete(db_form)
        db.commit()
        print("Form deleted:", db_form)  # Debugging print
        return db_form
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    except Exception as e:
        print("Error deleting form:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Get All Forms Endpoint
@router.get("/forms/", response_model=List[schemas.Form])
def get_all_forms(db: Session = Depends(get_db)):
    forms = db.query(models.Form).all()
    return forms

# Get Single Form Endpoint
@router.get("/forms/{form_id}", response_model=schemas.Form)
def get_single_form(form_id: int, db: Session = Depends(get_db)):
    form = db.query(models.Form).filter(models.Form.id == form_id).first()
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    return form

# Submit a Form Endpoint
@router.post("/forms/submit/{form_id}")
def submit_form(form_id: int, submission: schemas.FormSubmissionCreate, db: Session = Depends(get_db)):
    form = db.query(models.Form).filter(models.Form.id == form_id).first()
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    
    db_submission = models.FormSubmission(form_id=form_id, data=submission.responses)
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

# Get Form Submissions Endpoint
@router.get("/forms/submissions/{form_id}", response_model=schemas.PaginatedSubmissions)
def get_form_submissions(form_id: int, page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    submissions = db.query(models.FormSubmission).filter(models.FormSubmission.form_id == form_id).offset(offset).limit(limit).all()
    total_count = db.query(models.FormSubmission).filter(models.FormSubmission.form_id == form_id).count()
    
    return schemas.PaginatedSubmissions(
        total_count=total_count,
        page=page,
        limit=limit,
        submissions=submissions
    )
