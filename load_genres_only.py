import pandas as pd
from sqlalchemy.orm import sessionmaker
from src.database import engine
from src.models import Genre
import logging
import ast

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def parse_genres_for_loading(genres_str):
    """Sadece genre verilerini parse etmek için kullanılır."""
    try:
        if isinstance(genres_str, str):
            genres = ast.literal_eval(genres_str)
            return [{'id': g['id'], 'name': g['name']} for g in genres if isinstance(g, dict) and 'id' in g and 'name' in g]
    except (ValueError, SyntaxError, TypeError):
        pass
    return []

def load_genres_only():
    db = SessionLocal()
    logging.info("Veritabanı oturumu başlatıldı. Sadece 'genres' tablosu doldurulacak.")
    
    try:
        # --- Adım 1: Mevcut Türleri Hafızaya Al ---
        existing_genre_ids = {row[0] for row in db.query(Genre.id).all()}
        logging.info(f"Veritabanında {len(existing_genre_ids)} adet tür bulundu.")

        # --- Adım 2: CSV'den Yeni ve Benzersiz Türleri Topla ---
        unique_new_genres = {}  # {id: name} formatında
        file_path = 'movies_metadata.csv'
        logging.info(f"'{file_path}' dosyasından yeni türler aranıyor...")

        for chunk in pd.read_csv(file_path, usecols=['genres'], chunksize=5000, low_memory=False):
            for genres_str in chunk['genres']:
                genres = parse_genres_for_loading(genres_str)
                for genre_info in genres:
                    genre_id = int(genre_info['id'])
                    if genre_id not in existing_genre_ids and genre_id not in unique_new_genres:
                        unique_new_genres[genre_id] = genre_info['name']
        
        # --- Adım 3: Yeni Türleri Toplu Halde Ekle ---
        if not unique_new_genres:
            logging.info("Veritabanına eklenecek yeni bir tür bulunamadı. 'genres' tablosu zaten güncel.")
            return

        logging.info(f"Toplam {len(unique_new_genres)} yeni tür bulundu ve veritabanına ekleniyor...")
        
        genres_to_add = [Genre(id=gid, name=gname) for gid, gname in unique_new_genres.items()]
        
        db.bulk_save_objects(genres_to_add)
        db.commit()
        
        logging.info(f"✅ İşlem tamamlandı! {len(genres_to_add)} yeni tür başarıyla 'genres' tablosuna eklendi.")

    except Exception as e:
        logging.error(f"İşlem sırasında beklenmedik bir hata oluştu: {e}")
        db.rollback()
    finally:
        db.close()
        logging.info("Veritabanı oturumu kapatıldı.")

if __name__ == "__main__":
    load_genres_only()
