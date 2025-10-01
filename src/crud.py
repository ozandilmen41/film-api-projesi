from sqlalchemy.orm import Session, joinedload
from . import models

def get_movie_by_id(db: Session, movie_id: int):
    """
    Veritabanından verilen ID'ye sahip filmi, ilişkili türlerini ve aktörlerini sorgular.
    `joinedload` kullanarak N+1 problemini önler.
    """
    return db.query(models.Movie).options(
        joinedload(models.Movie.genres),
        joinedload(models.Movie.actors)
    ).filter(models.Movie.id == movie_id).first()

# YENİ FONKSİYON
def search_movies_by_title(db: Session, query: str, skip: int = 0, limit: int = 100):
    """
    Veritabanında başlığında aranan kelime geçen filmleri sorgular.
    Büyük/küçük harf duyarsız arama yapar (ilike).
    """
    # .filter(models.Movie.title.ilike(f"%{query}%")) -> 'WHERE title LIKE '%query%'' sorgusuna benzer.
    # 'ilike' büyük/küçük harf duyarsız arama sağlar. '%' wildcard karakteridir.
    # .offset(skip).limit(limit) -> Sayfalama (pagination) için kullanılır.
    return db.query(models.Movie).filter(models.Movie.title.ilike(f"%{query}%")).offset(skip).limit(limit).all()

def get_movies_by_genre(db: Session, genre_name: str, skip: int = 0, limit: int = 100):
    """
    Belirli bir türe ait filmleri sorgular.
    """
    return db.query(models.Movie).join(models.Movie.genres).filter(models.Genre.name.ilike(f"%{genre_name}%")).offset(skip).limit(limit).all()

def get_movies_by_actor(db: Session, actor_name: str, skip: int = 0, limit: int = 100):
    """
    Belirli bir aktörün rol aldığı filmleri sorgular.
    """
    return db.query(models.Movie).join(models.Movie.actors).filter(models.Actor.name.ilike(f"%{actor_name}%")).offset(skip).limit(limit).all()