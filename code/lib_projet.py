# lib_projet.py
# ============================
# Librairie du projet 
# Contient les fonctions utilitaires communes :
# - parsing des genres
# - extraction de l'année
# - choix du genre principal
# - analyse de sentiments
# - normalisation
# - mapping émotions -> genres
# - base pour le scoring

import json
from datetime import datetime
from textblob import TextBlob


# ---------- PARTIE "GENRES" ----------

def parser_genres(genre_str: str):
    """
    Transforme la chaîne JSON de genres en liste de noms de genres.

    Exemple d'entrée dans le CSV :
        "[{'id': 28, 'name': 'Action'}, {'id': 12, 'name': 'Adventure'}]"

    Sortie :
        ["Action", "Adventure"]

    Si la cellule est vide ou mal formée, on renvoie [].
    """
    if not isinstance(genre_str, str) or genre_str.strip() == "":
        return []

    try:
        cleaned = genre_str.replace("'", '"')
        genres_json = json.loads(cleaned)
        return [g.get("name", "").strip() for g in genres_json if isinstance(g, dict) and "name" in g]
    except Exception:
        return []


def get_main_genre(genres_list):
    """
    Retourne le genre principal (le premier de la liste) ou None si la liste est vide.
    """
    if not genres_list:
        return None
    return genres_list[0]


def extraire_annee(date_str):
    """
    Extrait l'année à partir d'une date au format 'YYYY-MM-DD'.
    Si la date est vide ou invalide, renvoie None.
    """
    if not isinstance(date_str, str) or date_str.strip() == "":
        return None

    try:
        return datetime.strptime(date_str, "%Y-%m-%d").year
    except ValueError:
        return None


# ---------- PARTIE "SENTIMENT" ----------

def analyser_sentiment_texte(texte: str):
    """
    Analyse le sentiment d'un texte en utilisant TextBlob.

    Retourne :
        - score : float entre -1 (très négatif) et 1 (très positif)
        - label : "negatif", "neutre" ou "positif"
    """
    if not isinstance(texte, str) or texte.strip() == "":
        return 0.0, "neutre"

    blob = TextBlob(texte)
    polarite = blob.sentiment.polarity  # entre -1 et 1

    if polarite > 0.1:
        label = "positif"
    elif polarite < -0.1:
        label = "negatif"
    else:
        label = "neutre"

    return float(polarite), label


def normaliser_sentiment(score: float) -> float:
    """
    Normalise un score de sentiment [-1, 1] en [0, 1].
    Utile pour le scoring (Phase 2).
    """
    if score < -1:
        score = -1
    if score > 1:
        score = 1
    return (score + 1.0) / 2.0


# ---------- PARTIE "EMOTIONS & GENRES" ----------

# Mapping émotion -> genres (enrichi pour avoir plus de recommandations)
emotion_to_genres = {
    "triste":      ["Comedy", "Family", "Drama", "Romance", "Animation"],
    "stressé":     ["Comedy", "Adventure", "Action", "Animation", "Family"],
    "heureux":     ["Romance", "Music", "Comedy", "Animation", "Family"],
    "nostalgique": ["Drama", "History", "Romance", "Music", "Family", "War"],
    "ennuyé":      ["Action", "Thriller", "Sci-Fi", "Adventure", "Crime", "Mystery"],
    "colere":      ["Action", "Thriller", "Crime", "War", "Drama", "History"],
    "peur":        ["Horror", "Thriller", "Mystery", "Crime", "Sci-Fi"],
    "surprise":    [],  # Cas spécial : retourne tous les films, triés par note
}


# ---------- PARTIE "SCORING DE BASE" ----------

def normaliser_note(note: float) -> float:
    """
    Normalise une note de film [0, 10] en [0, 1].
    """
    if note < 0:
        note = 0
    if note > 10:
        note = 10
    return note / 10.0


def calculer_score_film(film: dict, emotion_user: str) -> float:
    """
    Calcule un score global pour un film en fonction :
        - du sentiment du texte (overview)
        - de la note moyenne du film

    Pour l'instant, la formule est simple :
        score = 0.6 * sentiment_norm + 0.4 * note_norm

    On pourra l'améliorer plus tard en fonction de emotion_user.
    """
    sentiment_score = film.get("sentiment_score", 0.0)
    sentiment_norm = normaliser_sentiment(sentiment_score)

    note = film.get("vote_average", 0.0)
    note_norm = normaliser_note(note)

    w_sentiment = 0.6
    w_note = 0.4

    score = w_sentiment * sentiment_norm + w_note * note_norm
    return float(score)
