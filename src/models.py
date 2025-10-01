from sqlalchemy import Column, Integer, String, Float, Date, Text
# Bir üst klasördeki database.py dosyasından Base'i import ediyoruz
from .database import Base 

# Bu sınıf, veritabanındaki 'movies' tablosuna karşılık gelir.
# SQLAlchemy, bu sınıfı ve içindeki nitelikleri okuyarak
# 'CREATE TABLE' SQL komutlarını kendisi oluşturur.
class Movie(Base):
    __tablename__ = "movies" # Veritabanında tablonun adı 'movies' olacak

    # Tablonun sütunlarını (kolonlarını) tanımlıyoruz
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True) #burda index=True ile arama hızını artırıyoruz
    overview = Column(Text, nullable=True) # Açıklama bazen boş olabilir
    release_date = Column(Date, nullable=True) # Bazı filmlerin tarihi olmayabilir
    budget = Column(Float, nullable=True) # Bütçe bazen bilinmeyebilir
    revenue = Column(Float, nullable=True) # Gelir bazen bilinmeyebilir
    popularity = Column(Float, nullable=True) # Popülerlik bazen bilinmeyebilir
    vote_average = Column(Float, nullable=True) # Ortalama oy bazen bilinmeyebilir
    vote_count = Column(Integer, nullable=True) # Oy sayısı bazen bilinmeyebilir

# Buraya daha sonra Genre, Actor gibi diğer tablolar için sınıflar da ekleyeceğim.