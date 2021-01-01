from typing import Optional
from pydantic import BaseModel

class PulseDto(BaseModel):
    pulseId: Optional[int] = None
    recordDateTime: str
    userId: int
    pulse: int
    activity: str
    notes: Optional[str] = None