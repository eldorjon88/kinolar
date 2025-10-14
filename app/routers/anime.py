from fastapi.routing import APIRouter
from fastapi import Form, UploadFile, File, HTTPException, status, Path

from app.schemas.animes import AnimeResponse, AnimeListResponse
from app.db.database import LocalSession
from app.models.anime import Anime, anime_genres, Seria
from app.models.movie import Genre

from random import randint

router = APIRouter(
    prefix='/anime',
    tags=['anime']
)

@router.get('', response_model=AnimeListResponse)
def get_animes():
    db = LocalSession()
    try:
        animes = db.query(Anime).filter_by(active=True).all()
        for anime in animes:
            # Genres olish
            anime_genres_list = db.query(Genre.name).join(anime_genres, Genre.id == anime_genres.c.genre_id).filter(anime_genres.c.anime_id == anime.id).all()
            anime.ganres = [genre.name for genre in anime_genres_list]
            
            # Serias olish
            anime_serias_list = db.query(Seria).filter(Seria.anime_id == anime.id).all()
            anime.serias = anime_serias_list
                
        return AnimeListResponse(movies=animes)
    finally:
        db.close()

@router.get('/one/{anime_id}', response_model=AnimeResponse)
def get_anime_by_id(
    anime_id: int = Path(..., gt=0)
):
    db = LocalSession()
    try:
        anime = db.query(Anime).filter_by(id=anime_id).first()
        
        if anime:
            # Genres olish
            anime_genres_list = db.query(Genre.name).join(anime_genres, Genre.id == anime_genres.c.genre_id).filter(anime_genres.c.anime_id == anime.id).all()
            anime.ganres = [genre.name for genre in anime_genres_list]
            
            # Serias olish
            anime_serias_list = db.query(Seria).filter(Seria.anime_id == anime.id).all()
            anime.serias = anime_serias_list
                
            return anime
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday Anime mavjud emas.")
    finally:
        db.close()

@router.post('')
def create_anime(
    title: str = Form(min_length=5, max_length=256),
    description: str | None = Form(None),
    release_year: int = Form(2025),
    genres: str = Form(),
    age_limit: int = Form(),
    reyting: float = Form(0.0),
    trailer_url: str = Form(),
    image: UploadFile = File(),
):
    db = LocalSession()
    
    genre_list = [g.strip() for g in genres.split(',')]
    genres_ids = []
    
    for genre in genre_list:
        result = db.query(Genre).filter_by(name=genre).first()
        if result is None:
            new_genre = Genre(name=genre)
            db.add(new_genre)
            db.commit()
            db.refresh(new_genre)
            genres_ids.append(new_genre.id)
        else:
            genres_ids.append(result.id)
    
    random_number = randint(1, 10000000)
    img_path = f'media/images/{random_number}{image.filename}'
    with open(img_path, "wb") as f:
        f.write(image.file.read())
    
    if db.query(Anime).filter_by(title=title).first():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Bunday nomli anime mavjud.")
    
    anime = Anime(
        title=title,
        description=description,
        release_year=release_year,
        age_limit=age_limit,
        img_url=img_path,
        trailer_url=trailer_url,
        rtg=reyting
    )
    db.add(anime)
    db.commit()
    db.refresh(anime)
    

    for genre_id in genres_ids:
        db.execute(anime_genres.insert().values(anime_id=anime.id, genre_id=genre_id))
    db.commit()
    return {"message": "Anime muvaffaqiyatli yaratildi."}

@router.put('/{anime_id}')
def update_anime(
    anime_id: int = Path(..., gt=0),
    title: str = Form(min_length=5, max_length=256),
    description: str | None = Form(None),
    release_year: int = Form(2025),
    genres: str = Form(),
    age_limit: int = Form(),
    reyting: float = Form(0.0),
    trailer_url: str = Form(),
    image: UploadFile | None = File(None),
):
    import os
    
    db = LocalSession()
    anime = db.query(Anime).filter_by(id=anime_id).first()
    
    if not anime:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday anime mavjud emas.")
    
    genre_list = [g.strip() for g in genres.split(',')]
    genres_ids = []
    
    for genre in genre_list:
        result = db.query(Genre).filter_by(name=genre).first()
        if result is None:
            new_genre = Genre(name=genre)
            db.add(new_genre)
            db.commit()
            db.refresh(new_genre)
            genres_ids.append(new_genre.id)
        else:
            genres_ids.append(result.id)
    
    if image and image.filename:
        if anime.img_url and os.path.exists(anime.img_url):
            try:
                os.remove(anime.img_url)
            except:
                pass
        
        random_number = randint(1, 10000000)
        img_path = f'media/images/{random_number}_{image.filename}'
        with open(img_path, "wb") as f:
            f.write(image.file.read())
        anime.img_url = img_path
    
    anime.title = title
    anime.description = description
    anime.release_year = release_year
    anime.age_limit = age_limit
    anime.trailer_url = trailer_url
    anime.rtg = reyting
    
    db.commit()
    
    
    db.execute(anime_genres.delete().where(anime_genres.c.anime_id == anime.id))
    for genre_id in genres_ids:
        db.execute(anime_genres.insert().values(anime_id=anime.id, genre_id=genre_id))
    db.commit()
    
    return {"message": "Anime muvaffaqiyatli yangilandi."}

@router.delete('/{anime_id}')
def delete_anime(
    anime_id: int = Path(gt=0)
):
    db = LocalSession()
    anime = db.query(Anime).filter_by(id=anime_id).first()
 
    if not anime:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday anime mavjud emas.")
    
    db.delete(anime)
    db.commit()
    return {"message": "Anime muvaffaqiyatli o'chirildi."}