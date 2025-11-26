#!/usr/bin/env python3
"""
Script de diagnostic pour tester toutes les fonctionnalités de l'app.
Affiche ce qui fonctionne et ce qui ne fonctionne pas.
"""

import json
import sys
sys.path.insert(0, 'code')

from data_loading import charger_films_depuis_csv
from tmdb_api import enrichir_film_avec_api
from sound_manager import get_emotion_sound, get_movie_theme_sound, add_sound_to_film

print("=" * 80)
print("🔍 DIAGNOSTIC COMPLET DES FONCTIONNALITÉS")
print("=" * 80)

# 1. Charger les films
print("\n1️⃣  CHARGEMENT DES FILMS")
print("-" * 80)
films = charger_films_depuis_csv('data/dataset/tmdb_5000_movies.csv')
print(f"✅ Chargé {len(films)} films du CSV")
if films:
    film_test = films[0]
    print(f"   Film test: {film_test.get('title')} (ID: {film_test.get('id')})")

# 2. Vérifier les descriptions français
print("\n2️⃣  DESCRIPTIONS EN FRANÇAIS")
print("-" * 80)
film_test = films[0] if films else None
if film_test:
    has_overview_fr = 'overview_fr' in film_test
    overview_fr = film_test.get('overview_fr', '')[:100]
    print(f"   overview_fr présent: {has_overview_fr}")
    if overview_fr:
        print(f"   Texte: {overview_fr}...")
    else:
        print(f"   ⚠️ overview_fr vide ou non traduite")

# 3. Vérifier les images (poster/backdrop)
print("\n3️⃣  IMAGES (POSTER & BACKDROP)")
print("-" * 80)
if film_test:
    poster = film_test.get('poster_url', '')
    backdrop = film_test.get('backdrop_url', '')
    print(f"   poster_url: {poster[:50] if poster else '❌ VIDE'}...")
    print(f"   backdrop_url: {backdrop[:50] if backdrop else '❌ VIDE'}...")
    
    if not poster or not backdrop:
        print(f"   ⚠️ Images manquantes - TMDB enrichment n'a pas fonctionné")

# 4. Vérifier les trailers
print("\n4️⃣  TRAILERS (BANDE ANNONCE)")
print("-" * 80)
if film_test:
    trailer_url = film_test.get('trailer_url', '')
    trailer_key = film_test.get('trailer_key', '')
    print(f"   trailer_url: {trailer_url[:50] if trailer_url else '❌ VIDE'}...")
    print(f"   trailer_key: {trailer_key if trailer_key else '❌ VIDE'}")
    
    if not trailer_url and not trailer_key:
        print(f"   ⚠️ Trailers manquants")

# 5. Vérifier les liens streaming
print("\n5️⃣  LIENS STREAMING (PLATEFORMES)")
print("-" * 80)
if film_test:
    streaming = film_test.get('streaming_links', [])
    print(f"   Nombre de plateformes: {len(streaming) if streaming else 0}")
    if streaming:
        for link in streaming[:3]:
            print(f"   - {link.get('name', '?')}: {link.get('type', '?')}")
    else:
        print(f"   ⚠️ Aucun lien streaming")

# 6. Vérifier les sons d'émotion
print("\n6️⃣  SONS D'ÉMOTION (HEADER)")
print("-" * 80)
emotions = ['triste', 'stressé', 'heureux', 'nostalgique', 'surpris', 'ennuyé', 'peur', 'en_colère']
for emotion in emotions:
    sound_info = get_emotion_sound(emotion)
    sound_url = sound_info.get('url', '') if sound_info else ''
    status = "✅" if sound_url else "❌"
    print(f"   {status} {emotion}: {sound_url[:40] if sound_url else 'VIDE'}...")

# 7. Vérifier les sons de générique (musique du film)
print("\n7️⃣  SONS DE GÉNÉRIQUE (MUSIQUE DU FILM)")
print("-" * 80)
if film_test:
    film_id = film_test.get('id')
    title = film_test.get('title')
    theme_sound = get_movie_theme_sound(film_id, title)
    print(f"   Film: {title} (ID: {film_id})")
    print(f"   Theme sound: {theme_sound if theme_sound else '❌ VIDE (normal si pas de fichier local)'}")

# 8. Summary
print("\n" + "=" * 80)
print("📊 RÉSUMÉ")
print("=" * 80)

issues = []
if film_test:
    if not film_test.get('poster_url'):
        issues.append("❌ Images manquantes (poster_url vide)")
    if not film_test.get('backdrop_url'):
        issues.append("❌ Images manquantes (backdrop_url vide)")
    if not film_test.get('trailer_url'):
        issues.append("❌ Trailers manquants (trailer_url vide)")
    if not film_test.get('streaming_links'):
        issues.append("❌ Streaming links manquants")
    if not film_test.get('overview_fr'):
        issues.append("⚠️  Descriptions non traduites en français")

if issues:
    print("\n🔴 PROBLÈMES DÉTECTÉS:")
    for issue in issues:
        print(f"   {issue}")
    print("\n   → La plupart sont dus à la clé TMDB invalide")
    print("   → Voir INSTALLATION_STATUS.md pour les solutions")
else:
    print("\n✅ TOUS LES CHAMPS SONT PRÉSENTS!")

print("\n" + "=" * 80)
