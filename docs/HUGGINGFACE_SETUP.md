# ☁️ Hébergement du Dataset sur Hugging Face

Ce guide explique comment enrichir TOUS les films et les héberger sur Hugging Face pour alléger le projet.

## 📋 Prérequis

1. **Clé API TMDB** configurée :
```powershell
$env:TMDB_API_KEY = "votre_cle_api"
```

2. **Installer les dépendances** :
```powershell
pip install datasets huggingface_hub
```

3. **Token Hugging Face** (obtenez-le sur https://huggingface.co/settings/tokens)

## 🚀 Étapes

### Étape 1 : Enrichir TOUS les films

Ce script va enrichir **tous les ~5000 films** avec :
- ✅ Bandes annonces YouTube
- ✅ Affiches et images de fond
- ✅ Descriptions en français
- ✅ Liens de streaming
- ✅ Durée, budget, revenus

**Temps estimé : 10-15 minutes** (avec rate limiting pour respecter l'API TMDB)

```powershell
python code/enrich_all_films.py
```

Le fichier sera sauvegardé dans : `data/films_enriched_complete.csv`

### Étape 2 : Uploader sur Hugging Face

```powershell
# Option 1 : Token via variable d'environnement
$env:HF_TOKEN = "votre_token_huggingface"
python code/upload_to_huggingface.py

# Option 2 : Le script vous demandera le token
python code/upload_to_huggingface.py
```

Le dataset sera disponible sur : `https://huggingface.co/datasets/moviemood-dataset`

### Étape 3 : Utiliser le dataset depuis Hugging Face

Modifiez votre `.env` ou variables d'environnement :

```powershell
$env:USE_HF = "true"
$env:HF_DATASET_REPO = "moviemood-dataset"  # Optionnel, par défaut
```

Puis relancez l'app :

```powershell
python code/app.py
```

L'app chargera automatiquement depuis Hugging Face en priorité ! 🎉

## 📊 Ordre de chargement (priorité)

1. **Hugging Face** (si `USE_HF=true`)
2. **Fichier local enrichi complet** (`data/films_enriched_complete.csv`)
3. **Cache partiel** (`data/films_sentiment.csv`)
4. **CSV brut** (fallback, non enrichi)

## 💡 Avantages

- ✅ **Tous les films enrichis** (pas seulement 50)
- ✅ **Toutes les bandes annonces** disponibles
- ✅ **Projet allégé** (pas besoin du gros CSV local)
- ✅ **Partage facile** du dataset
- ✅ **Mise à jour centralisée**

## ⚠️ Notes

- Le script d'enrichissement respecte les rate limits de l'API TMDB
- En cas d'erreur, le script continue avec les autres films
- Vous pouvez relancer l'enrichissement si besoin (il écrasera le fichier)

## 🔧 Personnalisation

Pour changer le nom du repo Hugging Face, modifiez `REPO_NAME` dans `code/upload_to_huggingface.py` ou utilisez la variable d'environnement `HF_DATASET_REPO`.

