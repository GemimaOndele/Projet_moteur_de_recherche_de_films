# 📦 Guide de Migration et Nettoyage

## ✅ Modifications Effectuées

### 1. Configuration .env
- ✅ Création de `env.template` avec tous les tokens
- ✅ Modification de `app.py` et `tmdb_api.py` pour utiliser `python-dotenv`
- ✅ Plus besoin de variables d'environnement manuelles

### 2. Priorité Hugging Face
- ✅ `app.py` utilise maintenant Hugging Face en **priorité** (allège le projet)
- ✅ Fichier local comme fallback uniquement
- ✅ `USE_HF=true` par défaut dans `.env`

### 3. Nettoyage et Organisation
- ✅ Fichiers de test déplacés dans `tests/`
- ✅ Scripts utilitaires déplacés dans `scripts/utils/`
- ✅ Suppression des fichiers temporaires et inutiles
- ✅ Création de `.gitignore` pour exclure les gros fichiers

## 🚀 Actions à Faire

### 1. Créer le fichier .env

```powershell
copy env.template .env
```

Puis éditez `.env` avec vos vraies clés **(ne les poussez jamais sur GitHub)** :
```env
TMDB_API_KEY=VOTRE_CLE_TMDB_ICI
HF_TOKEN=hf_votre_token_huggingface_ici
HF_DATASET_REPO=Gkop/moviemood-dataset
USE_HF=true
```

### 2. Installer python-dotenv

```powershell
pip install python-dotenv
```

### 3. (Optionnel) Supprimer le fichier CSV local pour alléger

Si vous voulez vraiment alléger le projet et utiliser uniquement Hugging Face :

```powershell
# ATTENTION : Ne faites ça que si Hugging Face fonctionne bien
Remove-Item data\films_enriched_complete.csv
```

Le fichier servira de fallback si Hugging Face est indisponible.

### 4. Vérifier la structure

Votre projet devrait maintenant avoir cette structure :

```
Projet_moteur_de_recherche_de_films/
├── code/              # Code source
├── scripts/utils/     # Scripts utilitaires
├── tests/            # Tests
├── docs/             # Documentation
├── dataset/          # Dataset brut
├── data/             # Données enrichies (fallback)
├── .env              # Configuration (à créer)
├── env.template      # Template de configuration
└── requirements.txt
```

## 📊 Espace Disque Libéré

- ✅ Dossier `dataset/images/` supprimé (152 fichiers)
- ✅ Fichiers de test organisés
- ✅ Scripts organisés
- ✅ Fichiers temporaires supprimés

## ⚠️ Notes Importantes

1. **Le fichier CSV local** (`data/films_enriched_complete.csv`) sert de **fallback**
   - Si Hugging Face est indisponible, le fichier local sera utilisé
   - Pour vraiment alléger, supprimez-le après avoir vérifié que Hugging Face fonctionne

2. **Le cache Hugging Face** peut prendre de l'espace
   - Utilisez `scripts/utils/clean_hf_cache.py` pour nettoyer si besoin

3. **Les tokens** sont maintenant dans `.env` (ne pas commit dans Git)

## 🎯 Résultat

- ✅ Projet allégé (dataset sur Hugging Face)
- ✅ Configuration centralisée dans `.env`
- ✅ Structure organisée
- ✅ Fichiers inutiles supprimés

