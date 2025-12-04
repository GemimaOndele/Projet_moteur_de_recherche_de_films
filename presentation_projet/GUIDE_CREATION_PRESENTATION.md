# 🎨 Guide de Création de la Présentation MovieMood

## 📋 Checklist pour Canva/PowerPoint

### ✅ Préparation

- [ ] Créer un compte Canva (gratuit) ou utiliser PowerPoint
- [ ] Choisir un template "présentation" ou créer à partir de zéro
- [ ] Télécharger les logos/icônes nécessaires
- [ ] Préparer les captures d'écran de l'application
- [ ] Préparer les graphiques du notebook d'évaluation

---

## 🎨 Design & Visuels

### Palette de Couleurs Recommandée

**Option 1 : Cinématographique (Recommandé)**
```
Primaire (fond) : #0F0F0F (Noir profond)
Secondaire : #1A1A2E (Bleu foncé)
Accent : #E94560 (Rouge/Rose)
Texte : #FFFFFF (Blanc)
Texte secondaire : #B8B8B8 (Gris clair)
```

**Option 2 : Moderne & Professionnel**
```
Primaire : #2C3E50 (Bleu foncé)
Secondaire : #3498DB (Bleu clair)
Accent : #E74C3C (Rouge)
Texte : #FFFFFF
Texte secondaire : #ECF0F1 (Gris très clair)
```

**Option 3 : Doux & Accueillant**
```
Primaire : #667EEA (Violet)
Secondaire : #764BA2 (Violet foncé)
Accent : #F093FB (Rose)
Texte : #FFFFFF
Texte secondaire : #F7F7F7
```

### Polices Recommandées

**Titres :**
- Montserrat (Bold)
- Poppins (Bold)
- Bebas Neue

**Corps de texte :**
- Open Sans
- Roboto
- Lato

### Éléments Visuels à Ajouter

1. **Icônes** (gratuites sur Flaticon, Icons8)
   - 🎬 Film
   - 😊 Émotions
   - 🧠 IA/Brain
   - 📊 Graphiques
   - 💻 Code

2. **Captures d'écran**
   - Page d'accueil
   - Page de résultats
   - Détails d'un film
   - Détection faciale (si disponible)

3. **Graphiques du Notebook**
   - Distribution des notes
   - Top genres
   - Matrice de confusion
   - Performance des recommandations

4. **Schémas**
   - Architecture du système
   - Flux de données
   - Pipeline de traitement

---

## 📐 Structure des Slides (Canva Template)

### SLIDE 1 : Page de Titre

**Layout :** Centré avec image de fond

**Éléments :**
```
┌─────────────────────────────────────┐
│                                     │
│         [IMAGE DE FOND]             │
│      (cinéma/pellicule film)        │
│                                     │
│          🎬 MovieMood               │
│                                     │
│  Plateforme Web IA de               │
│  Recommandation de Films            │
│  par Émotion                        │
│                                     │
│  Gémima ONDELE POURU                │
│  Fatoumata BAH                      │
│  Hector KOMBOU                      │
│                                     │
└─────────────────────────────────────┘
```

**Style :**
- Fond sombre avec overlay
- Titre en grand (60-80pt)
- Noms en moyen (24-30pt)
- Centré verticalement et horizontalement

---

### SLIDE 2 : Problématique

**Layout :** 2 colonnes

```
┌─────────────────┬─────────────────┐
│  LE DÉFI ❓     │  NOTRE SOLUTION │
│                 │  🎯             │
│  [Icône]        │                 │
│                 │  [Liste à puces]│
│  "Comment       │                 │
│   choisir un    │                 │
│   film selon    │                 │
│   notre humeur?"│                 │
│                 │                 │
└─────────────────┴─────────────────┘
```

**Points à mentionner :**
- Le problème : choix difficile parmi des milliers de films
- La solution : IA qui comprend l'émotion
- L'impact : gain de temps, meilleure expérience

---

### SLIDE 3 : Architecture Technique

**Layout :** Schéma en couches

```
┌─────────────────────────────────────┐
│     Architecture du Système         │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Front-end Web               │  │
│  │  HTML/CSS/JavaScript         │  │
│  └──────────────┬───────────────┘  │
│                 │                   │
│  ┌──────────────▼───────────────┐  │
│  │  Back-end Flask (API)        │  │
│  └──────────────┬───────────────┘  │
│                 │                   │
│  ┌──────────────▼───────────────┐  │
│  │  Modules IA & Données        │  │
│  └──────────────┬───────────────┘  │
│                 │                   │
│  ┌──────────────▼───────────────┐  │
│  │  Dataset TMDB (4803 films)   │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Style :**
- Flèches entre les couches
- Couleurs différentes pour chaque couche
- Texte centré dans chaque bloc

---

### SLIDES 5-20 : Développement par Prompts

**Format Standard :**

```
┌─────────────────────────────────────┐
│  PHASE X : [Titre de la phase]     │
│                                     │
│  ┌──────────────────────────────┐  │
│  │ 🤔 PROMPT                    │  │
│  │                              │  │
│  │ "[Question posée à l'IA]"    │  │
│  │                              │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │ 💡 RÉPONSE DE L'IA           │  │
│  │                              │  │
│  │ [Solution proposée]          │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │ 💻 CODE GÉNÉRÉ               │  │
│  │                              │  │
│  │ [Extrait de code clé]        │  │
│  └──────────────────────────────┘  │
│                                     │
│  👤 Responsable : [Nom]            │
└─────────────────────────────────────┘
```

**Conseils :**
- Utiliser des blocs de couleur différents
- Code dans un bloc avec fond sombre (syntax highlighting)
- Icônes pour chaque section (🤔 💡 💻)

---

### SLIDE 23 : Résultats & Métriques

**Layout :** Cartes avec métriques

```
┌──────────┬──────────┬──────────┐
│  4,803   │  99.4%   │  8.50/10 │
│  Films   │  Genres  │  Note    │
│          │  Complets│  Moyenne │
└──────────┴──────────┴──────────┘
     │          │          │
┌────▼────┐ ┌───▼────┐ ┌───▼────┐
│ Dataset │ │Données │ │Recom-  │
│         │ │        │ │manda-  │
│         │ │        │ │tions   │
└─────────┘ └────────┘ └────────┘
```

**Style :**
- Grands chiffres (80-100pt)
- Petites descriptions en dessous
- Couleurs d'accent pour les chiffres
- Icônes pertinentes

---

### SLIDE 24 : Démo Live

**Layout :** Capture d'écran plein écran

```
┌─────────────────────────────────────┐
│                                     │
│     [CAPTURE D'ÉCRAN DE L'APP]     │
│                                     │
│  🔍 Recherche par titre            │
│  😊 Recommandation par émotion     │
│  📸 Détection faciale (bonus)      │
│                                     │
└─────────────────────────────────────┘
```

**Conseils :**
- Utiliser une vraie capture d'écran
- Ajouter des annotations (flèches, cercles)
- Montrer le flux utilisateur

---

## 🎬 Conseils pour la Présentation Orale

### Timing Recommandé

1. **Introduction** (2 min)
   - Présentation équipe
   - Problématique

2. **Architecture** (3 min)
   - Vue d'ensemble technique
   - Stack utilisé

3. **Développement** (8 min)
   - 2-3 prompts clés détaillés
   - Montrer l'évolution

4. **Démo Live** (3 min)
   - Recherche par titre
   - Recommandation par émotion
   - Fonctionnalités bonus

5. **Résultats** (2 min)
   - Métriques clés
   - Performance

6. **Conclusion** (2 min)
   - Ce qui a été fait
   - Améliorations futures

**Total : ~20 minutes + 5-10 min questions**

### Points Clés à Souligner

1. **Collaboration**
   - Répartition claire des tâches
   - Complémentarité de l'équipe

2. **Technologies Modernes**
   - IA/ML intégrés
   - Stack professionnel
   - Bonnes pratiques

3. **Valeur Produit**
   - Utilité réelle
   - Performance mesurée
   - Expérience utilisateur

4. **Progression**
   - Démonstrer l'évolution
   - Problèmes résolus
   - Améliorations continues

---

## 📸 Captures d'Écran à Préparer

### À Capturer :

1. **Page d'accueil**
   - Design complet
   - Formulaire de recherche
   - Vidéo de fond visible

2. **Page de résultats**
   - Cartes de films
   - Filtrage par émotion
   - Informations affichées

3. **Détails d'un film**
   - Affiche
   - Genres
   - Note et sentiment

4. **Détection faciale** (si disponible)
   - Webcam active
   - Émotion détectée
   - Recommandations automatiques

5. **Graphiques du notebook**
   - Distribution des notes
   - Top genres
   - Matrice de confusion
   - Performance des recommandations

---

## 🎯 Template Canva Recommandé

### Recherche dans Canva :

**Mots-clés :**
- "Technology Presentation"
- "AI Presentation"
- "Business Pitch"
- "Data Science Presentation"

**Styles à éviter :**
- Trop coloré (garder professionnel)
- Trop chargé (garder lisible)
- Polices fantaisie (garder lisible)

**Styles recommandés :**
- Moderne et minimaliste
- Sombre avec accents colorés
- Professionnel mais créatif

---

## 📝 Checklist Finale

### Avant la Présentation

- [ ] Toutes les slides créées
- [ ] Vérification orthographe/grammaire
- [ ] Captures d'écran à jour
- [ ] Graphiques exportés du notebook
- [ ] Démo testée et fonctionnelle
- [ ] Timing de la présentation testé
- [ ] Questions anticipées préparées

### Pendant la Présentation

- [ ] Maintenir contact visuel
- [ ] Parler clairement et lentement
- [ ] Pointer les éléments visuels
- [ ] Faire des pauses
- [ ] Interagir avec l'audience

### Support Technique

- [ ] Ordinateur chargé
- [ ] Adaptateur HDMI/VGA
- [ ] Démo fonctionne hors ligne
- [ ] Back-up (PDF de la présentation)
- [ ] Télécommande (si disponible)

---

## 💡 Conseils de Dernière Minute

1. **Pratiquez** : Répétez au moins 2-3 fois
2. **Soyez enthousiastes** : Montrez votre passion pour le projet
3. **Racontez une histoire** : Faites vivre le projet
4. **Anticipez les questions** : Préparez des réponses
5. **Restez calmes** : Prenez votre temps

---

## 🎬 Exemple de Script pour la Présentation

### Introduction

> "Bonjour, nous sommes Gémima, Fatoumata et Hector. 
> Aujourd'hui, nous vous présentons MovieMood, une plateforme web 
> intelligente de recommandation de films basée sur les émotions.
> 
> Le problème : Avec des milliers de films disponibles, comment 
> choisir celui qui correspond à notre humeur du moment ?
> 
> Notre solution : Une plateforme IA qui comprend votre émotion 
> et vous propose les films parfaits. Laissez-nous vous montrer 
> comment nous l'avons construite..."

### Transition entre slides

> "Maintenant, passons à l'architecture technique de notre système..."
> "Voyons comment nous avons développé cette fonctionnalité..."
> "Regardons les résultats que nous avons obtenus..."

### Conclusion

> "Pour conclure, nous avons créé une plateforme complète et 
> fonctionnelle qui démontre l'utilisation pratique de l'IA 
> pour améliorer l'expérience utilisateur. Nous sommes fiers 
> de ce que nous avons accompli et excités par les possibilités 
> d'amélioration futures.
> 
> Merci pour votre attention. Avez-vous des questions ?"

---

Bon courage pour votre présentation ! 🎉

