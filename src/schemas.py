from pydantic import BaseModel
from datetime import date
from typing import Optional

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

    # Bu ayar, Pydantic'in SQLAlchemy ORM modelleriyle (örn: movie.title)
    # uyumlu çalışmasını sağlar.
    class Config:
        orm_mode = True