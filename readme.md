# Film Sorgulama API'si ve Arayüzü

### 🚀 **[CANLI ARAYÜZÜ DENEMEK İÇİN TIKLA!](https://film-api-proje.netlify.app/)** 🚀

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-green.svg)](https://fastapi.tiangolo.com/)
[![AWS](https://img.shields.io/badge/AWS-RDS-orange.svg)](https://aws.amazon.com/rds/)

Bu proje, Kaggle'dan alınan "The Movies Dataset" kullanılarak geliştirilmiş, **canlı bir arayüze sahip**, AWS RDS (PostgreSQL) üzerinde çalışan, yüksek performanslı bir RESTful API'dir. Proje, büyük veri setlerini işleme, bulut tabanlı bir veritabanı yönetme, modern backend teknolojileriyle ölçeklenebilir bir servis sunma ve bu servisi bir frontend uygulamasıyla entegre etme yetkinliklerini sergilemek amacıyla oluşturulmuştur.

---

### 🚀 Temel Özellikler

- **Canlı ve İnteraktif Arayüz:** Netlify üzerinde yayınlanan, herkesin kullanabileceği bir web arayüzü.
- **Bulut Tabanlı Backend:** Render üzerinde 7/24 çalışan, Python & FastAPI ile geliştirilmiş API.
- **Yönetilen Veritabanı:** Tüm veriler, AWS RDS üzerinde çalışan bir PostgreSQL veritabanında güvenli bir şekilde saklanmaktadır.
- **Veri İşleme (ETL):** 250.000'den fazla satırlık kirli CSV verisinin Pandas ile temizlenmesi, dönüştürülmesi ve veritabanına yüklenmesi.
- **Otomatik Dokümantasyon:** FastAPI'nin sunduğu Swagger UI ile interaktif ve her zaman güncel API dokümantasyonu.

---

### 🏛️ Sistem Mimarisi

Bu projenin mimarisi, modern bir full-stack uygulamanın dağıtık yapısını göstermektedir. Kullanıcının web tarayıcısı Netlify'da barındırılan frontend uygulamasına erişir. Arayüzde yapılan bir arama, Render üzerinde çalışan backend API'sine bir HTTP isteği gönderir. API, bu isteği işleyerek AWS RDS'teki veritabanına bir sorgu atar ve dönen sonucu kullanıcıya sunar.

![Sistem Mimarisi](architecture.png)

---

### 🛠️ Kullanılan Teknolojiler

- **Frontend:** HTML5, CSS3, JavaScript (Vanilla JS)
- **Backend:** Python, FastAPI
- **Veritabanı:** PostgreSQL
- **Bulut Servisleri (Cloud):**
    - **Arayüz Hostingi:** Netlify
    - **API Hostingi:** Render
    - **Veritabanı Hostingi:** AWS RDS
- **Veri İşleme:** Pandas
- **ORM:** SQLAlchemy

---

### 📖 API Endpoint'leri

API'nin canlı dokümantasyonuna **[https://film-api-projesi.onrender.com//docs]** adresinden ulaşılabilir.

| Metot | Endpoint                  | Açıklama                                      |
| :---- | :------------------------ | :-------------------------------------------- |
| `GET` | `/`                       | API'nin çalıştığını teyit eden hoşgeldin mesajı. |
| `GET` | `/movies/{movie_id}`      | Verilen ID'ye sahip filmin detaylarını getirir. |
| `GET` | `/movies/search/`         | Başlığında aranan kelimeyi içeren filmleri listeler. |
| `...` |                           | *(Eklediğin yeni endpoint'leri buraya ekleyebilirsin)* |

---


### 🔧 Kurulum ve Çalıştırma

Projeyi lokal makinenizde çalıştırmak için aşağıdaki adımları izleyin:

1.  **Repository'yi klonlayın:**
    ```bash
    git clone https://github.com/ozandilmen41/film-api-projesi
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

- [✅] **Frontend Arayüzü:** Projeyi daha görsel ve interaktif hale getirmek için basit bir React veya Vue.js arayüzü eklenmesi.
- [✅] **Gelişmiş İlişkiler:** `genres`, `actors`, `keywords` gibi tabloların eklenerek filmlerle ilişkilendirilmesi.
- [✅] **Gelişmiş Filtreleme:** Yıla, puana veya türe göre filtreleme yapabilen endpoint'lerin eklenmesi.
- [✅] **Deployment:** API'nin Render veya Heroku gibi ücretsiz bir servise deploy edilerek canlıya alınması.