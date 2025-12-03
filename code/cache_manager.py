"""Gestionnaire de cache pour les films enrichis."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Cache en mémoire
_enrichment_cache: Dict[int, Dict] = {}
_cache_file = Path(__file__).parent.parent / "data" / "enrichment_cache.json"


def load_cache() -> None:
    """Charge le cache depuis le fichier."""
    global _enrichment_cache
    if _cache_file.exists():
        try:
            with open(_cache_file, 'r', encoding='utf-8') as f:
                _enrichment_cache = json.load(f)
            logger.info(f"📦 Cache chargé: {len(_enrichment_cache)} films en cache")
        except Exception as e:
            logger.warning(f"⚠️  Erreur lors du chargement du cache: {e}")
            _enrichment_cache = {}


def save_cache() -> None:
    """Sauvegarde le cache dans le fichier."""
    try:
        _cache_file.parent.mkdir(parents=True, exist_ok=True)
        with open(_cache_file, 'w', encoding='utf-8') as f:
            json.dump(_enrichment_cache, f, ensure_ascii=False, indent=2)
        logger.debug(f"💾 Cache sauvegardé: {len(_enrichment_cache)} films")
    except Exception as e:
        logger.warning(f"⚠️  Erreur lors de la sauvegarde du cache: {e}")


def get_cached_film(film_id: int) -> Optional[Dict]:
    """Récupère un film depuis le cache."""
    film_data = _enrichment_cache.get(str(film_id))
    if film_data:
        return film_data
    return None


def cache_film(film: Dict) -> None:
    """Met en cache un film enrichi."""
    film_id = film.get("id")
    if film_id:
        _enrichment_cache[str(film_id)] = film


def cache_films(films: List[Dict]) -> None:
    """Met en cache plusieurs films enrichis."""
    for film in films:
        cache_film(film)
    save_cache()


def get_cached_films(films: List[Dict]) -> tuple[List[Dict], List[Dict]]:
    """
    Sépare les films en deux listes : ceux qui sont en cache et ceux qui doivent être enrichis.
    
    Returns:
        (films_cached, films_to_enrich)
    """
    films_cached = []
    films_to_enrich = []
    
    for film in films:
        film_id = film.get("id")
        if film_id:
            cached = get_cached_film(film_id)
            if cached:
                # Fusionner les données du cache avec les données du film
                film_enriched = {**film, **cached}
                films_cached.append(film_enriched)
            else:
                films_to_enrich.append(film)
        else:
            films_to_enrich.append(film)
    
    return films_cached, films_to_enrich


# Charger le cache au démarrage
load_cache()

