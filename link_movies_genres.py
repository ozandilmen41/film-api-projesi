import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from src.database import engine, Base
from src.models import Genre, Movie, movie_genre
import logging
import ast

# --- Kurulum ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def parse_genres(genres_str):
    """Güvenli bir şekilde genre string'ini parse eder."""
    try:
        if isinstance(genres_str, str):
            genres = ast.literal_eval(genres_str)
            return [g['id'] for g in genres if isinstance(g, dict) and 'id' in g]
    except (ValueError, SyntaxError, TypeError):
        pass
    return []

def link_movies_to_genres():
    db = SessionLocal()
    logging.info("Veritabanı oturumu başlatıldı.")
    
    try:
        # --- Adım 1: Mevcut Durumu Hafızaya Al ---
        logging.info("Mevcut veriler hafızaya alınıyor...")
        
        # Veritabanındaki tüm mevcut film ID'lerini bir set'e al.
        existing_movie_ids = {row[0] for row in db.query(Movie.id).all()}
        logging.info(f"Veritabanında {len(existing_movie_ids)} film bulundu.")

        # Veritabanındaki tüm mevcut ilişikleri bir set'e al. Bu en önemli optimizasyon.
        existing_relations = {(row[0], row[1]) for row in db.query(movie_genre).all()}
        logging.info(f"Veritabanında {len(existing_relations)} film-tür ilişkisi bulundu.")

        # --- Adım 2: CSV'yi Tek Seferde Oku ve Yeni İlişkileri Hesapla ---
        logging.info("CSV dosyası okunuyor ve yeni ilişkiler hesaplanıyor...")
        
        new_relations_to_add = []
        file_path = 'movies_metadata.csv'
        
        # `usecols` ile sadece ihtiyacımız olan sütunları okuyarak bellekten tasarruf et.
        for chunk in pd.read_csv(file_path, usecols=['id', 'genres'], chunksize=5000, low_memory=False):
            for _, row in chunk.iterrows():
                try:
                    movie_id = int(row['id'])
                    
                    # Eğer film veritabanında yoksa bu satırı atla.
                    if movie_id not in existing_movie_ids:
                        continue
                        
                    genre_ids = parse_genres(row['genres'])
                    for genre_id in genre_ids:
                        relation = (movie_id, genre_id)
                        # Eğer ilişki zaten yoksa, eklenecekler listesine al.
                        if relation not in existing_relations:
                            new_relations_to_add.append({'movie_id': movie_id, 'genre_id': genre_id})
                            # Tekrar eklememek için hemen mevcut ilişkilere de ekle.
                            existing_relations.add(relation)
                except (ValueError, TypeError):
                    continue
            
            logging.info(f"Chunk işlendi. Eklenecek yeni ilişki sayısı: {len(new_relations_to_add)}")

        # --- Adım 3: Yeni İlişkileri Toplu Halde Veritabanına Ekle ---
        if not new_relations_to_add:
            logging.info("Eklenecek yeni bir ilişki bulunamadı. Veritabanı zaten güncel.")
            return

        logging.info(f"Toplam {len(new_relations_to_add)} yeni ilişki veritabanına ekleniyor. Bu işlem biraz sürebilir...")
        
        # SQLAlchemy Core kullanarak en hızlı şekilde toplu ekleme yap.
        # Bu, ORM'den çok daha hızlıdır.
        db.execute(movie_genre.insert(), new_relations_to_add)
        db.commit()
        
        logging.info(f"✅ İşlem tamamlandı! {len(new_relations_to_add)} yeni ilişki başarıyla eklendi.")

    except Exception as e:
        logging.error(f"İşlem sırasında beklenmedik bir hata oluştu: {e}")
        db.rollback()
    finally:
        db.close()
        logging.info("Veritabanı oturumu kapatıldı.")

if __name__ == "__main__":
    # Önce genre'lerin kendilerinin yüklendiğinden emin olalım.
    # Bu script sadece ilişkileri kurar.
    # Eğer `genres` tablosu boşsa, önce `load_genres.py`'nin
    # sadece genre'leri ekleyen versiyonu çalıştırılmalıdır.
    link_movies_to_genres()
