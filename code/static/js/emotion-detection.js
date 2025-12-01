// Détection d'émotion via webcam ou upload d'image

let stream = null;
let video = null;
let canvas = null;

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

  video = videoEl;
  canvas = canvasEl;

  // Démarrer webcam
  btnWebcam.addEventListener('click', async () => {
    try {
      stream = await navigator.mediaDevices.getUserMedia({ video: true });
      video.srcObject = stream;
      webcamContainer.classList.remove('hidden');
      btnWebcam.disabled = true;
    } catch (err) {
      alert('Erreur d\'accès à la webcam: ' + err.message);
    }
  });

  // Capturer l'image
  btnCapture.addEventListener('click', () => {
    if (!video || !canvas) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);

    canvas.toBlob(async (blob) => {
      const emotion = await detectEmotionFromImage(blob);
      if (emotion) {
        detectedEmotionEl.textContent = `Émotion détectée: ${emotion}`;
        emotionSelect.value = emotion;

        // Jouer automatiquement le son correspondant à l'émotion détectée
        if (typeof window.playEmotionSound === 'function') {
          window.playEmotionSound(emotion);
        }
        
        // Arrêter la webcam
        if (stream) {
          stream.getTracks().forEach(track => track.stop());
          stream = null;
        }
        video.srcObject = null;
        webcamContainer.classList.add('hidden');
        btnWebcam.disabled = false;
      }
    });
  });

  // Upload d'image
  btnUpload.addEventListener('click', () => {
    fileInput.click();
  });

  fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const emotion = await detectEmotionFromImage(file);
    if (emotion) {
      detectedEmotionEl.textContent = `Émotion détectée: ${emotion}`;
      emotionSelect.value = emotion;

      // Jouer automatiquement le son correspondant à l'émotion détectée
      if (typeof window.playEmotionSound === 'function') {
        window.playEmotionSound(emotion);
      }
    }
  });
});

async function detectEmotionFromImage(imageBlob) {
  const formData = new FormData();
  formData.append('image', imageBlob);

  try {
    const response = await fetch('/api/detect-emotion', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error('Erreur de détection');
    }

    const data = await response.json();
    return data.emotion;
  } catch (err) {
    console.error('Erreur détection émotion:', err);
    alert('Erreur lors de la détection d\'émotion');
    return null;
  }
}

