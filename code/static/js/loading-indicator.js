/**
 * Gestion des indicateurs de chargement
 */

// Afficher le loader lors de la soumission du formulaire de recherche
document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const searchBtn = document.getElementById('search-btn');
    const searchBtnText = document.getElementById('search-btn-text');
    const searchLoader = document.getElementById('search-loader');
    
    if (searchForm && searchBtn) {
        searchForm.addEventListener('submit', function(e) {
            // Désactiver le bouton
            if (searchBtn) {
                searchBtn.disabled = true;
                if (searchBtnText) searchBtnText.textContent = 'Recherche en cours...';
                if (searchLoader) searchLoader.classList.remove('hidden');
            }
            
            // Afficher l'overlay de chargement
            showLoadingOverlay('Recherche de films en cours...', 'Analyse de vos critères et enrichissement des données...');
        });
    }
    
    // Afficher l'overlay au chargement de la page de résultats
    if (window.location.pathname.includes('/search')) {
        showLoadingOverlay('Chargement des résultats...', 'Enrichissement des films et préparation de l\'affichage...');
        
        // Cacher l'overlay une fois que la page est chargée
        window.addEventListener('load', function() {
            setTimeout(hideLoadingOverlay, 500);
        });
    }
});

/**
 * Affiche l'overlay de chargement
 */
function showLoadingOverlay(title = 'Chargement...', subtitle = 'Veuillez patienter') {
    // Vérifier si l'overlay existe déjà
    let overlay = document.getElementById('loading-overlay');
    
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="loading-content">
                <div class="loading-spinner"></div>
                <div class="loading-text">${title}</div>
                <div class="loading-subtext">${subtitle}</div>
                <div class="loading-progress">
                    <div class="loading-progress-bar"></div>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);
    } else {
        // Mettre à jour le contenu
        const loadingText = overlay.querySelector('.loading-text');
        const loadingSubtext = overlay.querySelector('.loading-subtext');
        if (loadingText) loadingText.textContent = title;
        if (loadingSubtext) loadingSubtext.textContent = subtitle;
        overlay.classList.remove('hidden');
    }
}

/**
 * Cache l'overlay de chargement
 */
function hideLoadingOverlay() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.classList.add('hidden');
        setTimeout(function() {
            overlay.style.display = 'none';
        }, 300);
    }
}

