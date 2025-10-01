# src klasöründeki database.py dosyasından 'engine' objesini import et
from src.database import engine

def test_db_connection():
    """Veritabanına bağlanmayı deneyen basit bir fonksiyon."""
    try:
        # Engine'i kullanarak bir bağlantı kurmayı dene
        connection = engine.connect()
        print("✅ Veritabanı bağlantısı başarılı!")
        
        # Bağlantıyı hemen kapat
        connection.close()
        print("ℹ️ Bağlantı kapatıldı.")

    except Exception as e:
        # Bağlantı sırasında bir hata oluşursa, hatayı detaylıca ekrana yazdır
        print("❌ Veritabanı bağlantısı BAŞARISIZ!")
        print(f"Hata Detayı: {e}")

if __name__ == "__main__":
    test_db_connection()