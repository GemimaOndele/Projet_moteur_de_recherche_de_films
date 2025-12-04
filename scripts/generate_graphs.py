"""
Script pour générer et sauvegarder les graphiques du notebook d'évaluation
Les graphiques sont sauvegardés en PNG haute résolution dans notebooks/
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from typing import List, Dict
from pathlib import Path
import json

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
DATASET_PATH = PROJECT_ROOT / "dataset" / "tmdb_5000_movies.csv"
OUTPUT_DIR = PROJECT_ROOT / "notebooks"
OUTPUT_DIR.mkdir(exist_ok=True)

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

def generate_distribution_graphs(df):
    """Génère les graphiques de distribution des données."""
    print("\n📊 Génération des graphiques de distribution...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Distribution des notes
    axes[0, 0].hist(df['vote_average'].dropna(), bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    axes[0, 0].set_xlabel('Note moyenne (vote_average)')
    axes[0, 0].set_ylabel('Nombre de films')
    axes[0, 0].set_title('Distribution des Notes Moyennes')
    axes[0, 0].axvline(df['vote_average'].mean(), color='red', linestyle='--', 
                       label=f'Moyenne: {df["vote_average"].mean():.2f}')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Distribution des années de sortie
    axes[0, 1].hist(df['release_year'].dropna(), bins=30, color='lightcoral', edgecolor='black', alpha=0.7)
    axes[0, 1].set_xlabel('Année de sortie')
    axes[0, 1].set_ylabel('Nombre de films')
    axes[0, 1].set_title('Distribution des Années de Sortie')
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Distribution de la popularité
    axes[1, 0].hist(df['popularity'].dropna(), bins=50, color='lightgreen', edgecolor='black', alpha=0.7)
    axes[1, 0].set_xlabel('Popularité')
    axes[1, 0].set_ylabel('Nombre de films')
    axes[1, 0].set_title('Distribution de la Popularité')
    axes[1, 0].set_xlim(0, df['popularity'].quantile(0.95))
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. Relation Note vs Popularité
    scatter = axes[1, 1].scatter(df['popularity'], df['vote_average'],
                                alpha=0.5, s=20, c=df['vote_count'], cmap='viridis')
    axes[1, 1].set_xlabel('Popularité')
    axes[1, 1].set_ylabel('Note moyenne')
    axes[1, 1].set_title('Relation Note vs Popularité (couleur = nombre de votes)')
    axes[1, 1].set_xlim(0, df['popularity'].quantile(0.95))
    axes[1, 1].grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=axes[1, 1], label='Nombre de votes')
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / "distribution_des_notes.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Graphique sauvegardé : {output_path}")

def generate_top_genres_graph(df):
    """Génère le graphique des top genres."""
    print("\n📊 Génération du graphique des top genres...")
    
    # Analyser la distribution des genres
    all_genres = []
    for genres_list in df['genres']:
        if isinstance(genres_list, list):
            all_genres.extend(genres_list)
    
    genre_counts = Counter(all_genres)
    genre_df = pd.DataFrame(list(genre_counts.items()), columns=['Genre', 'Nombre de films'])
    genre_df = genre_df.sort_values('Nombre de films', ascending=False)
    
    # Visualisation
    fig, ax = plt.subplots(figsize=(12, 8))
    top_genres = genre_df.head(15)
    ax.barh(top_genres['Genre'], top_genres['Nombre de films'], 
           color='steelblue', edgecolor='black')
    ax.set_xlabel('Nombre de films', fontsize=12)
    ax.set_title('Top 15 Genres les Plus Représentés dans le Dataset', 
                fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / "top_genres.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Graphique sauvegardé : {output_path}")

def generate_recommendation_graphs(df, films):
    """Génère les graphiques de recommandations par émotion."""
    print("\n📊 Génération des graphiques de recommandations...")
    
    # Mapping émotions -> genres
    emotion_to_genres = {
        "triste": ["Comedy", "Family", "Drama", "Romance", "Animation"],
        "stressé": ["Comedy", "Adventure", "Action", "Animation", "Family"],
        "heureux": ["Romance", "Music", "Comedy", "Animation", "Family"],
        "nostalgique": ["Drama", "History", "Romance", "Music", "Family", "War"],
        "ennuyé": ["Action", "Thriller", "Science Fiction", "Adventure", "Crime", "Mystery"],
        "colere": ["Action", "Thriller", "Crime", "War", "Drama", "History"],
        "peur": ["Horror", "Thriller", "Mystery", "Crime", "Science Fiction"],
        "surprise": [],  # Cas spécial : retourne tous les films
    }
    
    def recommander_par_emotion_simple(emotion: str, films_list: List[Dict], n: int = 20) -> List[Dict]:
        """Version simplifiée de recommandation par émotion."""
        if not emotion:
            return []
        
        emotion_lower = emotion.lower()
        
        # Cas spécial pour 'surprise'
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
    
    # Test des recommandations pour chaque émotion
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
    
    # Visualisation
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # 1. Nombre de recommandations par émotion
    axes[0].bar(results_df['Émotion'], results_df['Nombre de recommandations'],
               color='lightblue', edgecolor='black', alpha=0.7)
    axes[0].set_xlabel('Émotion', fontsize=11)
    axes[0].set_ylabel('Nombre de recommandations', fontsize=11)
    axes[0].set_title('Nombre de Films Recommandés par Émotion', fontsize=13, fontweight='bold')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # 2. Note moyenne des recommandations par émotion
    axes[1].bar(results_df['Émotion'], results_df['Note moyenne des recommandations'],
               color='lightcoral', edgecolor='black', alpha=0.7)
    axes[1].set_xlabel('Émotion', fontsize=11)
    axes[1].set_ylabel('Note moyenne', fontsize=11)
    axes[1].set_title('Note Moyenne des Films Recommandés par Émotion', fontsize=13, fontweight='bold')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(True, alpha=0.3, axis='y')
    avg_global = df['vote_average'].mean()
    axes[1].axhline(y=avg_global, color='red', linestyle='--', linewidth=2,
                   label=f'Moyenne générale ({avg_global:.2f})')
    axes[1].legend()
    
    plt.tight_layout()
    output_path = OUTPUT_DIR / "performance_recommandations.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Graphique sauvegardé : {output_path}")

def generate_confusion_matrix(df, films):
    """Génère la matrice de confusion émotions × genres."""
    print("\n📊 Génération de la matrice de confusion...")
    
    # Mapping émotions -> genres
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
        """Version simplifiée de recommandation par émotion."""
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
    
    # Collecter tous les genres uniques
    all_genres = set()
    for genres_list in df['genres']:
        if isinstance(genres_list, list):
            all_genres.update(genres_list)
    all_genres = sorted(list(all_genres))
    
    # Construire la matrice de confusion
    confusion_data = []
    for emotion in emotion_to_genres.keys():
        recommendations = recommander_par_emotion_simple(emotion, films, n=20)
        
        # Compter les genres dans les recommandations
        genre_counts = {genre: 0 for genre in all_genres}
        for film in recommendations:
            for genre in film.get("genres", []):
                if genre in genre_counts:
                    genre_counts[genre] += 1
        
        row = {'Émotion': emotion}
        row.update(genre_counts)
        confusion_data.append(row)
    
    confusion_df = pd.DataFrame(confusion_data)
    
    # Visualisation
    fig, ax = plt.subplots(figsize=(16, 8))
    genre_cols = [col for col in confusion_df.columns if col != 'Émotion']
    data_matrix = confusion_df[genre_cols].values
    
    sns.heatmap(data_matrix,
                xticklabels=genre_cols,
                yticklabels=confusion_df['Émotion'],
                annot=True,
                fmt='d',
                cmap='YlOrRd',
                cbar_kws={'label': 'Fréquence du genre'},
                ax=ax)
    
    ax.set_xlabel('Genres', fontsize=12, fontweight='bold')
    ax.set_ylabel('Émotions', fontsize=12, fontweight='bold')
    ax.set_title('Matrice de Confusion : Distribution des Genres par Émotion',
                 fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    output_path = OUTPUT_DIR / "matrice_confusion.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Graphique sauvegardé : {output_path}")

def main():
    """Fonction principale."""
    print("=" * 60)
    print("🎬 GÉNÉRATION DES GRAPHIQUES POUR LA PRÉSENTATION")
    print("=" * 60)
    
    # Charger les données
    df, films = load_dataset()
    
    # Générer les graphiques
    generate_distribution_graphs(df)
    generate_top_genres_graph(df)
    generate_recommendation_graphs(df, films)
    generate_confusion_matrix(df, films)
    
    print("\n" + "=" * 60)
    print("✅ Tous les graphiques ont été générés avec succès !")
    print(f"📁 Emplacement : {OUTPUT_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Erreur lors de la génération : {e}")
        import traceback
        traceback.print_exc()

