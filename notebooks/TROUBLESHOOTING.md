# 🔧 Dépannage - Notebook Jupyter

## ✅ Problèmes Résolus

### ImportError avec numpy

**Erreur** :
```
ImportError: Error importing numpy: you should not try to import numpy from
        its source directory; please exit the numpy source tree, and relaunch
        your python interpreter from there.
```

**Cause** : Numpy était corrompu ou en conflit de version avec opencv-python.

**Solution** :
```powershell
# Réinstaller numpy avec une version compatible
.venv\Scripts\python.exe -m pip install "numpy<2.3.0,>=1.20.0" --force-reinstall
```

### Conflit de version numpy/opencv

**Erreur** :
```
opencv-python 4.12.0.88 requires numpy<2.3.0,>=2
```

**Solution** : Numpy a été mis à jour pour être compatible. Vérifiez `requirements.txt` pour la version correcte.

## 🚀 Solutions Rapides

### Réinstaller toutes les dépendances

```powershell
# Activer l'environnement virtuel
.venv\Scripts\activate

# Réinstaller depuis requirements.txt
pip install -r requirements.txt --force-reinstall
```

### Vérifier l'installation

```powershell
.venv\Scripts\python.exe -c "import numpy; import pandas; print('numpy:', numpy.__version__); print('pandas:', pandas.__version__)"
```

### Réinitialiser le kernel Jupyter

```powershell
# Désinstaller l'ancien kernel
jupyter kernelspec uninstall moviemood-env

# Réinstaller le kernel
.venv\Scripts\python.exe -m ipykernel install --user --name=moviemood-env --display-name "MovieMood (.venv)"
```

## 📋 Checklist de Dépannage

1. ✅ Environnement virtuel activé
2. ✅ Toutes les dépendances installées (`pip install -r requirements.txt`)
3. ✅ Numpy fonctionne (`python -c "import numpy"`)
4. ✅ Pandas fonctionne (`python -c "import pandas"`)
5. ✅ Kernel Jupyter enregistré
6. ✅ Bon kernel sélectionné dans le notebook

## 💡 Conseils

- Toujours activer l'environnement virtuel avant d'utiliser le notebook
- Si une erreur persiste, redémarrer VS Code/Cursor peut aider
- Vérifiez que vous utilisez le bon kernel (MovieMood (.venv))

