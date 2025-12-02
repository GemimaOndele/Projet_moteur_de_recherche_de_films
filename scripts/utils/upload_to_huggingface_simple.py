"""Script simplifié pour uploader le dataset enrichi sur Hugging Face (utilise requests uniquement)."""

from __future__ import annotations

import os
import json
from pathlib import Path

import pandas as pd
import os
import requests

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "films_enriched_complete.csv"
REPO_NAME = "moviemood-dataset"  # Changez si vous voulez un autre nom
HF_TOKEN = os.getenv("HF_TOKEN")  # Doit être défini dans votre environnement ou fichier .env (non commité)

HF_API_BASE = "https://huggingface.co/api"


def upload_csv_to_hf(csv_file: Path, repo_name: str, token: str):
    """Upload un CSV sur Hugging Face en utilisant l'API directement."""
    
    if not csv_file.exists():
        print(f"❌ Fichier introuvable: {csv_file}")
        return False
    
    print(f"📥 Chargement du fichier: {csv_file}")
    df = pd.read_csv(csv_file)
    print(f"✅ {len(df)} films chargés")
    
    # Convertir en JSON (format plus simple pour Hugging Face)
    print("🔄 Conversion en JSON...")
    json_data = df.to_dict(orient="records")
    
    # Créer le repo si nécessaire
    print(f"\n🔐 Connexion à Hugging Face...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Vérifier/créer le repo
    repo_url = f"{HF_API_BASE}/datasets/{repo_name}"
    response = requests.get(repo_url, headers=headers)
    
    if response.status_code == 404:
        print(f"📦 Création du repo: {repo_name}")
        create_data = {
            "type": "dataset",
            "name": repo_name.split("/")[-1] if "/" in repo_name else repo_name,
            "private": False
        }
        create_response = requests.post(
            f"{HF_API_BASE}/repos/create",
            headers=headers,
            json=create_data
        )
        if create_response.status_code not in [200, 201]:
            print(f"⚠️  Erreur création repo: {create_response.text}")
    elif response.status_code == 200:
        print(f"✅ Repo existe déjà")
    else:
        print(f"⚠️  Erreur vérification repo: {response.status_code}")
    
    # Sauvegarder en JSON localement d'abord
    json_file = csv_file.parent / "films_enriched_complete.json"
    print(f"💾 Sauvegarde en JSON: {json_file}")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n📤 Upload du fichier JSON sur Hugging Face...")
    print(f"   ⚠️  Cela peut prendre quelques minutes...")
    
    # Upload via l'API Hugging Face
    upload_url = f"https://huggingface.co/api/datasets/{repo_name}/upload"
    
    with open(json_file, "rb") as f:
        files = {"file": (json_file.name, f, "application/json")}
        upload_response = requests.post(
            upload_url,
            headers=headers,
            files=files
        )
    
    if upload_response.status_code in [200, 201]:
        print(f"✅ Dataset uploadé avec succès!")
        print(f"   URL: https://huggingface.co/datasets/{repo_name}")
        return True
    else:
        print(f"❌ Erreur lors de l'upload: {upload_response.status_code}")
        print(f"   Réponse: {upload_response.text[:500]}")
        
        # Alternative: utiliser git LFS (plus complexe mais plus fiable)
        print(f"\n💡 Alternative: Utilisez git LFS pour uploader manuellement")
        print(f"   1. git clone https://huggingface.co/datasets/{repo_name}")
        print(f"   2. Copiez {json_file.name} dans le repo")
        print(f"   3. git add . && git commit -m 'Add dataset' && git push")
        
        return False


if __name__ == "__main__":
    print("=" * 80)
    print("☁️  UPLOAD DU DATASET SUR HUGGING FACE (VERSION SIMPLIFIÉE)")
    print("=" * 80)
    print()
    
    if not INPUT_FILE.exists():
        print(f"❌ Fichier enrichi introuvable: {INPUT_FILE}")
        print(f"   Exécutez d'abord: python code/enrich_all_films.py")
    else:
        token = os.getenv("HF_TOKEN", HF_TOKEN)
        upload_csv_to_hf(INPUT_FILE, REPO_NAME, token)

