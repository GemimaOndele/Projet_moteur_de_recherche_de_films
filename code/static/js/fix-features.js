/**
 * Script pour corriger et améliorer:
 * 1. Traduction française des descriptions
 * 2. Animation du son avec visualiseur
 * 3. Bande annonce
 * 4. Liens streaming
 * 5. Sons des émotions
 */

console.log("✅ fix-features.js chargé");

// ============================================================
// 1. GESTION DES DESCRIPTIONS EN FRANÇAIS
// ============================================================

function afficherDescriptionFrancaise() {
  document.querySelectorAll(".card").forEach((card) => {
    // Récupérer la description depuis data-overview-fr (fournie par le serveur)
    const overviewFr = card.dataset.overviewFr;
    
    if (overviewFr) {
      // Afficher directement sans traduction client-side
      const overviewEl = card.querySelector(".overview");
      if (overviewEl) {
        overviewEl.textContent = overviewFr;
        overviewEl.classList.remove("translating");
        console.log(`✅ Description FR affichée pour: ${card.querySelector(".film-title")?.textContent}`);
      }
    }
  });
}

// ============================================================
// 2. GESTION DE L'AUDIO: VISUALISEUR + LECTEUR
// ============================================================

class AudioManager {
  constructor() {
    this.audioElements = new Map();
    this.visualizers = new Map();
    this.isPlaying = new Map();
    this.analyserNode = null;
    this.dataArray = null;
    this.animationId = null;
    this.setupAudioContext();
  }

  setupAudioContext() {
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      this.audioContext = new AudioContext();
    } catch (e) {
      console.warn("Web Audio API non supportée", e);
    }
  }

  createAudio(id, url, type = "emotion") {
    const audio = new Audio(url);
    audio.crossOrigin = "anonymous";
    audio.addEventListener("play", () => this.onAudioPlay(id, type));
    audio.addEventListener("pause", () => this.onAudioPause(id));
    audio.addEventListener("ended", () => this.onAudioEnded(id));
    this.audioElements.set(id, audio);
    return audio;
  }

  onAudioPlay(id, type) {
    this.isPlaying.set(id, true);
    const button = document.querySelector(`[data-audio-id="${id}"]`);
    if (button) {
      button.classList.add("playing");
      button.textContent = type === "emotion" ? "⏸ Arrêter" : "⏸ Arrêter";
    }

    // Afficher le visualiseur si disponible
    const visualizer = this.visualizers.get(id);
    if (visualizer) {
      visualizer.style.display = 'flex';
      visualizer.classList.add("active");
      this.animateVisualizer(id);
    }
  }

  onAudioPause(id) {
    this.isPlaying.set(id, false);
    const button = document.querySelector(`[data-audio-id="${id}"]`);
    if (button) {
      button.classList.remove("playing");
      button.textContent = button.dataset.originalText || "🎵";
    }

    const visualizer = this.visualizers.get(id);
    if (visualizer) {
      visualizer.classList.remove("active");
      // Si aucun autre audio en cours, cacher le visualizer
      const anyPlaying = Array.from(this.isPlaying.values()).some(v => v === true);
      if (!anyPlaying) {
        visualizer.style.display = 'none';
      }
    }
  }

  onAudioEnded(id) {
    this.onAudioPause(id);
  }

  animateVisualizer(id) {
    const visualizer = this.visualizers.get(id);
    if (!visualizer) return;

    const bars = visualizer.querySelectorAll(".visualizer-bar");
    if (bars.length === 0) return;

    // Animation simple basée sur CSS (pas de Web Audio API)
    bars.forEach((bar, index) => {
      bar.style.animation = `visualize 0.4s ease-in-out infinite`;
      bar.style.animationDelay = `${index * 0.1}s`;
    });
  }

  toggle(id, url, type = "emotion") {
    let audio = this.audioElements.get(id);
    
    if (!audio) {
      audio = this.createAudio(id, url, type);
    }

    if (this.isPlaying.get(id)) {
      audio.pause();
    } else {
      // Arrêter tous les autres
      this.audioElements.forEach((a, key) => {
        if (key !== id && this.isPlaying.get(key)) {
          a.pause();
        }
      });
      audio.play().catch(err => console.error("Erreur lecture audio:", err));
    }
  }
}

const audioManager = new AudioManager();

// ============================================================
// 3. GESTION DES BOUTONS D'AUDIO
// ============================================================

function setupAudioButtons() {
  console.log("🔧 Initialisation setupAudioButtons()");
  
  // Bouton émotion (header)
  const emotionBtns = document.querySelectorAll(".btn-emotion-sound");
  console.log(`📍 Trouvé ${emotionBtns.length} bouton(s) émotion`);
  
  emotionBtns.forEach((btn) => {
    const soundUrl = btn.dataset.emotionSound;
    console.log(`   🎵 Bouton émotion: soundUrl="${soundUrl}"`);
    
    if (!soundUrl) {
      console.warn("   ❌ Pas de soundUrl!");
      return;
    }

    // Créer un ID unique
    const emotionId = `emotion-${Date.now()}-${Math.random()}`;
    btn.dataset.audioId = emotionId;
    btn.dataset.originalText = btn.textContent;

    btn.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      console.log(`🎵 CLIC émotion: ${soundUrl}`);
      // Associer visualizer global à cet audio id
      const globalVisualizer = document.getElementById('audio-visualizer');
      if (globalVisualizer) {
        audioManager.visualizers.set(emotionId, globalVisualizer);
        console.log(`   ✅ Visualizer associé`);
      } else {
        console.warn(`   ⚠️ Visualizer non trouvé`);
      }
      audioManager.toggle(emotionId, soundUrl, "emotion");
    });
    console.log(`   ✅ Bouton émotion wired`);
  });

  // Boutons de bande annonce
  const trailerBtns = document.querySelectorAll(".btn-action.btn-trailer");
  console.log(`📍 Trouvé ${trailerBtns.length} bouton(s) trailer`);
  
  trailerBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const trailerUrl = btn.dataset.trailer;
      const title = btn.dataset.title;
      console.log(`🎬 CLIC trailer: ${trailerUrl} (${title})`);
      if (trailerUrl) {
        showTrailerModal(trailerUrl, title);
      }
    });
  });

  // Boutons générique de film (theme)
  const themeBtns = document.querySelectorAll(".btn-action.btn-theme, .btn-theme");
  console.log(`📍 Trouvé ${themeBtns.length} bouton(s) générique`);
  
  themeBtns.forEach((btn) => {
    const soundUrl = btn.dataset.sound;
    // créer id basé sur film id si disponible
    const filmId = btn.closest('.card') ? btn.closest('.card').dataset.filmId : null;
    const themeId = filmId ? `theme-${filmId}` : `theme-${Date.now()}-${Math.random()}`;
    btn.dataset.audioId = themeId;
    btn.dataset.originalText = btn.textContent;
    
    console.log(`   🎵 Bouton générique: filmId="${filmId}", soundUrl="${soundUrl}"`);

    btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();

      // Si il y a une URL de générique spécifique, on la joue, sinon on essaye le son d'émotion header
      let urlToPlay = soundUrl;
      if (!urlToPlay) {
        const headerBtn = document.querySelector('.btn-emotion-sound');
        urlToPlay = headerBtn ? headerBtn.dataset.emotionSound : null;
        console.log(`   🔄 Fallback à émotion header: ${urlToPlay}`);
      }

      if (!urlToPlay) {
        console.warn('   ❌ Aucun son disponible pour ce film ni pour l\'emotion courante.');
        return;
      }

      console.log(`🎵 CLIC générique: ${urlToPlay}`);
      // Associer visualizer
      const globalVisualizer = document.getElementById('audio-visualizer');
      if (globalVisualizer) {
        audioManager.visualizers.set(themeId, globalVisualizer);
        console.log(`   ✅ Visualizer associé`);
      }
      audioManager.toggle(themeId, urlToPlay, 'theme');
    });
  });

  // Boutons play-overlay
  document.querySelectorAll(".btn-play-trailer").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const trailerUrl = btn.dataset.trailer;
      if (trailerUrl) {
        showTrailerModal(trailerUrl, btn.dataset.title);
      }
    });
  });
}

// ============================================================
// 4. GESTION DE LA BANDE ANNONCE (MODAL)
// ============================================================

function showTrailerModal(trailerUrl, title) {
  // Créer le modal s'il n'existe pas
  let modal = document.getElementById("trailerModal");
  if (!modal) {
    modal = document.createElement("div");
    modal.id = "trailerModal";
    modal.className = "modal-trailer";
    modal.innerHTML = `
      <div class="modal-content">
        <div class="modal-header">
          <h3>${title || "Bande annonce"}</h3>
          <button class="btn-close" title="Fermer">✕</button>
        </div>
        <div class="modal-body">
          <iframe id="trailerIframe" width="100%" height="500" 
                  src="" frameborder="0" 
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowfullscreen>
          </iframe>
        </div>
      </div>
    `;
    document.body.appendChild(modal);

    // Fermer le modal
    modal.querySelector(".btn-close").addEventListener("click", () => {
      modal.classList.remove("active");
    });

    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        modal.classList.remove("active");
      }
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && modal.classList.contains("active")) {
        modal.classList.remove("active");
      }
    });
  }

  // Mettre à jour le contenu et afficher
  const iframe = modal.querySelector("#trailerIframe");
  iframe.src = trailerUrl + "?autoplay=1";
  modal.querySelector("h3").textContent = title || "Bande annonce";
  modal.classList.add("active");
}

// ============================================================
// 5. GESTION DES IMAGES DE FOND
// ============================================================

function setupBackdropImages() {
  document.querySelectorAll(".card").forEach((card) => {
    // Méthode 1: Récupérer depuis data-backdrop sur la carte
    let bgUrl = card.dataset.backdrop;
    
    // Méthode 2: Fallback depuis .card-backdrop data-bg
    if (!bgUrl) {
      const backdropEl = card.querySelector(".card-backdrop");
      if (backdropEl) {
        bgUrl = backdropEl.dataset.bg;
      }
    }
    
    // Afficher l'image de fond
    if (bgUrl) {
      const backdropEl = card.querySelector(".card-backdrop");
      if (backdropEl) {
        backdropEl.style.backgroundImage = `url('${bgUrl}')`;
        backdropEl.style.backgroundSize = "cover";
        backdropEl.style.backgroundPosition = "center";
        console.log(`✅ Backdrop image affichée pour: ${card.querySelector(".film-title")?.textContent}`);
      }
    }
    
    // Afficher le poster (img tag)
    const posterImg = card.querySelector(".card-poster img");
    if (posterImg && !posterImg.src) {
      const posterUrl = card.dataset.poster;
      if (posterUrl) {
        posterImg.src = posterUrl;
        console.log(`✅ Poster image affichée pour: ${card.querySelector(".film-title")?.textContent}`);
      }
    }
  });
}

// ============================================================
// 6. ANIMATIONS AU SCROLL
// ============================================================

function setupScrollAnimations() {
  if (!("IntersectionObserver" in window)) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
      }
    });
  }, { threshold: 0.2 });

  document.querySelectorAll(".card").forEach((card) => {
    observer.observe(card);
  });
}

// ============================================================
// 7. INITIALISATION AU CHARGEMENT
// ============================================================

document.addEventListener("DOMContentLoaded", () => {
  console.log("🚀 Initialisation des corrections...");

  // Afficher les descriptions en français (priorité 1)
  afficherDescriptionFrancaise();

  // Afficher les images (priorité 2)
  setupBackdropImages();

  // Configurer les boutons d'audio (priorité 3)
  setupAudioButtons();

  // Animations au scroll (priorité 4)
  setupScrollAnimations();

  console.log("✅ Toutes les corrections sont actives!");
  
  // Debug: afficher l'état des cartes
  document.querySelectorAll(".card").forEach((card, idx) => {
    const title = card.querySelector(".film-title")?.textContent || "?";
    const backdrop = card.dataset.backdrop;
    const overview = card.dataset.overviewFr?.substring(0, 30) || "?";
    console.log(`  Card ${idx}: ${title} | Backdrop: ${backdrop ? "✅" : "❌"} | Overview: ${overview}...`);
  });
});

// Ajouter les styles du modal s'ils n'existent pas
function addModalStyles() {
  if (document.getElementById("modalStyles")) return;

  const style = document.createElement("style");
  style.id = "modalStyles";
  style.textContent = `
    .modal-trailer {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.8);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      opacity: 0;
      transition: opacity 0.3s ease;
    }

    .modal-trailer.active {
      display: flex;
      opacity: 1;
    }

    .modal-content {
      background: #1e293b;
      border-radius: 12px;
      overflow: hidden;
      max-width: 900px;
      width: 90%;
      max-height: 80vh;
      display: flex;
      flex-direction: column;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    }

    .modal-header {
      padding: 1.5rem;
      border-bottom: 1px solid #334155;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .modal-header h3 {
      margin: 0;
      color: #f8fafc;
    }

    .btn-close {
      background: none;
      border: none;
      color: #f8fafc;
      font-size: 1.5rem;
      cursor: pointer;
      padding: 0;
      width: 30px;
      height: 30px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: color 0.2s;
    }

    .btn-close:hover {
      color: #f97316;
    }

    .modal-body {
      padding: 1rem;
      overflow-y: auto;
      flex: 1;
    }

    .modal-body iframe {
      border-radius: 8px;
    }

    @keyframes visualize {
      0%, 100% { height: 20px; opacity: 0.7; }
      50% { height: 60px; opacity: 1; }
    }

    .visualizer-bar {
      display: inline-block;
      width: 4px;
      height: 20px;
      background: #f97316;
      margin: 0 2px;
      border-radius: 2px;
      animation: visualize 0.4s ease-in-out infinite;
    }

    .audio-visualizer.active .visualizer-bar {
      animation: visualize 0.4s ease-in-out infinite;
    }
  `;
  document.head.appendChild(style);
}

// Charger les styles du modal
addModalStyles();
