import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Projenin ana dizinindeki .env dosyasını bul ve değişkenleri yükle
load_dotenv()

# .env dosyasından veritabanı bilgilerini güvenli bir şekilde al
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# SQLAlchemy için veritabanı bağlantı URL'sini oluştur
# Format: postgresql://kullanici_adi:sifre@host:port/veritabani_adi
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy 'engine'ini oluştur. Bu, veritabanına olan ana bağlantı noktasıdır.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Veritabanı oturumları (session) oluşturmak için bir 'fabrika' (factory)
# Her API isteği için ayrı bir veritabanı oturumu açıp kapatacağız.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM modellerimizin (veritabanı tablolarına karşılık gelen Python sınıfları)
# miras alacağı temel sınıf (base class)
Base = declarative_base()