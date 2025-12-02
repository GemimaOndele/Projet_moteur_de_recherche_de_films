"""Script pour uploader le dataset sur Hugging Face via Git LFS (méthode recommandée)."""

from __future__ import annotations

import os
import subprocess
import json
from pathlib import Path

import pandas as pd

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "films_enriched_complete.csv"
REPO_NAME = "moviemood-dataset"
# Le token doit être défini dans la variable d'environnement HF_TOKEN
# Obtenez votre token sur: https://huggingface.co/settings/tokens
HF_TOKEN = os.getenv("HF_TOKEN", "")  # Utilise la variable d'environnement
HF_USERNAME = os.getenv("HF_USERNAME", "your-username")  # À remplacer par votre username


def upload_via_git(csv_file: Path, repo_name: str, token: str, username: str):
    """Upload le dataset via Git LFS."""
    
    if not csv_file.exists():
        print(f"❌ Fichier introuvable: {csv_file}")
        return False
    
    print(f"📥 Chargement du fichier: {csv_file}")
    df = pd.read_csv(csv_file)
    print(f"✅ {len(df)} films chargés")
    
    # Convertir en JSON
    print("🔄 Conversion en JSON...")
    json_data = df.to_dict(orient="records")
    json_file = csv_file.parent / "data.json"
    
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON créé: {json_file}")
    
    repo_url = f"https://{username}:{token}@huggingface.co/datasets/{username}/{repo_name}"
    temp_dir = BASE_DIR / "temp_hf_upload"
    
    try:
        # Cloner ou mettre à jour le repo
        if temp_dir.exists():
            print(f"📂 Repo existe déjà, mise à jour...")
            os.chdir(temp_dir)
            subprocess.run(["git", "pull"], check=True)
        else:
            print(f"📂 Clonage du repo...")
            temp_dir.mkdir(exist_ok=True)
            subprocess.run(
                ["git", "clone", repo_url, str(temp_dir)],
                check=True,
                cwd=BASE_DIR
            )
            os.chdir(temp_dir)
        
        # Copier le fichier JSON
        import shutil
        shutil.copy(json_file, temp_dir / "data.json")
        
        # Ajouter et commit
        print(f"📝 Ajout des fichiers...")
        subprocess.run(["git", "add", "data.json"], check=True)
        subprocess.run(
            ["git", "commit", "-m", "Add enriched movies dataset"],
            check=True
        )
        
        # Push
        print(f"📤 Upload sur Hugging Face...")
        subprocess.run(["git", "push"], check=True)
        
        print(f"✅ Dataset uploadé avec succès!")
        print(f"   URL: https://huggingface.co/datasets/{username}/{repo_name}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur Git: {e}")
        print(f"\n💡 Instructions manuelles:")
        print(f"   1. Allez sur https://huggingface.co/new-dataset")
        print(f"   2. Créez un dataset nommé: {repo_name}")
        print(f"   3. Clonez-le: git clone https://huggingface.co/datasets/{username}/{repo_name}")
        print(f"   4. Copiez {json_file.name} dans le repo")
        print(f"   5. git add . && git commit -m 'Add dataset' && git push")
        return False
    finally:
        os.chdir(BASE_DIR)


if __name__ == "__main__":
    print("=" * 80)
    print("☁️  UPLOAD DU DATASET SUR HUGGING FACE (VIA GIT)")
    print("=" * 80)
    print()
    print("⚠️  IMPORTANT: Vous devez d'abord créer le dataset sur Hugging Face:")
    print("   1. Allez sur: https://huggingface.co/new-dataset")
    print(f"   2. Créez un dataset nommé: {REPO_NAME}")
    print(f"   3. Notez votre username Hugging Face")
    print()
    
    username = input(f"Entrez votre username Hugging Face (ou appuyez sur Entrée pour '{HF_USERNAME}'): ").strip()
    if not username:
        username = HF_USERNAME
    
    if username == "your-username":
        print("❌ Vous devez spécifier votre username Hugging Face")
        print("   Modifiez HF_USERNAME dans le script ou entrez-le maintenant")
    else:
        token = os.getenv("HF_TOKEN")
        if not token:
            print("❌ Variable d'environnement HF_TOKEN non définie")
            print("   Définissez-la avec: export HF_TOKEN='votre_token'")
            print("   Ou obtenez votre token sur: https://huggingface.co/settings/tokens")
        else:
            upload_via_git(INPUT_FILE, REPO_NAME, token, username)

