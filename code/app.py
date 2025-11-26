"""Application Flask : formulaire titre + émotion + page de résultats avec fonctionnalités avancées."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List
import logging
import os

import pandas as pd
from flask import Flask, jsonify, render_template, request

from data_loading import charger_films_prepares
from emotion_detection import detecter_emotion_image, image_base64_to_bytes
from recommendation import rechercher_par_titre, recommander_par_emotion
from sentiment import ajouter_sentiment_aux_films
from sound_manager import add_sound_to_film, get_emotion_sound
from tmdb_api import enrichir_liste_films

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_ENRICHED = DATA_DIR / "films_sentiment.csv"
DATASET_TMBD = BASE_DIR / "dataset" / "tmdb_5000_movies.csv"

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max pour les uploads


def _charger_catalogue() -> List[Dict]:
    """Charge les films enrichis s'ils existent, sinon fallback vers le CSV brut avec enrichissement limité."""
    # Si un cache enrichi existe, l'utiliser
    if DATA_ENRICHED.exists():
        df = pd.read_csv(DATA_ENRICHED)
        films = df.to_dict(orient="records")
        # Convertir les genres de string en liste si nécessaire
        for film in films:
            if isinstance(film.get("genres"), str):
                try:
                    import ast
                    film["genres"] = ast.literal_eval(film["genres"])
                except Exception:
                    film["genres"] = []
        return films

    # Sinon: charger le CSV brut
    films = charger_films_prepares(str(DATASET_TMBD))
    films = ajouter_sentiment_aux_films(films)

    # S'assurer que chaque film a des URLs valides pour l'affiche et le backdrop (évite les img vides)
    for film in films:
        title = film.get("title", "Film") or "Film"
        # Coerce poster/backdrop à une chaîne non vide si absent
        if not film.get("poster_url"):
            film["poster_url"] = f"https://via.placeholder.com/500x750?text={title[:20].replace(' ', '+')}"
        if not film.get("backdrop_url"):
            film["backdrop_url"] = f"https://via.placeholder.com/1280x720?text={title[:30].replace(' ', '+')}"
        if not film.get("streaming_links"):
            film["streaming_links"] = []

    # Si une clé TMDB est présente, enrichir les TOP 50 films seulement (rapide au démarrage)
    try:
        from tmdb_api import TMDB_API_KEY
        if TMDB_API_KEY and TMDB_API_KEY != "your_api_key_here":
            try:
                # Enrichir seulement les 50 premiers films (rapide, ~30-60 sec)
                top_n = 50
                logger.info(f"ℹ️ Enrichissement des top {top_n} films via TMDB (rapide)...")
                films_top = films[:top_n]
                films_top = enrichir_liste_films(films_top)
                films = films_top + films[top_n:]  # Recombiner

                # Ajouter les sons à tous les films
                for f in films:
                    add_sound_to_film(f)

                # Sauvegarder le cache partiel pour éviter re-enrichir les top 50
                try:
                    df_out = pd.DataFrame(films)
                    df_out["genres"] = df_out["genres"].apply(lambda g: str(g) if not pd.isna(g) else "[]")
                    DATA_ENRICHED.parent.mkdir(parents=True, exist_ok=True)
                    df_out.to_csv(DATA_ENRICHED, index=False)
                    logger.info(f"✅ Cache partiel sauvegardé ({top_n} films enrichis): {DATA_ENRICHED}")
                except Exception as e:
                    logger.warning(f"⚠️ Échec sauvegarde cache: {e}")
            except Exception as e:
                logger.warning(f"⚠️ Erreur enrichissement TMDB: {e}")
                # Fallback: ajouter juste les sons
                for film in films:
                    add_sound_to_film(film)
        else:
            logger.warning("⚠️ Clé TMDB manquante; saut enrichissement, utilisation données locales.")
            for film in films:
                add_sound_to_film(film)
    except Exception as e:
        # Fallback final: ajouter juste les sons
        logger.warning(f"Fallback: enrichissement TMDB a échoué: {e}")
        for film in films:
            add_sound_to_film(film)

    return films


def _dedupe_films(films: List[Dict]) -> List[Dict]:
    """Déduplique les films par ID."""
    seen = set()
    uniques = []
    for film in films:
        film_id = film.get("id")
        if film_id in seen:
            continue
        seen.add(film_id)
        uniques.append(film)
    return uniques


def _enrichir_films(films: List[Dict]) -> List[Dict]:
    """Enrichit les films avec API TMDB et sons."""
    # Enrichir avec API TMDB (optionnel, peut être désactivé si pas de clé API)
    try:
        films = enrichir_liste_films(films)
    except Exception as e:
        logger.warning(f"⚠️ Erreur enrichissement TMDB: {e}")
    
    # Ajouter fallbacks pour posters/backdrops/trailers si manquants
    for film in films:
        # Si pas de poster_url, utiliser une image par défaut
        if not film.get("poster_url"):
            film["poster_url"] = f"https://via.placeholder.com/500x750?text={film.get('title', 'Film')[:20]}"
        
        # Si pas de backdrop_url, utiliser backdrop par défaut
        if not film.get("backdrop_url"):
            film["backdrop_url"] = f"https://via.placeholder.com/1280x720?text={film.get('title', 'Film')[:20]}"
        
        # Si pas de overview_fr, utiliser overview EN ET traduire si nécessaire
        if not film.get("overview_fr") or film.get("overview_fr") == "Pas de description disponible.":
            overview = film.get("overview", "Pas de description disponible.")
            if overview and len(overview) > 10:
                # Essayer traduction rapide côté serveur (synchrone)
                from tmdb_api import traduire_texte_avec_google_translate
                film["overview_fr"] = traduire_texte_avec_google_translate(overview, "en", "fr")
            else:
                film["overview_fr"] = overview
        
        # Si pas de trailer_url, laisser vide (pas de fallback pour video)
        if not film.get("trailer_url"):
            film["trailer_url"] = None
        
        # Si pas de streaming_links, créer liste vide
        if not film.get("streaming_links"):
            film["streaming_links"] = []
        
        add_sound_to_film(film)
    
    return films


catalogue_films = _charger_catalogue()


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/search")
def search():
    titre = request.args.get("titre", "").strip()
    emotion = request.args.get("emotion", "").strip().lower()

    resultats: List[Dict] = []

    if titre:
        film = rechercher_par_titre(titre, catalogue_films)
        if film:
            resultats.append(film)

    if emotion:
        resultats.extend(recommander_par_emotion(emotion, catalogue_films, n=5))

    resultats = _dedupe_films(resultats)
    
    # Enrichir avec API TMDB et sons
    resultats = _enrichir_films(resultats)

    # Ajouter le son d'émotion si une émotion est sélectionnée
    emotion_sound = get_emotion_sound(emotion) if emotion else None

    return render_template(
        "results.html",
        titre=titre,
        emotion=emotion,
        films=resultats,
        emotion_sound=emotion_sound
    )


@app.post("/api/detect-emotion")
def api_detect_emotion():
    """API endpoint pour détecter l'émotion depuis une image uploadée."""
    if 'image' not in request.files:
        return jsonify({"error": "Aucune image fournie"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Fichier vide"}), 400

    try:
        image_data = file.read()
        emotion = detecter_emotion_image(image_data)
        
        if emotion:
            return jsonify({"emotion": emotion}), 200
        else:
            return jsonify({"error": "Aucune émotion détectée"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
