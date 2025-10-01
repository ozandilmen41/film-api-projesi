from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

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