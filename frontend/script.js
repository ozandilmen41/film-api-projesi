document.addEventListener('DOMContentLoaded', () => {
    const API_URL = 'https://film-api-projesi.onrender.com';

    // DOM Elementleri
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const mainContent = document.getElementById('mainContent');
    
    const categoryNav = document.getElementById('categoryNav');
    const categoryList = document.getElementById('categoryList');
    
    const searchResultsSection = document.getElementById('searchResults');
    const searchResultsGrid = document.getElementById('searchResultsGrid');
    const searchResultsTitle = document.getElementById('searchResultsTitle');

    const contentDisplay = document.getElementById('contentDisplay');
    const contentTitle = document.getElementById('contentTitle');
    const contentGrid = document.getElementById('contentGrid');
    
    const movieModal = document.getElementById('movieModal');
    const modalBody = document.getElementById('modalBody');
    const closeButton = document.querySelector('.close-button');

    // --- Yardımcı Fonksiyonlar ---

    const createMovieCard = (movie) => {
        const movieCard = document.createElement('div');
        movieCard.className = 'movie-card';
        movieCard.dataset.movieId = movie.id;

        movieCard.innerHTML = `
            <div class="movie-info">
                <h3>${movie.title}</h3>
                <p>⭐ ${movie.vote_average.toFixed(1)}</p>
            </div>
        `;
        return movieCard;
    };

    const displayMovies = (movies, gridElement, message = 'Sonuç bulunamadı.') => {
        gridElement.innerHTML = '';
        if (!movies || movies.length === 0) {
            gridElement.innerHTML = `<p class="info-message">${message}</p>`;
            return;
        }
        movies.forEach(movie => {
            const movieCard = createMovieCard(movie);
            gridElement.appendChild(movieCard);
        });
    };

    // --- UI Durum Yönetimi ---

    const showContentDisplay = () => {
        contentDisplay.style.display = 'block';
        categoryNav.style.display = 'block';
        searchResultsSection.style.display = 'none';
    };

    const showSearchResults = () => {
        contentDisplay.style.display = 'none';
        categoryNav.style.display = 'none';
        searchResultsSection.style.display = 'block';
    };


    // --- API'den Veri Çekme ve Görüntüleme ---

    const fetchAndDisplayCategory = async (categoryItem) => {
        const categoryType = categoryItem.dataset.type;
        const categoryName = categoryItem.dataset.name;

        // Aktif kategori stilini ayarla
        document.querySelectorAll('#categoryList li').forEach(li => li.classList.remove('active'));
        categoryItem.classList.add('active');

        contentGrid.innerHTML = `<p class="info-message">Yükleniyor...</p>`;
        showContentDisplay();

        try {
            let movies = [];
            let title = '';

            if (categoryType === 'top_rated') {
                title = 'En Yüksek Puanlı 100 Film';
                const response = await fetch(`${API_URL}/movies/top_rated/?limit=100`);
                if (!response.ok) throw new Error('En yüksek puanlı filmler alınamadı.');
                movies = await response.json();
            } else if (categoryType === 'genre') {
                title = `${categoryName} Filmleri`;
                const response = await fetch(`${API_URL}/movies/genre/${categoryName}`);
                if (!response.ok) throw new Error(`${categoryName} filmleri alınamadı.`);
                movies = await response.json();
            }
            
            contentTitle.textContent = title;
            displayMovies(movies, contentGrid, 'Bu kategoride film bulunamadı.');

        } catch (error) {
            console.error(error);
            contentGrid.innerHTML = `<p class="info-message">Filmler yüklenirken bir hata oluştu.</p>`;
        }
    };

    const searchMovies = async (query) => {
        if (!query) {
            showContentDisplay();
            return;
        }

        showSearchResults();
        searchResultsGrid.innerHTML = `<p class="info-message">Aranıyor...</p>`;
        searchResultsTitle.textContent = `'${query}' için sonuçlar`;

        try {
            const response = await fetch(`${API_URL}/movies/search/?q=${query}`);
            if (!response.ok) throw new Error('Film arama başarısız oldu.');
            const movies = await response.json();
            displayMovies(movies, searchResultsGrid);
        } catch (error) {
            console.error(error);
            searchResultsGrid.innerHTML = '<p class="info-message">Arama sırasında bir hata oluştu.</p>';
        }
    };

    const showMovieDetails = async (movieId) => {
        try {
            const response = await fetch(`${API_URL}/movies/${movieId}`);
            if (!response.ok) throw new Error('Film detayları alınamadı.');
            const movie = await response.json();
            
            const genres = movie.genres ? movie.genres.map(g => g.name).join(', ') : 'Belirtilmemiş';
            const actors = movie.actors ? movie.actors.slice(0, 10).map(a => a.name).join(', ') : 'Belirtilmemiş';
            
            modalBody.innerHTML = `
                <h2>${movie.title}</h2>
                <p><strong>Yayın Tarihi:</strong> ${movie.release_date || 'N/A'}</p>
                <p><strong>Puan:</strong> ${movie.vote_average ? `⭐ ${movie.vote_average.toFixed(1)} (${movie.vote_count} oy)` : 'N/A'}</p>
                <p><strong>Özet:</strong> ${movie.overview || 'Özet bulunamadı.'}</p>
                <p><strong>Türler:</strong> ${genres}</p>
                <p><strong>Oyuncular:</strong> ${actors}</p>
            `;
            movieModal.classList.add('show');
        } catch (error) {
            console.error(error);
            modalBody.innerHTML = '<p>Detaylar yüklenirken bir hata oluştu.</p>';
        }
    };

    // --- Kategorileri Oluşturma ---

    const createCategoryNavigation = async () => {
        try {
            // 1. Statik "En İyi 100" kategorisini ekle
            const topRatedLi = document.createElement('li');
            topRatedLi.textContent = 'En İyi 100 Film';
            topRatedLi.dataset.type = 'top_rated';
            topRatedLi.dataset.name = 'Top 100';
            categoryList.appendChild(topRatedLi);

            // 2. API'den türleri çek ve ekle
            const response = await fetch(`${API_URL}/genres/`);
            if (!response.ok) throw new Error('Türler alınamadı.');
            const genres = await response.json();

            // Sadece belirli, yaygın türleri göstermek için bir filtre listesi
            const allowedGenres = [
                'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 
                'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 
                'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction', 
                'TV Movie', 'Thriller', 'War', 'Western'
            ];

            // API'den gelen türleri bu listeye göre filtrele
            const filteredGenres = genres.filter(genre => allowedGenres.includes(genre.name));

            filteredGenres.forEach(genre => {
                const genreLi = document.createElement('li');
                genreLi.textContent = genre.name;
                genreLi.dataset.type = 'genre';
                genreLi.dataset.name = genre.name;
                categoryList.appendChild(genreLi);
            });

            // 3. Kategori tıklama olayını ekle
            categoryList.addEventListener('click', (e) => {
                if (e.target.tagName === 'LI') {
                    fetchAndDisplayCategory(e.target);
                }
            });

            // 4. Başlangıçta ilk kategoriyi yükle
            if (categoryList.firstChild) {
                fetchAndDisplayCategory(categoryList.firstChild);
            }

        } catch (error) {
            console.error(error);
            categoryNav.innerHTML = '<p class="info-message">Kategoriler yüklenemedi.</p>';
        }
    };


    // --- Event Listeners ---

    searchButton.addEventListener('click', () => searchMovies(searchInput.value));
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            searchMovies(searchInput.value);
        }
    });
    
    searchInput.addEventListener('input', () => {
        if (searchInput.value === '') {
            showContentDisplay();
        }
    });

    mainContent.addEventListener('click', (e) => {
        const card = e.target.closest('.movie-card');
        if (card) {
            const movieId = card.dataset.movieId;
            showMovieDetails(movieId);
        }
    });

    closeButton.addEventListener('click', () => movieModal.classList.remove('show'));
    movieModal.addEventListener('click', (e) => {
        if (e.target === movieModal) {
            movieModal.classList.remove('show');
        }
    });

    // --- Sayfa Başlatma ---
    
    createCategoryNavigation();
});