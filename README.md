# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

This is a **content-based** recommender: it never looks at other users, only at how well each song's attributes match one user's taste profile.

### Song features

The catalog (`data/songs.csv`) has 18 songs across 15 genres and 14 moods. Each song stores:

- **Categorical:** `genre`, `mood`
- **Numeric (0.0–1.0):** `energy`, `valence`, `danceability`, `acousticness`
- **Numeric (other scale):** `tempo_bpm`, which isn't scored yet

### User profile

The profile is a dictionary of target values:

```python
user_prefs = {
    "genre": "lofi",
    "mood": "chill",
    "energy": 0.40,
    "acousticness": 0.75,
}
```

I checked this profile against the "intense rock vs. chill lofi" question. Energy and acousticness sit at opposite ends for those two tastes (energy 0.40 vs. 0.92, acousticness 0.75 vs. 0.08). That gives the system numeric signals to separate them even when genre and mood don't match. A profile with only genre and mood would be too narrow, because every song outside that genre and mood would tie at zero.

### Algorithm recipe

Each song gets a score from 0 to 5.0:

| Rule | Points |
|---|---|
| Genre matches `favorite_genre` | +2.0 |
| Mood matches `favorite_mood` | +1.0 |
| Energy closeness: `1.5 × (1 − abs(song.energy − target_energy))` | 0 to 1.5 |
| Acousticness closeness: `0.5 × (1 − abs(song.acousticness − target_acousticness))` | 0 to 0.5 |

Genre is weighted above mood because a genre mismatch usually feels more jarring than a mood mismatch. Closeness scores reward near-misses instead of giving all-or-nothing credit.

A sanity check on the 18-song catalog gave sensible rankings:

- **Chill lofi profile:** Midnight Coding (4.95), Library Rain (4.87), Focus Flow (3.98)
- **Intense rock profile:** Storm Runner (4.97), then Gym Hero (2.97)

### Data flow

```
INPUT                    PROCESS (loop over every row)              OUTPUT
user_profile  ──►  for song in songs.csv:                    ──►  sort by score,
                     score = genre pts + mood pts                  descending
songs.csv     ──►            + energy closeness                    ──► top K
                             + acousticness closeness              recommendations
                     keep (song, score)
```

### Expected biases

- **Genre dominance.** Genre can contribute 2.0 of 5.0 points, so a song in the favorite genre that is wrong in every other way can outrank a song that fits the mood and energy perfectly in another genre.
- **Filter bubble.** The system only rewards similarity to the profile, so it won't surface surprising songs.
- **Small catalog.** Some genres (like lofi) have 3 songs and others have 1, so the top results are shaped by what happens to be in the file.
- **Exact-match labels.** "Chill" and "relaxed" count as a total mismatch even though they are close in meaning.
- **Unused features.** `tempo_bpm`, `valence` and `danceability` are ignored, so two songs with very different feel can score the same.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` for the default profile (`genre=pop, mood=happy, energy=0.8`):

```
Loaded songs: 18

============================================================
  TOP RECOMMENDATIONS
  Profile: genre=pop, mood=happy, energy=0.8
============================================================

1. Sunrise City - Neon Echo
   Score: 4.47 pts   [pop, happy]
   Why:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.82 vs target 0.80 (+1.47)

2. Gym Hero - Max Pulse
   Score: 3.30 pts   [pop, intense]
   Why:
     - genre match (+2.0)
     - energy 0.93 vs target 0.80 (+1.30)

3. Rooftop Lights - Indigo Parade
   Score: 2.44 pts   [indie pop, happy]
   Why:
     - mood match (+1.0)
     - energy 0.76 vs target 0.80 (+1.44)

4. Concrete Crown - Rhyme Atlas
   Score: 1.47 pts   [hip hop, confident]
   Why:
     - energy 0.78 vs target 0.80 (+1.47)

5. Night Drive Loop - Neon Echo
   Score: 1.42 pts   [synthwave, moody]
   Why:
     - energy 0.75 vs target 0.80 (+1.42)

============================================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



