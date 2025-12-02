# 🚀 Configuration Rapide

## 1. Installer les dépendances

```powershell
pip install -r requirements.txt
```

## 2. Créer le fichier .env

```powershell
copy env.template .env
```

Puis éditez `.env` avec vos clés :

```env
TMDB_API_KEY=VOTRE_CLE_TMDB_ICI
HF_TOKEN=hf_votre_token_huggingface_ici
HF_DATASET_REPO=Gkop/moviemood-dataset
USE_HF=true
```

## 3. Lancer l'application

```powershell
python code/app.py
```

L'app chargera automatiquement le dataset depuis Hugging Face (allège le projet local).

## 📦 Structure Propre

- ✅ **Code source** : `code/`
- ✅ **Scripts utilitaires** : `scripts/utils/`
- ✅ **Tests** : `tests/`
- ✅ **Documentation** : `docs/`
- ✅ **Dataset brut** : `dataset/` (CSV uniquement)
- ✅ **Données enrichies** : Sur Hugging Face (fallback local dans `data/`)

## 💡 Avantages

- ✅ **Projet allégé** : Dataset sur Hugging Face
- ✅ **Configuration centralisée** : Tous les tokens dans `.env`
- ✅ **Structure organisée** : Fichiers à leur place
- ✅ **Fichiers inutiles supprimés** : Plus d'espace disque

