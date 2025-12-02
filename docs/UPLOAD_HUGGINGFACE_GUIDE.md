# 📤 Guide : Uploader le Dataset sur Hugging Face

Votre dataset enrichi est prêt ! Voici **3 méthodes** pour l'uploader sur Hugging Face.

## ✅ Méthode 1 : Interface Web (LA PLUS SIMPLE)

### Étape 1 : Créer le dataset sur Hugging Face

1. Allez sur : **https://huggingface.co/new-dataset**
2. Remplissez :
   - **Name** : `moviemood-dataset` (ou un autre nom)
   - **Visibility** : Public (ou Private si vous préférez)
3. Cliquez sur **"Create dataset"**

### Étape 2 : Uploader le fichier

1. Dans votre nouveau dataset, cliquez sur **"Add file"** → **"Upload file"**
2. Glissez-déposez le fichier : `data/films_enriched_complete.json`
   - (Si vous n'avez pas le JSON, exécutez d'abord le script ci-dessous)
3. Cliquez sur **"Commit changes"**

**C'est tout !** 🎉

---

## 🔧 Méthode 2 : Script Python (nécessite datasets + huggingface_hub)

Si vous avez assez d'espace disque :

```powershell
pip install datasets huggingface_hub
# Remplacez ci-dessous par VOTRE token Hugging Face (ne le poussez jamais dans Git)
$env:HF_TOKEN = "hf_votre_token_huggingface_ici"
python code/upload_to_huggingface.py
```

---

## 📝 Méthode 3 : Git LFS (pour développeurs)

### Étape 1 : Créer le dataset sur Hugging Face
Allez sur https://huggingface.co/new-dataset et créez `moviemood-dataset`

### Étape 2 : Convertir en JSON (si pas déjà fait)
```powershell
python -c "import pandas as pd; import json; df = pd.read_csv('data/films_enriched_complete.csv'); json.dump(df.to_dict('records'), open('data/films_enriched_complete.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)"
```

### Étape 3 : Cloner et uploader
```powershell
# Remplacez YOUR_USERNAME par votre username Hugging Face
git clone https://huggingface.co/datasets/YOUR_USERNAME/moviemood-dataset
cd moviemood-dataset
copy ..\data\films_enriched_complete.json data.json
git add data.json
git commit -m "Add enriched movies dataset"
git push
```

---

## 🎯 Recommandation

**Utilisez la Méthode 1 (Interface Web)** - c'est la plus simple et ne nécessite aucune installation supplémentaire !

Une fois uploadé, votre dataset sera disponible à :
**https://huggingface.co/datasets/VOTRE_USERNAME/moviemood-dataset**

---

## 📊 Statistiques de votre dataset

- ✅ **4803 films** enrichis
- ✅ **2414 films** avec bandes annonces YouTube
- ✅ **4779 films** avec affiches
- ✅ Toutes les descriptions en **français**
- ✅ Liens de streaming pour la France

