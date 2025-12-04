"""Script pour enrichir TOUS les films avec l'API TMDB (bandes annonces, images, etc.)."""

from __future__ import annotations

import time
import logging
from pathlib import Path
from typing import List, Dict

import pandas as pd
import sys

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CODE_DIR = BASE_DIR / "code"

# Ajouter le dossier code au path pour les imports
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from data_loading import charger_films_prepares
from sentiment import ajouter_sentiment_aux_films
from tmdb_api import enrichir_film_avec_api, check_tmdb_env
from sound_manager import add_sound_to_film
DATASET_TMBD = BASE_DIR / "dataset" / "tmdb_5000_movies.csv"
OUTPUT_FILE = BASE_DIR / "data" / "films_enriched_complete.csv"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Rate limiting : 40 requêtes toutes les 10 secondes (limite TMDB)
DELAY_BETWEEN_REQUESTS = 0.25  # 250ms entre chaque requête
BATCH_SIZE = 40  # Pause après chaque batch


def enrichir_tous_films() -> List[Dict]:
    """Enrichit TOUS les films avec l'API TMDB."""
    
    if not check_tmdb_env():
        logger.error("❌ Clé API TMDB non configurée. Configurez TMDB_API_KEY dans l'environnement.")
        return []
    
    logger.info("📥 Chargement du dataset brut...")
    films = charger_films_prepares(str(DATASET_TMBD))
    films = ajouter_sentiment_aux_films(films)
    total = len(films)
    logger.info(f"✅ {total} films chargés")
    
    logger.info("🔄 Enrichissement avec API TMDB (cela peut prendre 10-15 minutes)...")
    logger.info("   ⚠️  Rate limiting activé pour respecter les limites de l'API")
    
    enriched_films = []
    errors = 0
    
    for i, film in enumerate(films, 1):
        try:
            # Enrichir le film
            film_enriched = enrichir_film_avec_api(film)
            # Ajouter le son
            add_sound_to_film(film_enriched)
            enriched_films.append(film_enriched)
            
            # Log progress
            if i % 50 == 0:
                logger.info(f"   📊 Progression: {i}/{total} films ({i*100//total}%)")
            
            # Rate limiting : pause entre chaque requête
            time.sleep(DELAY_BETWEEN_REQUESTS)
            
            # Pause plus longue après chaque batch
            if i % BATCH_SIZE == 0:
                logger.info(f"   ⏸️  Pause de 10 secondes (rate limit)...")
                time.sleep(10)
                
        except Exception as e:
            errors += 1
            logger.warning(f"⚠️  Erreur pour film {film.get('id')} ({film.get('title')}): {e}")
            # Ajouter quand même le film sans enrichissement
            add_sound_to_film(film)
            enriched_films.append(film)
    
    logger.info(f"✅ Enrichissement terminé: {len(enriched_films)} films ({errors} erreurs)")
    
    # Sauvegarder
    logger.info(f"💾 Sauvegarde dans {OUTPUT_FILE}...")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    df = pd.DataFrame(enriched_films)
    # Convertir les listes en string pour le CSV
    if "genres" in df.columns:
        df["genres"] = df["genres"].apply(lambda g: str(g) if g else "[]")
    if "streaming_links" in df.columns:
        df["streaming_links"] = df["streaming_links"].apply(lambda s: str(s) if s else "[]")
    if "streaming_providers" in df.columns:
        df["streaming_providers"] = df["streaming_providers"].apply(lambda s: str(s) if s else "[]")
    
    df.to_csv(OUTPUT_FILE, index=False)
    logger.info(f"✅ Fichier sauvegardé: {OUTPUT_FILE}")
    
    # Statistiques
    films_avec_trailer = sum(1 for f in enriched_films if f.get("trailer_url"))
    films_avec_poster = sum(1 for f in enriched_films if f.get("poster_url"))
    logger.info(f"\n📊 Statistiques:")
    logger.info(f"   - Films avec bande annonce: {films_avec_trailer}/{total}")
    logger.info(f"   - Films avec affiche: {films_avec_poster}/{total}")
    
    return enriched_films


if __name__ == "__main__":
    print("=" * 80)
    print("🎬 ENRICHISSEMENT COMPLET DE TOUS LES FILMS")
    print("=" * 80)
    print()
    print("⚠️  ATTENTION: Ce script va faire ~5000 requêtes à l'API TMDB")
    print("   Temps estimé: 10-15 minutes")
    print("   Assurez-vous d'avoir configuré TMDB_API_KEY")
    print()
    response = input("Continuer? (oui/non): ")
    if response.lower() in ["oui", "o", "yes", "y"]:
        enrichir_tous_films()
    else:
        print("❌ Annulé")

