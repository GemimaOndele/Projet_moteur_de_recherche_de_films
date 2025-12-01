#!/usr/bin/env python3
"""Script de diagnostic rapide : tester enrichissement TMDB sur 1 film."""

import os
import sys
import json

# Setup path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "code"))

from tmdb_api import enrichir_film_avec_api

# Film de test (ID 550 = Fight Club, film populaire)
test_film = {
    "id": 550,
    "title": "Fight Club",
    "overview": "An insomniac office worker and a devil-may-care soapmaker form an underground fight club..."
}

print("=" * 80)
print("🧪 TEST ENRICHISSEMENT TMDB")
print("=" * 80)
print(f"\n📽️ Film de test: {test_film['title']} (ID {test_film['id']})")
print(f"Clé TMDB: {os.getenv('TMDB_API_KEY', 'NON CONFIGURÉE')[:10]}...")

print("\n🔄 Appel enrichir_film_avec_api()...")
enriched = enrichir_film_avec_api(test_film)

print("\n📊 Résultats enrichissement:\n")
keys_to_check = [
    "poster_url",
    "backdrop_url",
    "trailer_url",
    "trailer_key",
    "overview_fr",
    "runtime",
    "streaming_links",
    "streaming_providers"
]

for key in keys_to_check:
    value = enriched.get(key)
    if value is None:
        print(f"  ❌ {key}: MANQUANT")
    elif isinstance(value, str):
        print(f"  ✅ {key}: {value[:60]}..." if len(value) > 60 else f"  ✅ {key}: {value}")
    elif isinstance(value, list):
        print(f"  ✅ {key}: {len(value)} items")
        if value and isinstance(value[0], dict):
            print(f"     Exemple: {value[0]}")
    elif isinstance(value, int):
        print(f"  ✅ {key}: {value}")
    else:
        print(f"  ✅ {key}: {str(value)[:60]}")

print("\n" + "=" * 80)
print("📝 RÉSUMÉ DES PROBLÈMES:\n")

issues = []
if not enriched.get("poster_url"):
    issues.append("❌ Pas de poster_url → images ne s'afficheront pas")
if not enriched.get("backdrop_url"):
    issues.append("❌ Pas de backdrop_url → fond de carte vide")
if not enriched.get("trailer_url"):
    issues.append("❌ Pas de trailer_url → bouton trailer ne fonctionnera pas")
if not enriched.get("overview_fr") or enriched.get("overview_fr") == enriched.get("overview"):
    issues.append("❌ overview_fr non traduit ou manquant → descriptions en anglais")
if not enriched.get("streaming_links"):
    issues.append("❌ Pas de streaming_links → section 'où regarder' vide")

if issues:
    for issue in issues:
        print(issue)
else:
    print("✅ TOUS LES CHAMPS ENRICHIS CORRECTEMENT!")

print("\n" + "=" * 80)
