import pandas as pd
import ast
import logging
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from src.database import SessionLocal, engine
from src.models import Movie, Actor, movie_actor

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def link_movies_actors():
    """
    credits.csv dosyasını okur, film ID'leri ile aktör isimlerini eşleştirir
    ve 'movie_actors' ilişki tablosunu toplu olarak günceller.
    Bu betik, veritabanında zaten var olan ilişkileri tekrar eklemez.
    """
    db: Session = SessionLocal()
    
    try:
        # 1. Veritabanındaki mevcut verileri hafızaya yükle
        logging.info("Veritabanındaki mevcut veriler hafızaya alınıyor...")
        
        # Mevcut tüm film ID'lerini bir sete al
        movie_ids_db = {row[0] for row in db.query(Movie.id).all()}
        logging.info(f"{len(movie_ids_db)} adet film ID'si hafızaya alındı.")

        # Mevcut tüm aktör isimlerini ve ID'lerini bir sözlüğe al
        actor_map = {actor.name: actor.id for actor in db.query(Actor.id, Actor.name).all()}
        logging.info(f"{len(actor_map)} adet aktör ID'si ve ismi hafızaya alındı.")

        # Mevcut film-aktör ilişkilerini bir sete al (tuple olarak)
        existing_relations = {
            (relation.movie_id, relation.actor_id) 
            for relation in db.execute(text('SELECT movie_id, actor_id FROM movie_actors')).fetchall()
        }
        logging.info(f"{len(existing_relations)} adet mevcut film-aktör ilişkisi hafızaya alındı.")

        # 2. CSV dosyasını işle ve yeni ilişkileri bul
        chunk_size = 1000
        new_relations_to_add = set()
        
        logging.info("'credits.csv' dosyası işleniyor...")
        for chunk in pd.read_csv('credits.csv', chunksize=chunk_size, iterator=True, low_memory=False):
            
            # 'id' (movie_id) ve 'cast' sütunlarını işle
            for index, row in chunk.iterrows():
                try:
                    movie_id_str = row['id']
                    cast_str = row['cast']
                    
                    # Film ID'sini integer'a çevir, hatalıysa atla
                    try:
                        movie_id = int(movie_id_str)
                    except (ValueError, TypeError):
                        continue

                    # Eğer film veritabanında yoksa bu satırı atla
                    if movie_id not in movie_ids_db:
                        continue

                    # Cast string'ini Python listesine çevir
                    cast_list = ast.literal_eval(cast_str)
                    
                    for actor_info in cast_list:
                        if isinstance(actor_info, dict) and 'name' in actor_info:
                            actor_name = actor_info['name']
                            
                            # Aktör veritabanında varsa ID'sini al
                            if actor_name in actor_map:
                                actor_id = actor_map[actor_name]
                                relation = (movie_id, actor_id)
                                
                                # Eğer bu ilişki daha önce eklenmediyse yeni ilişki setine ekle
                                if relation not in existing_relations:
                                    new_relations_to_add.add(relation)

                except (ValueError, SyntaxError, KeyError):
                    continue
        
        logging.info(f"İşlem sonucunda {len(new_relations_to_add)} yeni film-aktör ilişkisi bulundu.")

        # 3. Yeni ilişkileri toplu olarak veritabanına ekle
        if not new_relations_to_add:
            logging.info("Veritabanına eklenecek yeni ilişki bulunmuyor.")
            return

        logging.info("Yeni ilişkiler veritabanına toplu olarak ekleniyor...")
        
        # SQLAlchemy Core kullanarak bulk insert yap
        db.execute(
            movie_actor.insert(),
            [{"movie_id": movie_id, "actor_id": actor_id} for movie_id, actor_id in new_relations_to_add]
        )
        db.commit()
        
        logging.info(f"✅ {len(new_relations_to_add)} yeni film-aktör ilişkisi başarıyla eklendi.")

    except Exception as e:
        logging.error(f"Bir hata oluştu: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    link_movies_actors()
