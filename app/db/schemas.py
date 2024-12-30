# app/db/schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Dict, Union

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    name: str

class User(UserBase):
    id: int
    name: str

    class Config:
        orm_mode = True
        from_attributes = True

class Field(BaseModel):
    field_id: int
    type: str
    label: str
    required: bool

class FormBase(BaseModel):
    title: str
    description: str

class FieldCreate(BaseModel):
    field_id: int
    field_type: str
    label: str
    type: str
    required: bool

class FormCreate(FormBase):
    fields: List[FieldCreate]

class Form(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class FormSubmissionBase(BaseModel):
    form_id: int
    data: List[Dict[str, Union[str, int, bool]]]  # Change to List of Dicts

class FormSubmissionCreate(BaseModel):
    responses: List[Dict[str, Union[str, int, bool]]]

class FormSubmission(FormSubmissionBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

class PaginatedSubmissions(BaseModel):
    total_count: int
    page: int
    limit: int
    submissions: List[FormSubmission]

    class Config:
        orm_mode = True
        from_attributes = True
