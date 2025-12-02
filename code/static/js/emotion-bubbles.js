// Animation de bulles d'émojis flottantes selon l'émotion sélectionnée

const EMOTION_EMOJIS = {
    'heureux': '😊',
    'triste': '😢',
    'stressé': '😰',
    'nostalgique': '🥰',
    'ennuyé': '😑',
    'colere': '😠',
    'peur': '😨',
    'surprise': '😲'
};

let bubblesContainer = null;
let activeBubbles = [];
let animationFrameId = null;
let createIntervalId = null;

function createBubblesContainer() {
    if (bubblesContainer) return bubblesContainer;
    
    bubblesContainer = document.createElement('div');
    bubblesContainer.id = 'emotion-bubbles-container';
    bubblesContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1000;
        overflow: hidden;
    `;
    document.body.appendChild(bubblesContainer);
    return bubblesContainer;
}

function createBubble(emoji) {
    const bubble = document.createElement('div');
    bubble.textContent = emoji;
    bubble.style.cssText = `
        position: absolute;
        font-size: ${30 + Math.random() * 40}px;
        opacity: ${0.6 + Math.random() * 0.4};
        user-select: none;
        pointer-events: none;
        will-change: transform;
        transition: opacity 0.5s ease-out;
    `;
    
    // Position initiale aléatoire
    bubble.style.left = Math.random() * 100 + '%';
    bubble.style.top = '100%';
    
    // Vitesse et direction aléatoires
    bubble.vx = (Math.random() - 0.5) * 2; // -1 à 1
    bubble.vy = -2 - Math.random() * 3; // -2 à -5 (vers le haut)
    bubble.rotation = (Math.random() - 0.5) * 360;
    bubble.rotationSpeed = (Math.random() - 0.5) * 4;
    
    return bubble;
}

function animateBubbles() {
    if (activeBubbles.length === 0) {
        if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
            animationFrameId = null;
        }
        return;
    }
    
    const container = bubblesContainer;
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    
    activeBubbles = activeBubbles.filter(bubble => {
        if (!bubble.parentElement) return false;
        
        const rect = bubble.getBoundingClientRect();
        const x = parseFloat(bubble.style.left) || 0;
        const y = parseFloat(bubble.style.top) || 100;
        
        // Mise à jour de la position
        let newX = x + bubble.vx;
        let newY = y + bubble.vy;
        
        // Rotation
        bubble.rotation += bubble.rotationSpeed;
        
        // Rebond sur les bords horizontaux
        if (newX < 0 || newX > 100) {
            bubble.vx *= -1;
            newX = Math.max(0, Math.min(100, newX));
        }
        
        // Supprimer si hors de l'écran (en haut)
        if (newY < -10) {
            bubble.style.opacity = '0';
            setTimeout(() => {
                if (bubble.parentElement) {
                    bubble.parentElement.removeChild(bubble);
                }
            }, 500);
            return false;
        }
        
        // Appliquer les transformations
        bubble.style.left = newX + '%';
        bubble.style.top = newY + '%';
        bubble.style.transform = `rotate(${bubble.rotation}deg)`;
        
        return true;
    });
    
    animationFrameId = requestAnimationFrame(animateBubbles);
}

function startEmotionBubbles(emotion) {
    const emoji = EMOTION_EMOJIS[emotion.toLowerCase()];
    if (!emoji) return;
    
    // Nettoyer les bulles précédentes
    stopEmotionBubbles();
    
    const container = createBubblesContainer();
    
    // Créer plusieurs bulles initiales
    const initialBubbles = 8 + Math.floor(Math.random() * 5);
    for (let i = 0; i < initialBubbles; i++) {
        const bubble = createBubble(emoji);
        container.appendChild(bubble);
        activeBubbles.push(bubble);
    }
    
    // Continuer à créer des bulles périodiquement
    createIntervalId = setInterval(() => {
        if (activeBubbles.length < 15) {
            const bubble = createBubble(emoji);
            container.appendChild(bubble);
            activeBubbles.push(bubble);
        }
    }, 800);
    
    // Démarrer l'animation
    if (!animationFrameId) {
        animateBubbles();
    }
}

function stopEmotionBubbles() {
    // Arrêter la création de nouvelles bulles
    if (createIntervalId) {
        clearInterval(createIntervalId);
        createIntervalId = null;
    }

    if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
        animationFrameId = null;
    }
    
    activeBubbles.forEach(bubble => {
        if (bubble.parentElement) {
            bubble.style.opacity = '0';
            setTimeout(() => {
                if (bubble.parentElement) {
                    bubble.parentElement.removeChild(bubble);
                }
            }, 500);
        }
    });
    
    activeBubbles = [];
}

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    const emotionSelect = document.getElementById('emotion');
    if (emotionSelect) {
        emotionSelect.addEventListener('change', (e) => {
            const emotion = e.target.value;
            if (emotion) {
                startEmotionBubbles(emotion);
            } else {
                stopEmotionBubbles();
            }
        });
    }
});

// Exporter pour utilisation externe
window.startEmotionBubbles = startEmotionBubbles;
window.stopEmotionBubbles = stopEmotionBubbles;

