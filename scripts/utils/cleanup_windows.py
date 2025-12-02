"""Script pour nettoyer Windows et libérer plus d'espace disque."""

from __future__ import annotations

import subprocess
import os
from pathlib import Path

def clean_windows_temp():
    """Nettoie les dossiers temporaires Windows."""
    print("🧹 Nettoyage des dossiers temporaires Windows...")
    
    temp_dirs = [
        os.path.expandvars(r'%TEMP%'),
        os.path.expandvars(r'%TMP%'),
        r'C:\Windows\Temp',
    ]
    
    total_freed = 0
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            print(f"  📁 Nettoyage: {temp_dir}")
            try:
                # Utiliser PowerShell pour nettoyer
                cmd = f'Get-ChildItem -Path "{temp_dir}" -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue'
                subprocess.run(['powershell', '-Command', cmd], capture_output=True)
                print(f"  ✅ Nettoyé")
            except Exception as e:
                print(f"  ⚠️  Erreur: {e}")

def clean_recycle_bin():
    """Vide la corbeille Windows."""
    print("\n🗑️  Vidage de la corbeille...")
    try:
        subprocess.run(['powershell', '-Command', 'Clear-RecycleBin -Force'], capture_output=True)
        print("  ✅ Corbeille vidée")
    except Exception as e:
        print(f"  ⚠️  Erreur: {e}")

def clean_browser_cache():
    """Suggère de nettoyer le cache du navigateur."""
    print("\n🌐 Cache du navigateur:")
    print("  💡 Pour nettoyer Chrome:")
    print("     - Ouvrez Chrome → Paramètres → Confidentialité → Effacer les données de navigation")
    print("  💡 Pour nettoyer Edge:")
    print("     - Ouvrez Edge → Paramètres → Confidentialité → Effacer les données de navigation")

def suggest_disk_cleanup():
    """Suggère d'utiliser l'outil de nettoyage de disque Windows."""
    print("\n💡 Utiliser l'outil de nettoyage de disque Windows:")
    print("  1. Appuyez sur Windows + R")
    print("  2. Tapez: cleanmgr")
    print("  3. Sélectionnez le disque C:")
    print("  4. Cochez tous les éléments")
    print("  5. Cliquez sur 'Nettoyer les fichiers système'")
    print("  6. Validez")

def suggest_move_dataset():
    """Suggère de déplacer le dataset vers un autre disque."""
    print("\n💡 Déplacer le dataset vers un autre disque:")
    print("  Si vous avez un disque D: ou autre:")
    print("  1. Créez un dossier: D:\\datasets\\")
    print("  2. Déplacez: dataset/tmdb_5000_movies.csv")
    print("  3. Modifiez DATASET_TMBD dans code/app.py")

def main():
    print("=" * 80)
    print("🧹 NETTOYAGE WINDOWS - LIBÉRATION D'ESPACE DISQUE")
    print("=" * 80)
    print()
    
    print("⚠️  ATTENTION: Ces opérations peuvent prendre du temps")
    print()
    response = input("Continuer avec le nettoyage Windows? (oui/non): ")
    
    if response.lower() in ["oui", "o", "yes", "y"]:
        clean_windows_temp()
        clean_recycle_bin()
    else:
        print("❌ Nettoyage Windows annulé")
    
    print()
    clean_browser_cache()
    suggest_disk_cleanup()
    suggest_move_dataset()
    
    print("\n" + "=" * 80)
    print("✅ Suggestions affichées")
    print("=" * 80)

if __name__ == "__main__":
    main()

