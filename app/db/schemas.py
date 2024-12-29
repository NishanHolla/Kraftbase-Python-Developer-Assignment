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
    field_id: str
    type: str
    label: str
    required: bool

class FormBase(BaseModel):
    title: str
    description: str

class FormCreate(FormBase):
    fields: List[Field]

class Form(FormBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
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
