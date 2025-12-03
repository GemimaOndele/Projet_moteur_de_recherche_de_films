# 🔧 Solution au Problème Regex dans le Notebook

## ⚠️ Problème

Le module `regex` a un problème d'importation circulaire dans Jupyter lorsqu'on importe les modules du projet qui utilisent `textblob`.

## ✅ Solution : Charger le Dataset Directement

Remplacez le contenu de la cellule de chargement du dataset par ce code :

```python
# Charger le dataset directement depuis le CSV (évite les conflits avec textblob/regex)
import json

dataset_path = project_root / "dataset" / "tmdb_5000_movies.csv"

print(f"📥 Chargement du dataset depuis : {dataset_path}")

# Charger le CSV directement avec pandas
df_raw = pd.read_csv(dataset_path, engine="python", encoding="utf-8", on_bad_lines="skip")

# Convertir en liste de dictionnaires
films = []
for idx, row in df_raw.iterrows():
    # Parser les genres
    genres_str = row.get("genres", "[]")
    try:
        if isinstance(genres_str, str):
            genres_json = json.loads(genres_str.replace("'", '"'))
            genres = [g.get("name", "") for g in genres_json if isinstance(g, dict) and "name" in g]
        else:
            genres = []
    except:
        genres = []
    
    # Extraire l'année
    release_date = str(row.get("release_date", ""))
    release_year = None
    if release_date and len(release_date) >= 4:
        try:
            release_year = int(release_date[:4])
        except:
            pass
    
    film = {
        "id": int(row.get("id", 0)),
        "title": str(row.get("title", "")),
        "overview": str(row.get("overview", "")),
        "genres": genres,
        "vote_average": float(row.get("vote_average", 0.0)) if pd.notna(row.get("vote_average")) else 0.0,
        "vote_count": int(row.get("vote_count", 0)),
        "popularity": float(row.get("popularity", 0.0)) if pd.notna(row.get("popularity")) else 0.0,
        "release_date": release_date,
        "release_year": release_year,
        "budget": float(row.get("budget", 0.0)) if pd.notna(row.get("budget")) else 0.0,
        "revenue": float(row.get("revenue", 0.0)) if pd.notna(row.get("revenue")) else 0.0,
        "runtime": float(row.get("runtime", 0.0)) if pd.notna(row.get("runtime")) else None,
    }
    films.append(film)

# Créer un DataFrame
df = pd.DataFrame(films)

print(f"✅ Dataset chargé : {len(films)} films")
print(f"📋 Colonnes disponibles : {list(df.columns)}")
if len(films) > 0:
    print(f"🎭 Exemple de genres : {films[0]['genres']}")
```

## 📝 Pour les Fonctions du Projet

Pour utiliser les fonctions de recommandation, copiez-les dans le notebook ou importez-les après avoir chargé le dataset directement.

## 🔄 Alternative : Importer les Fonctions Séparément

```python
# Importer seulement les fonctions nécessaires sans textblob
from lib_projet import emotion_to_genres

# Pour recommendation.py, copiez la fonction recommander_par_emotion dans le notebook
```

