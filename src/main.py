"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import sys

try:
    from src import recommender  # python -m src.main
except ImportError:
    import recommender  # python src/main.py

load_songs = recommender.load_songs
recommend_songs = recommender.recommend_songs


WIDTH = 60


PROFILES = {
    # --- Standard profiles ---
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.90, "acousticness": 0.10},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.40, "acousticness": 0.75},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92, "acousticness": 0.08},
    # --- Adversarial / edge-case profiles ---
    # Conflicting: wants a sad mood but maximum energy.
    "Adversarial: Sad but Energetic": {"genre": "classical", "mood": "melancholy", "energy": 0.95, "acousticness": 0.90},
    # Genre and mood that do not exist in the catalog: only numbers can score.
    "Adversarial: Unknown Genre (k-pop)": {"genre": "k-pop", "mood": "bubbly", "energy": 0.80, "acousticness": 0.20},
    # Right genre and mood, but the numbers describe a totally different song.
    "Adversarial: Lofi Label, Metal Numbers": {"genre": "lofi", "mood": "chill", "energy": 0.97, "acousticness": 0.04},
}


def print_recommendations(name: str, user_prefs: dict, recommendations: list) -> None:
    """Print a readable ranked list: title, score and one line per reason."""
    profile = ", ".join(f"{key}={value}" for key, value in user_prefs.items())
    print("=" * WIDTH)
    print(f"  {name}")
    print(f"  Profile: {profile}")
    print("=" * WIDTH)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} - {song['artist']}")
        print(f"   Score: {score:.2f} pts   [{song['genre']}, {song['mood']}]")
        print("   Why:")
        for reason in explanation.split("; "):
            print(f"     - {reason}")

    print("\n" + "=" * WIDTH + "\n")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Experiment: double the importance of energy, halve the importance of genre.
    if "--experiment" in sys.argv:
        recommender.GENRE_WEIGHT = 1.0   # was 2.0
        recommender.ENERGY_WEIGHT = 3.0  # was 1.5
        print("EXPERIMENT: genre weight 2.0 -> 1.0, energy weight 1.5 -> 3.0")
    print()

    for name, user_prefs in PROFILES.items():
        print_recommendations(name, user_prefs, recommend_songs(user_prefs, songs, k=5))


if __name__ == "__main__":
    main()
