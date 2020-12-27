from typing import Optional
from pydantic import BaseModel

class UserIn(BaseModel):
    password: str
    email: str
    full_name: Optional[str] = None

class UserOutClean(BaseModel):
    userId: str
    email: str
    firstname: str
    lastname: str
    image: Optional[str] = None
    # dob: Optional[str] = None
    # gender: Optional[str] = None
    