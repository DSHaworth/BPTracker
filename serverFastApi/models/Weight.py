from typing import Optional
from pydantic import BaseModel

class WeightDto(BaseModel):
    weightId: Optional[int] = None    
    userId: int
    weight: str
    notes: Optional[str] = None
    recordDateTime: str