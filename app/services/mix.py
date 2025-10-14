from ..db.database import LocalSession
from ..models.anime import Anime
from ..models.movie import Movie
from ..models.serial import Serial
from sqlalchemy import or_, and_

def get_news(type: str | None = None):
    db = LocalSession()
    try:
        if type == "anime":
            animes = db.query(Anime).filter_by(active=True).order_by(Anime.created_at.desc()).limit(4).all()
            return [
                {
                    "id": anime.id,
                    "title": anime.title,
                    "img_url": anime.img_url,
                    "release_year": anime.release_year,
                    "age_limit": anime.age_limit,
                    "rtg": anime.rtg,
                    "duration": getattr(anime, 'duration', 0),
                    "movie_type": "anime"
                }
                for anime in animes
            ]
        elif type == "serial":
            serials = db.query(Serial).filter_by(active=True).order_by(Serial.created_at.desc()).limit(4).all()
            return [
                {
                    "id": serial.id,
                    "title": serial.title,
                    "img_url": serial.img_url,
                    "release_year": serial.release_year,
                    "age_limit": serial.age_limit,
                    "rtg": serial.rtg,
                    "duration": getattr(serial, 'duration', 0),
                    "movie_type": "serial"
                }
                for serial in serials
            ]
        elif type == "movie":
            movies = db.query(Movie).filter_by(active=True).order_by(Movie.created_at.desc()).limit(4).all()
            return [
                {
                    "id": movie.id,
                    "title": movie.title,
                    "img_url": movie.img_url,
                    "release_year": movie.release_year,
                    "age_limit": movie.age_limit,
                    "rtg": movie.rtg,
                    "duration": getattr(movie, 'duration', 0),
                    "movie_type": "movie"
                }
                for movie in movies
            ]
        else:
            mixed = []
            
            animes = db.query(Anime).filter_by(active=True).order_by(Anime.created_at.desc()).limit(2).all()
            for anime in animes:
                mixed.append({
                    "id": anime.id,
                    "title": anime.title,
                    "img_url": anime.img_url,
                    "release_year": anime.release_year,
                    "age_limit": anime.age_limit,
                    "rtg": anime.rtg,
                    "duration": getattr(anime, 'duration', 0),
                    "movie_type": "anime",
                    "created_at": anime.created_at
                })
            
            serials = db.query(Serial).filter_by(active=True).order_by(Serial.created_at.desc()).limit(2).all()
            for serial in serials:
                mixed.append({
                    "id": serial.id,
                    "title": serial.title,
                    "img_url": serial.img_url,
                    "release_year": serial.release_year,
                    "age_limit": serial.age_limit,
                    "rtg": serial.rtg,
                    "duration": getattr(serial, 'duration', 0),
                    "movie_type": "serial",
                    "created_at": serial.created_at
                })
            
            movies = db.query(Movie).filter_by(active=True).order_by(Movie.created_at.desc()).limit(4).all()
            for movie in movies:
                mixed.append({
                    "id": movie.id,
                    "title": movie.title,
                    "img_url": movie.img_url,
                    "release_year": movie.release_year,
                    "age_limit": movie.age_limit,
                    "rtg": movie.rtg,
                    "duration": getattr(movie, 'duration', 0),
                    "movie_type": "movie",
                    "created_at": movie.created_at
                })
            
            mixed.sort(key=lambda x: x['created_at'], reverse=True)
            return mixed[:4]
    finally:
        db.close()
        
def get_all(search: str = None, genre: str = None, type: str = None, year: int = None):
    db = LocalSession()
    try:
        mixed = []
        
        def build_filters(model):
            filters = [model.active == True]
            
            if search:
                filters.append(model.title.ilike(f"%{search}%"))
            
            if year:
                filters.append(model.release_year == year)
                
            return and_(*filters)
        
        if type == "anime":
            items = db.query(Anime).filter(build_filters(Anime)).order_by(Anime.created_at.desc()).all()
            for item in items:
                mixed.append({
                    "id": item.id,
                    "title": item.title,
                    "img_url": item.img_url,
                    "release_year": item.release_year,
                    "age_limit": item.age_limit,
                    "rtg": item.rtg,
                    "duration": getattr(item, 'duration', 0),
                    "movie_type": "anime",
                    "created_at": item.created_at
                })
        elif type == "serial":
            items = db.query(Serial).filter(build_filters(Serial)).order_by(Serial.created_at.desc()).all()
            for item in items:
                mixed.append({
                    "id": item.id,
                    "title": item.title,
                    "img_url": item.img_url,
                    "release_year": item.release_year,
                    "age_limit": item.age_limit,
                    "rtg": item.rtg,
                    "duration": getattr(item, 'duration', 0),
                    "movie_type": "serial",
                    "created_at": item.created_at
                })
        elif type == "movie":
            items = db.query(Movie).filter(build_filters(Movie)).order_by(Movie.created_at.desc()).all()
            for item in items:
                mixed.append({
                    "id": item.id,
                    "title": item.title,
                    "img_url": item.img_url,
                    "release_year": item.release_year,
                    "age_limit": item.age_limit,
                    "rtg": item.rtg,
                    "duration": getattr(item, 'duration', 0),
                    "movie_type": "movie",
                    "created_at": item.created_at
                })
        else:
            animes = db.query(Anime).filter(build_filters(Anime)).all()
            serials = db.query(Serial).filter(build_filters(Serial)).all()
            movies = db.query(Movie).filter(build_filters(Movie)).all()
            
            for anime in animes:
                mixed.append({
                    "id": anime.id,
                    "title": anime.title,
                    "img_url": anime.img_url,
                    "release_year": anime.release_year,
                    "age_limit": anime.age_limit,
                    "rtg": anime.rtg,
                    "duration": getattr(anime, 'duration', 0),
                    "movie_type": "anime",
                    "created_at": anime.created_at
                })
            
            for serial in serials:
                mixed.append({
                    "id": serial.id,
                    "title": serial.title,
                    "img_url": serial.img_url,
                    "release_year": serial.release_year,
                    "age_limit": serial.age_limit,
                    "rtg": serial.rtg,
                    "duration": getattr(serial, 'duration', 0),
                    "movie_type": "serial",
                    "created_at": serial.created_at
                })
            
            for movie in movies:
                mixed.append({
                    "id": movie.id,
                    "title": movie.title,
                    "img_url": movie.img_url,
                    "release_year": movie.release_year,
                    "age_limit": movie.age_limit,
                    "rtg": movie.rtg,
                    "duration": getattr(movie, 'duration', 0),
                    "movie_type": "movie",
                    "created_at": movie.created_at
                })
        
        mixed.sort(key=lambda x: x['created_at'], reverse=True)
        return mixed
    finally:
        db.close()