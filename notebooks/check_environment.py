"""Script pour vérifier que l'environnement est correctement configuré pour le notebook."""

import sys
from pathlib import Path

print("🔍 Vérification de l'environnement...")
print("=" * 60)

# Vérifier Python
print(f"✅ Python : {sys.version.split()[0]}")

# Vérifier les imports essentiels
packages = {
    'numpy': 'numpy',
    'pandas': 'pandas',
    'matplotlib': 'matplotlib',
    'seaborn': 'seaborn',
    'PIL': 'Pillow'
}

print("\n📦 Vérification des packages :")
all_ok = True
for package_name, import_name in packages.items():
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'N/A')
        print(f"  ✅ {package_name}: {version}")
    except ImportError as e:
        print(f"  ❌ {package_name}: ERREUR - {e}")
        all_ok = False

# Vérifier le chemin
print("\n📁 Vérification des chemins :")
notebook_dir = Path(__file__).resolve().parent
project_root = notebook_dir.parent
code_dir = project_root / "code"

print(f"  📂 Dossier notebook : {notebook_dir}")
print(f"  📁 Dossier projet : {project_root}")
print(f"  📦 Dossier code : {code_dir}")

if code_dir.exists():
    print(f"  ✅ Dossier code existe")
else:
    print(f"  ❌ Dossier code introuvable")
    all_ok = False

# Vérifier les imports du projet
print("\n🔧 Vérification des modules du projet :")
sys.path.insert(0, str(code_dir))

project_modules = ['data_loading', 'recommendation', 'lib_projet']
for module_name in project_modules:
    try:
        __import__(module_name)
        print(f"  ✅ {module_name}")
    except ImportError as e:
        print(f"  ❌ {module_name}: {e}")
        all_ok = False

print("\n" + "=" * 60)
if all_ok:
    print("✅ Environnement correctement configuré !")
    print("🎉 Vous pouvez utiliser le notebook d'évaluation.")
    sys.exit(0)
else:
    print("❌ Des problèmes ont été détectés.")
    print("💡 Exécutez : pip install -r requirements.txt")
    sys.exit(1)

