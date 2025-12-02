"""Script pour libérer de l'espace disque en nettoyant les fichiers inutiles."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def get_size(path: Path) -> int:
    """Calcule la taille d'un fichier ou dossier en bytes."""
    if path.is_file():
        return path.stat().st_size
    elif path.is_dir():
        total = 0
        try:
            for item in path.rglob('*'):
                if item.is_file():
                    total += item.stat().st_size
        except Exception:
            pass
        return total
    return 0


def format_size(size_bytes: int) -> str:
    """Formate la taille en format lisible."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def clean_python_cache():
    """Nettoie les caches Python (__pycache__, *.pyc)."""
    logger.info("🧹 Nettoyage des caches Python...")
    total_freed = 0
    
    for pattern in ['__pycache__', '*.pyc', '*.pyo', '*.pyd']:
        for path in BASE_DIR.rglob(pattern):
            try:
                if path.is_dir():
                    size = get_size(path)
                    shutil.rmtree(path)
                    total_freed += size
                    logger.info(f"  ✅ Supprimé: {path.relative_to(BASE_DIR)} ({format_size(size)})")
                elif path.is_file():
                    size = path.stat().st_size
                    path.unlink()
                    total_freed += size
            except Exception as e:
                logger.warning(f"  ⚠️  Erreur avec {path}: {e}")
    
    return total_freed


def clean_huggingface_cache():
    """Nettoie le cache Hugging Face."""
    logger.info("🧹 Nettoyage du cache Hugging Face...")
    hf_cache = Path.home() / ".cache" / "huggingface"
    
    if not hf_cache.exists():
        logger.info("  ℹ️  Cache Hugging Face introuvable")
        return 0
    
    try:
        size = get_size(hf_cache)
        shutil.rmtree(hf_cache)
        logger.info(f"  ✅ Cache supprimé: {format_size(size)}")
        return size
    except Exception as e:
        logger.warning(f"  ⚠️  Erreur: {e}")
        return 0


def clean_logs():
    """Nettoie les fichiers de log."""
    logger.info("🧹 Nettoyage des fichiers de log...")
    total_freed = 0
    
    for log_file in BASE_DIR.rglob('*.log'):
        try:
            size = log_file.stat().st_size
            log_file.unlink()
            total_freed += size
            logger.info(f"  ✅ Supprimé: {log_file.relative_to(BASE_DIR)} ({format_size(size)})")
        except Exception as e:
            logger.warning(f"  ⚠️  Erreur avec {log_file}: {e}")
    
    return total_freed


def clean_temp_files():
    """Nettoie les fichiers temporaires."""
    logger.info("🧹 Nettoyage des fichiers temporaires...")
    total_freed = 0
    
    patterns = ['*.tmp', '*.temp', '*.cache', '*.swp', '*.swo', '.DS_Store', 'Thumbs.db']
    
    for pattern in patterns:
        for path in BASE_DIR.rglob(pattern):
            try:
                if path.is_file():
                    size = path.stat().st_size
                    path.unlink()
                    total_freed += size
            except Exception as e:
                pass
    
    return total_freed


def clean_egg_info():
    """Nettoie les dossiers *.egg-info."""
    logger.info("🧹 Nettoyage des dossiers *.egg-info...")
    total_freed = 0
    
    for path in BASE_DIR.rglob('*.egg-info'):
        try:
            if path.is_dir():
                size = get_size(path)
                shutil.rmtree(path)
                total_freed += size
                logger.info(f"  ✅ Supprimé: {path.relative_to(BASE_DIR)} ({format_size(size)})")
        except Exception as e:
            logger.warning(f"  ⚠️  Erreur avec {path}: {e}")
    
    return total_freed


def clean_virtual_envs():
    """Nettoie les environnements virtuels (optionnel)."""
    logger.info("🧹 Recherche d'environnements virtuels...")
    venv_dirs = ['.venv', 'venv', 'ENV', 'env']
    total_freed = 0
    
    for venv_name in venv_dirs:
        venv_path = BASE_DIR / venv_name
        if venv_path.exists() and venv_path.is_dir():
            size = get_size(venv_path)
            logger.warning(f"  ⚠️  Environnement virtuel trouvé: {venv_path} ({format_size(size)})")
            logger.warning(f"      ⚠️  NON SUPPRIMÉ (important pour le projet)")
            # On ne supprime pas les venv automatiquement
    
    return total_freed


def analyze_disk_usage():
    """Analyse l'utilisation du disque par dossier."""
    logger.info("\n📊 Analyse de l'utilisation du disque...")
    
    dirs_to_check = [
        BASE_DIR / 'code' / '__pycache__',
        BASE_DIR / 'tests' / '__pycache__',
        BASE_DIR / '.cache',
        BASE_DIR / 'data',
        BASE_DIR / 'dataset',
        Path.home() / '.cache' / 'huggingface',
    ]
    
    for dir_path in dirs_to_check:
        if dir_path.exists():
            size = get_size(dir_path)
            if size > 0:
                logger.info(f"  📁 {dir_path.name}: {format_size(size)}")


def main():
    """Fonction principale de nettoyage."""
    print("=" * 80)
    print("🧹 NETTOYAGE DE L'ESPACE DISQUE")
    print("=" * 80)
    print()
    
    total_freed = 0
    
    # Analyse avant nettoyage
    analyze_disk_usage()
    
    print("\n" + "=" * 80)
    print("🚀 DÉBUT DU NETTOYAGE")
    print("=" * 80)
    print()
    
    # Nettoyages
    total_freed += clean_python_cache()
    total_freed += clean_huggingface_cache()
    total_freed += clean_logs()
    total_freed += clean_temp_files()
    total_freed += clean_egg_info()
    clean_virtual_envs()  # Info seulement
    
    print()
    print("=" * 80)
    print(f"✅ NETTOYAGE TERMINÉ")
    print("=" * 80)
    print(f"📊 Espace libéré: {format_size(total_freed)}")
    print()
    
    # Suggestions supplémentaires
    print("💡 Suggestions pour libérer plus d'espace:")
    print("   1. Déplacer le dataset CSV vers un autre disque")
    print("   2. Utiliser uniquement Hugging Face (supprimer data/films_enriched_complete.csv)")
    print("   3. Nettoyer le cache du navigateur")
    print("   4. Vider la corbeille Windows")
    print("   5. Utiliser l'outil de nettoyage de disque Windows")


if __name__ == "__main__":
    main()

