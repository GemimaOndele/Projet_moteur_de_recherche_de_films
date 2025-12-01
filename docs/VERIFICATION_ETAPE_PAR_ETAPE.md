# 🧪 Guide Complet de Vérification - Étape par Étape

## ⚠️ PRÉREQUIS

### 1. Clé API TMDB (Gratuite)

Si vous n'avez pas encore de clé:

1. Allez à: https://www.themoviedb.org/settings/api
2. Créez un compte (gratuit)
3. Demandez une clé API
4. Configurez dans PowerShell:

```powershell
$env:TMDB_API_KEY = "votre_clé_ici"
```

### 2. Vérifiez Python

```powershell
python --version
# Doit afficher: Python 3.8+
```

### 3. Dossier Projet

```powershell
cd "c:\Users\gemim\OneDrive\Bureau\M1-cours-Data engineer\Semestre 1\Algorithmique et programmation\Projet\Projet_moteur_de_recherche_de_films"
pwd
# Doit afficher le chemin du projet
```

---

## 🚀 DÉMARRAGE

### Étape 1: Lancer le Serveur Flask

```powershell
# Terminal 1: Lancer l'app
python code/app.py

# Vous devez voir:
# * Serving Flask app 'app'
# * Debug mode: off
# * Running on http://127.0.0.1:5000
# WARNING: This is a development server...
```

**✅ Si vous voyez ce message**: Le serveur est lancé avec succès!

**❌ Si erreur**:
- Vérifiez votre clé API TMDB
- Vérifiez que Python est installé
- Vérifiez le chemin du projet

### Étape 2: Ouvrir le Navigateur

- Ouvrez: **http://localhost:5000**
- Vous voyez: Page d'accueil MovieMood

---

## 🎬 TEST 1: Description en Français

### Étape 1: Sélectionner une Émotion

1. Sur la page d'accueil
2. Cherchez: `💭 Votre émotion du moment`
3. Sélectionnez: **😊 Heureux**

### Étape 2: Rechercher un Film

1. Entrez dans `🎥 Titre de film`:
   - **Inception** (film populaire avec descriptions)
   
2. Cliquez: **🔍 Chercher / Recommander**

### Étape 3: Vérifier la Description

Regardez la première carte film:

```
✅ ATTENDU:
- Titre: "Inception"
- Genre: Science-Fiction, Thriller, Mystère
- Description: Commence par "Un voleur spécialisé..."
  → Texte EN FRANÇAIS ✅

❌ PROBLÈME:
- Description commence par "A skilled thief..."
  → Texte EN ANGLAIS ❌
```

**Si Description EN FRANÇAIS**: ✅ TEST RÉUSSI!

**Si Description EN ANGLAIS**:
1. Ouvrez Console: **F12**
2. Tab: **Console**
3. Cherchez erreurs (texte rouge)
4. Notez l'erreur

---

## 🎵 TEST 2: Animation du Son

### Étape 1: Localiser le Bouton Son

Sur la page de résultats, en haut:
```
😊 Recommandations pour l'émotion: Heureux
[🎵 Écouter l'ambiance]  ← BOUTON ICI
```

### Étape 2: Tester Play/Pause

1. Cliquez sur **🎵 Écouter l'ambiance**
2. Le bouton doit changer en: **⏸ Arrêter**
3. En dessous du bouton, vous devez voir:
   ```
   ▌ ▌ ▌ ▌ ▌    ← 5 barres animées
   ```

### Étape 3: Vérifier Animation

**✅ ATTENDU**:
- Les 5 barres bougent (montent et descendent)
- Animation lisse et continue
- Durée: ~0.4 secondes par cycle

**❌ PROBLÈME - Barres statiques**:
1. F12 → Elements
2. Cherchez: `class="audio-visualizer"`
3. Cherchez les 5 `<div class="visualizer-bar"></div>`
4. Si absent: problème HTML
5. Si présent: problème CSS animation

**❌ PROBLÈME - Pas de son**:
- Vérifiez volume navigateur (pas de son = c'est normal si fichiers non présents)
- Vérifiez dossier: `code/static/audio/sounds/emotion_heureux.mp3`

**Si Animation Visible**: ✅ TEST RÉUSSI!

---

## 🎬 TEST 3: Bande Annonce

### Étape 1: Trouver le Bouton Trailer

Sur chaque carte film, cherchez:
```
┌─────────────────────┐
│  [POSTER]     ▶️    │  ← Ce bouton Play
│                     │
└─────────────────────┘
```

OU dans la description:
```
[🎬 Bande annonce]
```

### Étape 2: Cliquer sur Play

Cliquez sur le **▶️** ou le bouton **🎬**

### Étape 3: Vérifier la Modal

**✅ ATTENDU**:
- Une fenêtre noire s'ouvre au centre
- Elle contient: YouTube iframe
- La vidéo se joue automatiquement
- Titre du film s'affiche
- Bouton ✕ en haut à droite

**Pour fermer la modal**:
- Méthode 1: Cliquez le bouton **✕**
- Méthode 2: Appuyez **Échap**
- Méthode 3: Cliquez en dehors (noir)

**❌ Si rien ne se passe**:
1. Vérifiez: ce film a-t-il un trailer sur TMDB?
   - Essayez "Avatar", "Inception", "Interstellar"
2. F12 → Console: cherchez erreurs JavaScript

**Si Modal s'Ouvre**: ✅ TEST RÉUSSI!

---

## 🖼️ TEST 4: Images Officielles

### Étape 1: Vérifier le Poster

Sur chaque carte film:
```
┌─────────────────────┐
│   [IMAGE AFFICHE]   │  ← Poster du film
│   [3-4 pouces x 6]  │     (doit être visible)
└─────────────────────┘
```

**✅ ATTENDU**:
- Image bien définie
- Logo/titre du film visible
- Couleurs vives et claires
- Source: TMDB CDN

### Étape 2: Vérifier le Backdrop

Au-dessus/derrière le poster:
```
[ARRIÈRE-PLAN FLOU]  ← Image de fond
[Image affiche]      ← Poster par-dessus
```

**✅ ATTENDU**:
- Image de fond visible
- Flou subtil
- Couleurs coordonnées au film

**❌ Si pas d'images**:
1. Vérifiez: F12 → Network
2. Cherchez: `image.tmdb.org`
3. Devrait y avoir des requêtes d'images
4. Si 0 requête: problème récupération données

**Si Images Visibles**: ✅ TEST RÉUSSI!

---

## 📺 TEST 5: Liens Streaming

### Étape 1: Scrollez sur une Carte

Scrollez vers le bas de la carte film:
```
Titre: Inception
Genre: Sci-Fi
Description: ...
Rating: 8.8/10
📺 OÙ REGARDER:  ← Section ici
  [Netflix] [Prime Video] [Disney+]
```

### Étape 2: Vérifier Présence

**✅ ATTENDU**:
- Logos des plateformes visibles
- Noms des services (Netflix, Prime, etc)
- Badges: Abonnement, Location, Achat
- France: Filtrée pour votre région

**❌ Si rien n'apparaît**:
1. Vérifiez: F12 → Network
2. Cherchez: requête API `watch/providers`
3. Vérifiez réponse JSON
4. Film a-t-il des données streaming en France?
   - Essayez "Avatar" qui a plus de plateformes

**Si Streaming Visible**: ✅ TEST RÉUSSI!

---

## 😊 TEST 6: Sons Émotions

### Étape 1: Revenir à l'Accueil

Cliquez: **← Retour** ou **Accueil**

### Étape 2: Tester Différentes Émotions

Pour CHAQUE émotion:

1. Sélectionnez: `💭 Votre émotion du moment`
   - Heureux (😊)
   - Triste (😢)
   - Stressé (😰)
   - etc...

2. Faites une recherche

3. Vérifiez:
   - Emoji correct en header
   - Couleur correcte
   - Son joue quand cliquez 🎵

**✅ ATTENDU**:
```
😊 Heureux: Jaune + Son heureux
😢 Triste: Bleu + Son triste
😰 Stressé: Orange + Son stressé
... etc
```

**❌ Si couleur incorrecte**:
- Vérifiez: `code/static/css/style.css`
- Cherchez: `.emotion-color-heureux { color: yellow }`

**Si Sons Jouent**: ✅ TEST RÉUSSI!

---

## ✨ TEST 7: Réactions Visuelles

### Étape 1: Observer l'Header

Après chaque recherche, regardez le header:
```
┌─────────────────────────────────────────────┐
│  😊 Recommandations pour: Heureux            │
│  Background jaune, texte blanc               │
│  [🎵 Écouter l'ambiance]                    │
└─────────────────────────────────────────────┘
```

### Étape 2: Vérifier Changements

**✅ ATTENDU - Heureux (😊)**:
- Emoji: 😊
- Couleur: Jaune pâle
- Ton: Positif

**✅ ATTENDU - Triste (😢)**:
- Emoji: 😢
- Couleur: Bleu pâle
- Ton: Mélancolique

**✅ ATTENDU - Stressé (😰)**:
- Emoji: 😰
- Couleur: Orange
- Ton: Urgent

**Si Réactions Visibles**: ✅ TEST RÉUSSI!

---

## 🔍 TESTS CONSOLE (F12)

### Ouvrir la Console

1. Appuyez: **F12**
2. Allez à l'onglet: **Console**

### Chercher les Erreurs

**✅ NORMAL** (pas d'erreur):
```
Console vide ou avec warnings jaunis (ignorez-les)
```

**❌ PROBLÈME** (erreur rouge):
```
Uncaught TypeError: Cannot read property 'X' of undefined
CORS error: Access denied...
```

Si vous voyez des erreurs rouges:
1. **Notez** le message exact
2. **Vérifiez** que les scripts se chargent:
   - Onglet: **Network**
   - Cherchez: `fix-features.js`
   - Doit avoir status: **200**

---

## 📊 RÉSULTATS

### Complétez le Checklist

```
□ Description EN FRANÇAIS ✅
□ Animation Son (visualiseur) ✅
□ Bande Annonce Modal ✅
□ Images Officielles ✅
□ Liens Streaming ✅
□ Sons Émotions ✅
□ Réactions Visuelles ✅
□ Pas d'erreurs Console ✅
```

**Si 8/8 cochés**: 🎉 **SUCCÈS TOTAL!**

---

## 🐛 DÉPANNAGE AVANCÉ

### Problème: Description Reste Anglaise

**Étape 1**: Vérifiez Internet
```powershell
# Test MyMemory API
Invoke-WebRequest -Uri "https://api.mymemory.translated.net/get?q=Hello&langpair=en|fr"
# Doit retour JSON avec traduction
```

**Étape 2**: Vérifiez les Logs Flask
```
Terminal où app.py s'exécute:
Cherchez: "translat" ou "Traceback"
```

**Étape 3**: Force Refresh
```
F12 → Storage (ou Application tab)
Clear All → Reload page
```

### Problème: Pas de Visuel Animé

**Étape 1**: Vérifiez CSS chargé
```
F12 → Elements
Cherchez: <style> pour visualize keyframe
```

**Étape 2**: Vérifiez HTML structure
```
F12 → Elements
Cherchez: <div class="audio-visualizer">
      <div class="visualizer-bar"></div> ×5
```

**Étape 3**: Vérifiez JavaScript chargé
```
F12 → Sources
Cherchez: fix-features.js dans la liste
Doit avoir content (pas vide)
```

### Problème: Erreur "TMDB API Key Invalid"

**Solution**:
```powershell
# Vérifiez la clé
$env:TMDB_API_KEY
# Doit retourner votre clé

# Testez l'API
Invoke-WebRequest -Uri "https://api.themoviedb.org/3/movie/550?api_key=$env:TMDB_API_KEY"
# Doit retourner JSON film
```

---

## 📱 Test Mobile (Optionnel)

Pour tester sur téléphone:

1. Trouvez votre IP locale:
```powershell
ipconfig
# Cherchez: IPv4 Address (ex: 192.168.1.100)
```

2. Accédez depuis téléphone:
```
http://192.168.1.100:5000
# Doit afficher le site mobile-friendly
```

---

## ✅ CONCLUSION

**Si tous les tests passent**:
- 🎬 Descriptions EN FRANÇAIS ✅
- 🎵 Animations son ✅
- 🎞️ Trailers YouTube ✅
- 🖼️ Images officielles ✅
- 📺 Liens streaming ✅
- 😊 Sons émotions ✅
- ✨ Réactions visuelles ✅

**Vous avez un système COMPLET et FONCTIONNEL!** 🚀

---

## 📞 Questions?

Si un test échoue:
1. **Relisez** les instructions du test
2. **Vérifiez** les prérequis
3. **Consultez** la section Dépannage
4. **Ouvrez** F12 → Console pour erreurs

Bon test! 🎬✨

