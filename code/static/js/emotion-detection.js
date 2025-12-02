// Détection d'émotion via webcam ou upload d'image avec encadrement visage en temps réel

let stream = null;
let video = null;
let canvas = null;
let faceDetectionInterval = null;
let currentFaceBbox = null;

document.addEventListener('DOMContentLoaded', () => {
  const btnWebcam = document.getElementById('btn-webcam');
  const btnUpload = document.getElementById('btn-upload');
  const btnCapture = document.getElementById('btn-capture');
  const fileInput = document.getElementById('file-input');
  const webcamContainer = document.getElementById('webcam-container');
  const videoEl = document.getElementById('video');
  const canvasEl = document.getElementById('canvas');
  const detectedEmotionEl = document.getElementById('detected-emotion');
  const emotionSelect = document.getElementById('emotion');
  const helpMessagesEl = document.getElementById('help-messages');

  video = videoEl;
  canvas = canvasEl;

  // Démarrer webcam
  btnWebcam.addEventListener('click', async () => {
    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert("La webcam n'est pas disponible dans ce contexte. Ouvre l'application sur https ou sur http://localhost:5000.");
        return;
      }
      
      stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: 'user'
        } 
      });
      video.srcObject = stream;
      webcamContainer.classList.remove('hidden');
      btnWebcam.disabled = true;
      
      // Démarrer la détection de visage en temps réel
      startFaceDetection();
    } catch (err) {
      alert('Erreur d\'accès à la webcam: ' + err.message);
    }
  });

  // Capturer l'image
  btnCapture.addEventListener('click', async () => {
    if (!video || !canvas) return;

    // Désactiver le bouton pendant le traitement
    btnCapture.disabled = true;
    btnCapture.textContent = '⏳ Analyse en cours...';

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);

    canvas.toBlob(async (blob) => {
      const result = await detectEmotionFromImage(blob);
      
      if (result && result.emotion) {
        const emotionLabel = getEmotionLabel(result.emotion);
        detectedEmotionEl.textContent = `✅ Émotion détectée: ${emotionLabel} (${Math.round(result.confidence * 100)}% confiance)`;
        detectedEmotionEl.className = 'detected-emotion success';
        emotionSelect.value = result.emotion;

        // Jouer automatiquement le son correspondant à l'émotion détectée
        // (les bulles seront automatiquement synchronisées avec la durée de l'audio)
        if (typeof window.playEmotionSound === 'function') {
          window.playEmotionSound(result.emotion);
        }
        
        // Arrêter la webcam après un court délai
        setTimeout(() => {
          stopWebcam();
        }, 2000);
      } else {
        // Afficher les messages d'aide
        displayHelpMessages(result);
      }
      
      btnCapture.disabled = false;
      btnCapture.textContent = 'Capturer';
    }, 'image/jpeg', 0.95);
  });

  // Upload d'image
  btnUpload.addEventListener('click', () => {
    fileInput.click();
  });

  fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const result = await detectEmotionFromImage(file);
    if (result && result.emotion) {
      const emotionLabel = getEmotionLabel(result.emotion);
      detectedEmotionEl.textContent = `✅ Émotion détectée: ${emotionLabel} (${Math.round(result.confidence * 100)}% confiance)`;
      detectedEmotionEl.className = 'detected-emotion success';
      emotionSelect.value = result.emotion;

      // Jouer automatiquement le son correspondant à l'émotion détectée
      // (les bulles seront automatiquement synchronisées avec la durée de l'audio)
      if (typeof window.playEmotionSound === 'function') {
        window.playEmotionSound(result.emotion);
      }
    } else {
      displayHelpMessages(result);
    }
  });

  // Fonction pour arrêter la webcam
  function stopWebcam() {
    if (faceDetectionInterval) {
      clearInterval(faceDetectionInterval);
      faceDetectionInterval = null;
    }
    
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      stream = null;
    }
    video.srcObject = null;
    webcamContainer.classList.add('hidden');
    btnWebcam.disabled = false;
    currentFaceBbox = null;
    clearFaceOverlay();
  }
});

// Détection de visage en temps réel (toutes les 200ms)
function startFaceDetection() {
  if (faceDetectionInterval) {
    clearInterval(faceDetectionInterval);
  }
  
  faceDetectionInterval = setInterval(async () => {
    if (!video || video.readyState !== video.HAVE_ENOUGH_DATA) return;
    
    // Capturer une frame
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = video.videoWidth;
    tempCanvas.height = video.videoHeight;
    const ctx = tempCanvas.getContext('2d');
    ctx.drawImage(video, 0, 0);
    
    // Envoyer au serveur pour détection (version légère, juste pour le bbox)
    tempCanvas.toBlob(async (blob) => {
      try {
        const formData = new FormData();
        formData.append('image', blob);
        
        const response = await fetch('/api/detect-emotion', {
          method: 'POST',
          body: formData
        });
        
        if (response.ok) {
          const result = await response.json();
          if (result.face_bbox) {
            currentFaceBbox = result.face_bbox;
            drawFaceOverlay(result.face_bbox, result.quality);
            displayHelpMessages(result, true); // true = mode temps réel
          } else {
            currentFaceBbox = null;
            clearFaceOverlay();
            if (result.quality && result.quality.messages) {
              displayHelpMessages(result, true);
            }
          }
        }
      } catch (err) {
        console.error('Erreur détection visage:', err);
      }
    }, 'image/jpeg', 0.7);
  }, 500); // Détection toutes les 500ms pour ne pas surcharger
}

// Dessiner l'encadrement du visage sur la vidéo
function drawFaceOverlay(bbox, quality) {
  const videoEl = document.getElementById('video');
  if (!videoEl) return;
  
  // Créer ou récupérer le canvas overlay
  let overlay = document.getElementById('face-overlay');
  if (!overlay) {
    overlay = document.createElement('canvas');
    overlay.id = 'face-overlay';
    overlay.className = 'face-overlay';
    const container = document.getElementById('webcam-container');
    if (container) {
      container.appendChild(overlay);
    }
  }
  
  overlay.width = videoEl.videoWidth;
  overlay.height = videoEl.videoHeight;
  overlay.style.width = videoEl.offsetWidth + 'px';
  overlay.style.height = videoEl.offsetHeight + 'px';
  
  const ctx = overlay.getContext('2d');
  ctx.clearRect(0, 0, overlay.width, overlay.height);
  
  // Calculer le ratio de mise à l'échelle
  const scaleX = overlay.offsetWidth / overlay.width;
  const scaleY = overlay.offsetHeight / overlay.height;
  
  const [x, y, w, h] = bbox;
  const scaledX = x * scaleX;
  const scaledY = y * scaleY;
  const scaledW = w * scaleX;
  const scaledH = h * scaleY;
  
  // Dessiner le rectangle
  ctx.strokeStyle = quality && quality.face_detected ? '#10b981' : '#ef4444';
  ctx.lineWidth = 3;
  ctx.strokeRect(scaledX, scaledY, scaledW, scaledH);
  
  // Dessiner les coins arrondis
  const cornerLength = 20;
  ctx.beginPath();
  // Coin haut-gauche
  ctx.moveTo(scaledX, scaledY + cornerLength);
  ctx.lineTo(scaledX, scaledY);
  ctx.lineTo(scaledX + cornerLength, scaledY);
  // Coin haut-droite
  ctx.moveTo(scaledX + scaledW - cornerLength, scaledY);
  ctx.lineTo(scaledX + scaledW, scaledY);
  ctx.lineTo(scaledX + scaledW, scaledY + cornerLength);
  // Coin bas-droite
  ctx.moveTo(scaledX + scaledW, scaledY + scaledH - cornerLength);
  ctx.lineTo(scaledX + scaledW, scaledY + scaledH);
  ctx.lineTo(scaledX + scaledW - cornerLength, scaledY + scaledH);
  // Coin bas-gauche
  ctx.moveTo(scaledX + cornerLength, scaledY + scaledH);
  ctx.lineTo(scaledX, scaledY + scaledH);
  ctx.lineTo(scaledX, scaledY + scaledH - cornerLength);
  ctx.stroke();
}

// Effacer l'overlay
function clearFaceOverlay() {
  const overlay = document.getElementById('face-overlay');
  if (overlay) {
    const ctx = overlay.getContext('2d');
    ctx.clearRect(0, 0, overlay.width, overlay.height);
  }
}

// Afficher les messages d'aide
function displayHelpMessages(result, realtime = false) {
  const helpMessagesEl = document.getElementById('help-messages');
  if (!helpMessagesEl) return;
  
  if (!result || !result.quality || !result.quality.messages || result.quality.messages.length === 0) {
    helpMessagesEl.innerHTML = '';
    helpMessagesEl.className = 'help-messages';
    return;
  }
  
  const messages = result.quality.messages;
  helpMessagesEl.innerHTML = messages.map(msg => `<div class="help-message">${msg}</div>`).join('');
  
  // Changer la classe selon la qualité
  if (result.quality.face_detected && result.quality.brightness_status === 'ok') {
    helpMessagesEl.className = 'help-messages success';
  } else {
    helpMessagesEl.className = 'help-messages warning';
  }
  
  if (!realtime) {
    helpMessagesEl.style.display = 'block';
  }
}

// Fonction pour détecter l'émotion depuis une image
async function detectEmotionFromImage(imageBlob) {
  const formData = new FormData();
  formData.append('image', imageBlob);

  try {
    const response = await fetch('/api/detect-emotion', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Erreur de détection');
    }

    const data = await response.json();
    return data;
  } catch (err) {
    console.error('Erreur détection émotion:', err);
    const detectedEmotionEl = document.getElementById('detected-emotion');
    if (detectedEmotionEl) {
      detectedEmotionEl.textContent = `❌ ${err.message}`;
      detectedEmotionEl.className = 'detected-emotion error';
    }
    return null;
  }
}

// Mapper les émotions vers des labels français
function getEmotionLabel(emotion) {
  const labels = {
    'heureux': '😊 Heureux',
    'triste': '😢 Triste',
    'stressé': '😰 Stressé',
    'nostalgique': '🥰 Nostalgique',
    'ennuyé': '😑 Ennuyé',
    'colere': '😠 Colère',
    'peur': '😨 Peur',
    'surprise': '😲 Surprise',
    'neutre': '😐 Neutre'
  };
  return labels[emotion] || emotion;
}
