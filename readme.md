# Film Sorgulama API'si ve Arayüzü

### 🚀 **[CANLI ARAYÜZÜ DENEMEK İÇİN TIKLA!](https://film-api-proje.netlify.app/)** 🚀

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-green.svg)](https://fastapi.tiangolo.com/)
[![AWS](https://img.shields.io/badge/AWS-RDS-orange.svg)](https://aws.amazon.com/rds/)

Bu proje, Kaggle'dan alınan "The Movies Dataset" kullanılarak geliştirilmiş, **canlı bir arayüze sahip**, AWS RDS (PostgreSQL) üzerinde çalışan, yüksek performanslı bir RESTful API'dir. Proje, birden çok büyük veri setini işleme, ilişkisel bir veritabanını sıfırdan tasarlama ve yönetme, modern backend teknolojileriyle ölçeklenebilir bir servis sunma ve bu servisi bir frontend uygulamasıyla entegre etme yetkinliklerini sergilemek amacıyla oluşturulmuştur.
**Önemli Not:** Veri setindeki film puanları (`vote_average`), MovieLens platformunun kendi kullanıcı oylamalarını yansıtmaktadır. Bu puanlar, IMDb gibi genel geçer puanlama sitelerindeki değerlerle farklılık gösterebilir. Bu durum, projenin bir hatası değil, veri setinin kendi özelliğidir.

---

### 🚀 Temel Özellikler

- **Canlı ve İnteraktif Arayüz:** Netlify üzerinde yayınlanan, film arama ve kategori bazlı listeleme özelliklerine sahip, modern bir web arayüzü.
- **Bulut Tabanlı Backend:** Render üzerinde 7/24 çalışan, Python & FastAPI ile geliştirilmiş, asenkron ve hızlı bir API.
- **Yönetilen ve İlişkisel Veritabanı:** Tüm veriler, AWS RDS üzerinde çalışan bir PostgreSQL veritabanında, filmler, türler ve aktörler arasındaki ilişkiler korunarak saklanmaktadır.
- **Kompleks Veri İşleme (ETL):** `movies_metadata.csv` ve `credits.csv` gibi birden çok kaynaktan gelen yüz binlerce satırlık kirli verinin Pandas ile temizlenmesi, dönüştürülmesi ve ilişkisel tablolara yüklenmesi.
- **Otomatik Dokümantasyon:** FastAPI'nin sunduğu Swagger UI ile interaktif ve her zaman güncel API dokümantasyonu.
- **Gelişmiş Sorgular:** Puana göre sıralama (`Top Rated`) ve türe göre filtreleme gibi gelişmiş ve optimize edilmiş veritabanı sorguları.

---

### 🏛️ Sistem Mimarisi

Bu projenin mimarisi, modern bir full-stack uygulamanın dağıtık yapısını göstermektedir. Kullanıcının web tarayıcısı Netlify'da barındırılan frontend uygulamasına erişir. Arayüzde yapılan bir arama veya kategori seçimi, Render üzerinde çalışan backend API'sine bir HTTP isteği gönderir. API, bu isteği işleyerek AWS RDS'teki veritabanına bir sorgu atar ve dönen sonucu kullanıcıya JSON formatında sunar.

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

API'nin canlı dokümantasyonuna **[https://film-api-projesi.onrender.com/docs](https://film-api-projesi.onrender.com/docs)** adresinden ulaşılabilir.

| Metot | Endpoint                  | Açıklama                                      |
| :---- | :------------------------ | :-------------------------------------------- |
| `GET` | `/`                       | API'nin çalıştığını teyit eden hoşgeldin mesajı. |
| `GET` | `/genres/`                | Veritabanındaki tüm film türlerini listeler.    |
| `GET` | `/movies/top_rated/`      | En yüksek puanlı 100 filmi listeler.          |
| `GET` | `/movies/search/`         | Başlığında aranan kelimeyi içeren filmleri listeler. |
| `GET` | `/movies/genre/{genre_name}` | Belirtilen türe ait en yüksek puanlı filmleri getirir. |
| `GET` | `/movies/{movie_id}`      | Verilen ID'ye sahip filmin detaylarını (tür ve aktörler dahil) getirir. |

---

### 🔧 Kurulum ve Çalıştırma

Projeyi lokal makinenizde çalıştırmak için aşağıdaki adımları izleyin:

1.  **Repository'yi klonlayın:**
    ```bash
    git clone [https://github.com/ozandilmen41/film-api-projesi](https://github.com/ozandilmen41/film-api-projesi)
    cd film-api-projesi
    ```

2.  **Veri Setlerini İndirin:**
    Bu proje, `movies_metadata.csv` ve `credits.csv` dosyalarını kullanır.
    - Veri setini [Kaggle'dan indirin](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset).
    - İndirdiğiniz `.zip` dosyasından çıkan `movies_metadata.csv` ve `credits.csv` dosyalarını projenin ana dizinine kopyalayın.

3.  **Sanal ortam oluşturun ve aktif edin:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # macOS/Linux için
    .\venv\Scripts\activate    # Windows için
    ```

4.  **Gerekli kütüphaneleri yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Ortam değişkenlerini ayarlayın:**
    `.env` adında yeni bir dosya oluşturun ve içine kendi AWS RDS bilgilerinizi girin. (`DB_HOST`, `DB_USER`, `DB_PASSWORD` vb.)

6.  **Veritabanını Doldurun:**
    Verileri veritabanına yüklemek için `load_data.py` script'ini çalıştırın. Bu işlem birkaç dakika sürebilir.
    ```bash
    python load_data.py
    ```

7.  **API sunucusunu başlatın:**
    ```bash
    uvicorn src.main:app --reload
    ```
    Sunucu `http://127.0.0.1:8000` adresinde çalışmaya başlayacaktır. Frontend'i test etmek için `frontend/index.html` dosyasını Live Server ile açabilirsiniz.

---

### 🌟 Gelecek Geliştirmeleri

Projenin mevcut hali tamamlanmış olsa da, potansiyel geliştirmeler şunları içerebilir:

- [ ] **Testler:** `pytest` kullanarak API endpoint'leri için birim (unit) ve entegrasyon (integration) testleri yazmak.
- [ ] **Pagination:** Arama ve kategori sonuçları için sayfalama (pagination) eklemek.
- [ ] **Gelişmiş Filtreleme:** Filmleri çıkış yılına veya puan aralığına göre filtreleyen endpoint'ler eklemek.
- [ ] **Caching:** Popüler isteklerin sonuçlarını Redis gibi bir serviste cache'leyerek performansı artırmak.
- [ ] **Keywords Verisi:** `keywords.csv` dosyasını da işleyerek filmlere anahtar kelime bazlı arama özelliği eklemek.