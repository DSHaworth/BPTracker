from typing import Optional
from pydantic import BaseModel

class PulseDto(BaseModel):
    pulseId: Optional[int] = None    
    userId: int
    pulse: int
    activity: str
    notes: Optional[str] = None
    recordDateTime: str