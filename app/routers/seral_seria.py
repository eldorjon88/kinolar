from fastapi.routing import APIRouter
from fastapi import UploadFile, File, HTTPException, status, Path, Form

from app.schemas.serials import SerialResponse, SerialListResponse
from app.db.database import LocalSession
from app.models.serial import Serial, serial_genres, SerialEpisode
from app.models.movie import Genre

from random import randint

router = APIRouter(
    prefix='/SSerias',
    tags=['Serial Serias']
)

@router.post('/add')
def create_serial_seria(
    title: str = Form(min_length=5, max_length=256),
    episode_number: int = Form(),
    duration: int = Form(),
    serial_id: int = Form(),
    video: UploadFile = File(),
):
    db = LocalSession()
    
    serial = db.query(Serial).filter_by(id=serial_id).first()
    if serial is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday Serial mavjud emas.")
    
    if not video or not video.filename:
        raise HTTPException(status_code=400, detail="Video fayli majburiy")
    
    random_num = randint(1, 10000000)
    
    import os
    os.makedirs("media/serial_serias", exist_ok=True)
    
    video_path = f'media/serial_serias/{random_num}_{video.filename}'
    
    try:
        with open(video_path, "wb") as f:
            f.write(video.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video saqlashda xatolik: {str(e)}")
    
    new_seria = SerialEpisode(
        title=title,
        episode_number=episode_number,
        video_url=video_path,
        duration=duration,
        serial_id=serial_id
    )
    
    db.add(new_seria)
    db.commit()
    db.refresh(new_seria)
    db.close()
    
    return {"message": "Serial Seria muvaffaqiyatli yaratildi.", "seria_id": new_seria.id}

@router.get('/{serial_id}')
def get_serial_with_serias(
    serial_id: int = Path(..., gt=0)
):
    db = LocalSession()
    serial = db.query(Serial).filter_by(id=serial_id).first()
    
    if serial:
        serial_genres_list = db.query(Genre.name).join(serial_genres, Genre.id == serial_genres.c.genre_id).filter(serial_genres.c.serial_id == serial.id).all()
        serial.ganres = [genre.name for genre in serial_genres_list]
        serial_serias_list = db.query(SerialEpisode).filter(SerialEpisode.serial_id == serial.id).all()
        serial.serias = serial_serias_list
        return serial
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday Serial mavjud emas.")

@router.put('/update/{seria_id}')
def update_serial_seria(
    seria_id: int = Path(..., gt=0),
    title: str = Form(min_length=5, max_length=256),
    episode_number: int = Form(),
    duration: int = Form(),
    video: UploadFile | None = File(None),
):
    db = LocalSession()
    
    seria = db.query(SerialEpisode).filter_by(id=seria_id).first()
    if seria is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday Serial Seria mavjud emas.")
    
    if video:
        random_num = randint(1, 10000000)
        video_path = f'media/serial_serias/{random_num}{video.filename}'
        with open(video_path, "wb") as f:
            f.write(video.file.read())
        seria.video_url = video_path
    
    seria.title = title
    seria.episode_number = episode_number
    seria.duration = duration
    
    db.commit()
    db.refresh(seria)
    
    return {"message": "Serial Seria muvaffaqiyatli yangilandi.", "seria_id": seria.id}

@router.delete('/delete/{seria_id}')
def delete_serial_seria(
    seria_id: int = Path(..., gt=0)
):
    db = LocalSession()
    
    seria = db.query(SerialEpisode).filter_by(id=seria_id).first()
    if seria is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday Serial Seria mavjud emas.")
    
    db.delete(seria)
    db.commit()
    
    return {"message": "Serial Seria muvaffaqiyatli o'chirildi."}

