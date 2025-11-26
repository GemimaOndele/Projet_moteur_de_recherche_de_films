# Fonctionnalités Avancées - MovieMood

## 🎬 Fonctionnalités Implémentées

### 1. **Détection d'émotions par CNN (Webcam/Image)**
- Capture d'image via webcam
- Upload d'image depuis l'ordinateur
- Détection automatique de l'émotion (triste, heureux, stressé, etc.)
- Mise à jour automatique du formulaire avec l'émotion détectée

**Fichiers concernés :**
- `emotion_detection.py` : Module de détection
- `static/js/emotion-detection.js` : Interface webcam
- Route API : `/api/detect-emotion`

### 2. **Sons et Musiques**
- **Sons d'émotion** : Musique correspondant à l'humeur choisie
- **Génériques de films** : Thème officiel de chaque film
- Lecteur audio intégré avec contrôle play/pause

**Structure des fichiers audio :**
```
static/audio/
├── emotion_sad.mp3
├── emotion_stressed.mp3
├── emotion_happy.mp3
├── emotion_nostalgic.mp3
├── emotion_bored.mp3
├── emotion_angry.mp3
└── movie_{id}.mp3 (génériques de films)
```

### 3. **Intégration API TMDB**
- **Affiches de films** : Posters haute qualité
- **Images de bande annonce** : Backdrops pour ambiance
- **Bandes annonces YouTube** : Lecteur intégré dans une modal
- **Liens de streaming** : Accès direct aux plateformes (Netflix, Amazon, etc.)

**Configuration :**
1. Obtenir une clé API sur [TMDB](https://www.themoviedb.org/settings/api)
2. Définir la variable d'environnement : `export TMDB_API_KEY="votre_cle"`
3. Ou modifier directement dans `tmdb_api.py`

### 4. **Design Animé et Immersif**
- **Animations CSS** :
  - Cartes flottantes avec effet de profondeur
  - Transitions fluides au survol
  - Fond animé avec dégradé
  - Effet glow sur le titre
- **Fenêtres flottantes** : Cartes avec animation de flottement
- **Modal pour bandes annonces** : Lecteur vidéo plein écran
- **Transitions** : Animations d'entrée pour chaque carte

### 5. **Expérience Utilisateur Améliorée**
- Interface responsive et moderne
- Feedback visuel immédiat
- Sons contextuels selon l'émotion
- Navigation intuitive
- Design sombre pour une expérience cinématographique

## 🚀 Installation et Utilisation

### Prérequis
```bash
pip install -r requirements.txt
```

### Configuration API TMDB (optionnel)
```bash
export TMDB_API_KEY="votre_cle_api"
```

### Ajouter des fichiers audio

1. **Sons d'émotion** : Placez les fichiers dans `static/audio/` avec les noms :
   - `emotion_sad.mp3`
   - `emotion_stressed.mp3`
   - `emotion_happy.mp3`
   - `emotion_nostalgic.mp3`
   - `emotion_bored.mp3`
   - `emotion_angry.mp3`

2. **Génériques de films** : Nommez les fichiers :
   - `movie_{id}.mp3` (ex: `movie_550.mp3` pour Fight Club)
   - Ou `{titre_slug}.mp3` (ex: `fight_club.mp3`)

### Lancer l'application
```bash
cd code
python app.py
```

Puis ouvrir : `http://localhost:5000`

## 📝 Notes Techniques

### Détection d'émotions
- Actuellement utilise des heuristiques simples (luminosité, contours)
- **Amélioration future** : Intégrer un modèle CNN pré-entraîné (FER2013, AffectNet)
- Nécessite OpenCV et éventuellement TensorFlow

### API TMDB
- Rate limit : 40 requêtes toutes les 10 secondes
- Cache recommandé pour éviter les appels répétés
- Les données sont enrichies à la volée lors de la recherche

### Performance
- Les images sont chargées en lazy loading
- Les sons sont préchargés mais ne jouent qu'à la demande
- Les animations CSS sont optimisées avec GPU acceleration

## 🔮 Améliorations Futures

- [ ] Modèle CNN réel pour détection d'émotions
- [ ] Cache Redis pour les données TMDB
- [ ] Support de plusieurs langues
- [ ] Mode sombre/clair
- [ ] Historique des recherches
- [ ] Recommandations personnalisées basées sur l'historique
- [ ] Partage social des recommandations

