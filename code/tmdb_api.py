"""Module pour récupérer les données enrichies depuis l'API TMDB."""

from __future__ import annotations

import os
import logging
from typing import Dict, Optional, Tuple

import requests

# Logger
logger = logging.getLogger(__name__)

# Clé API TMDB (à mettre dans une variable d'environnement en production)
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "your_api_key_here")
# Token API v4 (si vous préférez utiliser le jeton plutôt que la clé v3)
# Token API v4 (si vous préférez utiliser le jeton plutôt que la clé v3)
TMDB_API_TOKEN = os.getenv("TMDB_API_TOKEN")
# En-têtes optionnels pour l'API TMDB v4 (Bearer token)
HEADERS = {'Authorization': f'Bearer {TMDB_API_TOKEN}'} if TMDB_API_TOKEN else None
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
TMDB_POSTER_BASE = "https://image.tmdb.org/t/p/w780"

# Mapping des providers de streaming
PROVIDER_MAPPING = {
    "netflix": {"name": "Netflix", "color": "#E50914"},
    "prime": {"name": "Amazon Prime Video", "color": "#00A8E1"},
    "disney": {"name": "Disney+", "color": "#113CCF"},
    "hbo": {"name": "HBO Max", "color": "#000000"},
}


def _get_tmdb_params_and_headers(language: str = "fr-FR") -> Tuple[dict, dict]:
        """Retourne les params et headers à utiliser pour les appels à l'API TMDB.

        - Si `TMDB_API_TOKEN` est configuré, on utilisera `HEADERS` (Bearer token) et
            on n'inclura pas `api_key` dans les params.
        - Sinon, si `TMDB_API_KEY` est présent et différent de la placeholder, on
            l'inclura en tant que param `api_key`.
        """
        params = {
                "language": language,
                "append_to_response": "videos,watch/providers",
        }
        headers = HEADERS if TMDB_API_TOKEN else None
        if not TMDB_API_TOKEN and TMDB_API_KEY and TMDB_API_KEY != "your_api_key_here":
                params["api_key"] = TMDB_API_KEY
        return params, headers


def check_tmdb_env() -> bool:
    """Retourne True si une clé TMDB (v3) ou un token (v4) est configuré."""
    return bool((TMDB_API_KEY and TMDB_API_KEY != "your_api_key_here") or TMDB_API_TOKEN)



def traduire_texte_avec_google_translate(text: str, source_lang: str = "en", target_lang: str = "fr") -> Optional[str]:
    """Traduit un texte en utilisant l'API MyMemory (gratuite et fiable)."""
    if not text or len(text) < 5:
        return text
    
    try:
        import urllib.parse
        # Limiter à 500 caractères pour éviter les erreurs
        text_to_translate = text[:500] if len(text) > 500 else text
        url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text_to_translate)}&langpair={source_lang}|{target_lang}"
        # MyMemory API: no special headers/params needed
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("responseStatus") == 200:
                translated = data.get("responseData", {}).get("translatedText", text)
                if translated and translated != text:
                    return translated
    except Exception as e:
        logger.warning(f"⚠️ Erreur traduction MyMemory: {e}")
    
    # Fallback: retourner le texte original si rien ne marche
    return text


def enrichir_film_avec_api(film: Dict) -> Dict:
    """
    Enrichit un film avec :
    - Affiche (poster_path)
    - Image de fond (backdrop_path)
    - Lien vers bande annonce YouTube
    - Liens de streaming (si disponibles)
    - Description en français
    - Durée du film
    - Budget et revenus
    """
    film_id = film.get("id")
    if not film_id:
        return film

    # Check if TMDB credentials available
    if not ((TMDB_API_KEY and TMDB_API_KEY != "your_api_key_here") or TMDB_API_TOKEN):
        logger.warning("TMDB API Key or Token not configured; requests may fail or be rate-limited.")

    try:
        # Récupérer les détails du film en français
        url = f"{TMDB_BASE_URL}/movie/{film_id}"
        params, headers = _get_tmdb_params_and_headers(language="fr-FR")
        response = requests.get(url, params=params, headers=headers, timeout=5)
        
        if response.status_code != 200:
            return film

        data = response.json()

        # Affiche
        if data.get("poster_path"):
            film["poster_url"] = f"{TMDB_POSTER_BASE}{data['poster_path']}"
        else:
            film["poster_url"] = None

        # Image de fond (backdrop)
        if data.get("backdrop_path"):
            film["backdrop_url"] = f"{TMDB_POSTER_BASE}{data['backdrop_path']}"
        else:
            film["backdrop_url"] = None

        # Description OBLIGATOIREMENT en français
        # 1. D'abord essayer la réponse fr-FR
        overview = data.get("overview", "")
        
        # 2. Si pas de contenu ou texte vide, récupérer en anglais et traduire
        if not overview or len(overview.strip()) < 10:
            try:
                params_en, headers_en = _get_tmdb_params_and_headers(language="en-US")
                response_en = requests.get(url, params=params_en, headers=headers_en, timeout=5)
                if response_en.status_code == 200:
                    data_en = response_en.json()
                    overview = data_en.get("overview", "")
            except:
                pass
        
        # 3. Traduire en français si nécessaire
        if overview and len(overview.strip()) > 0:
            # Vérifier si c'est de l'anglais ou du français
            # Les mots français courants
            french_words = {"le", "la", "de", "et", "un", "une", "est", "pour", "avec", "qui", "se", "film"}
            overview_lower = overview.lower()
            word_count = len(overview_lower.split())
            french_matches = sum(1 for word in french_words if word in overview_lower)
            
            # Si moins de 30% de mots français, on traduit
            if word_count > 0 and (french_matches / max(word_count, 1)) < 0.3:
                film["overview_fr"] = traduire_texte_avec_google_translate(overview, "en", "fr")
            else:
                film["overview_fr"] = overview
        else:
            film["overview_fr"] = "Pas de description disponible."

        # Bande annonce YouTube (français ou anglais)
        film["trailer_url"] = None
        film["trailer_key"] = None
        if "videos" in data and "results" in data["videos"]:
            for video in data["videos"]["results"]:
                if video.get("type") == "Trailer" and video.get("site") == "YouTube":
                    key = video.get("key")
                    film["trailer_url"] = f"https://www.youtube.com/embed/{key}"
                    film["trailer_key"] = key
                    break

        # Durée du film
        film["runtime"] = data.get("runtime", 0)

        # Budget et revenus
        film["budget"] = data.get("budget", 0)
        film["revenue"] = data.get("revenue", 0)

        # Liens de streaming
        film["streaming_links"] = []
        film["streaming_providers"] = []
        
        if "watch/providers" in data and data["watch/providers"].get("results", {}).get("FR"):
            providers_data = data["watch/providers"]["results"]["FR"]
            
            # Plateforme "flatrate" (abonnement)
            if "flatrate" in providers_data:
                for provider in providers_data["flatrate"]:
                    provider_name = provider.get("provider_name", "").lower()
                    film["streaming_links"].append({
                        "name": provider.get("provider_name", ""),
                        "logo": f"{TMDB_IMAGE_BASE}{provider.get('logo_path', '')}" if provider.get("logo_path") else None,
                        "type": "subscription"
                    })
                    film["streaming_providers"].append(provider_name)
            
            # Plateforme "rent"
            if "rent" in providers_data:
                for provider in providers_data["rent"]:
                    film["streaming_links"].append({
                        "name": f"{provider.get('provider_name', '')} (Location)",
                        "logo": f"{TMDB_IMAGE_BASE}{provider.get('logo_path', '')}" if provider.get("logo_path") else None,
                        "type": "rent"
                    })
                    # Add provider to streaming_providers list if we can
                    try:
                        provider_name = provider.get("provider_name", "").lower()
                        if provider_name and provider_name not in film["streaming_providers"]:
                            film["streaming_providers"].append(provider_name)
                    except Exception:
                        pass
            
            # Plateforme "buy"
            if "buy" in providers_data:
                for provider in providers_data["buy"]:
                    film["streaming_links"].append({
                        "name": f"{provider.get('provider_name', '')} (Achat)",
                        "logo": f"{TMDB_IMAGE_BASE}{provider.get('logo_path', '')}" if provider.get("logo_path") else None,
                        "type": "buy"
                    })
                    try:
                        provider_name = provider.get("provider_name", "").lower()
                        if provider_name and provider_name not in film["streaming_providers"]:
                            film["streaming_providers"].append(provider_name)
                    except Exception:
                        pass

        return film

    except Exception as e:
        logger.error(f"Erreur API TMDB pour film {film_id}: {e}")
        return film


def enrichir_liste_films(films: list[Dict]) -> list[Dict]:
    """Enrichit une liste de films avec les données de l'API TMDB."""
    return [enrichir_film_avec_api(film) for film in films]

