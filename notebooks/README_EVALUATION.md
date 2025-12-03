# 📊 Notebook d'Évaluation - MovieMood

Ce notebook permet d'évaluer la qualité du dataset et les performances du système de recommandation.

## 🎯 Objectifs

1. **Évaluer la qualité du dataset**
   - Complétude des champs importants
   - Distribution des notes
   - Distribution des genres
   - Analyse temporelle (années de sortie)

2. **Évaluer le système de recommandation**
   - Nombre de recommandations par émotion
   - Qualité des recommandations (notes moyennes)
   - Précision des genres recommandés
   - Score global par émotion

## 📋 Utilisation

1. Assurez-vous d'avoir installé les dépendances :
   ```bash
   pip install pandas numpy matplotlib seaborn jupyter
   ```

2. Ouvrez le notebook :
   ```bash
   jupyter notebook evaluation_notebook.ipynb
   ```

3. Exécutez les cellules dans l'ordre pour générer les analyses et graphiques.

## 📊 Métriques Évaluées

### Qualité du Dataset
- **Complétude** : Pourcentage de films avec chaque champ rempli
- **Notes** : Statistiques descriptives (moyenne, médiane, écart-type)
- **Genres** : Distribution et fréquence des genres
- **Temporel** : Répartition par année de sortie

### Performances de Recommandation
- **Couverture** : Nombre de recommandations par émotion
- **Qualité** : Note moyenne des films recommandés
- **Précision** : Alignement entre genres attendus et recommandés
- **Score global** : Combinaison des métriques

## 📈 Graphiques Générés

Le notebook génère automatiquement :
- Graphiques de complétude des champs
- Histogramme de distribution des notes
- Top genres les plus fréquents
- Distribution temporelle
- Performances par émotion
- Scores globaux de recommandation

Les graphiques sont sauvegardés en PNG haute résolution dans le dossier notebooks.

## 🔍 Analyse des Résultats

Le notebook fournit :
- Un résumé textuel des métriques clés
- Des visualisations pour faciliter l'interprétation
- Des recommandations d'amélioration basées sur les résultats

