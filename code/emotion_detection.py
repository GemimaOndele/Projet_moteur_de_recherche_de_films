"""Module pour la détection d'émotions via CNN (webcam/image)."""

from __future__ import annotations

import base64
import io
from typing import Dict, Optional

import cv2
import numpy as np
from PIL import Image

# Pour l'instant, on utilise une détection simple basée sur les expressions faciales
# En production, on pourrait utiliser un modèle pré-entraîné comme FER2013 ou AffectNet

try:
    import tensorflow as tf
    from tensorflow import keras
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("TensorFlow non disponible. Utilisation d'un modèle simplifié.")


def detecter_emotion_image(image_data: bytes) -> Optional[str]:
    """
    Détecte l'émotion à partir d'une image (webcam ou upload).
    
    Retourne une émotion parmi : "triste", "stressé", "heureux", "nostalgique", "ennuyé", "colere"
    """
    try:
        # Convertir les bytes en image OpenCV
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return None

        # Charger le classificateur de visages Haar
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) == 0:
            return None

        # Pour l'instant, on retourne une émotion aléatoire basée sur des heuristiques simples
        # TODO: Intégrer un vrai modèle CNN pré-entraîné (FER2013, AffectNet, etc.)
        
        # Analyse simplifiée basée sur la luminosité et les contours
        mean_brightness = np.mean(gray)
        
        # Heuristiques simples (à remplacer par un vrai modèle)
        if mean_brightness < 80:
            return "triste"
        elif mean_brightness > 180:
            return "heureux"
        else:
            return "neutre"

    except Exception as e:
        print(f"Erreur détection émotion: {e}")
        return None


def detecter_emotion_webcam() -> Optional[str]:
    """
    Capture une image depuis la webcam et détecte l'émotion.
    """
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return None

        ret, frame = cap.read()
        cap.release()

        if not ret:
            return None

        # Convertir en bytes
        _, buffer = cv2.imencode('.jpg', frame)
        image_bytes = buffer.tobytes()

        return detecter_emotion_image(image_bytes)

    except Exception as e:
        print(f"Erreur webcam: {e}")
        return None


def image_base64_to_bytes(base64_string: str) -> bytes:
    """Convertit une image base64 en bytes."""
    if base64_string.startswith("data:image"):
        base64_string = base64_string.split(",")[1]
    return base64.b64decode(base64_string)

