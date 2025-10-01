from pydantic import BaseModel
from datetime import date
from typing import Optional

class Genre(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class Actor(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# API üzerinden bir film döndürülürken kullanılacak olan temel model.
# Veritabanı modelindeki (models.py) alanlarla eşleşir.
class Movie(BaseModel):
    id: int
    title: str
    overview: Optional[str] = None
    release_date: Optional[date] = None
    budget: Optional[float] = None
    revenue: Optional[float] = None
    popularity: Optional[float] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None
    genres: list[Genre] = []
    actors: list[Actor] = []

    # Bu ayar, Pydantic'in SQLAlchemy ORM modelleriyle (örn: movie.title)
    # uyumlu çalışmasını sağlar.
    class Config:
        from_attributes = True