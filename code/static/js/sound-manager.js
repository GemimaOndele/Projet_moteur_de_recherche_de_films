// Gestion des sons selon l'émotion

function playEmotionSound(emotion) {
  const emotionSound = document.getElementById('emotion-sound');
  if (!emotionSound) return;

  const soundMap = {
    'triste': '/static/audio/sounds/emotion_sad.mp3',
    'stressé': '/static/audio/sounds/emotion_stressed.mp3',
    'heureux': '/static/audio/sounds/emotion_happy.mp3',
    'nostalgique': '/static/audio/sounds/emotion_nostalgic.mp3',
    'ennuyé': '/static/audio/sounds/emotion_bored.mp3',
    'colere': '/static/audio/sounds/emotion_angry.mp3',
    'peur': '/static/audio/sounds/emotion_fear.mp3',
    'surprise': '/static/audio/sounds/emotion_surprise.mp3'
  };

  const soundUrl = soundMap[emotion];
  if (soundUrl) {
    // Arrêter les bulles en cours avant de rejouer
    if (typeof window.stopEmotionBubbles === 'function') {
      window.stopEmotionBubbles();
    }

    // Reconfigurer les callbacks pour lier bulles ↔ audio
    emotionSound.onplay = () => {
      if (typeof window.startEmotionBubbles === 'function') {
        window.startEmotionBubbles(emotion);
      }
    };
    emotionSound.onended = () => {
      if (typeof window.stopEmotionBubbles === 'function') {
        window.stopEmotionBubbles();
      }
    };
    emotionSound.onpause = () => {
      if (typeof window.stopEmotionBubbles === 'function') {
        window.stopEmotionBubbles();
      }
    };

    emotionSound.src = soundUrl;
    emotionSound.play().catch(err => {
      console.log('Impossible de jouer le son:', err);
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const emotionSelect = document.getElementById('emotion');
  const emotionSound = document.getElementById('emotion-sound');

  // Jouer le son correspondant à l'émotion sélectionnée
  emotionSelect.addEventListener('change', (e) => {
    const emotion = e.target.value;
    if (emotion) {
      playEmotionSound(emotion);
    } else {
      // Arrêter les bulles si aucune émotion sélectionnée
      if (typeof window.stopEmotionBubbles === 'function') {
        window.stopEmotionBubbles();
      }
    }
  });

  // Jouer le son au chargement si une émotion est déjà sélectionnée
  if (emotionSelect.value) {
    playEmotionSound(emotionSelect.value);
  }
});

// Exporter la fonction pour utilisation externe
window.playEmotionSound = playEmotionSound;

