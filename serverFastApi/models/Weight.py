from typing import Optional
from pydantic import BaseModel

class WeightDto(BaseModel):
    weightId: Optional[int] = None
    recordDateTime: str
    userId: int
    weight: str
    notes: Optional[str] = None