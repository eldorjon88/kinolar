from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .db.database import Base, engine
from .models.movie import *
from .models.anime import *
from .models.serial import *
from app.routers import (
    movies_router,
    ganres_router,
    animes_router,
    anime_serial_router,
    serial_router,
    serial_serial_router,
    mix_router
)

app = FastAPI(title="Uzmovie API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media", StaticFiles(directory="media"), name="media")

Base.metadata.create_all(engine)

app.include_router(movies_router)
app.include_router(ganres_router)
app.include_router(animes_router)
app.include_router(anime_serial_router)
app.include_router(serial_router)
app.include_router(serial_serial_router)
app.include_router(mix_router)