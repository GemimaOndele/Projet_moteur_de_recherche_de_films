# 📓 Notebooks d'Évaluation - MovieMood

Ce dossier contient les notebooks Jupyter pour l'analyse et l'évaluation du projet.

## 📋 Notebooks Disponibles

- **`evaluation_notebook.ipynb`** : Évaluation complète de la qualité du dataset et des performances du système de recommandation

## 🚀 Démarrage Rapide

### 1. Configuration Initiale (une seule fois)

Le kernel Jupyter a déjà été configuré. Si vous avez des problèmes, exécutez :

```powershell
# Dans le dossier racine du projet
.venv\Scripts\python.exe -m ipykernel install --user --name=moviemood-env --display-name "MovieMood (.venv)"
```

### 2. Ouvrir le Notebook

```powershell
# Option 1 : Depuis VS Code ou Cursor
# Ouvrez simplement le fichier .ipynb - le kernel devrait être détecté automatiquement

# Option 2 : Depuis Jupyter Notebook classique
cd notebooks
jupyter notebook evaluation_notebook.ipynb

# Option 3 : Depuis JupyterLab
jupyter lab evaluation_notebook.ipynb
```

### 3. Sélectionner le Bon Kernel

Dans VS Code / Cursor :
1. Ouvrez le notebook `evaluation_notebook.ipynb`
2. En haut à droite, cliquez sur le sélecteur de kernel (peut afficher "Select Kernel")
3. Choisissez **"MovieMood (.venv)"** ou **".venv"**

Dans Jupyter Notebook/Lab :
1. Menu : **Kernel** → **Change Kernel**
2. Sélectionnez **"MovieMood (.venv)"**

### 4. Exécuter les Cellules

- **Shift + Enter** : Exécuter la cellule et passer à la suivante
- **Ctrl + Enter** : Exécuter la cellule sans passer à la suivante
- Bouton **"Run"** dans la barre d'outils

## 📊 Contenu du Notebook d'Évaluation

Le notebook `evaluation_notebook.ipynb` contient :

1. **Chargement du Dataset**
   - Import des données
   - Statistiques de base

2. **Évaluation de la Qualité**
   - Complétude des champs
   - Distribution des notes
   - Analyse des genres
   - Analyse temporelle

3. **Évaluation des Recommandations**
   - Performance par émotion
   - Qualité des recommandations
   - Précision des genres

4. **Visualisations**
   - Graphiques de qualité
   - Graphiques de performance
   - Export en PNG

## 🔧 Dépannage

### Erreur : "Running cells requires the ipykernel package"

```powershell
.venv\Scripts\python.exe -m pip install ipykernel -U
.venv\Scripts\python.exe -m ipykernel install --user --name=moviemood-env --display-name "MovieMood (.venv)" --force
```

### Le kernel n'apparaît pas

1. Vérifiez que vous êtes dans l'environnement virtuel
2. Réinstallez le kernel (voir ci-dessus)
3. Redémarrez VS Code/Cursor ou Jupyter

### Erreurs d'import

Vérifiez que toutes les dépendances sont installées :

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

## 📖 Documentation Complète

Pour plus de détails, consultez :
- `SETUP_NOTEBOOK.md` : Guide détaillé de configuration
- `README_EVALUATION.md` : Documentation du notebook d'évaluation

## 💡 Conseils

- Exécutez les cellules dans l'ordre (de haut en bas)
- Les graphiques sont sauvegardés automatiquement dans le dossier `notebooks/`
- Le notebook peut prendre quelques minutes pour charger et analyser les données
- N'hésitez pas à modifier les cellules pour personnaliser les analyses
