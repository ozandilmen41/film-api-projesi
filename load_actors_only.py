import pandas as pd
import ast
import logging
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine
from src.models import Actor, Base

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_actors():
    """
    credits.csv dosyasındaki 'cast' sütununu okur,
    her bir aktörü ayıklar ve veritabanındaki 'actors' tablosuna kaydeder.
    Mevcut aktörleri tekrar eklemez.
    """
    # Veritabanı tablolarını oluştur (eğer yoksa)
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    try:
        # Veritabanındaki mevcut aktör isimlerini bir sete alıyoruz
        existing_actors = {actor.name for actor in db.query(Actor.name).all()}
        logging.info(f"Veritabanında {len(existing_actors)} adet mevcut aktör bulundu.")
        
        # CSV dosyasını chunk'lar halinde oku
        chunk_size = 1000
        all_actor_names = set()

        logging.info("'credits.csv' dosyasından aktörler okunuyor...")
        # low_memory=False, büyük dosyalarda karışık veri tiplerinden kaynaklanan sorunları önleyebilir.
        for chunk in pd.read_csv('credits.csv', chunksize=chunk_size, iterator=True, low_memory=False):
            # 'cast' sütunu chunk'ta var mı diye kontrol et
            if 'cast' not in chunk.columns:
                logging.warning("Bu chunk'ta 'cast' sütunu bulunamadı. Atlanıyor.")
                continue

            # 'cast' sütunundaki verileri işle
            for cast_str in chunk['cast'].dropna(): # .dropna() ile boş değerleri atla
                try:
                    # String halindeki listeyi Python listesine çevir
                    cast_list = ast.literal_eval(cast_str)
                    # Her bir aktörün ismini sete ekle
                    for actor_info in cast_list:
                        if isinstance(actor_info, dict) and 'name' in actor_info:
                            all_actor_names.add(actor_info['name'])
                except (ValueError, SyntaxError):
                    # Hatalı formatta olan verileri atla
                    logging.warning(f"Hatalı formatlı 'cast' verisi atlanıyor: {cast_str[:100]}")
                    continue
        
        logging.info(f"CSV dosyasından toplam {len(all_actor_names)} benzersiz aktör ismi okundu.")

        # Veritabanında olmayan yeni aktörleri bul
        new_actors_to_add = all_actor_names - existing_actors
        logging.info(f"Veritabanına eklenecek {len(new_actors_to_add)} yeni aktör bulundu.")

        if not new_actors_to_add:
            logging.info("Veritabanına eklenecek yeni aktör bulunmuyor.")
            return

        # Yeni aktörleri veritabanına ekle
        new_actor_objects = [Actor(name=name) for name in new_actors_to_add]
        
        logging.info("Yeni aktörler veritabanına ekleniyor...")
        db.bulk_save_objects(new_actor_objects)
        db.commit()
        logging.info(f"✅ {len(new_actor_objects)} yeni aktör başarıyla veritabanına eklendi.")

    except Exception as e:
        logging.error(f"Bir hata oluştu: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_actors()
