from fastapi.routing import APIRouter
from fastapi import Form, UploadFile, File, HTTPException, status
from fastapi import Path

from app.db.database import LocalSession
from app.models.anime import Anime, anime_genres, Seria
from app.models.movie import Genre


from random import randint

router = APIRouter(
    prefix='/ASerias',
    tags=['Anime Serias']
)

@router.post('/add')
def create_anime_seria(
    title: str = Form(min_length=5, max_length=256),
    duration: int = Form(),
    anime_id: int = Form(),
    seria_number: int = Form(),
    video: UploadFile = File(),
):
    db = LocalSession()
    
    anime = db.query(Anime).filter_by(id=anime_id).first()
    if anime is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday Anime mavjud emas.")
    
    random_num = randint(1, 10000000)
    print(video.filename)
    video_path = f'media/anime_serias/{random_num}{video.filename}'
    with open(video_path, "wb") as f:
        f.write(video.file.read())
    
    new_seria = Seria(
        title=title,
        video_url=video_path,
        seria_number=seria_number,
        duration=duration,
        anime_id=anime_id
    )
    
    db.add(new_seria)
    db.commit()
    db.refresh(new_seria)
    
    return {"message": "Anime Seria muvaffaqiyatli yaratildi.", "seria_id": new_seria.id}

@router.get('/{anime_id}')
def get_anime_with_serias(
    anime_id: int = Path(..., gt=0)
):
    db = LocalSession()
    anime = db.query(Anime).filter_by(id=anime_id).first()
    
    if anime:
        anime_genres_list = db.query(Genre.name).join(anime_genres, Genre.id == anime_genres.c.genre_id).filter(anime_genres.c.anime_id == anime.id).all()
        anime.ganres = [genre.name for genre in anime_genres_list]
        anime_serias_list = db.query(Seria).filter(Seria.anime_id == anime.id).all()
        

        seria_data = []
        for seria in anime_serias_list:
            seria_data.append({
                "id": seria.id,
                "title": seria.title,
                "video_url": seria.video_url,
                "seria_number": seria.seria_number,
                "duration": seria.duration,
                "created_at": seria.created_at,
                "updated_at": seria.updated_at
            })
        
        return {"serias": seria_data}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday Anime mavjud emas.")

@router.put('/update/{seria_id}')
def update_anime_seria(
    seria_id: int = Path(..., gt=0),
    title: str = Form(min_length=5, max_length=256),
    duration: int = Form(),
    seria_number: int = Form(),
    video: UploadFile | None = File(None),
):
    db = LocalSession()
    
    seria = db.query(Seria).filter_by(id=seria_id).first()
    if seria is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday Seria mavjud emas.")
    
    seria.title = title
    seria.duration = duration
    seria.seria_number = seria_number
    
    if video:
        random_num = randint(1, 10000000)
        video_path = f'media/anime_serias/{random_num}{video.filename}'
        with open(video_path, "wb") as f:
            f.write(video.file.read())
        seria.video_url = video_path
    
    db.commit()
    db.refresh(seria)
    
    return {"message": "Anime Seria muvaffaqiyatli yangilandi.", "seria_id": seria.id}

@router.delete('/delete/{seria_id}')
def delete_anime_seria(
    seria_id: int = Path(..., gt=0)
):
    db = LocalSession()
    
    seria = db.query(Seria).filter_by(id=seria_id).first()
    if seria is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday Seria mavjud emas.")
    
    db.delete(seria)
    db.commit()
    
    return {"message": "Anime Seria muvaffaqiyatli o'chirildi."}