from datetime import datetime
from pydantic import BaseModel

class MovieResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    release_year: int
    duration: int
    age_limit: int
    video_url: str
    img_url: str
    trailer_url: str | None = None
    active: bool
    rtg: float
    movie_type: str
    ganres: list[str] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MovieListResponse(BaseModel):
    movies: list[MovieResponse]

    class Config:
        from_attributes = True