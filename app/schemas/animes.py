from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class SeriaResponse(BaseModel):
    id: int
    title: str
    seria_number: int
    video_url: str
    duration: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AnimeResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    release_year: int
    age_limit: int
    trailer_url: Optional[str] = None
    img_url: str
    rtg: float = 0.0
    ganres: List[str] = []
    serias: List[SeriaResponse] = []

    class Config:
        from_attributes = True
        
class AnimeListResponse(BaseModel):
    movies: List[AnimeResponse]

    class Config:
        from_attributes = True