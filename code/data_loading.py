# data_loading.py
# ============================
# Module de Gémima : chargement et préparation des données films
# Utilise la librairie du projet (lib_projet)

import pandas as pd
from lib_projet import parser_genres, get_main_genre, extraire_annee


def charger_dataframe(path_csv: str) -> pd.DataFrame:
    """
    Charge le fichier CSV TMDB en DataFrame pandas.
    """
    df = pd.read_csv(path_csv)
    return df


def construire_liste_films(df: pd.DataFrame):
    """
    Construit une liste de dictionnaires 'film' à partir du DataFrame brut.

    Chaque film est représenté sous la forme :
        {
            "id": int,
            "title": str,
            "genres": [str, ...],
            "main_genre": str ou None,
            "overview": str,
            "vote_average": float,
            "popularity": float,
            "release_year": int ou None
        }
    """
    films = []

    for _, row in df.iterrows():
        genres_list = parser_genres(row.get("genres", ""))

        film = {
            "id": int(row["id"]),
            "title": str(row["title"]),
            "genres": genres_list,
            "main_genre": get_main_genre(genres_list),
            "overview": str(row.get("overview", "")),
            "vote_average": float(row.get("vote_average", 0.0)),
            "popularity": float(row.get("popularity", 0.0)),
            "release_year": extraire_annee(row.get("release_date", "")),
        }
        films.append(film)

    return films


def charger_films_prepares(path_csv: str):
    """
    Étape 1 pour Gémima :
    - charge le CSV brut TMDB
    - construit une liste de films avec :
        - genres sous forme de liste
        - main_genre
        - overview
        - vote_average, popularity
        - release_year
    """
    df = charger_dataframe(path_csv)
    films = construire_liste_films(df)
    return films
