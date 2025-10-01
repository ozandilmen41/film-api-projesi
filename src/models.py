from sqlalchemy import Column, Integer, String, Float, Date, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
# Bir üst klasördeki database.py dosyasından Base'i import ediyoruz
from .database import Base 

# Movie ve Genre arasındaki many-to-many ilişkiyi tanımlayan ara tablo
movie_genre = Table('movie_genres', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)

# Movie ve Actor arasındaki many-to-many ilişkiyi tanımlayan ara tablo
movie_actor = Table('movie_actors', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('actor_id', Integer, ForeignKey('actors.id'))
)

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
    
    # Genre ilişkisini tanımlıyoruz
    genres = relationship("Genre", secondary=movie_genre, back_populates="movies")
    # Actor ilişkisini tanımlıyoruz
    actors = relationship("Actor", secondary=movie_actor, back_populates="movies")

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    # Movie ilişkisini tanımlıyoruz
    movies = relationship("Movie", secondary=movie_genre, back_populates="genres")

class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    # Movie ilişkisini tanımlıyoruz
    movies = relationship("Movie", secondary=movie_actor, back_populates="actors")