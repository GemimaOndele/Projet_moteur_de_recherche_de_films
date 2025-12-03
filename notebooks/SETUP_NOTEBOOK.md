# 📓 Configuration du Notebook Jupyter

## 🔧 Installation des dépendances

Le notebook nécessite quelques packages pour fonctionner correctement. Assurez-vous qu'ils sont installés :

```powershell
# Activer l'environnement virtuel
.venv\Scripts\activate

# Installer les dépendances (si pas déjà fait)
pip install -r requirements.txt

# Installer ipykernel si nécessaire
pip install ipykernel -U
```

## ⚙️ Configuration du Kernel Jupyter

Pour que Jupyter reconnaisse votre environnement virtuel, vous devez enregistrer le kernel :

```powershell
# Enregistrer le kernel de l'environnement virtuel
.venv\Scripts\python.exe -m ipykernel install --user --name=moviemood-env --display-name "MovieMood (.venv)"
```

## 📖 Utilisation

1. **Ouvrir le notebook dans Jupyter** :
   ```powershell
   jupyter notebook evaluation_notebook.ipynb
   ```

2. **Sélectionner le bon kernel** :
   - Dans Jupyter, cliquez sur "Kernel" → "Change kernel"
   - Sélectionnez "MovieMood (.venv)" ou ".venv"

3. **Exécuter les cellules** :
   - Utilisez `Shift + Enter` pour exécuter une cellule
   - Ou cliquez sur le bouton "Run" dans la barre d'outils

## 🔍 Dépannage

### Erreur : "Running cells requires the ipykernel package"

**Solution** :
```powershell
.venv\Scripts\python.exe -m pip install ipykernel -U --force-reinstall
.venv\Scripts\python.exe -m ipykernel install --user --name=moviemood-env --display-name "MovieMood (.venv)"
```

### Le kernel n'apparaît pas dans la liste

**Solution** :
1. Vérifiez que vous êtes dans l'environnement virtuel
2. Réinstallez le kernel :
   ```powershell
   .venv\Scripts\python.exe -m ipykernel install --user --name=moviemood-env --display-name "MovieMood (.venv)" --force
   ```
3. Redémarrez Jupyter

### Erreurs d'import dans le notebook

**Solution** :
- Vérifiez que toutes les dépendances sont installées : `pip install -r requirements.txt`
- Vérifiez que vous utilisez le bon kernel (celui de `.venv`)

## 📦 Packages nécessaires

Le notebook nécessite ces packages spécifiques :
- `pandas` : Manipulation de données
- `numpy` : Calculs numériques
- `matplotlib` : Graphiques de base
- `seaborn` : Graphiques avancés
- `jupyter` : Interface notebook
- `ipykernel` : Kernel Python pour Jupyter

Tous sont déjà dans `requirements.txt`.

