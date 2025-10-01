from src.database import engine, Base # Veritabanı bağlantısı ve Base objesini import ediyoruz
from src.models import Movie # Oluşturduğumuz Movie modelini import ediyoruz

def main(): 
    print("Tablolar oluşturuluyor...")
    
    # Base objesine bağlı olan tüm modelleri (şu an için sadece Movie)
    # engine'in bağlı olduğu veritabanında oluşturur.
    # ÖNEMLİ: Eğer tablolar zaten varsa, bu komut hata vermez veya
    # tabloları silip yeniden oluşturmaz. Sadece eksik olanları oluşturur.
    Base.metadata.create_all(bind=engine)
    
    print("✅ Tablolar başarıyla oluşturuldu!")

if __name__ == "__main__":
    main()