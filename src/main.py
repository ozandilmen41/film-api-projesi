from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import unquote # URL kod çözümü için import ekliyoruz

# Kendi oluşturduğumuz modülleri import ediyoruz
from . import crud, models, schemas
from .database import SessionLocal, engine

# Veritabanı tablolarını oluştur (eğer yoksa)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Film Veritabanı API",
    description="Kaggle'daki 'The Movies Dataset' kullanılarak oluşturulmuş bir film sorgulama API'si.",
    version="1.0.0"
)
# CORS ayarları
origins = [
    "*"  # Herkese izin ver (geliştirme için)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency: Her istek için bir veritabanı oturumu oluşturur ve istek bitince kapatır.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Film API'sine Hoş Geldiniz! /docs adresine giderek dokümantasyonu görebilirsiniz."}


# YENİ ENDPOINT
@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Verilen ID'ye sahip bir filmin detaylarını getirir.
    """
    db_movie = crud.get_movie_by_id(db=db, movie_id=movie_id)
    if db_movie is None:
        # Eğer film bulunamazsa, 404 Not Found hatası döndür.
        raise HTTPException(status_code=404, detail="Film bulunamadı")
    return db_movie

@app.get("/movies/search/", response_model=List[schemas.Movie])
def search_movies(q: str, db: Session = Depends(get_db)):
    """
    Başlığında aranan kelimeyi içeren filmleri listeler.
    Sorgu parametresi olarak 'q' kullanılır. Örnek: /movies/search/?q=Batman
    """
    movies = crud.search_movies_by_title(db=db, query=q)
    if not movies:
        # Arama sonucu boşsa 404 hatası da verilebilir veya boş bir liste de döndürülebilir.
        # Boş liste döndürmek genellikle daha yaygındır.
        return []
    return movies

@app.get("/movies/genre/{genre_name}", response_model=List[schemas.Movie])
def read_movies_by_genre(genre_name: str, db: Session = Depends(get_db)):
    """
    Belirtilen türe ait en yüksek puanlı 10 filmi listeler.
    """
    # FastAPI'nin otomatik URL kod çözümüne güveniyoruz.
    movies = crud.get_movies_by_genre(db=db, genre_name=genre_name)
    if not movies:
        return []
    return movies

@app.get("/movies/actor/{actor_name}", response_model=List[schemas.Movie])
def read_movies_by_actor(actor_name: str, db: Session = Depends(get_db)):
    """
    Belirli bir aktörün rol aldığı filmleri listeler.
    """
    movies = crud.get_movies_by_actor(db=db, actor_name=actor_name)
    if not movies:
        return []
    return movies

@app.get("/genres/", response_model=List[schemas.Genre])
def read_all_genres(db: Session = Depends(get_db)):
    """
    Veritabanındaki tüm film türlerini listeler.
    """
    genres = crud.get_all_genres(db=db)
    return genres

@app.get("/movies/top_rated/", response_model=List[schemas.Movie])
def read_top_rated_movies(limit: int = 100, db: Session = Depends(get_db)):
    """
    En yüksek puanlı filmleri listeler.
    'limit' parametresi ile kaç film getirileceği belirlenebilir. Varsayılan: 100.
    """
    movies = crud.get_top_rated_movies(db=db, limit=limit)
    return movies