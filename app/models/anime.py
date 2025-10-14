from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Boolean,
    DateTime,
    Numeric,
    Table
)
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime


anime_genres = Table(
    'anime_genres',
    Base.metadata,
    Column('anime_id', Integer, ForeignKey('animes.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)

class Anime(Base):
    __tablename__ = 'animes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    release_year = Column(Integer, nullable=False)
    age_limit = Column(Integer, nullable=False)
    trailer_url = Column(String(512), nullable=True)
    img_url = Column(String(512), nullable=False)
    rtg = Column(Numeric(3, 1), default=0)
    active = Column(Boolean, default=True)
    movie_type = Column(String(50), default="anime")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


    genres = relationship("Genre", secondary=anime_genres, back_populates="animes")
    serias = relationship("Seria", back_populates="anime")

class Seria(Base):
    __tablename__ = 'a_serias'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    seria_number = Column(Integer, nullable=False)
    video_url = Column(String(512), nullable=False)
    duration = Column(Integer, nullable=False)
    anime_id = Column(Integer, ForeignKey('animes.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    anime = relationship("Anime", back_populates="serias")