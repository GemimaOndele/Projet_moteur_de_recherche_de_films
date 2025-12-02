"""Module pour la détection d'émotions via Deep Learning (webcam/image)."""

from __future__ import annotations

import base64
import io
import tempfile
from pathlib import Path
from typing import Dict, Optional, Tuple

import cv2
import numpy as np
from PIL import Image

# Essayer d'importer deepface pour la détection d'émotion par deep learning
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    DEEPFACE_AVAILABLE = False
    print("⚠️  DeepFace non disponible. Installation: pip install deepface")

# Mapping des émotions DeepFace vers nos émotions
EMOTION_MAPPING = {
    "happy": "heureux",
    "sad": "triste",
    "angry": "colere",
    "fear": "peur",
    "surprise": "surprise",
    "neutral": "neutre",
    "disgust": "ennuyé",
    # Pour "stressé" et "nostalgique", on utilise des combinaisons
}

# Mapping inverse pour les émotions non directement supportées
EMOTION_FALLBACK = {
    "stressé": "angry",  # Colère peut indiquer du stress
    "nostalgique": "sad",  # Tristesse peut être nostalgique
}


def _analyser_qualite_image(img: np.ndarray, face_bbox: Optional[Tuple[int, int, int, int]] = None) -> Dict[str, any]:
    """
    Analyse la qualité de l'image pour la détection d'émotion.
    
    Retourne un dictionnaire avec:
    - brightness: luminosité moyenne (0-255)
    - brightness_status: "trop_sombre", "ok", "trop_lumineux"
    - face_detected: bool
    - face_size_ratio: ratio de la taille du visage par rapport à l'image
    - messages: liste de messages d'aide
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    messages = []
    
    # Calculer la luminosité (convertie en float Python pour compat JSON)
    if face_bbox is not None:
        x, y, w, h = face_bbox
        face_roi = gray[y:y+h, x:x+w]
        brightness = float(np.mean(face_roi))
    else:
        brightness = float(np.mean(gray))
    
    # Évaluer la luminosité
    if brightness < 60:
        brightness_status = "trop_sombre"
        messages.append("💡 La luminosité est trop faible. Placez-vous dans un endroit plus lumineux ou augmentez la luminosité de votre écran.")
    elif brightness > 200:
        brightness_status = "trop_lumineux"
        messages.append("☀️ La luminosité est trop forte. Réduisez l'éclairage ou éloignez-vous de la source de lumière.")
    else:
        brightness_status = "ok"
    
    # Détecter le visage si pas déjà fait
    face_detected = face_bbox is not None
    face_size_ratio: float = 0.0
    
    if face_bbox is not None:
        x, y, w, h = face_bbox
        img_area = img.shape[0] * img.shape[1]
        face_area = int(w) * int(h)
        face_size_ratio = float(face_area / img_area) if img_area > 0 else 0.0
        
        # Vérifier si le visage est assez grand
        if face_size_ratio < 0.05:
            messages.append("📏 Votre visage est trop petit. Approchez-vous de la caméra.")
        elif face_size_ratio > 0.5:
            messages.append("📏 Votre visage est trop proche. Éloignez-vous un peu de la caméra.")
        else:
            # Vérifier le centrage
            center_x = x + w // 2
            center_y = y + h // 2
            img_center_x = img.shape[1] // 2
            img_center_y = img.shape[0] // 2
            
            offset_x = abs(center_x - img_center_x) / img.shape[1]
            offset_y = abs(center_y - img_center_y) / img.shape[0]
            
            if offset_x > 0.3 or offset_y > 0.3:
                messages.append("📍 Centrez votre visage dans le cadre.")
    else:
        messages.append("👤 Aucun visage détecté. Assurez-vous que votre visage est bien visible et centré.")
    
    return {
        "brightness": brightness,
        "brightness_status": brightness_status,
        "face_detected": face_detected,
        "face_size_ratio": face_size_ratio,
        "messages": messages
    }


def detecter_emotion_image(image_data: bytes) -> Dict[str, any]:
    """
    Détecte l'émotion à partir d'une image (webcam ou upload) avec deep learning.
    
    Retourne un dictionnaire avec:
    - emotion: émotion détectée (str) ou None
    - face_bbox: (x, y, w, h) du visage détecté ou None
    - quality: informations sur la qualité de l'image
    - confidence: confiance de la détection (0-1)
    """
    try:
        # Convertir les bytes en image OpenCV
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return {
                "emotion": None,
                "face_bbox": None,
                "quality": {
                    "brightness": 0,
                    "brightness_status": "erreur",
                    "face_detected": False,
                    "face_size_ratio": 0,
                    "messages": ["❌ Impossible de décoder l'image. Vérifiez le format."]
                },
                "confidence": 0.0
            }
        
        # Détecter le visage avec OpenCV
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(50, 50))
        
        face_bbox = None
        if len(faces) > 0:
            # Prendre le plus grand visage
            face_bbox = max(faces, key=lambda f: f[2] * f[3])
            x, y, w, h = face_bbox
        
        # Analyser la qualité de l'image
        quality = _analyser_qualite_image(img, face_bbox)
        
        # Si pas de visage détecté, retourner avec les messages d'aide
        if face_bbox is None:
            return {
                "emotion": None,
                "face_bbox": None,
                "quality": quality,
                "confidence": 0.0
            }
        
        # Utiliser DeepFace pour la détection d'émotion
        emotion_detected = None
        confidence = 0.0
        
        if DEEPFACE_AVAILABLE:
            try:
                # Extraire la région du visage
                x, y, w, h = face_bbox
                face_roi = img[y:y+h, x:x+w]
                
                # Sauvegarder temporairement pour DeepFace
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
                    tmp_path = tmp_file.name
                    cv2.imwrite(tmp_path, face_roi)
                
                try:
                    # Analyser avec DeepFace
                    result = DeepFace.analyze(
                        img_path=tmp_path,
                        actions=['emotion'],
                        enforce_detection=False,
                        silent=True
                    )
                    
                    # Extraire l'émotion dominante
                    if isinstance(result, list):
                        result = result[0]
                    
                        emotions = result.get('emotion', {})
                        if emotions:
                            # Trouver l'émotion avec la plus haute confiance
                            emotion_key, score = max(emotions.items(), key=lambda x: x[1])
                            confidence = float(score) / 100.0  # np.float32 -> float
                            
                            # Mapper vers nos émotions
                            emotion_detected = EMOTION_MAPPING.get(str(emotion_key).lower(), "neutre")
                        
                finally:
                    # Nettoyer le fichier temporaire
                    Path(tmp_path).unlink(missing_ok=True)
                    
            except Exception as e:
                print(f"⚠️  Erreur DeepFace: {e}")
                # Fallback vers méthode simple si DeepFace échoue
                emotion_detected = _detecter_emotion_simple(img, face_bbox)
                confidence = 0.5
        else:
            # Fallback vers méthode simple si DeepFace n'est pas disponible
            emotion_detected = _detecter_emotion_simple(img, face_bbox)
            confidence = 0.3
        
        return {
            "emotion": emotion_detected,
            "face_bbox": tuple(int(v) for v in face_bbox) if face_bbox is not None else None,
            "quality": quality,
            "confidence": float(confidence)
        }
        
    except Exception as e:
        print(f"❌ Erreur détection émotion: {e}")
        import traceback
        traceback.print_exc()
        return {
            "emotion": None,
            "face_bbox": None,
            "quality": {
                "brightness": 0,
                "brightness_status": "erreur",
                "face_detected": False,
                "face_size_ratio": 0,
                "messages": [f"❌ Erreur lors de la détection: {str(e)}"]
            },
            "confidence": 0.0
        }


def _detecter_emotion_simple(img: np.ndarray, face_bbox: Tuple[int, int, int, int]) -> str:
    """
    Méthode de fallback simple basée sur la luminosité et les contours.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    x, y, w, h = face_bbox
    face_roi = gray[y:y+h, x:x+w]
    
    mean_brightness = np.mean(face_roi)
    
    # Heuristiques simples
    if mean_brightness < 80:
        return "triste"
    elif mean_brightness > 180:
        return "heureux"
    else:
        return "neutre"


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

        result = detecter_emotion_image(image_bytes)
        return result.get("emotion")

    except Exception as e:
        print(f"Erreur webcam: {e}")
        return None


def image_base64_to_bytes(base64_string: str) -> bytes:
    """Convertit une image base64 en bytes."""
    if base64_string.startswith("data:image"):
        base64_string = base64_string.split(",")[1]
    return base64.b64decode(base64_string)
