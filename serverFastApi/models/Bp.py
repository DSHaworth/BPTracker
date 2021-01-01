from typing import Optional
from pydantic import BaseModel

class BpDto(BaseModel):
    bpId: Optional[int] = None    
    userId: int
    sys: int
    dia: int
    position: str
    arm: str
    activity: str
    notes: Optional[str] = None
    recordDateTime: str