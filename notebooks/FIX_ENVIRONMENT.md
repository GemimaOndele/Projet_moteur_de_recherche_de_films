# 🔧 Réparation Complète de l'Environnement

Si vous rencontrez des erreurs d'import, voici comment réparer complètement l'environnement :

## 🚀 Réinstallation Complète (Recommandé)

```powershell
# 1. Activer l'environnement virtuel
.venv\Scripts\activate

# 2. Réinstaller tous les packages essentiels
pip install --upgrade --force-reinstall --no-cache-dir numpy pandas matplotlib seaborn Pillow

# 3. Vérifier les versions compatibles
pip install "numpy<2.3.0,>=2.0.0" "pillow<12.0,>=9.2.0"

# 4. Réinstaller les dépendances problématiques
pip install --upgrade --force-reinstall regex kiwisolver contourpy
```

## 🔍 Vérification

Après réinstallation, testez :

```powershell
python -c "import numpy; import pandas; import matplotlib.pyplot as plt; import seaborn; print('✅ OK')"
```

## 📝 Si les erreurs persistent

### Option 1 : Réinstaller depuis requirements.txt

```powershell
pip install -r requirements.txt --upgrade --force-reinstall
```

### Option 2 : Recréer l'environnement virtuel (solution radicale)

```powershell
# 1. Supprimer l'ancien environnement
Remove-Item -Recurse -Force .venv

# 2. Créer un nouvel environnement
python -m venv .venv

# 3. Activer
.venv\Scripts\activate

# 4. Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt
```

## ⚠️ Versions Compatibles

Pour éviter les conflits, utilisez ces versions :

- `numpy<2.3.0,>=2.0.0` (compatible avec opencv-python)
- `pillow<12.0,>=9.2.0` (compatible avec moviepy)
- `matplotlib>=3.7.0`
- `seaborn>=0.12.0`

