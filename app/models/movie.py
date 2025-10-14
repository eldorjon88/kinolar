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


movie_genres = Table(
    'movie_genres',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)

class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    

    movies = relationship("Movie", secondary=movie_genres, back_populates="genres")
    animes = relationship("Anime", secondary="anime_genres", back_populates="genres")
    serials = relationship("Serial", secondary="serial_genres", back_populates="genres")

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    release_year = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)  
    age_limit = Column(Integer, nullable=False)
    video_url = Column(String(512), nullable=False)
    img_url = Column(String(512), nullable=False)
    trailer_url = Column(String(512), nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    rtg = Column(Numeric(2,1), nullable=False)
    movie_type = Column(String(50), nullable=False, default="movie")


    genres = relationship("Genre", secondary=movie_genres, back_populates="movies")

    def __repr__(self):
        return f"Movie(title={self.title}, desc={self.description}, release_year={self.release_year})"
    