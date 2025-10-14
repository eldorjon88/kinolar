from ..db.database import LocalSession
from app.models.serial import Serial, serial_genres, SerialEpisode
from app.models.movie import Genre

class SerialService:
    @staticmethod
    def get_serials():
        db = LocalSession()
        try:
            serials = db.query(Serial).filter_by(active=True).all()
            for serial in serials:
                # Genres olish
                serial_genres_list = db.query(Genre.name).join(serial_genres, Genre.id == serial_genres.c.genre_id).filter(serial_genres.c.serial_id == serial.id).all()
                serial.ganres = [genre.name for genre in serial_genres_list]
                
                # Serialar olish
                try:
                    serial_serias_list = db.query(SerialEpisode).filter(SerialEpisode.serial_id == serial.id).all()
                    serial.serias = serial_serias_list
                except Exception as e:
                    print(f"Episodes yuklanmadi: {e}")
                    serial.serias = []
                    
            return serials
        finally:
            db.close()
            
    @staticmethod
    def get_top_serials():
        db = LocalSession()
        try:
            serials = db.query(Serial).filter_by(active=True).order_by(Serial.rtg.desc()).limit(4).all()
            for serial in serials:
                # Genres olish
                serial_genres_list = db.query(Genre.name).join(serial_genres, Genre.id == serial_genres.c.genre_id).filter(serial_genres.c.serial_id == serial.id).all()
                serial.ganres = [genre.name for genre in serial_genres_list]
                
                # Serialar olish
                try:
                    serial_serias_list = db.query(SerialEpisode).filter(SerialEpisode.serial_id == serial.id).all()
                    serial.serias = serial_serias_list
                except Exception as e:
                    print(f"Episodes yuklanmadi: {e}")
                    serial.serias = []
                    
            return serials
        finally:
            db.close()