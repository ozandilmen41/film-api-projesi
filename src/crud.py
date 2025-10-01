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

# Düzeltilmiş Kod
def get_movies_by_genre(db: Session, genre_name: str, limit: int = 10):
    """
    Belirli bir türe ait en yüksek puanlı filmleri sorgular.
    """
    # DEĞİŞİKLİK: .ilike(f"%{genre_name}%") yerine .ilike(genre_name) kullanarak
    # birebir eşleşme (büyük/küçük harf duyarsız) sağlıyoruz.
    return db.query(models.Movie).join(models.Movie.genres).filter(models.Genre.name.ilike(genre_name)).order_by(models.Movie.vote_average.desc()).limit(limit).all()

def get_movies_by_actor(db: Session, actor_name: str, skip: int = 0, limit: int = 100):
    """
    Belirli bir aktörün rol aldığı filmleri sorgular.
    """
    return db.query(models.Movie).join(models.Movie.actors).filter(models.Actor.name.ilike(f"%{actor_name}%")).offset(skip).limit(limit).all()

def get_all_genres(db: Session):
    """
    Veritabanındaki tüm film türlerini, isme göre sıralanmış olarak sorgular.
    """
    return db.query(models.Genre).order_by(models.Genre.name).all()

def get_top_rated_movies(db: Session, limit: int = 100):
    """
    En yüksek puana sahip filmleri sorgular.
    Puanlamanın anlamlı olması için oy sayısı 150'den fazla olanları filtreler.
    """
    return db.query(models.Movie).filter(models.Movie.vote_count > 150).order_by(models.Movie.vote_average.desc()).limit(limit).all()