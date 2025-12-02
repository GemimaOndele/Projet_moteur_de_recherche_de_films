# 💾 Guide pour Libérer l'Espace Disque

## ✅ Déjà Fait

- ✅ **690.84 MB libérés** par le script de nettoyage
- ✅ Cache Hugging Face nettoyé (442 MB)
- ✅ Caches Python nettoyés

## 🎯 Actions Supplémentaires pour Libérer Plus d'Espace

### 1. Supprimer le CSV Local (si Hugging Face fonctionne)

Si Hugging Face fonctionne bien, vous pouvez supprimer le fichier CSV local :

```powershell
# Vérifier d'abord que Hugging Face fonctionne
python code/app.py
# Si ça marche, supprimer le CSV local
Remove-Item "data\films_enriched_complete.csv"
```

**Gain estimé** : ~50-100 MB

### 2. Nettoyer Windows

```powershell
python scripts/utils/cleanup_windows.py
```

Ou manuellement :
- **Corbeille** : Clic droit → Vider la corbeille
- **Fichiers temporaires** : Windows + R → `%TEMP%` → Supprimer tout
- **Nettoyage de disque** : Windows + R → `cleanmgr` → Sélectionner C: → Tout cocher

**Gain estimé** : 1-5 GB

### 3. Nettoyer le Cache du Navigateur

**Chrome/Edge** :
1. Ouvrez le navigateur
2. Paramètres → Confidentialité
3. Effacer les données de navigation
4. Cochez "Images et fichiers en cache"
5. Effacer

**Gain estimé** : 500 MB - 2 GB

### 4. Déplacer le Dataset vers un Autre Disque

Si vous avez un disque D: ou externe :

```powershell
# Créer le dossier sur l'autre disque
New-Item -ItemType Directory -Path "D:\datasets" -Force

# Déplacer le CSV
Move-Item "dataset\tmdb_5000_movies.csv" "D:\datasets\"

# Modifier code/app.py pour pointer vers D:\datasets\tmdb_5000_movies.csv
```

**Gain estimé** : ~50 MB

### 5. Réduire la Taille de l'Environnement Virtuel

L'environnement virtuel fait **1.89 GB**. Vous pouvez :

**Option A** : Supprimer les packages non utilisés
```powershell
pip uninstall tensorflow -y  # Si vous n'utilisez pas vraiment TensorFlow
pip uninstall moviepy -y     # Si vous n'utilisez pas moviepy
pip uninstall selenium -y    # Si vous n'utilisez pas selenium
```

**Option B** : Réinstaller un environnement virtuel minimal
```powershell
# Créer un nouveau venv minimal
python -m venv .venv_minimal
.venv_minimal\Scripts\activate
pip install flask pandas requests opencv-python datasets huggingface_hub python-dotenv
```

**Gain estimé** : 500 MB - 1 GB

### 6. Nettoyer OneDrive

Si votre projet est synchronisé avec OneDrive :
- Vérifiez les fichiers en double
- Désactivez la synchronisation des dossiers `__pycache__`, `.cache`, etc.

## 📊 Résumé des Gains Potentiels

| Action | Gain Estimé |
|--------|-------------|
| CSV local (si HF OK) | 50-100 MB |
| Nettoyage Windows | 1-5 GB |
| Cache navigateur | 500 MB - 2 GB |
| Réduire venv | 500 MB - 1 GB |
| **TOTAL POTENTIEL** | **2-8 GB** |

## 🚀 Action Rapide (Recommandée)

1. **Vider la corbeille** (clic droit → Vider)
2. **Nettoyer Windows** : `cleanmgr` → Tout cocher
3. **Supprimer CSV local** si Hugging Face fonctionne
4. **Nettoyer cache navigateur**

Ces 4 actions devraient libérer **2-5 GB** rapidement.

---

**Script disponible** : `scripts/utils/cleanup_disk_space.py` (déjà exécuté)
**Script Windows** : `scripts/utils/cleanup_windows.py` (pour nettoyage système)

