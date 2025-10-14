from datetime import datetime
from pydantic import BaseModel

class SeriaResponse(BaseModel):
    id: int
    title: str
    episode_number: int
    video_url: str
    duration: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SerialResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    release_year: int
    age_limit: int
    trailer_url: str | None = None
    img_url: str
    rtg: float
    active: bool
    ganres: list[str] = []
    serias: list[SeriaResponse] = []
    movie_type: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        
class SeriaListResponse(BaseModel):
    serias: list[SeriaResponse]

    class Config:
        from_attributes = True
        
class SerialListResponse(BaseModel):
    movies: list[SerialResponse]

    class Config:
        from_attributes = True