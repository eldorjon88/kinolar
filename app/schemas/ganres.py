from pydantic import BaseModel
from typing import List

class Ganre(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True

class GanreListResponse(BaseModel):
    ganres: List[Ganre]
    
    class Config:
        from_attributes = True