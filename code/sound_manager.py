"""Module pour gérer les sons : génériques de films et sons selon émotion."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Optional

# Mapping des émotions vers des fichiers audio et réactions
EMOTION_SOUNDS = {
    "triste": {
        "sound": "sounds/emotion_sad.mp3",
        "reaction": "😢",
        "label": "Triste",
        "color": "#4A90E2"
    },
    "stressé": {
        "sound": "sounds/emotion_stressed.mp3",
        "reaction": "😰",
        "label": "Stressé",
        "color": "#FF6B6B"
    },
    "heureux": {
        "sound": "sounds/emotion_happy.mp3",
        "reaction": "😊",
        "label": "Heureux",
        "color": "#FFD700"
    },
    "nostalgique": {
        "sound": "sounds/emotion_nostalgic.mp3",
        "reaction": "🥰",
        "label": "Nostalgique",
        "color": "#FF69B4"
    },
    "ennuyé": {
        "sound": "sounds/emotion_bored.mp3",
        "reaction": "😑",
        "label": "Ennuyé",
        "color": "#95A5A6"
    },
    "colere": {
        "sound": "sounds/emotion_angry.mp3",
        "reaction": "😠",
        "label": "Colère",
        "color": "#E74C3C"
    },
    "peur": {
        "sound": "sounds/emotion_fear.mp3",
        "reaction": "😨",
        "label": "Peur",
        "color": "#8B008B"
    },
    "surprise": {
        "sound": "sounds/emotion_surprise.mp3",
        "reaction": "😲",
        "label": "Surprise",
        "color": "#FF8C00"
    },
}

# Dossier pour stocker les génériques de films
SOUNDS_DIR = Path(__file__).parent.parent / "static" / "audio"
SOUNDS_DIR.mkdir(parents=True, exist_ok=True)


def get_emotion_sound(emotion: str) -> Optional[Dict]:
    """Retourne le dictionnaire de données audio correspondant à l'émotion."""
    emotion = emotion.lower().strip()
    emotion_data = EMOTION_SOUNDS.get(emotion)
    
    if not emotion_data:
        return None
    
    sound_file = emotion_data.get("sound")
    if sound_file and (SOUNDS_DIR / sound_file).exists():
        return {
            "url": f"/static/audio/{sound_file}",
            "label": emotion_data.get("label"),
            "reaction": emotion_data.get("reaction"),
            "color": emotion_data.get("color"),
            "emotion": emotion
        }
    return None


def get_movie_theme_sound(movie_id: int, movie_title: str) -> Optional[str]:
    """
    Retourne le chemin du générique du film.
    Les fichiers doivent être nommés : movie_{id}.mp3 ou {title_slug}.mp3
    """
    try:
        # Essayer par ID
        sound_file = SOUNDS_DIR / f"movie_{movie_id}.mp3"
        if sound_file.exists():
            return f"/static/audio/movie_{movie_id}.mp3"
        
        # Essayer par titre (slug)
        title_slug = movie_title.lower().replace(" ", "_").replace(":", "").replace("'", "").replace("-", "_")
        sound_file = SOUNDS_DIR / f"{title_slug}.mp3"
        if sound_file.exists():
            return f"/static/audio/{title_slug}.mp3"
    except Exception as e:
        # Silencieusement ignorer les erreurs de chemin (caractères spéciaux, etc.)
        pass
    
    return None


def add_sound_to_film(film: Dict) -> Dict:
    """Ajoute les informations de son à un film."""
    film_id = film.get("id")
    film_title = film.get("title", "")
    
    theme_sound = get_movie_theme_sound(film_id, film_title)
    if theme_sound:
        film["theme_sound"] = theme_sound
    
    return film


def get_all_emotions() -> list[Dict]:
    """Retourne la liste de toutes les émotions disponibles."""
    return [
        {
            "emotion": emotion_key,
            "label": data.get("label"),
            "reaction": data.get("reaction"),
            "color": data.get("color")
        }
        for emotion_key, data in EMOTION_SOUNDS.items()
    ]

