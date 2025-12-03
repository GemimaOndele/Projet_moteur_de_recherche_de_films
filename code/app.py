"""Application Flask : formulaire titre + émotion + page de résultats avec fonctionnalités avancées."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional
import logging
import os

import pandas as pd
from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from data_loading import charger_films_prepares
from emotion_detection import detecter_emotion_image, image_base64_to_bytes
from recommendation import rechercher_par_titre, recommander_par_emotion
from sentiment import ajouter_sentiment_aux_films
from sound_manager import add_sound_to_film, get_emotion_sound
from tmdb_api import enrichir_film_avec_api, enrichir_liste_films
from cache_manager import get_cached_films, cache_films

# Charger les variables d'environnement depuis .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATA_DIR = BASE_DIR / "data"
DATA_ENRICHED = DATA_DIR / "films_sentiment.csv"
DATA_ENRICHED_COMPLETE = DATA_DIR / "films_enriched_complete.csv"
DATASET_TMBD = BASE_DIR / "dataset" / "tmdb_5000_movies.csv"

# Configuration Hugging Face (depuis .env)
HF_REPO_NAME = os.getenv("HF_DATASET_REPO", "Gkop/moviemood-dataset")
USE_HUGGINGFACE = os.getenv("USE_HF", "true").lower() == "true"  # Par défaut activé pour alléger le projet

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Clé secrète pour les sessions (à surcharger en prod via variable d'environnement)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max pour les uploads

# ===== Configuration base de données (SQLite simple) =====
DB_PATH = BASE_DIR / "data" / "users.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    """Utilisateur pour l'authentification."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


# S'assurer que le dossier data existe pour la base
DATA_DIR.mkdir(parents=True, exist_ok=True)
with app.app_context():
    db.create_all()


def _charger_depuis_huggingface() -> Optional[List[Dict]]:
    """Charge le dataset depuis Hugging Face (priorité pour alléger le projet)."""
    if not USE_HUGGINGFACE:
        logger.info("💡 Hugging Face désactivé dans .env")
        return None
    
    try:
        from datasets import load_dataset
        logger.info(f"📥 Chargement depuis Hugging Face: {HF_REPO_NAME}")
        logger.info("   💡 Utilisation du dataset distant pour alléger le projet local")
        
        # Charger depuis Hugging Face
        dataset = load_dataset(HF_REPO_NAME, split="train")
        df = dataset.to_pandas()
        films = df.to_dict(orient="records")
        
        # Convertir les genres de string en liste si nécessaire
        for film in films:
            if isinstance(film.get("genres"), str):
                try:
                    import ast
                    film["genres"] = ast.literal_eval(film["genres"])
                except Exception:
                    film["genres"] = []
        
        logger.info(f"✅ {len(films)} films chargés depuis Hugging Face")
        return films
    except Exception as e:
        error_msg = str(e)
        logger.warning(f"⚠️  Impossible de charger depuis Hugging Face: {e}")
        logger.info("   💡 Fallback vers fichier local si disponible")
        return None


def _charger_catalogue() -> List[Dict]:
    """Charge les films enrichis depuis Hugging Face (priorité) ou fichier local (fallback)."""
    
    # 1. PRIORITÉ : Hugging Face (pour alléger le projet)
    films = _charger_depuis_huggingface()
    if films:
        return films
    
    # 2. Fallback : fichier local enrichi (si Hugging Face indisponible)
    if DATA_ENRICHED_COMPLETE.exists():
        logger.info(f"📥 Fallback: Chargement depuis fichier local: {DATA_ENRICHED_COMPLETE}")
        logger.info("   💡 Pour alléger le projet, utilisez Hugging Face (configurez .env)")
        df = pd.read_csv(DATA_ENRICHED_COMPLETE)
        films = df.to_dict(orient="records")
        # Convertir les genres de string en liste si nécessaire
        for film in films:
            if isinstance(film.get("genres"), str):
                try:
                    import ast
                    film["genres"] = ast.literal_eval(film["genres"])
                except Exception:
                    film["genres"] = []
        logger.info(f"✅ {len(films)} films chargés depuis fichier local enrichi")
        return films
    
    # 3. Si cache enrichi partiel existe, l'utiliser
    if DATA_ENRICHED.exists():
        logger.info(f"📥 Chargement depuis cache partiel: {DATA_ENRICHED}")
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
        logger.info(f"✅ {len(films)} films chargés depuis cache partiel")
        return films

    # 4. Fallback: charger le CSV brut (sans enrichissement complet)
    logger.info("📥 Chargement depuis CSV brut (fallback)...")
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
        add_sound_to_film(film)
    
    logger.warning("⚠️  Dataset non enrichi - utilisez enrich_all_films.py pour enrichir tous les films")
    logger.info(f"✅ {len(films)} films chargés (non enrichis)")

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
    """Enrichit les films avec API TMDB et sons (avec cache pour optimiser les performances)."""
    if not films:
        return []
    
    # Séparer les films en cache et ceux à enrichir
    films_cached, films_to_enrich = get_cached_films(films)
    
    logger.info(f"📦 {len(films_cached)} films depuis le cache, {len(films_to_enrich)} à enrichir")
    
    # Enrichir uniquement les films qui ne sont pas en cache
    if films_to_enrich:
        try:
            films_enriched_new = []
            for film in films_to_enrich:
                try:
                    film_enriched = enrichir_film_avec_api(film)
                    films_enriched_new.append(film_enriched)
                except Exception as e:
                    logger.warning(f"⚠️ Erreur enrichissement film {film.get('id')}: {e}")
                    films_enriched_new.append(film)
            
            # Mettre en cache les nouveaux films enrichis
            cache_films(films_enriched_new)
            
            # Combiner avec les films en cache
            films = films_cached + films_enriched_new
        except Exception as e:
            logger.warning(f"⚠️ Erreur enrichissement TMDB: {e}")
            films = films_cached + films_to_enrich
    else:
        films = films_cached
    
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


# Charger le catalogue avec message de progression
logger.info("🚀 Initialisation de l'application...")
logger.info("📥 Chargement du catalogue de films (cela peut prendre quelques secondes)...")
catalogue_films = _charger_catalogue()
logger.info(f"✅ Catalogue chargé : {len(catalogue_films)} films disponibles")
logger.info("🌐 Application prête à recevoir les requêtes")


@app.get("/")
def auth_form():
    """
    Première page affichée : formulaire connexion / inscription.
    Cette vue doit rendre ton fichier `form.html` (à placer dans le dossier `templates/`).
    """
    return render_template("form.html")


@app.post("/login")
def login():
    """
    Connexion de l'utilisateur contre la base SQL.
    """
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""

    if not email or not password:
        return render_template(
            "form.html",
            error_login="Veuillez remplir email et mot de passe.",
            active_tab="login",
        )

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return render_template(
            "form.html",
            error_login="Email ou mot de passe incorrect.",
            active_tab="login",
        )

    # Auth OK : on stocke l'id utilisateur dans la session
    session["user_id"] = user.id
    session["user_email"] = user.email
    session["user_name"] = user.name
    return redirect(url_for("movie_mood"))


@app.post("/signup")
def signup():
    """
    Inscription : création de l'utilisateur dans la base SQL.
    """
    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    confirm = request.form.get("confirm_password") or ""

    if not email or not password or not confirm or not name:
        return render_template(
            "form.html",
            error_signup="Veuillez remplir tous les champs.",
            active_tab="signup",
        )

    if password != confirm:
        return render_template(
            "form.html",
            error_signup="Les mots de passe ne correspondent pas.",
            active_tab="signup",
        )

    # Vérifier que l'utilisateur n'existe pas déjà
    if User.query.filter_by(email=email).first():
        return render_template(
            "form.html",
            error_signup="Un compte existe déjà avec cet email.",
            active_tab="signup",
        )

    # Créer l'utilisateur
    user = User(email=email, name=name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # Connexion automatique après inscription
    session["user_id"] = user.id
    session["user_email"] = user.email
    session["user_name"] = user.name
    return redirect(url_for("movie_mood"))


@app.get("/logout")
def logout():
    """Déconnexion de l'utilisateur, retour au formulaire."""
    session.clear()
    return redirect(url_for("auth_form"))


@app.get("/movie-mood")
def movie_mood():
    """
    Page principale MovieMood (ancienne page d'accueil).
    Accessible uniquement si l'utilisateur est connecté.
    """
    if "user_id" not in session:
        return redirect(url_for("auth_form"))
    return render_template("index.html")


@app.get("/search")
def search():
    # Protection : uniquement pour utilisateur connecté
    if "user_id" not in session:
        return redirect(url_for("auth_form"))

    titre = request.args.get("titre", "").strip()
    emotion = request.args.get("emotion", "").strip().lower()

    resultats: List[Dict] = []

    if titre:
        film = rechercher_par_titre(titre, catalogue_films)
        if film:
            resultats.append(film)

    if emotion:
        resultats.extend(recommander_par_emotion(emotion, catalogue_films, n=20))

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
    if "user_id" not in session:
        return jsonify({"error": "Non autorisé. Veuillez vous connecter."}), 401
    if 'image' not in request.files:
        return jsonify({"error": "Aucune image fournie"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Fichier vide"}), 400

    try:
        image_data = file.read()
        result = detecter_emotion_image(image_data)
        
        # Retourner toutes les informations (emotion, face_bbox, quality, confidence)
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Erreur détection émotion: {e}")
        return jsonify({
            "error": str(e),
            "emotion": None,
            "face_bbox": None,
            "quality": {
                "brightness": 0,
                "brightness_status": "erreur",
                "face_detected": False,
                "face_size_ratio": 0,
                "messages": [f"❌ Erreur: {str(e)}"]
            },
            "confidence": 0.0
        }), 500


if __name__ == "__main__":
    logger.info("🌐 Application démarrée. Ouvrez votre navigateur sur http://localhost:5000")
    logger.info("💡 La détection d'émotion par webcam fonctionne uniquement sur http://localhost:5000 ou en HTTPS.")
    app.run(debug=True, host="0.0.0.0", port=5000)
