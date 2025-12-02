#!/usr/bin/env python3
"""
verify_implementation.py
Script de vérification que toutes les améliorations sont bien implémentées
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Vérifie qu'un fichier existe"""
    if Path(filepath).exists():
        print(f"✓ {description}")
        return True
    else:
        print(f"✗ {description}")
        return False

def check_file_contains(filepath, search_string, description):
    """Vérifie qu'un fichier contient une chaîne"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if search_string in content:
                print(f"✓ {description}")
                return True
            else:
                print(f"✗ {description}")
                return False
    except Exception as e:
        print(f"✗ {description} (Erreur: {e})")
        return False

def main():
    print("\n" + "="*70)
    print("🔍 VÉRIFICATION DE L'IMPLÉMENTATION DES AMÉLIORATIONS".center(70))
    print("="*70 + "\n")
    
    all_ok = True
    
    # ===== FICHIERS CRÉÉS =====
    print("📁 Vérification des fichiers:\n")
    
    files_to_check = [
        ("code/app.py", "✓ app.py (Flask app)"),
        ("code/tmdb_api.py", "✓ tmdb_api.py (API TMDB améliorée)"),
        ("code/sound_manager.py", "✓ sound_manager.py (Gestion sons améliorée)"),
        ("code/templates/index.html", "✓ index.html (Accueil amélioré)"),
        ("code/templates/results.html", "✓ results.html (Résultats refondus)"),
        ("code/static/css/style.css", "✓ style.css (CSS amélioré)"),
        ("code/static/js/results-enhanced.js", "✓ results-enhanced.js (JS amélioré)"),
        ("setup_enhancements.py", "✓ setup_enhancements.py (Script setup)"),
        ("CHANGELOG_IMPROVEMENTS.md", "✓ CHANGELOG_IMPROVEMENTS.md (Documentation)"),
        ("TEST_GUIDE.md", "✓ TEST_GUIDE.md (Guide de test)"),
        ("IMPLEMENTATION_SUMMARY.md", "✓ IMPLEMENTATION_SUMMARY.md (Synthèse)"),
        ("requirements.txt", "✓ requirements.txt (Dépendances)"),
    ]
    
    for filepath, desc in files_to_check:
        if not check_file_exists(filepath, desc):
            all_ok = False
    
    # ===== FONCTIONNALITÉS BACKEND =====
    print("\n🐍 Vérification des fonctionnalités Python:\n")
    
    features_backend = [
        ("code/tmdb_api.py", "traduire_texte_avec_google_translate", "✓ Traduction français"),
        ("code/tmdb_api.py", "overview_fr", "✓ Champ overview_fr"),
        ("code/tmdb_api.py", "streaming_links", "✓ Liens streaming"),
        ("code/tmdb_api.py", "trailer_url", "✓ URL bande annonce"),
        ("code/sound_manager.py", "EMOTION_SOUNDS", "✓ Dictionnaire émotions"),
        ("code/sound_manager.py", "get_emotion_sound", "✓ Fonction get_emotion_sound"),
        ("code/sound_manager.py", "reaction", "✓ Réactions emoji"),
        ("code/sound_manager.py", "color", "✓ Couleurs émotions"),
    ]
    
    for filepath, search, desc in features_backend:
        if not check_file_contains(filepath, search, desc):
            all_ok = False
    
    # ===== FONCTIONNALITÉS FRONTEND =====
    print("\n🌐 Vérification des fonctionnalités Frontend:\n")
    
    features_frontend = [
        ("code/templates/results.html", "emotion-header", "✓ En-tête émotion"),
        ("code/templates/results.html", "card-visual", "✓ Visuel carte enrichi"),
        ("code/templates/results.html", "overview-details", "✓ Détails synopsis"),
        ("code/templates/results.html", "btn-action", "✓ Boutons actions"),
        ("code/templates/results.html", "streaming-links", "✓ Section streaming"),
        ("code/templates/results.html", "trailer-modal", "✓ Modal bande annonce"),
        ("code/static/css/style.css", "emotion-header", "✓ Style emotion-header"),
        ("code/static/css/style.css", "audio-visualizer", "✓ Style visualiseur audio"),
        ("code/static/css/style.css", "emotionPulse", "✓ Animation emotionPulse"),
        ("code/static/css/style.css", "visualize", "✓ Animation visualiseur"),
        ("code/static/js/results-enhanced.js", "trailerModal", "✓ Gestion modal trailer"),
        ("code/static/js/results-enhanced.js", "emotionAudio", "✓ Audio émotions"),
        ("code/static/js/results-enhanced.js", "showAudioVisualizer", "✓ Visualiseur audio JS"),
    ]
    
    for filepath, search, desc in features_frontend:
        if not check_file_contains(filepath, search, desc):
            all_ok = False
    
    # ===== ÉMOTIONS SUPPORTÉES =====
    print("\n😊 Vérification des émotions:\n")
    
    emotions = {
        "heureux": "#FFD700",
        "triste": "#4A90E2",
        "stressé": "#FF6B6B",
        "nostalgique": "#FF69B4",
        "ennuyé": "#95A5A6",
        "colere": "#E74C3C",
        "peur": "#8B008B",
        "surprise": "#FF8C00",
    }
    
    for emotion_name, emotion_color in emotions.items():
        if check_file_contains("code/sound_manager.py", emotion_name, f"✓ Émotion '{emotion_name}'"):
            continue
        else:
            all_ok = False
    
    # ===== DÉPENDANCES =====
    print("\n📦 Vérification des dépendances:\n")
    
    dependencies = [
        ("flask", "✓ Flask"),
        ("pandas", "✓ Pandas"),
        ("requests", "✓ Requests"),
        ("PIL", "✓ Pillow"),
    ]
    
    for package, desc in dependencies:
        try:
            __import__(package)
            print(desc)
        except ImportError:
            print(f"✗ {desc} (manquant)")
            all_ok = False
    
    # ===== RÉSUMÉ =====
    print("\n" + "="*70)
    if all_ok:
        print("✅ IMPLÉMENTATION COMPLÈTE ET VÉRIFIÉE!".center(70))
    else:
        print("⚠️  CERTAINS ÉLÉMENTS MANQUENT".center(70))
    print("="*70 + "\n")
    
    # Instructions finales
    print("📝 PROCHAINES ÉTAPES:\n")
    print("1. Configurez la clé API TMDB:")
    print("   $env:TMDB_API_KEY = \"votre_clé\"\n")
    print("2. Installez les dépendances manquantes (si nécessaire):")
    print("   pip install -r requirements.txt\n")
    print("3. Exécutez le setup:")
    print("   python setup_enhancements.py\n")
    print("4. Lancez l'application:")
    print("   python code/app.py\n")
    print("5. Accédez à l'application:")
    print("   http://localhost:5000\n")
    
    print("📚 DOCUMENTATION:")
    print("  • IMPLEMENTATION_SUMMARY.md - Synthèse complète")
    print("  • CHANGELOG_IMPROVEMENTS.md - Détails des améliorations")
    print("  • TEST_GUIDE.md - Guide de test\n")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
