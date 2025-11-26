/**
 * results-enhanced.js
 * Gestion avancée des résultats avec animations audio, vidéos et interactions
 */

document.addEventListener('DOMContentLoaded', () => {
  // ===== MODAL BANDE ANNONCE =====
  const trailerModal = document.getElementById('trailer-modal');
  const trailerIframe = document.getElementById('trailer-iframe');
  const trailerTitle = document.getElementById('trailer-title');
  const closeModalBtn = document.querySelector('.modal-close-btn');

  // Ouvrir modal pour bande annonce
  document.querySelectorAll('.btn-trailer, .btn-play-trailer').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const trailer = btn.dataset.trailer;
      const title = btn.dataset.title || 'Bande annonce';
      if (trailer) {
        trailerTitle.textContent = `${title} - Bande annonce`;
        trailerIframe.src = trailer;
        trailerModal.classList.remove('hidden');
        trailerModal.classList.add('show');
      }
    });
  });

  // Fermer modal
  const closeModal = () => {
    trailerModal.classList.add('hidden');
    trailerModal.classList.remove('show');
    trailerIframe.src = '';
  };

  closeModalBtn?.addEventListener('click', closeModal);
  trailerModal?.addEventListener('click', (e) => {
    if (e.target === trailerModal) closeModal();
  });

  // Fermer avec Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !trailerModal.classList.contains('hidden')) {
      closeModal();
    }
  });

  // ===== AUDIO ÉMOTIONS =====
  const emotionAudio = document.getElementById('emotion-audio');
  const btnEmotionSound = document.querySelector('.btn-emotion-sound');

  if (btnEmotionSound) {
    btnEmotionSound.addEventListener('click', () => {
      const soundUrl = btnEmotionSound.dataset.emotionSound;
      if (soundUrl) {
        if (emotionAudio.src !== soundUrl) {
          emotionAudio.src = soundUrl;
          emotionAudio.play();
          btnEmotionSound.textContent = '⏸️ Arrêter l\'ambiance';
          btnEmotionSound.classList.add('playing');
        } else if (emotionAudio.paused) {
          emotionAudio.play();
          btnEmotionSound.textContent = '⏸️ Arrêter l\'ambiance';
          btnEmotionSound.classList.add('playing');
        } else {
          emotionAudio.pause();
          btnEmotionSound.textContent = '🎵 Écouter l\'ambiance';
          btnEmotionSound.classList.remove('playing');
        }
      }
    });

    emotionAudio.addEventListener('ended', () => {
      btnEmotionSound.textContent = '🎵 Écouter l\'ambiance';
      btnEmotionSound.classList.remove('playing');
    });
  }

  // ===== AUDIO GÉNÉRIQUES DE FILMS =====
  document.querySelectorAll('.btn-theme').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const soundUrl = btn.dataset.sound;
      const audioElement = btn.parentElement.querySelector('.theme-audio');

      if (soundUrl && audioElement) {
        if (audioElement.src !== soundUrl) {
          audioElement.src = soundUrl;
          audioElement.play();
          btn.textContent = '⏸️ Arrêter';
          btn.classList.add('playing');
          showAudioVisualizer(btn);
        } else if (audioElement.paused) {
          audioElement.play();
          btn.textContent = '⏸️ Arrêter';
          btn.classList.add('playing');
          showAudioVisualizer(btn);
        } else {
          audioElement.pause();
          btn.textContent = '🎵 Générique';
          btn.classList.remove('playing');
          hideAudioVisualizer(btn);
        }
      }
    });
  });

  document.querySelectorAll('.theme-audio').forEach(audio => {
    audio.addEventListener('ended', () => {
      const btn = audio.parentElement.querySelector('.btn-theme');
      if (btn) {
        btn.textContent = '🎵 Générique';
        btn.classList.remove('playing');
      }
    });
  });

  // ===== VISUALISEUR AUDIO =====
  function showAudioVisualizer(btn) {
    const card = btn.closest('.card');
    let visualizer = card.querySelector('.audio-visualizer');

    if (!visualizer) {
      visualizer = document.createElement('div');
      visualizer.className = 'audio-visualizer';
      visualizer.innerHTML = `
        <div class="visualizer-bar"></div>
        <div class="visualizer-bar"></div>
        <div class="visualizer-bar"></div>
        <div class="visualizer-bar"></div>
        <div class="visualizer-bar"></div>
      `;
      btn.parentElement.appendChild(visualizer);
    }

    visualizer.style.display = 'flex';
  }

  function hideAudioVisualizer(btn) {
    const card = btn.closest('.card');
    const visualizer = card.querySelector('.audio-visualizer');
    if (visualizer) {
      visualizer.style.display = 'none';
    }
  }

  // ===== BACKDROP IMAGE =====
  document.querySelectorAll('.card-backdrop[data-bg]').forEach(el => {
    const bgUrl = el.dataset.bg;
    if (bgUrl) {
      el.style.backgroundImage = `url('${bgUrl}')`;
    }
  });

  // ===== ANIMATION CARDS =====
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, observerOptions);

  document.querySelectorAll('.card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(card);
  });

  // ===== DETAILS/SYNOPSIS =====
  document.querySelectorAll('.overview-details').forEach(details => {
    details.addEventListener('toggle', () => {
      if (details.open) {
        // Animation d'ouverture
        const summary = details.querySelector('summary');
        const p = details.querySelector('p');
        p.style.animation = 'fadeIn 0.3s ease';
      }
    });
  });

  // ===== RÉACTIONS STREAMING =====
  document.querySelectorAll('.stream-link').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      // Afficher un message de notification
      const type = link.classList.contains('stream-subscription') ? 'abonnement' :
                   link.classList.contains('stream-rent') ? 'location' : 'achat';
      showNotification(`Redirection vers la plateforme pour ${type}...`);
    });
  });

  // ===== NOTIFICATIONS =====
  function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: var(--accent, #f97316);
      color: #000;
      padding: 1rem 1.5rem;
      border-radius: 0.5rem;
      font-weight: 600;
      z-index: 2000;
      animation: slideIn 0.3s ease;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
      notification.style.animation = 'slideOut 0.3s ease';
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  }

  // ===== ANIMATIONS CSS =====
  if (!document.getElementById('dynamic-animations')) {
    const style = document.createElement('style');
    style.id = 'dynamic-animations';
    style.textContent = `
      @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
      }

      @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
      }

      @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }

      .btn-action.playing {
        background: var(--accent, #f97316);
        color: #000;
        animation: pulse 1s ease-in-out infinite;
      }

      @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
      }
    `;
    document.head.appendChild(style);
  }
});

// ===== API DÉTECTION ÉMOTION =====
async function uploadEmotionImage(file) {
  const formData = new FormData();
  formData.append('image', file);

  try {
    const response = await fetch('/api/detect-emotion', {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      const data = await response.json();
      return data.emotion;
    } else {
      console.error('Erreur détection émotion:', response.status);
      return null;
    }
  } catch (error) {
    console.error('Erreur upload image:', error);
    return null;
  }
}

// Export pour utilisation externe
window.emotionDetection = {
  uploadImage: uploadEmotionImage
};
