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
        from_attributes = True

class Field(BaseModel):
    field_id: int  # Change to int to match FieldCreate
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

class FormSubmissionCreate(BaseModel):
    responses: List[Dict[str, Union[str, int, bool]]]

class PaginatedSubmissions(BaseModel):
    total_count: int
    page: int
    limit: int
    submissions: List[Dict[str, Union[str, int, bool]]]

    class Config:
        from_attributes = True
