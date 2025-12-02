"""Script pour uploader le dataset enrichi sur Hugging Face."""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Dict

import pandas as pd

try:
    from datasets import Dataset
    from huggingface_hub import HfApi, login
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    print("❌ Bibliothèques manquantes. Installez: pip install datasets huggingface_hub")

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "films_enriched_complete.csv"
REPO_NAME = "moviemood-dataset"  # Changez si vous voulez un autre nom


def upload_dataset_to_hf(csv_file: Path, repo_name: str = REPO_NAME):
    """Upload le dataset CSV sur Hugging Face."""
    
    if not HF_AVAILABLE:
        print("❌ Bibliothèques Hugging Face non disponibles")
        return False
    
    if not csv_file.exists():
        print(f"❌ Fichier introuvable: {csv_file}")
        print(f"   Exécutez d'abord: python code/enrich_all_films.py")
        return False
    
    print(f"📥 Chargement du fichier: {csv_file}")
    df = pd.read_csv(csv_file)
    print(f"✅ {len(df)} films chargés")
    
    # Convertir en Dataset Hugging Face
    print("🔄 Conversion en Dataset Hugging Face...")
    dataset = Dataset.from_pandas(df)
    
    # Login Hugging Face (demande le token)
    print("\n🔐 Connexion à Hugging Face...")
    print("   Vous pouvez obtenir un token sur: https://huggingface.co/settings/tokens")
    token = os.getenv("HF_TOKEN")
    if not token:
        token = input("Entrez votre token Hugging Face: ").strip()
    
    if not token:
        print("❌ Token requis")
        return False
    
    try:
        login(token=token)
        print("✅ Connecté à Hugging Face")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    
    # Upload
    print(f"\n📤 Upload du dataset sur Hugging Face (repo: {repo_name})...")
    print("   ⚠️  Cela peut prendre quelques minutes...")
    
    try:
        dataset.push_to_hub(
            repo_name,
            private=False,  # Mettez True si vous voulez un repo privé
            token=token
        )
        print(f"✅ Dataset uploadé avec succès!")
        print(f"   URL: https://huggingface.co/datasets/{repo_name}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'upload: {e}")
        return False


if __name__ == "__main__":
    print("=" * 80)
    print("☁️  UPLOAD DU DATASET SUR HUGGING FACE")
    print("=" * 80)
    print()
    
    if not INPUT_FILE.exists():
        print(f"❌ Fichier enrichi introuvable: {INPUT_FILE}")
        print(f"   Exécutez d'abord: python code/enrich_all_films.py")
    else:
        upload_dataset_to_hf(INPUT_FILE, REPO_NAME)

