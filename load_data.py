import pandas as pd
import ast
import logging
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models import Movie, Genre, Actor, movie_genre, movie_actor

# --- Kurulum ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
db: Session = SessionLocal()

def safe_literal_eval(val):
    """Güvenli bir şekilde string'i Python objesine çevirir, hata olursa None döner."""
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError, TypeError, MemoryError):
        return None

def load_all_data_optimized():
    """Tüm veriyi optimize edilmiş şekilde, toplu işlemlerle yükler."""
    try:
        # === BÖLÜM 1: FİLMLERİ YÜKLE (Bu kısım zaten hızlıydı) ===
        logging.info("--- BÖLÜM 1: Filmler Yükleniyor ---")
        existing_movie_ids = {row[0] for row in db.query(Movie.id).all()}
        
        movies_df = pd.read_csv('movies_metadata.csv', usecols=['id', 'title', 'overview', 'release_date', 'budget', 'revenue', 'popularity', 'vote_average', 'vote_count'], low_memory=False)
        
        movies_to_add = []
        for _, row in movies_df.iterrows():
            try:
                movie_id = int(row['id'])
                if movie_id in existing_movie_ids: continue

                budget, revenue, popularity, vote_average, vote_count = map(lambda x: pd.to_numeric(x, errors='coerce'), [row.get('budget'), row.get('revenue'), row.get('popularity'), row.get('vote_average'), row.get('vote_count')])
                release_date = pd.to_datetime(row.get('release_date'), errors='coerce').date() if pd.notna(row.get('release_date')) else None

                movies_to_add.append(Movie(
                    id=movie_id, title=row.get('title'), overview=row.get('overview'), release_date=release_date,
                    budget=float(budget) if pd.notna(budget) else None, revenue=float(revenue) if pd.notna(revenue) else None,
                    popularity=float(popularity) if pd.notna(popularity) else None, vote_average=float(vote_average) if pd.notna(vote_average) else None,
                    vote_count=int(vote_count) if pd.notna(vote_count) else None
                ))
                existing_movie_ids.add(movie_id)
            except (ValueError, TypeError): continue
        
        if movies_to_add:
            db.add_all(movies_to_add)
            db.commit()
            logging.info(f"{len(movies_to_add)} yeni film eklendi.")
        else:
            logging.info("Veritabanı filmler açısından güncel.")

        # === BÖLÜM 2: TÜRLERİ VE İLİŞKİLERİ TOPLU YÜKLE (Optimize Edilmiş) ===
        logging.info("--- BÖLÜM 2: Türler ve İlişkiler Hazırlanıyor ---")
        
        genres_df = pd.read_csv('movies_metadata.csv', usecols=['id', 'genres'], low_memory=False)
        
        all_genres_in_csv = set()
        movie_genre_pairs = set()

        for _, row in genres_df.iterrows():
            try:
                movie_id = int(row['id'])
                genres_list = safe_literal_eval(row['genres'])
                if isinstance(genres_list, list):
                    for genre_data in genres_list:
                        if 'name' in genre_data:
                            genre_name = genre_data['name']
                            all_genres_in_csv.add(genre_name)
                            movie_genre_pairs.add((movie_id, genre_name))
            except (ValueError, TypeError): continue
        
        existing_genres_db = {g.name for g in db.query(Genre.name).all()}
        new_genres_to_add = [Genre(name=name) for name in all_genres_in_csv if name not in existing_genres_db]

        if new_genres_to_add:
            db.bulk_save_objects(new_genres_to_add)
            db.commit()
            logging.info(f"{len(new_genres_to_add)} yeni tür veritabanına eklendi.")

        genre_map = {g.name: g.id for g in db.query(Genre.id, Genre.name).all()}
        existing_movie_ids = {m[0] for m in db.query(Movie.id).all()}
        
        relations_to_add = [
            {'movie_id': movie_id, 'genre_id': genre_map[genre_name]}
            for movie_id, genre_name in movie_genre_pairs
            if movie_id in existing_movie_ids and genre_name in genre_map
        ]
        
        if relations_to_add:
            db.execute(movie_genre.insert(), relations_to_add)
            db.commit()
            logging.info(f"{len(relations_to_add)} film-tür ilişkisi eklendi.")

        # === BÖLÜM 3: AKTÖRLERİ VE İLİŞKİLERİ TOPLU YÜKLE (Optimize Edilmiş) ===
        logging.info("--- BÖLÜM 3: Aktörler ve İlişkiler Hazırlanıyor ---")

        credits_df = pd.read_csv('credits.csv', usecols=['id', 'cast'], low_memory=False)
        all_actors_in_csv = set()
        movie_actor_pairs = set()

        for _, row in credits_df.iterrows():
            try:
                movie_id = int(row['id'])
                cast_list = safe_literal_eval(row['cast'])
                if isinstance(cast_list, list):
                    for actor_data in cast_list:
                        if 'name' in actor_data:
                            actor_name = actor_data['name']
                            all_actors_in_csv.add(actor_name)
                            movie_actor_pairs.add((movie_id, actor_name))
            except (ValueError, TypeError): continue
            
        existing_actors_db = {a.name for a in db.query(Actor.name).all()}
        new_actors_to_add = [Actor(name=name) for name in all_actors_in_csv if name not in existing_actors_db]

        if new_actors_to_add:
            db.bulk_save_objects(new_actors_to_add)
            db.commit()
            logging.info(f"{len(new_actors_to_add)} yeni aktör veritabanına eklendi.")

        actor_map = {a.name: a.id for a in db.query(Actor.id, Actor.name).all()}
        
        actor_relations_to_add = [
            {'movie_id': movie_id, 'actor_id': actor_map[actor_name]}
            for movie_id, actor_name in movie_actor_pairs
            if movie_id in existing_movie_ids and actor_name in actor_map
        ]

        if actor_relations_to_add:
            db.execute(movie_actor.insert(), actor_relations_to_add)
            db.commit()
            logging.info(f"{len(actor_relations_to_add)} film-aktör ilişkisi eklendi.")

    except Exception as e:
        logging.error(f"Kritik bir hata oluştu: {e}")
        db.rollback()
    finally:
        db.close()
        logging.info("Veritabanı oturumu kapatıldı.")

if __name__ == "__main__":
    load_all_data_optimized()