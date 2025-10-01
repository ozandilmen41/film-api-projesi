from sqlalchemy.orm import Session
from . import models

def get_movie_by_id(db: Session, movie_id: int):
    """
    Veritabanından verilen ID'ye sahip filmi sorgular.
    """
    # db.query(models.Movie) -> 'SELECT * FROM movies' sorgusuna benzer.
    # .filter(models.Movie.id == movie_id) -> 'WHERE id = movie_id' koşulunu ekler.
    # .first() -> Bulduğu ilk sonucu döndürür veya sonuç yoksa None döndürür.
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

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