// Gestion des sons selon l'émotion

document.addEventListener('DOMContentLoaded', () => {
  const emotionSelect = document.getElementById('emotion');
  const emotionSound = document.getElementById('emotion-sound');

  // Jouer le son correspondant à l'émotion sélectionnée
  emotionSelect.addEventListener('change', (e) => {
    const emotion = e.target.value;
    if (emotion) {
      playEmotionSound(emotion);
    }
  });

  // Jouer le son au chargement si une émotion est déjà sélectionnée
  if (emotionSelect.value) {
    playEmotionSound(emotionSelect.value);
  }
});

function playEmotionSound(emotion) {
  const emotionSound = document.getElementById('emotion-sound');
  if (!emotionSound) return;

  const soundMap = {
    'triste': '/static/audio/emotion_sad.mp3',
    'stressé': '/static/audio/emotion_stressed.mp3',
    'heureux': '/static/audio/emotion_happy.mp3',
    'nostalgique': '/static/audio/emotion_nostalgic.mp3',
    'ennuyé': '/static/audio/emotion_bored.mp3',
    'colere': '/static/audio/emotion_angry.mp3'
  };

  const soundUrl = soundMap[emotion];
  if (soundUrl) {
    emotionSound.src = soundUrl;
    emotionSound.play().catch(err => {
      console.log('Impossible de jouer le son:', err);
    });
  }
}

