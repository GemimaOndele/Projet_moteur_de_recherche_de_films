// Gestion des interactions sur la page de résultats

document.addEventListener('DOMContentLoaded', () => {
  // Boutons de bande annonce
  document.querySelectorAll('.btn-trailer').forEach(btn => {
    btn.addEventListener('click', () => {
      const trailerUrl = btn.getAttribute('data-trailer');
      if (trailerUrl) {
        showTrailerModal(trailerUrl);
      }
    });
  });

  // Boutons de générique
  document.querySelectorAll('.btn-theme').forEach(btn => {
    btn.addEventListener('click', () => {
      const soundUrl = btn.getAttribute('data-sound');
      if (soundUrl) {
        playThemeSound(soundUrl, btn);
      }
    });
  });

  // Fermer la modal
  const closeModal = document.querySelector('.close-modal');
  if (closeModal) {
    closeModal.addEventListener('click', () => {
      hideTrailerModal();
    });
  }

  // Fermer la modal en cliquant en dehors
  const modal = document.getElementById('trailer-modal');
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        hideTrailerModal();
      }
    });
  }

  // Animation d'entrée des cartes
  const cards = document.querySelectorAll('.card');
  cards.forEach((card, index) => {
    card.style.animationDelay = `${index * 0.1}s`;
    card.classList.add('fade-in');
  });
});

function showTrailerModal(trailerUrl) {
  const modal = document.getElementById('trailer-modal');
  const iframe = document.getElementById('trailer-iframe');
  
  if (modal && iframe) {
    iframe.src = trailerUrl;
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
  }
}

function hideTrailerModal() {
  const modal = document.getElementById('trailer-modal');
  const iframe = document.getElementById('trailer-iframe');
  
  if (modal && iframe) {
    modal.classList.remove('show');
    iframe.src = '';
    document.body.style.overflow = '';
  }
}

function playThemeSound(soundUrl, button) {
  const audio = new Audio(soundUrl);
  
  // Toggle play/pause
  if (button.dataset.playing === 'true') {
    audio.pause();
    button.textContent = '🎵 Générique';
    button.dataset.playing = 'false';
  } else {
    // Arrêter tous les autres sons
    document.querySelectorAll('.btn-theme').forEach(btn => {
      if (btn !== button && btn.dataset.playing === 'true') {
        btn.click();
      }
    });

    audio.play();
    button.textContent = '⏸️ Pause';
    button.dataset.playing = 'true';

    audio.addEventListener('ended', () => {
      button.textContent = '🎵 Générique';
      button.dataset.playing = 'false';
    });
  }
}

