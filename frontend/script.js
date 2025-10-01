document.addEventListener('DOMContentLoaded', () => {
    const API_URL = 'https://film-api-projesi.onrender.com'; // FastAPI sunucunuzun adresi

    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const resultsGrid = document.getElementById('resultsGrid');
    const movieModal = document.getElementById('movieModal');
    const modalBody = document.getElementById('modalBody');
    const closeButton = document.querySelector('.close-button');

    // Arama fonksiyonu
    const searchMovies = async (query) => {
        if (!query) return;

        try {
            const response = await fetch(`${API_URL}/movies/search/?q=${query}`);
            if (!response.ok) {
                throw new Error('Film arama başarısız oldu.');
            }
            const movies = await response.json();
            displayResults(movies);
        } catch (error) {
            console.error(error);
            resultsGrid.innerHTML = '<p>Bir hata oluştu. Lütfen tekrar deneyin.</p>';
        }
    };

    // Arama sonuçlarını ekranda gösterme
    const displayResults = (movies) => {
        resultsGrid.innerHTML = ''; // Önceki sonuçları temizle
        if (movies.length === 0) {
            resultsGrid.innerHTML = '<p>Sonuç bulunamadı.</p>';
            return;
        }

        movies.forEach(movie => {
            const movieCard = document.createElement('div');
            movieCard.className = 'movie-card';
            movieCard.dataset.movieId = movie.id; // Detaylar için ID'yi sakla

            // Afiş görseli için basit bir yer tutucu
            const posterPath = "https://via.placeholder.com/200x300.png?text=No+Image";
            
            movieCard.innerHTML = `
                <img src="${posterPath}" alt="${movie.title}">
                <h3>${movie.title}</h3>
            `;
            resultsGrid.appendChild(movieCard);
        });
    };

    // Film detaylarını modal'da gösterme
    const showMovieDetails = async (movieId) => {
        try {
            const response = await fetch(`${API_URL}/movies/${movieId}`);
            if (!response.ok) {
                throw new Error('Film detayları alınamadı.');
            }
            const movie = await response.json();
            
            // API'den gelen veriye göre (varsayılan)
            const genres = movie.genres ? movie.genres.map(g => g.name).join(', ') : 'Belirtilmemiş';
            const actors = movie.actors ? movie.actors.slice(0, 5).map(a => a.name).join(', ') : 'Belirtilmemiş';
            
            modalBody.innerHTML = `
                <h2>${movie.title}</h2>
                <p><strong>Yayın Tarihi:</strong> ${movie.release_date || 'N/A'}</p>
                <p><strong>Puan:</strong> ${movie.vote_average || 'N/A'}</p>
                <p><strong>Özet:</strong> ${movie.overview || 'Özet bulunamadı.'}</p>
                <p><strong>Türler:</strong> ${genres}</p>
                <p><strong>Oyuncular (İlk 5):</strong> ${actors}</p>
            `;
            movieModal.classList.add('show');
        } catch (error) {
            console.error(error);
            modalBody.innerHTML = '<p>Detaylar yüklenirken bir hata oluştu.</p>';
        }
    };

    // Event Listeners
    searchButton.addEventListener('click', () => searchMovies(searchInput.value));
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            searchMovies(searchInput.value);
        }
    });

    resultsGrid.addEventListener('click', (e) => {
        const card = e.target.closest('.movie-card');
        if (card) {
            const movieId = card.dataset.movieId;
            showMovieDetails(movieId);
        }
    });

    closeButton.addEventListener('click', () => movieModal.classList.remove('show'));
    movieModal.addEventListener('click', (e) => {
        if (e.target === movieModal) { // Sadece modal arka planına tıklanırsa kapat
            movieModal.classList.remove('show');
        }
    });

});