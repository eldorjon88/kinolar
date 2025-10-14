from fastapi.routing import APIRouter
from fastapi import Query
from typing import Optional
from app.services.mix import get_news as service_get_news, get_all as service_get_all

router = APIRouter(
    prefix="/mix",
    tags=["mix"],
)

@router.get("/news")
def get_news(type: Optional[str] = Query(None, description="Type of news to filter by")):
    result = service_get_news(type)
    return {"movies": result}

@router.get("/")
def get_all(
    search: Optional[str] = Query(None, description="Search by title"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    type: Optional[str] = Query(None, description="Filter by type (movie, anime, serial)"),
    year: Optional[int] = Query(None, description="Filter by year")
):
    result = service_get_all(search, genre, type, year)
    return {"movies": result}