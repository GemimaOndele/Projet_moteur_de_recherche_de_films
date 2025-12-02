# ⚡ Quick Start - Guide Complet

## 🎯 Démarrage en 3 Étapes

### 1. Installation

```powershell
pip install -r requirements.txt
```

### 2. Configuration

Créez `.env` depuis le template :

```powershell
copy env.template .env
```

Éditez `.env` avec vos clés :
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

---

## ✅ Fonctionnalités

| Feature | Status |
|---------|--------|
| 📝 Descriptions en français | ✅ |
| 🎵 Visualiseur Audio Animé | ✅ |
| 🎬 Trailers YouTube | ✅ |
| 🖼️ Images TMDB | ✅ |
| 📺 Liens Streaming | ✅ |
| 😊 Sons 8 Émotions | ✅ |
| ✨ Bulles Émojis Animées | ✅ |

---

## 😊 Les 8 Émotions

| Emotion | Emoji | Son |
|---------|-------|-----|
| Heureux | 😊 | emotion_happy.mp3 |
| Triste | 😢 | emotion_sad.mp3 |
| Stressé | 😰 | emotion_stressed.mp3 |
| Nostalgique | 🥰 | emotion_nostalgic.mp3 |
| Ennuyé | 😑 | emotion_bored.mp3 |
| Colère | 😠 | emotion_angry.mp3 |
| Peur | 😨 | emotion_fear.mp3 |
| Surprise | 😲 | emotion_surprise.mp3 |

---

## 📁 Structure du Projet

```
Projet_moteur_de_recherche_de_films/
├── code/              # Code source
├── scripts/utils/     # Scripts utilitaires
├── tests/            # Tests
├── docs/             # Documentation
├── dataset/          # Dataset brut
└── data/             # Fallback local (optionnel)
```

---

## 💡 Utilisation

1. **Sélectionnez une émotion** dans le menu déroulant
2. **Entrez un titre** (optionnel)
3. **Cliquez sur "Chercher"**
4. **Profitez** des recommandations avec bandes annonces, images, etc.

---

## 🔧 Dépannage

| Problème | Solution |
|----------|----------|
| Erreur API | Vérifiez `.env` avec vos clés |
| Pas de son | Vérifiez les fichiers dans `code/static/audio/sounds/` |
| Dataset non chargé | Vérifiez `USE_HF=true` dans `.env` |

---

## 📚 Documentation Complète

- **Architecture** : `docs/ARCHITECTURE_FINAL.md`
- **Tests** : `docs/TEST_GUIDE.md`
- **Hugging Face** : `docs/HUGGINGFACE_SETUP.md`

---

**Status**: ✅ Prêt à l'emploi
