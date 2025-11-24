# sentiment.py
# ============================
# Module de Gémima : analyse de sentiments
# Utilise la librairie du projet (lib_projet)

from typing import List, Dict
import pandas as pd

from lib_projet import analyser_sentiment_texte, normaliser_sentiment


def ajouter_sentiment_aux_films(liste_films: List[Dict]) -> List[Dict]:
    """
    Parcourt la liste des films et ajoute :
        - sentiment_score (float [-1, 1])
        - sentiment_label ("positif", "neutre", "negatif")
        - sentiment_score_norm (float [0, 1])
    en se basant sur le champ "overview".
    """
    for film in liste_films:
        overview = film.get("overview", "")
        score, label = analyser_sentiment_texte(overview)
        film["sentiment_score"] = score
        film["sentiment_label"] = label
        film["sentiment_score_norm"] = normaliser_sentiment(score)
    return liste_films


def films_vers_dataframe(liste_films: List[Dict]) -> pd.DataFrame:
    """
    Convertit la liste de dictionnaires 'films' en DataFrame pandas.
    """
    df = pd.DataFrame(liste_films)
    return df


def sauvegarder_films_sentiment(liste_films: List[Dict], path_csv_sortie: str):
    """
    Convertit la liste de films enrichis en DataFrame et sauvegarde dans un CSV.
    """
    df = films_vers_dataframe(liste_films)
    df.to_csv(path_csv_sortie, index=False, encoding="utf-8")
    print(f"[OK] Fichier sauvegardé avec sentiments : {path_csv_sortie}")
