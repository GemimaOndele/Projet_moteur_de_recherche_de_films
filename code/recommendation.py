"""Moteur de recherche et recommandations (Phase 2)."""

from __future__ import annotations

from difflib import get_close_matches
from typing import Dict, List, Optional

from lib_projet import calculer_score_film, emotion_to_genres

Film = Dict


def rechercher_par_titre(titre: str, films: List[Film]) -> Optional[Film]:
    """Retourne le film correspondant le mieux au titre fourni (matching flou)."""
    titre = (titre or "").strip()
    if not titre:
        return None

    exact = next((film for film in films if film.get("title", "").lower() == titre.lower()), None)
    if exact:
        return exact

    titres = [film.get("title", "") for film in films]
    matches = get_close_matches(titre, titres, n=1, cutoff=0.55)
    if not matches:
        return None

    match = matches[0]
    return next((film for film in films if film.get("title") == match), None)


def recommander_similaires(film_ref: Film, films: List[Film], n: int = 5) -> List[Film]:
    """Recommande des films partageant des genres avec celui de référence."""
    if not film_ref:
        return []

    ref_genres = set(film_ref.get("genres", []))
    recommandations = []

    for film in films:
        if film.get("id") == film_ref.get("id"):
            continue

        genres = set(film.get("genres", []))
        overlap = len(ref_genres & genres)
        if overlap == 0:
            continue

        score = overlap * 0.7 + (film.get("vote_average", 0.0) / 10.0) * 0.3
        film_copy = dict(film)
        film_copy["score_similarite"] = round(score, 3)
        recommandations.append(film_copy)

    recommandations.sort(key=lambda film: film["score_similarite"], reverse=True)
    return recommandations[:n]


def recommander_par_emotion(emotion: str, films: List[Film], n: int = 5) -> List[Film]:
    """Filtre les films par genres liés à l'émotion et applique un scoring simple."""
    if not emotion:
        return []

    genres_cibles = emotion_to_genres.get(emotion.lower(), [])
    if not genres_cibles:
        return []

    genres_cibles_set = set(genres_cibles)
    candidats: List[Film] = []

    for film in films:
        if not genres_cibles_set.intersection(set(film.get("genres", []))):
            continue
        film_copy = dict(film)
        film_copy["score_emotion"] = calculer_score_film(film_copy, emotion)
        candidats.append(film_copy)

    candidats.sort(key=lambda f: f["score_emotion"], reverse=True)
    return candidats[:n]
