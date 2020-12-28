from typing import Optional
from pydantic import BaseModel

class UserLogon(BaseModel):
    password: str
    email: str
    userId: int

class UserCreateDto(BaseModel):
    email: str
    firstname: str
    lastname: str
    gender: str
    dob: str
    password: str
    confirmPassword: str
    image: Optional[str] = None

class UserOutClean(BaseModel):
    userId: int
    email: str
    firstname: str
    lastname: str
    image: Optional[str] = None
    # dob: Optional[str] = None
    # gender: Optional[str] = None
    