# Film Sorgulama API'si (MovieLens API)

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-green.svg)](https://fastapi.tiangolo.com/)
[![AWS](https://img.shields.io/badge/AWS-RDS-orange.svg)](https://aws.amazon.com/rds/)



---

### 🚀 Temel Özellikler

- **Bulut Tabanlı Veritabanı:** Tüm veriler, AWS RDS üzerinde çalışan bir PostgreSQL veritabanında güvenli bir şekilde saklanmaktadır.
- **Yüksek Performanslı API:** Modern ve asenkron bir framework olan FastAPI kullanılarak geliştirilmiştir.
- **Dinamik Arama:** Film başlıklarında büyük/küçük harfe duyarsız, esnek arama yapabilme.
- **Veri İşleme (ETL):** 45.000'den fazla satırlık kirli CSV verisinin Pandas ile temizlenmesi, dönüştürülmesi ve veritabanına yüklenmesi.
- **Otomatik Dokümantasyon:** FastAPI'nin sunduğu Swagger UI ile interaktif ve her zaman güncel API dokümantasyonu.

---

### 🏛️ Sistem Mimarisi

Bu projenin mimarisi, modern bulut uygulamalarının temel prensiplerini yansıtmaktadır. Kullanıcıdan gelen bir HTTP isteği, API sunucusuna ulaşır, sunucu bu isteği işleyerek AWS RDS'teki veritabanına bir sorgu gönderir ve dönen sonucu kullanıcıya JSON formatında sunar.

![Sistem Mimarisi](architecture.png)

---

### 🛠️ Kullanılan Teknolojiler

- **Backend:** Python, FastAPI
- **Veritabanı:** PostgreSQL
- **Bulut Servisi (Cloud):** AWS RDS
- **Veri İşleme:** Pandas
- **ORM (Object-Relational Mapper):** SQLAlchemy
- **API Sunucusu:** Uvicorn

---

### 📖 API Endpoint'leri

Aşağıda projenin sunduğu temel API endpoint'leri listelenmiştir:

| Metot | Endpoint                  | Açıklama                                      | Örnek                                      |
| :---- | :------------------------ | :-------------------------------------------- | :----------------------------------------- |
| `GET` | `/`                       | API'nin çalıştığını teyit eden hoşgeldin mesajı. | `/`                                        |
| `GET` | `/movies/{movie_id}`      | Verilen ID'ye sahip filmin detaylarını getirir. | `/movies/862`                              |
| `GET` | `/movies/search/`         | Başlığında aranan kelimeyi içeren filmleri listeler. | `/movies/search/?q=Matrix`                 |

---


### 📥 Gerekli Veri Seti

Bu projenin çalışması için "The Movies Dataset" gereklidir. Veri seti, reponun boyutunu küçük tutmak amacıyla versiyon kontrolüne dahil edilmemiştir.

1.  Veri setini [Kaggle'dan indirin](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset).
2.  İndirdiğiniz `.zip` dosyasından çıkan `movies_metadata.csv` dosyasını projenin ana dizinine kopyalayın.
3.  Veriyi veritabanına yüklemek için `load_data.py` script'ini çalıştırın:
    ```bash
    python load_data.py
    ```

---



### 🔧 Kurulum ve Çalıştırma

Projeyi lokal makinenizde çalıştırmak için aşağıdaki adımları izleyin:

1.  **Repository'yi klonlayın:**
    ```bash
    git clone [SENİN GITHUB REPO LİNKİN]
    cd film-api-projesi
    ```

2.  **Sanal ortam oluşturun ve aktif edin:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # macOS/Linux için
    .\venv\Scripts\activate    # Windows için
    ```

3.  **Gerekli kütüphaneleri yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ortam değişkenlerini ayarlayın:**
    `.env.example` dosyasını kopyalayıp `.env` adında yeni bir dosya oluşturun ve içine kendi AWS RDS bilgilerinizi girin.

5.  **API sunucusunu başlatın:**
    ```bash
    uvicorn src.main:app --reload
    ```
    Sunucu `http://127.0.0.1:8000` adresinde çalışmaya başlayacaktır.

---

### 🌟 Gelecek Geliştirmeleri

- [ ] **Frontend Arayüzü:** Projeyi daha görsel ve interaktif hale getirmek için basit bir React veya Vue.js arayüzü eklenmesi.
- [ ] **Gelişmiş İlişkiler:** `genres`, `actors`, `keywords` gibi tabloların eklenerek filmlerle ilişkilendirilmesi.
- [ ] **Gelişmiş Filtreleme:** Yıla, puana veya türe göre filtreleme yapabilen endpoint'lerin eklenmesi.
- [ ] **Deployment:** API'nin Render veya Heroku gibi ücretsiz bir servise deploy edilerek canlıya alınması.