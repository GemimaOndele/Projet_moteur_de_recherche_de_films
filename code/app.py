"""Application Flask : formulaire titre + émotion + page de résultats."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import pandas as pd
from flask import Flask, render_template, request

from data_loading import charger_films_prepares
from recommendation import rechercher_par_titre, recommander_par_emotion
from sentiment import ajouter_sentiment_aux_films

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_ENRICHED = DATA_DIR / "films_sentiment.csv"
DATASET_TMBD = BASE_DIR / "dataset" / "tmdb_5000_movies.csv"

app = Flask(__name__)


def _charger_catalogue() -> List[Dict]:
    """Charge les films enrichis s'ils existent, sinon fallback vers le CSV brut."""
    if DATA_ENRICHED.exists():
        df = pd.read_csv(DATA_ENRICHED)
        films = df.to_dict(orient="records")
        return films

    # Fallback : re-construire les films et appliquer l'analyse de sentiments.
    films = charger_films_prepares(str(DATASET_TMBD))
    films = ajouter_sentiment_aux_films(films)
    return films


def _dedupe_films(films: List[Dict]) -> List[Dict]:
    seen = set()
    uniques = []
    for film in films:
        film_id = film.get("id")
        if film_id in seen:
            continue
        seen.add(film_id)
        uniques.append(film)
    return uniques


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

    return render_template("results.html", titre=titre, emotion=emotion, films=resultats)


if __name__ == "__main__":
    app.run(debug=True)
