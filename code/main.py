# main_gemima.py
# ============================
# Script de test pour la partie de Gémima

import os

from data_loading import charger_films_prepares
from sentiment import ajouter_sentiment_aux_films, sauvegarder_films_sentiment

PATH_CSV_ORIGINE = "tmdb_5000_movies.csv"
PATH_CSV_SORTIE = os.path.join("data", "films_sentiment.csv")


def main():
    os.makedirs("data", exist_ok=True)

    print("[1/3] Chargement et préparation des films...")
    films = charger_films_prepares(PATH_CSV_ORIGINE)
    print(f"    Nombre de films chargés : {len(films)}")

    print("[2/3] Analyse de sentiments sur 'overview'...")
    films = ajouter_sentiment_aux_films(films)

    print("    Exemple de film enrichi :")
    print("    Titre :", films[0]["title"])
    print("    Genres :", films[0]["genres"])
    print("    Sentiment score :", films[0]["sentiment_score"])
    print("    Sentiment label :", films[0]["sentiment_label"])
    print("    Sentiment normalisé :", films[0]["sentiment_score_norm"])

    print("[3/3] Sauvegarde du CSV enrichi...")
    sauvegarder_films_sentiment(films, PATH_CSV_SORTIE)

    print("[TERMINE] Partie Data + Sentiment prête pour la Phase 2.")


if __name__ == "__main__":
    main()
