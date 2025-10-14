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

serial_genres = Table(
    'serial_genres',
    Base.metadata,
    Column('serial_id', Integer, ForeignKey('s_serials.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)

class Serial(Base):
    __tablename__ = 's_serials'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    release_year = Column(Integer, nullable=False)
    age_limit = Column(Integer, nullable=False)
    trailer_url = Column(String(512), nullable=True)
    img_url = Column(String(512), nullable=False)
    rtg = Column(Numeric(3, 1), default=0)
    active = Column(Boolean, default=True)
    movie_type = Column(String(50), default="serial")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    genres = relationship("Genre", secondary=serial_genres, back_populates="serials")
    episodes = relationship("SerialEpisode", back_populates="serial", cascade="all, delete-orphan")

class SerialEpisode(Base):
    __tablename__ = 'serial_episodes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    episode_number = Column(Integer, nullable=False)
    video_url = Column(String(512), nullable=False)
    duration = Column(Integer, nullable=False)
    serial_id = Column(Integer, ForeignKey('s_serials.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    serial = relationship("Serial", back_populates="episodes")





    