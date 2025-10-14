from fastapi.routing import APIRouter
from fastapi import Form, UploadFile, File, HTTPException, status
from fastapi import Path
from app.schemas.movies import MovieListResponse, MovieResponse
from app.db.database import LocalSession
from app.models.movie import Movie, Genre, movie_genres
from random import randint

router = APIRouter(
    prefix='/movies',
    tags=['movies']
)

@router.get('/', response_model=MovieListResponse)
async def get_movies(
    top: int | None = None,
):
    if top is not None and top <= 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Musbati son kiriting.")
    elif top is not None:
        db = LocalSession()
        movies = db.query(Movie).filter_by(active=True).order_by(Movie.rtg.desc()).limit(top).all()
        movies_list = []
        for movie in movies:
            movie_genres_list = db.query(Genre.name).join(movie_genres, Genre.id == movie_genres.c.genre_id).filter(movie_genres.c.movie_id == movie.id).all()
            movie_dict = {
                "id": movie.id,
                "title": movie.title,
                "description": movie.description,
                "release_year": movie.release_year,
                "duration": movie.duration,
                "age_limit": movie.age_limit,
                "video_url": movie.video_url,
                "img_url": movie.img_url,
                "trailer_url": movie.trailer_url,
                "active": movie.active,
                "rtg": movie.rtg,
                "movie_type": movie.movie_type,
                "ganres": [genre.name for genre in movie_genres_list],
                "created_at": movie.created_at,
                "updated_at": movie.updated_at
            }
            movies_list.append(MovieResponse(**movie_dict))
        return MovieListResponse(movies=movies_list)
    
    db = LocalSession()
    movies = db.query(Movie).filter_by(active=True).all()
    movies_list = []
    for movie in movies:
        movie_genres_list = db.query(Genre.name).join(movie_genres, Genre.id == movie_genres.c.genre_id).filter(movie_genres.c.movie_id == movie.id).all()
        movie_dict = {
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "release_year": movie.release_year,
            "duration": movie.duration,
            "age_limit": movie.age_limit,
            "video_url": movie.video_url,
            "img_url": movie.img_url,
            "trailer_url": movie.trailer_url,
            "active": movie.active,
            "rtg": movie.rtg,
            "movie_type": movie.movie_type,
            "ganres": [genre.name for genre in movie_genres_list],
            "created_at": movie.created_at,
            "updated_at": movie.updated_at
        }
        movies_list.append(MovieResponse(**movie_dict))
    return MovieListResponse(movies=movies_list)

@router.get('', response_model=MovieListResponse)  
def get_movies_no_slash(top: int | None = None):
    return get_movies(top)

@router.get('/one/{movie_id}', response_model=MovieResponse)
async def get_movie_by_id(
    movie_id: int = Path(..., gt=0)
):
    db = LocalSession()
    movie = db.query(Movie).filter_by(id=movie_id).first()
    
    if movie:
        movie_genres_list = db.query(Genre.name).join(movie_genres, Genre.id == movie_genres.c.genre_id).filter(movie_genres.c.movie_id == movie.id).all()
        movie_dict = {
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "release_year": movie.release_year,
            "duration": movie.duration,
            "age_limit": movie.age_limit,
            "video_url": movie.video_url,
            "img_url": movie.img_url,
            "trailer_url": movie.trailer_url,
            "active": movie.active,
            "rtg": movie.rtg,
            "movie_type": movie.movie_type,
            "ganres": [genre.name for genre in movie_genres_list],
            "created_at": movie.created_at,
            "updated_at": movie.updated_at
        }
        return MovieResponse(**movie_dict)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday Movie mavjud emas.")

@router.get('/lastMovies', response_model=MovieListResponse)
async def get_last_movies():
    db = LocalSession()
    movies = db.query(Movie).filter_by(active=True).order_by(Movie.created_at.desc()).limit(4).all()
    movies_list = []
    for movie in movies:
        movie_genres_list = db.query(Genre.name).join(movie_genres, Genre.id == movie_genres.c.genre_id).filter(movie_genres.c.movie_id == movie.id).all()
        movie_dict = {
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "release_year": movie.release_year,
            "duration": movie.duration,
            "age_limit": movie.age_limit,
            "video_url": movie.video_url,
            "img_url": movie.img_url,
            "trailer_url": movie.trailer_url,
            "active": movie.active,
            "rtg": movie.rtg,
            "movie_type": movie.movie_type,
            "ganres": [genre.name for genre in movie_genres_list],
            "created_at": movie.created_at,
            "updated_at": movie.updated_at
        }
        movies_list.append(MovieResponse(**movie_dict))
    return MovieListResponse(movies=movies_list)

@router.post('')
def create_movie(
    title: str = Form(min_length=5, max_length=256),
    description: str | None = Form(None),
    release_year: int = Form(2025),
    genres: str = Form(),
    duration: int = Form(),
    age_limit: int = Form(),
    reyting: float = Form(0.0),
    trailer_url: str = Form(),
    video: UploadFile = File(),
    image: UploadFile = File(),
):
    db = LocalSession()

    genre_list = [g.strip() for g in genres.split(',')]
    genres_ids = []
    
    for genre in genre_list:
        result = db.query(Genre).filter_by(name=genre).first()
        if result is None:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=f"{genre} bunday janr mavjud emas.")
        genres_ids.append(result.id)

    random_num = randint(1, 10000000)

    video_path = f'media/movies/{random_num}{video.filename}'
    with open(video_path, "wb") as f:
        f.write(video.file.read())

    img_path = f'media/images/{random_num}{image.filename}'
    with open(img_path, "wb") as f:
        f.write(image.file.read())

    if db.query(Movie).filter_by(title=title).first():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=f"{title} bunday kino mavjud.")

    movie = Movie(
        title=title,
        description=description,
        release_year=release_year,
        duration=duration,
        age_limit=age_limit,
        trailer_url=trailer_url,
        video_url=video_path,
        img_url=img_path,
        rtg=reyting
    )

    db.add(movie)
    db.commit()
    db.refresh(movie)

    for genre_id in genres_ids:
        db.execute(movie_genres.insert().values(movie_id=movie.id, genre_id=genre_id))
    
    db.commit()
    return {"message": "Kino muvaffaqiyatli qo'shildi"}

@router.put('/{movie_id}')
def update_movie(
    movie_id: int = Path(..., gt=0),
    title: str = Form(min_length=5, max_length=256),
    description: str | None = Form(None),
    release_year: int = Form(2025),
    genres: str = Form(),
    duration: int = Form(),
    age_limit: int = Form(),
    reyting: float = Form(0.0),
    trailer_url: str = Form(),
    movie_type: str = Form('movie'),
    video: UploadFile = File(None),
    image: UploadFile = File(None),
):
    db = LocalSession()
    
    movie = db.query(Movie).filter_by(id=movie_id).first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie topilmadi")
    
    genre_list = [g.strip() for g in genres.split(',')]
    genres_ids = []
    
    for genre in genre_list:
        result = db.query(Genre).filter_by(name=genre).first()
        if result is None:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=f"{genre} bunday janr mavjud emas.")
        genres_ids.append(result.id)

    if video and video.filename:
        random_num = randint(1, 10000000)
        video_path = f'media/movies/{random_num}{video.filename}'
        with open(video_path, "wb") as f:
            f.write(video.file.read())
        movie.video_url = video_path

    if image and image.filename:
        random_num = randint(1, 10000000)
        img_path = f'media/images/{random_num}{image.filename}'
        with open(img_path, "wb") as f:
            f.write(image.file.read())
        movie.img_url = img_path

    movie.title = title
    movie.description = description
    movie.release_year = release_year
    movie.duration = duration
    movie.age_limit = age_limit
    movie.trailer_url = trailer_url
    movie.rtg = reyting
    movie.movie_type = movie_type


    db.execute(movie_genres.delete().where(movie_genres.c.movie_id == movie_id))
    

    for genre_id in genres_ids:
        db.execute(movie_genres.insert().values(movie_id=movie_id, genre_id=genre_id))
    
    db.commit()
    return {"message": "Movie muvaffaqiyatli yangilandi"}

@router.delete('/{movie_id}')
def delete_movie(movie_id: int = Path(..., gt=0)):
    db = LocalSession()
    
    movie = db.query(Movie).filter_by(id=movie_id).first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie topilmadi")
    

    db.execute(movie_genres.delete().where(movie_genres.c.movie_id == movie_id))
    

    db.delete(movie)
    db.commit()
    
    return {"message": "Movie muvaffaqiyatli o'chirildi"}