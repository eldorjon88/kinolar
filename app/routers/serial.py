from fastapi.routing import APIRouter
from fastapi import UploadFile, File, HTTPException, status, Path, Form

from app.schemas.serials import SerialResponse, SerialListResponse
from app.db.database import LocalSession
from app.models.serial import Serial, serial_genres, SerialEpisode
from app.models.movie import Genre
from app.services.serial import SerialService

from random import randint

router = APIRouter(
    prefix='/serial',
    tags=['serial']
)

@router.get('', response_model=SerialListResponse)
async def get_serial(
    top: int | None = None
):
    if top == None:
        serials = SerialService.get_serials()
    else:
        serials = SerialService.get_top_serials()
    return SerialListResponse(movies=serials)

@router.get('/one/{serial_id}', response_model=SerialResponse)
async def get_serial_by_id(
    serial_id: int = Path(..., gt=0)
):
    db = LocalSession()
    try:
        serial = db.query(Serial).filter_by(id=serial_id).first()
        
        if serial:
            # Genres olish
            serial_genres_list = db.query(Genre.name).join(serial_genres, Genre.id == serial_genres.c.genre_id).filter(serial_genres.c.serial_id == serial.id).all()
            serial.ganres = [genre.name for genre in serial_genres_list]
            
            # Episodes olish
            try:
                serial_serias_list = db.query(SerialEpisode).filter(SerialEpisode.serial_id == serial.id).all()
                serial.serias = serial_serias_list
            except Exception as e:
                print(f"Episodes yuklanmadi: {e}")
                serial.serias = []
                
            return serial
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday Serial mavjud emas.")
    finally:
        db.close()

@router.post('')
def create_serial(
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
    
    try:
        if not image or not image.filename:
            raise HTTPException(status_code=400, detail="Rasm fayli majburiy")
        
        if db.query(Serial).filter_by(title=title).first():
            raise HTTPException(status_code=400, detail="Bunday nomli serial mavjud")
        
        genre_list = [g.strip() for g in genres.split(',') if g.strip()]
        genres_ids = []
        
        for genre in genre_list:
            genre_obj = db.query(Genre).filter_by(name=genre).first()
            if not genre_obj:
                new_genre = Genre(name=genre)
                db.add(new_genre)
                db.commit()
                db.refresh(new_genre)
                genres_ids.append(new_genre.id)
            else:
                genres_ids.append(genre_obj.id)
        
        img_filename = f"{randint(100000, 999999)}_{image.filename}"
        img_path = f"media/images/{img_filename}"
        
        import os
        os.makedirs("media/images", exist_ok=True)
        
        with open(img_path, "wb") as img_file:
            img_file.write(image.file.read())
        
        new_serial = Serial(
            title=title,
            description=description,
            release_year=release_year,
            age_limit=age_limit,
            rtg=reyting,
            trailer_url=trailer_url,
            img_url=f"media/images/{img_filename}",
            movie_type="serial"
        )
        
        db.add(new_serial)
        db.commit()
        db.refresh(new_serial)
        
        for genre_id in genres_ids:
            stmt = serial_genres.insert().values(serial_id=new_serial.id, genre_id=genre_id)
            db.execute(stmt)
        
        db.commit()
        return {"message": "Yangi serial muvaffaqiyatli qo'shildi.", "serial_id": new_serial.id}
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Server xatosi: {str(e)}")
    finally:
        db.close()

@router.put('/{serial_id}')
def update_serial(
    serial_id: int = Path(..., gt=0),
    title: str = Form(min_length=5, max_length=256),
    description: str | None = Form(None),
    release_year: int = Form(2025),
    genres: str = Form(),
    age_limit: int = Form(),
    reyting: float = Form(0.0),
    trailer_url: str = Form(),
    image: UploadFile | None = File(None),
):
    db = LocalSession()
    
    serial = db.query(Serial).filter_by(id=serial_id).first()
    if not serial:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday serial mavjud emas.")
    
    genre_list = [g.strip() for g in genres.split(',') if g.strip()]
    genres_ids = []
    
    for genre in genre_list:
        genre_obj = db.query(Genre).filter_by(name=genre).first()
        if not genre_obj:
            new_genre = Genre(name=genre)
            db.add(new_genre)
            db.commit()
            db.refresh(new_genre)
            genres_ids.append(new_genre.id)
        else:
            genres_ids.append(genre_obj.id)
    
    if image and image.filename:
        img_filename = f"{randint(100000, 999999)}_{image.filename}"
        img_path = f"media/images/{img_filename}"
        
        import os
        os.makedirs("media/images", exist_ok=True)
        
        with open(img_path, "wb") as img_file:
            img_file.write(image.file.read())
        
        serial.img_url = f"media/images/{img_filename}"
    
    serial.title = title
    serial.description = description
    serial.release_year = release_year
    serial.age_limit = age_limit
    serial.rtg = reyting
    serial.trailer_url = trailer_url
    
    db.commit()
    
    db.execute(serial_genres.delete().where(serial_genres.c.serial_id == serial.id))
    
    for genre_id in genres_ids:
        stmt = serial_genres.insert().values(serial_id=serial.id, genre_id=genre_id)
        db.execute(stmt)
    
    db.commit()
    db.close()
    
    return {"message": "Serial muvaffaqiyatli yangilandi."}

@router.delete('/{serial_id}')
def delete_serial(
    serial_id: int = Path(..., gt=0)
):
    db = LocalSession()
    serial = db.query(Serial).filter_by(id=serial_id).first()
    
    if not serial:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday serial mavjud emas.")
    
    db.delete(serial)
    db.commit()
    db.close()
    
    return {"message": "Serial muvaffaqiyatli o'chirildi."}