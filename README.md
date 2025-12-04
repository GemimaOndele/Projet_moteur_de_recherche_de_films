# 🎬 MovieMood - Moteur de Recherche de Films par Émotion

Application Flask de recommandation de films basée sur les émotions de l'utilisateur.

## 🚀 Démarrage Rapide

### 1. Installation

```powershell
#Création de votre propre environnement virtuel de travail pour enregistrer l'installation des extentions, des librairies du projet.
python -m venv .moteur

#Installation des librairies du projet
pip install -r requirements.txt
```

### 2. Configuration

Copiez `env.template` vers `.env` et remplissez vos clés API :

```powershell
copy env.template .env
```

Éditez `.env` :

```env
TMDB_API_KEY=votre_cle_tmdb
HF_TOKEN=votre_token_huggingface
HF_DATASET_REPO=Gkop/moviemood-dataset
USE_HF=true
```

### 3. Lancer l'application

```powershell
python code/app.py
```

Ouvrez http://localhost:5000 dans votre navigateur.

## 📁 Structure du Projet

```
Projet_moteur_de_recherche_de_films/
├── code/                    # Code source principal
│   ├── app.py              # Application Flask
│   ├── data_loading.py     # Chargement des données
│   ├── emotion_detection.py
│   ├── recommendation.py
│   ├── sentiment.py
│   ├── sound_manager.py
│   ├── tmdb_api.py
│   ├── static/            # Assets (CSS, JS, audio)
│   └── templates/         # Templates HTML
├── scripts/                # Scripts utilitaires
│   └── utils/             # Scripts d'enrichissement et upload
├── tests/                  # Tests
├── docs/                   # Documentation
├── dataset/                # Dataset brut (CSV)
├── data/                   # Données enrichies (optionnel, fallback)
├── .env                    # Configuration (créer depuis env.template)
└── requirements.txt
```

## ☁️ Dataset sur Hugging Face

Le dataset enrichi est hébergé sur Hugging Face pour alléger le projet local.

- **Dataset** : https://huggingface.co/datasets/Gkop/moviemood-dataset
- **4803 films** enrichis avec bandes annonces, images, descriptions en français

Pour utiliser le dataset local (fallback), mettez `USE_HF=false` dans `.env`.

## 🛠️ Scripts Utilitaires

### Enrichir tous les films

```powershell
python scripts/utils/enrich_all_films.py
```

### Uploader sur Hugging Face

```powershell
python scripts/utils/upload_to_huggingface.py
```

### Nettoyer le cache Hugging Face

```powershell
python scripts/utils/clean_hf_cache.py
```

## 📚 Documentation

Voir le dossier `docs/` pour la documentation complète.

## 🎯 Fonctionnalités

- ✅ Détection d'émotion (webcam ou upload)
- ✅ Recommandations par émotion
- ✅ Recherche par titre
- ✅ Bandes annonces YouTube
- ✅ Images TMDB
- ✅ Descriptions en français
- ✅ Liens de streaming
- ✅ Sons d'émotion

## 📝 Notes

- Le dataset est chargé depuis Hugging Face par défaut (allège le projet)
- Les fichiers locaux dans `data/` servent de fallback
- Configurez `.env` avec vos clés API pour utiliser toutes les fonctionnalités
