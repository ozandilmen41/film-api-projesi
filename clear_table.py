from src.database import SessionLocal, engine, Base
from src.models import Movie, Genre
import logging

logging.basicConfig(level=logging.INFO)

def clear_tables():
    db = SessionLocal()
    try:
        logging.info("Tüm tablolar siliniyor...")
        # Tüm tabloları sil
        Base.metadata.drop_all(bind=engine)
        logging.info("✅ Tüm tablolar başarıyla silindi.")
        
        # Tabloları yeniden oluştur
        logging.info("Tablolar yeniden oluşturuluyor...")
        Base.metadata.create_all(bind=engine)
        logging.info("✅ Tablolar başarıyla yeniden oluşturuldu.")
        
    except Exception as e:
        logging.error(f"İşlem sırasında hata oluştu: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clear_tables()