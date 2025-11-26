#!/usr/bin/env python3
"""
setup_enhancements.py
Script d'installation et de configuration des améliorations du moteur de recherche de films
"""

import os
import sys
from pathlib import Path

# Couleurs pour terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def setup_directories():
    """Crée les répertoires nécessaires"""
    print_header("Création des répertoires")
    
    dirs_to_create = [
        "code/static/audio/sounds",
        "data",
        "static/audio"
    ]
    
    for dir_path in dirs_to_create:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print_success(f"Répertoire créé: {dir_path}")

def create_placeholder_sounds():
    """Crée des fichiers placeholder pour les sons"""
    print_header("Création des fichiers audio placeholder")
    
    emotions = {
        'happy': 'Heureux',
        'sad': 'Triste',
        'stressed': 'Stressé',
        'nostalgic': 'Nostalgique',
        'bored': 'Ennuyé',
        'angry': 'Colère',
        'fear': 'Peur',
        'surprise': 'Surprise'
    }
    
    sounds_dir = Path("code/static/audio/sounds")
    sounds_dir.mkdir(parents=True, exist_ok=True)
    
    for emotion_en, emotion_fr in emotions.items():
        filename = sounds_dir / f"emotion_{emotion_en}.mp3"
        if not filename.exists():
            # Créer un fichier placeholder (vide pour l'instant)
            filename.touch()
            print_warning(f"Placeholder créé: {filename} (à remplacer par un vrai fichier audio)")
        else:
            print_success(f"Fichier audio existant: {filename}")

def check_tmdb_api_key():
    """Vérifie si la clé API TMDB est configurée"""
    print_header("Vérification de la clé API TMDB")
    
    api_key = os.getenv("TMDB_API_KEY")
    
    if api_key and api_key != "your_api_key_here":
        print_success(f"Clé API TMDB détectée: {api_key[:5]}...")
    else:
        print_error("Clé API TMDB non configurée ou invalide")
        print_warning("Pour obtenir une clé API TMDB:")
        print("  1. Allez sur https://www.themoviedb.org/settings/api")
        print("  2. Créez un compte et validez l'email")
        print("  3. Acceptez les conditions")
        print("  4. Remplissez le formulaire d'application")
        print("  5. Copiez votre clé API")
        print("\nConfigurer la clé:")
        print("  Windows (PowerShell): $env:TMDB_API_KEY = \"votre_clé\"")
        print("  Windows (CMD):       set TMDB_API_KEY=votre_clé")
        print("  Linux/Mac:           export TMDB_API_KEY=\"votre_clé\"")

def check_dependencies():
    """Vérifie les dépendances Python"""
    print_header("Vérification des dépendances")
    
    required_packages = [
        ('flask', 'Flask'),
        ('pandas', 'Pandas'),
        ('requests', 'Requests'),
        ('PIL', 'Pillow'),
        ('cv2', 'OpenCV'),
        ('numpy', 'NumPy'),
    ]
    
    missing = []
    
    for import_name, display_name in required_packages:
        try:
            __import__(import_name)
            print_success(f"{display_name} ✓")
        except ImportError:
            print_error(f"{display_name} ✗ (manquant)")
            missing.append(import_name)
    
    if missing:
        print_error("Packages manquants détectés!")
        print_warning("Installez-les avec: pip install -r requirements.txt")
    else:
        print_success("Toutes les dépendances sont installées!")

def display_instructions():
    """Affiche les instructions d'utilisation"""
    print_header("Instructions d'utilisation")
    
    print("""
📝 ÉTAPE 1: Configuration TMDB API
   • Obtenez une clé API sur https://www.themoviedb.org/settings/api
   • Configurez la variable d'environnement TMDB_API_KEY

🎵 ÉTAPE 2: Fichiers audio (Optionnel)
   • Placez les génériques de films dans: code/static/audio/
     - movie_{id}.mp3 (par ID TMDB)
     - {titre_film}.mp3 (par titre)
   • Placez les sons d'émotions dans: code/static/audio/sounds/
     - emotion_happy.mp3
     - emotion_sad.mp3
     - emotion_stressed.mp3
     - etc.

🚀 ÉTAPE 3: Lancer l'application
   • Windows:  python code/app.py
   • Linux:    python3 code/app.py
   • Puis ouvrez: http://localhost:5000

✨ FONCTIONNALITÉS DISPONIBLES:
   ✓ Traduction automatique en français
   ✓ Bande annonce YouTube intégrée
   ✓ Images officielles (poster + backdrop)
   ✓ Liens vers plateformes de streaming
   ✓ Sons des émotions avec animations
   ✓ Générique de film (si fichier disponible)
   ✓ Détection d'émotion par webcam
   ✓ Interface moderne et responsive

📚 DOCUMENTATION:
   • Voir CHANGELOG_IMPROVEMENTS.md pour les détails complets
   • Voir README.md pour le contexte du projet
    """)

def create_env_file_template():
    """Crée un fichier template .env"""
    print_header("Création du fichier .env template")
    
    env_template = """# Fichier de configuration pour le projet
# Copiez ce fichier en .env et remplissez les valeurs

# API TMDB - Obtenir une clé sur https://www.themoviedb.org/settings/api
TMDB_API_KEY=votre_clé_api_ici

# Configuration Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=votre_clé_secrète_ici

# Configuration Audio
ENABLE_AUDIO=True
AUDIO_DIR=code/static/audio

# Configuration Traduction
ENABLE_TRANSLATION=True
TRANSLATION_SERVICE=google  # ou 'mymemory' pour traduction gratuite
"""
    
    env_file = Path(".env.template")
    if not env_file.exists():
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_template)
        print_success("Fichier .env.template créé")
        print_warning("Copiez-le en .env et remplissez vos valeurs")
    else:
        print_success("Fichier .env.template existe déjà")

def main():
    print(f"""
{Colors.BLUE}
╔══════════════════════════════════════════════════════════════╗
║  🎬 Setup des Améliorations - Moteur de Recherche de Films  ║
║                       Version 2.0                            ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}
    """)
    
    try:
        # Exécuter les vérifications et configurations
        setup_directories()
        create_placeholder_sounds()
        check_dependencies()
        check_tmdb_api_key()
        create_env_file_template()
        display_instructions()
        
        print_header("Configuration terminée!")
        print_success("L'application est prête à démarrer!")
        print_warning("N'oubliez pas de configurer TMDB_API_KEY avant de lancer l'app")
        
    except Exception as e:
        print_error(f"Erreur lors de la configuration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
