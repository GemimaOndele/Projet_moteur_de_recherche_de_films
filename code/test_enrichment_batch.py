#!/usr/bin/env python3
"""Script de diagnostic : tester enrichissement TMDB pour plusieurs films."""

import os
import sys

# Ajouter code/ au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "code"))

from tmdb_api import enrichir_film_avec_api

# Films de test: (id, title)
films_to_test = [
    {"id": 6016, "title": "The Good Thief"},
    {"id": 205596, "title": "The Imitation Game"},
    {"id": 323677, "title": "Race"},
]

print("=" * 80)
print("🧪 TEST ENRICHISSEMENT TMDB - BATCH")
print("=" * 80)
print(f"TMDB API KEY: {os.getenv('TMDB_API_KEY', 'NON CONFIGURÉE')[:15]}...")
print(f"TMDB API TOKEN: {('CONFIGURÉ' if os.getenv('TMDB_API_TOKEN') else 'NON CONFIGURÉ')}")

for f in films_to_test:
    print("\n" + "-" * 40)
    print(f"🔎 Film: {f['title']} (ID {f['id']})")
    enriched = enrichir_film_avec_api(f.copy())

    fields = [
        "poster_url",
        "backdrop_url",
        "trailer_url",
        "trailer_key",
        "overview_fr",
        "runtime",
        "streaming_links",
        "streaming_providers",
    ]

    for key in fields:
        val = enriched.get(key)
        ok = False
        # For trailer_key, accept either an explicit key or a trailer_url
        if key == "trailer_key":
            ok = bool(val) or bool(enriched.get("trailer_url"))
        elif key in ["poster_url", "backdrop_url", "trailer_url", "overview_fr"]:
            ok = bool(val)
        elif key == "runtime":
            ok = val is not None and val > 0
        elif key == "streaming_links":
            ok = isinstance(val, list) and len(val) > 0
        elif key == "streaming_providers":
            # Accept if providers list is present OR streaming_links exists (we can derive providers)
            if isinstance(val, list) and len(val) > 0:
                ok = True
            else:
                sl = enriched.get("streaming_links")
                ok = isinstance(sl, list) and len(sl) > 0

        status = "✅" if ok else "❌"
        print(f"{status} {key}: {str(val) if val else 'None or empty'}")

print("\n" + "=" * 80)
print("Fin du test batch.")
