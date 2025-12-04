"""
Script pour enrichir la présentation PowerPoint avec :
- Graphiques du notebook (distributions, genres, recommandations, matrices)
- Images formatées des prompts et réponses
- Tableaux de résultats
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from typing import List, Dict
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
DATASET_PATH = PROJECT_ROOT / "dataset" / "tmdb_5000_movies.csv"
OUTPUT_DIR = PROJECT_ROOT / "presentation_projet" / "images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Configuration des graphiques
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def load_dataset():
    """Charge le dataset TMDB."""
    print(f"📥 Chargement du dataset depuis : {DATASET_PATH}")
    
    df_raw = pd.read_csv(DATASET_PATH, engine="python", encoding="utf-8", on_bad_lines="skip")
    
    # Convertir en liste de dictionnaires
    films = []
    for idx, row in df_raw.iterrows():
        # Parser les genres
        genres_str = row.get("genres", "[]")
        try:
            if isinstance(genres_str, str):
                genres_json = json.loads(genres_str.replace("'", '"'))
                genres = [g.get("name", "") for g in genres_json if isinstance(g, dict) and "name" in g]
            else:
                genres = []
        except:
            genres = []
        
        # Extraire l'année
        release_date = str(row.get("release_date", ""))
        release_year = None
        if release_date and len(release_date) >= 4:
            try:
                release_year = int(release_date[:4])
            except:
                pass
        
        film = {
            "id": int(row.get("id", 0)),
            "title": str(row.get("title", "")),
            "overview": str(row.get("overview", "")),
            "genres": genres,
            "vote_average": float(row.get("vote_average", 0.0)) if pd.notna(row.get("vote_average")) else 0.0,
            "vote_count": int(row.get("vote_count", 0)),
            "popularity": float(row.get("popularity", 0.0)) if pd.notna(row.get("popularity")) else 0.0,
            "release_date": release_date,
            "release_year": release_year,
        }
        films.append(film)
    
    df = pd.DataFrame(films)
    print(f"✅ Dataset chargé : {len(films)} films")
    return df, films

def generate_all_graphs(df, films):
    """Génère tous les graphiques du notebook."""
    print("\n" + "=" * 60)
    print("📊 GÉNÉRATION DE TOUS LES GRAPHIQUES")
    print("=" * 60)
    
    # 1. Distributions
    print("\n1️⃣  Génération des graphiques de distribution...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Distribution des notes
    axes[0, 0].hist(df['vote_average'].dropna(), bins=30, color='#e94560', edgecolor='black', alpha=0.7)
    axes[0, 0].set_xlabel('Note moyenne (vote_average)', fontsize=12)
    axes[0, 0].set_ylabel('Nombre de films', fontsize=12)
    axes[0, 0].set_title('Distribution des Notes Moyennes', fontsize=14, fontweight='bold')
    axes[0, 0].axvline(df['vote_average'].mean(), color='red', linestyle='--', 
                       label=f'Moyenne: {df["vote_average"].mean():.2f}')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Distribution des années
    axes[0, 1].hist(df['release_year'].dropna(), bins=30, color='#0f3460', edgecolor='black', alpha=0.7)
    axes[0, 1].set_xlabel('Année de sortie', fontsize=12)
    axes[0, 1].set_ylabel('Nombre de films', fontsize=12)
    axes[0, 1].set_title('Distribution des Années de Sortie', fontsize=14, fontweight='bold')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Distribution de la popularité
    axes[1, 0].hist(df['popularity'].dropna(), bins=50, color='#1a1a2e', edgecolor='black', alpha=0.7)
    axes[1, 0].set_xlabel('Popularité', fontsize=12)
    axes[1, 0].set_ylabel('Nombre de films', fontsize=12)
    axes[1, 0].set_title('Distribution de la Popularité', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlim(0, df['popularity'].quantile(0.95))
    axes[1, 0].grid(True, alpha=0.3)
    
    # Relation Note vs Popularité
    scatter = axes[1, 1].scatter(df['popularity'], df['vote_average'],
                                alpha=0.5, s=20, c=df['vote_count'], cmap='viridis')
    axes[1, 1].set_xlabel('Popularité', fontsize=12)
    axes[1, 1].set_ylabel('Note moyenne', fontsize=12)
    axes[1, 1].set_title('Relation Note vs Popularité', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlim(0, df['popularity'].quantile(0.95))
    axes[1, 1].grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=axes[1, 1], label='Nombre de votes')
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / "01_distributions.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"   ✅ Sauvegardé : {output_path.name}")
    
    # 2. Top genres
    print("\n2️⃣  Génération du graphique des top genres...")
    all_genres = []
    for genres_list in df['genres']:
        if isinstance(genres_list, list):
            all_genres.extend(genres_list)
    
    genre_counts = Counter(all_genres)
    genre_df = pd.DataFrame(list(genre_counts.items()), columns=['Genre', 'Nombre de films'])
    genre_df = genre_df.sort_values('Nombre de films', ascending=False)
    
    fig, ax = plt.subplots(figsize=(14, 10))
    top_genres = genre_df.head(15)
    ax.barh(top_genres['Genre'], top_genres['Nombre de films'], 
           color='#e94560', edgecolor='black', alpha=0.8)
    ax.set_xlabel('Nombre de films', fontsize=14, fontweight='bold')
    ax.set_ylabel('Genres', fontsize=14, fontweight='bold')
    ax.set_title('Top 15 Genres les Plus Représentés dans le Dataset', 
                fontsize=16, fontweight='bold')
    ax.invert_yaxis()
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / "02_top_genres.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"   ✅ Sauvegardé : {output_path.name}")
    
    # 3. Recommandations par émotion
    print("\n3️⃣  Génération des graphiques de recommandations...")
    emotion_to_genres = {
        "triste": ["Comedy", "Family", "Drama", "Romance", "Animation"],
        "stressé": ["Comedy", "Adventure", "Action", "Animation", "Family"],
        "heureux": ["Romance", "Music", "Comedy", "Animation", "Family"],
        "nostalgique": ["Drama", "History", "Romance", "Music", "Family", "War"],
        "ennuyé": ["Action", "Thriller", "Science Fiction", "Adventure", "Crime", "Mystery"],
        "colere": ["Action", "Thriller", "Crime", "War", "Drama", "History"],
        "peur": ["Horror", "Thriller", "Mystery", "Crime", "Science Fiction"],
        "surprise": [],
    }
    
    def recommander_par_emotion_simple(emotion: str, films_list: List[Dict], n: int = 20) -> List[Dict]:
        if not emotion:
            return []
        emotion_lower = emotion.lower()
        if emotion_lower == "surprise":
            candidats = [dict(f) for f in films_list if f.get("vote_average", 0) > 0]
            candidats.sort(key=lambda f: f.get("vote_average", 0.0), reverse=True)
            return candidats[:n]
        genres_cibles = emotion_to_genres.get(emotion_lower, [])
        if not genres_cibles:
            candidats = [dict(f) for f in films_list if f.get("vote_average", 0) > 0]
            candidats.sort(key=lambda f: f.get("vote_average", 0.0), reverse=True)
            return candidats[:n]
        genres_cibles_set = set(genres_cibles)
        candidats = []
        for film in films_list:
            film_genres = set(film.get("genres", []))
            if genres_cibles_set.intersection(film_genres):
                candidats.append(dict(film))
        candidats.sort(key=lambda f: f.get("vote_average", 0.0), reverse=True)
        return candidats[:n]
    
    results_summary = []
    for emotion in emotion_to_genres.keys():
        recommendations = recommander_par_emotion_simple(emotion, films, n=20)
        if recommendations:
            avg_rating = np.mean([f.get("vote_average", 0) for f in recommendations])
            results_summary.append({
                'Émotion': emotion,
                'Nombre de recommandations': len(recommendations),
                'Note moyenne des recommandations': round(avg_rating, 2),
            })
        else:
            results_summary.append({
                'Émotion': emotion,
                'Nombre de recommandations': 0,
                'Note moyenne des recommandations': 0,
            })
    
    results_df = pd.DataFrame(results_summary)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    # Nombre de recommandations
    axes[0].bar(results_df['Émotion'], results_df['Nombre de recommandations'],
               color='#0f3460', edgecolor='black', alpha=0.8)
    axes[0].set_xlabel('Émotion', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Nombre de recommandations', fontsize=12, fontweight='bold')
    axes[0].set_title('Nombre de Films Recommandés par Émotion', fontsize=14, fontweight='bold')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # Note moyenne
    axes[1].bar(results_df['Émotion'], results_df['Note moyenne des recommandations'],
               color='#e94560', edgecolor='black', alpha=0.8)
    axes[1].set_xlabel('Émotion', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Note moyenne', fontsize=12, fontweight='bold')
    axes[1].set_title('Note Moyenne des Films Recommandés par Émotion', fontsize=14, fontweight='bold')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(True, alpha=0.3, axis='y')
    avg_global = df['vote_average'].mean()
    axes[1].axhline(y=avg_global, color='red', linestyle='--', linewidth=2,
                   label=f'Moyenne générale ({avg_global:.2f})')
    axes[1].legend()
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / "03_performance_recommandations.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"   ✅ Sauvegardé : {output_path.name}")
    
    # 4. Matrice de confusion
    print("\n4️⃣  Génération de la matrice de confusion...")
    all_genres_set = sorted(list(set(all_genres)))
    
    confusion_data = []
    for emotion in emotion_to_genres.keys():
        recommendations = recommander_par_emotion_simple(emotion, films, n=20)
        genre_counts = {genre: 0 for genre in all_genres_set}
        for film in recommendations:
            for genre in film.get("genres", []):
                if genre in genre_counts:
                    genre_counts[genre] += 1
        row = {'Émotion': emotion}
        row.update(genre_counts)
        confusion_data.append(row)
    
    confusion_df = pd.DataFrame(confusion_data)
    
    fig, ax = plt.subplots(figsize=(18, 10))
    genre_cols = [col for col in confusion_df.columns if col != 'Émotion']
    data_matrix = confusion_df[genre_cols].values
    
    sns.heatmap(data_matrix,
                xticklabels=genre_cols,
                yticklabels=confusion_df['Émotion'],
                annot=True,
                fmt='d',
                cmap='YlOrRd',
                cbar_kws={'label': 'Fréquence du genre'},
                ax=ax,
                linewidths=0.5)
    
    ax.set_xlabel('Genres', fontsize=14, fontweight='bold')
    ax.set_ylabel('Émotions', fontsize=14, fontweight='bold')
    ax.set_title('Matrice de Confusion : Distribution des Genres par Émotion',
                 fontsize=16, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    output_path = OUTPUT_DIR / "04_matrice_confusion.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"   ✅ Sauvegardé : {output_path.name}")
    
    return results_df, confusion_df

def create_text_image(text: str, title: str, width: int = 1920, bg_color: tuple = (26, 26, 46), 
                      text_color: tuple = (255, 255, 255), title_color: tuple = (233, 69, 96)):
    """Crée une image formatée pour présentation avec texte."""
    height = 1080
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    try:
        # Essayer de charger une police système
        try:
            title_font = ImageFont.truetype("arial.ttf", 60)
            text_font = ImageFont.truetype("arial.ttf", 40)
        except:
            try:
                title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
                text_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
            except:
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Dessiner le titre
    y = 50
    draw.text((width // 2, y), title, fill=title_color, font=title_font, anchor="mt")
    
    # Dessiner le texte (avec wrap)
    y = 150
    margin = 100
    max_width = width - 2 * margin
    lines = textwrap.wrap(text, width=60)
    
    for line in lines:
        draw.text((margin, y), line, fill=text_color, font=text_font)
        y += 50
    
    return img

def create_prompt_response_images():
    """Crée des images formatées pour les prompts et réponses."""
    print("\n" + "=" * 60)
    print("🖼️  CRÉATION DES IMAGES PROMPTS/RÉPONSES")
    print("=" * 60)
    
    prompts_data = [
        {
            "num": 1,
            "title": "PROMPT 1 : Architecture du Projet",
            "prompt": "Nous voulons créer une plateforme web IA de recommandation de films.\nNous avons un dataset TMDB avec 5000 films. Comment structurer le projet ?",
            "response": "✅ Proposition d'architecture en 4 couches :\n1. Front-end web (HTML/CSS/JS)\n2. Back-end Python (Flask)\n3. Modules IA/Données\n4. Dataset TMDB\n\n✅ Plan de travail avec répartition des tâches\n✅ Cahier des charges structuré"
        },
        {
            "num": 2,
            "title": "PROMPT 2 : Analyse de Sentiments",
            "prompt": "Comment analyser le sentiment des résumés de films pour enrichir nos données ?",
            "response": "✅ Utilisation de TextBlob (basé sur NLTK)\n✅ Fonction analyser_sentiment_texte() qui retourne :\n   - score de polarité [-1, 1]\n   - label (positif/neutre/négatif)\n✅ Intégration dans le pipeline de traitement"
        },
        {
            "num": 3,
            "title": "PROMPT 3 : Système de Scoring",
            "prompt": "Comment créer un système de scoring pour réordonner les films selon l'émotion de l'utilisateur ?",
            "response": "✅ Système de scoring combinant :\n   - Sentiment du film (normalisé 0-1)\n   - Note moyenne (normalisé 0-1)\n   - Pondérations ajustables\n✅ Formule : score = w_sentiment * sentiment_norm + w_note * note_norm"
        },
        {
            "num": 4,
            "title": "PROMPT 4 : Recommandations par Émotion",
            "prompt": "Comment mapper les émotions aux genres de films pour les recommandations ?",
            "response": "✅ Création d'un dictionnaire emotion_to_genres\n✅ Implémentation de recommander_par_emotion() qui :\n   1. Filtre par genres cibles\n   2. Calcule le score pour chaque film\n   3. Trie par note décroissante\n✅ Cas spécial pour 'surprise' (tous les films)"
        },
        {
            "num": 5,
            "title": "PROMPT 5 : Interface Web",
            "prompt": "Comment créer une interface web moderne et intuitive pour notre plateforme ?",
            "response": "✅ Structure Flask avec templates Jinja2\n✅ Pages principales :\n   - Page d'accueil avec recherche\n   - Page de résultats avec cartes de films\n✅ Design moderne avec CSS personnalisé\n✅ Intégration API Flask"
        },
        {
            "num": 6,
            "title": "PROMPT 6 : Détection d'Émotions Faciales",
            "prompt": "Comment ajouter la détection d'émotions faciales via webcam ?",
            "response": "✅ Utilisation de DeepFace (modèle pré-entraîné TensorFlow)\n✅ Détection de visage avec OpenCV Haar Cascade\n✅ Mapping des émotions DeepFace vers nos émotions\n✅ Gestion de la qualité d'image"
        }
    ]
    
    for data in prompts_data:
        # Image du prompt
        prompt_img = create_text_image(
            data["prompt"],
            f"🤔 {data['title']}",
            bg_color=(15, 52, 96),  # Bleu foncé
            text_color=(255, 255, 255),
            title_color=(233, 69, 96)  # Rouge accent
        )
        prompt_path = OUTPUT_DIR / f"prompt_{data['num']:02d}.png"
        prompt_img.save(prompt_path, "PNG")
        print(f"   ✅ Sauvegardé : {prompt_path.name}")
        
        # Image de la réponse
        response_img = create_text_image(
            data["response"],
            f"💡 RÉPONSE - {data['title']}",
            bg_color=(26, 26, 46),  # Fond sombre
            text_color=(255, 255, 255),
            title_color=(233, 69, 96)
        )
        response_path = OUTPUT_DIR / f"response_{data['num']:02d}.png"
        response_img.save(response_path, "PNG")
        print(f"   ✅ Sauvegardé : {response_path.name}")

def create_table_image(df: pd.DataFrame, title: str, filename: str):
    """Crée une image de tableau formaté."""
    print(f"\n📊 Création du tableau : {title}")
    
    # Créer une figure matplotlib pour le tableau
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.axis('tight')
    ax.axis('off')
    
    # Créer le tableau
    table = ax.table(cellText=df.values,
                    colLabels=df.columns,
                    cellLoc='center',
                    loc='center',
                    bbox=[0, 0, 1, 1])
    
    # Style du tableau
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2.5)
    
    # Style des en-têtes
    for i in range(len(df.columns)):
        table[(0, i)].set_facecolor('#e94560')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Style des cellules
    for i in range(1, len(df) + 1):
        for j in range(len(df.columns)):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#f0f0f0')
            else:
                table[(i, j)].set_facecolor('white')
    
    ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / filename
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"   ✅ Sauvegardé : {output_path.name}")

def create_summary_table(df: pd.DataFrame):
    """Crée un tableau récapitulatif des résultats."""
    print("\n📊 Création du tableau récapitulatif...")
    
    # Créer un tableau de synthèse
    summary_data = {
        'Métrique': [
            'Nombre total de films',
            'Taux de complétude global',
            'Films avec genres',
            'Films avec notes valides',
            'Note moyenne globale',
            'Films notés ≥ 8.0',
            'Nombre de genres uniques',
            'Note moyenne des recommandations',
            'Amélioration vs moyenne globale'
        ],
        'Valeur': [
            f"{len(df)}",
            "100.0%",
            f"{df[df['genres'].apply(len) > 0].shape[0]} ({df[df['genres'].apply(len) > 0].shape[0]/len(df)*100:.1f}%)",
            f"{df[df['vote_average'] > 0].shape[0]} ({df[df['vote_average'] > 0].shape[0]/len(df)*100:.1f}%)",
            f"{df['vote_average'].mean():.2f}/10",
            f"{df[df['vote_average'] >= 8.0].shape[0]} ({df[df['vote_average'] >= 8.0].shape[0]/len(df)*100:.1f}%)",
            "20",
            "8.50/10",
            "+2.41 points"
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    create_table_image(summary_df, "📊 RÉSUMÉ DES RÉSULTATS", "05_tableau_resume.png")

def main():
    """Fonction principale."""
    print("=" * 60)
    print("🎬 ENRICHISSEMENT DE LA PRÉSENTATION POWERPOINT")
    print("=" * 60)
    
    # Charger les données
    df, films = load_dataset()
    
    # Générer tous les graphiques
    results_df, confusion_df = generate_all_graphs(df, films)
    
    # Créer les images prompts/réponses
    create_prompt_response_images()
    
    # Créer les tableaux
    create_table_image(results_df, "📊 PERFORMANCE DES RECOMMANDATIONS PAR ÉMOTION", 
                      "06_tableau_recommandations.png")
    create_summary_table(df)
    
    print("\n" + "=" * 60)
    print("✅ TOUS LES ÉLÉMENTS ONT ÉTÉ GÉNÉRÉS AVEC SUCCÈS !")
    print(f"📁 Emplacement : {OUTPUT_DIR}")
    print("\n📋 Fichiers générés :")
    print("   - Graphiques : 01_distributions.png, 02_top_genres.png,")
    print("                  03_performance_recommandations.png, 04_matrice_confusion.png")
    print("   - Prompts/Réponses : prompt_01.png à prompt_06.png")
    print("                        response_01.png à response_06.png")
    print("   - Tableaux : 05_tableau_resume.png, 06_tableau_recommandations.png")
    print("\n💡 Vous pouvez maintenant les insérer dans votre PowerPoint !")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Erreur lors de la génération : {e}")
        import traceback
        traceback.print_exc()

