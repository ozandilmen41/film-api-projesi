from src.database import SessionLocal
from src.models import Movie
import logging

logging.basicConfig(level=logging.INFO)

def clear_movies_table():
    db = SessionLocal()
    try:
        logging.info("'movies' tablosundaki tüm veriler siliniyor...")
        num_rows_deleted = db.query(Movie).delete()
        db.commit()
        logging.info(f"✅ Başarılı! {num_rows_deleted} satır silindi.")
    except Exception as e:
        logging.error(f"Tablo temizlenirken hata oluştu: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clear_movies_table()