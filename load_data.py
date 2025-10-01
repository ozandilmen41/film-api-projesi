import pandas as pd
from sqlalchemy.orm import sessionmaker
from src.database import engine
from src.models import Movie
import logging

# Hataları ve ilerlemeyi görmek için temel bir loglama ayarı
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Veritabanı oturumu oluşturmak için SessionLocal'ı tanımla
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def load_movies_data():
    db = SessionLocal()
    logging.info("Veritabanı oturumu başlatıldı.")
    
    try:
        # ÖNCE: Veritabanında zaten var olan tüm film ID'lerini bir sete yükle.
        existing_ids = {row[0] for row in db.query(Movie.id).all()}
        logging.info(f"Veritabanında {len(existing_ids)} adet mevcut film ID'si bulundu.")
        
        chunksize = 1000
        file_path = 'movies_metadata.csv'
        logging.info(f"'{file_path}' dosyasından veriler okunuyor...")
        
        for chunk in pd.read_csv(file_path, chunksize=chunksize, low_memory=False):
            movies_to_add = []
            
            for _, row in chunk.iterrows():
                try:
                    movie_id = int(row['id'])

                    if movie_id in existing_ids:
                        continue
                    
                    # Gerekli veri dönüşümlerini ve temizliğini yap
                    budget = pd.to_numeric(row.get('budget'), errors='coerce')
                    revenue = pd.to_numeric(row.get('revenue'), errors='coerce')
                    popularity = pd.to_numeric(row.get('popularity'), errors='coerce')
                    release_date = pd.to_datetime(row.get('release_date'), errors='coerce').date() if pd.notna(row.get('release_date')) else None
                    vote_average = pd.to_numeric(row.get('vote_average'), errors='coerce')
                    vote_count = pd.to_numeric(row.get('vote_count'), errors='coerce')

                    # Movie model objesini oluştur
                    movie = Movie(
                        id=movie_id,
                        title=row.get('title'),
                        overview=row.get('overview'),
                        release_date=release_date,
                        
                        # DÜZELTME: NumPy tiplerini standart Python tiplerine çevir
                        budget=float(budget) if pd.notna(budget) else None,
                        revenue=float(revenue) if pd.notna(revenue) else None,
                        popularity=float(popularity) if pd.notna(popularity) else None,
                        vote_average=float(vote_average) if pd.notna(vote_average) else None,
                        vote_count=int(vote_count) if pd.notna(vote_count) else None
                    )
                    movies_to_add.append(movie)
                    existing_ids.add(movie_id)

                except (ValueError, TypeError) as e:
                    logging.warning(f"Satır atlanıyor (ID: {row.get('id')}): {e}")
                    continue
            
            if movies_to_add:
                db.bulk_save_objects(movies_to_add)
                db.commit()
                logging.info(f"{len(movies_to_add)} film başarıyla veritabanına eklendi.")
                
    except Exception as e:
        logging.error(f"Veri yükleme sırasında bir hata oluştu: {e}")
        db.rollback()
    finally:
        db.close()
        logging.info("Veritabanı oturumu kapatıldı.")

if __name__ == "__main__":
    load_movies_data()