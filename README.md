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

## Stress Test Output

Output of `python -m src.main` for six profiles. The first three are standard tastes. The last three are adversarial profiles meant to trick the scoring.

### High-Energy Pop

```
============================================================
  High-Energy Pop
  Profile: genre=pop, mood=happy, energy=0.9, acousticness=0.1
============================================================

1. Sunrise City - Neon Echo
   Score: 4.84 pts   [pop, happy]
   Why:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.82 vs target 0.90 (+1.38)
     - acousticness 0.18 vs target 0.10 (+0.46)

2. Gym Hero - Max Pulse
   Score: 3.93 pts   [pop, intense]
   Why:
     - genre match (+2.0)
     - energy 0.93 vs target 0.90 (+1.46)
     - acousticness 0.05 vs target 0.10 (+0.47)

3. Rooftop Lights - Indigo Parade
   Score: 2.67 pts   [indie pop, happy]
   Why:
     - mood match (+1.0)
     - energy 0.76 vs target 0.90 (+1.29)
     - acousticness 0.35 vs target 0.10 (+0.38)

4. Storm Runner - Voltline
   Score: 1.98 pts   [rock, intense]
   Why:
     - energy 0.91 vs target 0.90 (+1.48)
     - acousticness 0.10 vs target 0.10 (+0.50)

5. Neon Pulse - Circuit Bloom
   Score: 1.89 pts   [edm, euphoric]
   Why:
     - energy 0.95 vs target 0.90 (+1.43)
     - acousticness 0.03 vs target 0.10 (+0.46)
```

### Chill Lofi

```
============================================================
  Chill Lofi
  Profile: genre=lofi, mood=chill, energy=0.4, acousticness=0.75
============================================================

1. Midnight Coding - LoRoom
   Score: 4.95 pts   [lofi, chill]
   Why:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.42 vs target 0.40 (+1.47)
     - acousticness 0.71 vs target 0.75 (+0.48)

2. Library Rain - Paper Lanterns
   Score: 4.87 pts   [lofi, chill]
   Why:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.35 vs target 0.40 (+1.42)
     - acousticness 0.86 vs target 0.75 (+0.45)

3. Focus Flow - LoRoom
   Score: 3.98 pts   [lofi, focused]
   Why:
     - genre match (+2.0)
     - energy 0.40 vs target 0.40 (+1.50)
     - acousticness 0.78 vs target 0.75 (+0.48)

4. Spacewalk Thoughts - Orbit Bloom
   Score: 2.74 pts   [ambient, chill]
   Why:
     - mood match (+1.0)
     - energy 0.28 vs target 0.40 (+1.32)
     - acousticness 0.92 vs target 0.75 (+0.41)

5. Coffee Shop Stories - Slow Stereo
   Score: 1.89 pts   [jazz, relaxed]
   Why:
     - energy 0.37 vs target 0.40 (+1.46)
     - acousticness 0.89 vs target 0.75 (+0.43)
```

### Deep Intense Rock

```
============================================================
  Deep Intense Rock
  Profile: genre=rock, mood=intense, energy=0.92, acousticness=0.08
============================================================

1. Storm Runner - Voltline
   Score: 4.97 pts   [rock, intense]
   Why:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.91 vs target 0.92 (+1.48)
     - acousticness 0.10 vs target 0.08 (+0.49)

2. Gym Hero - Max Pulse
   Score: 2.97 pts   [pop, intense]
   Why:
     - mood match (+1.0)
     - energy 0.93 vs target 0.92 (+1.48)
     - acousticness 0.05 vs target 0.08 (+0.48)

3. Neon Pulse - Circuit Bloom
   Score: 1.93 pts   [edm, euphoric]
   Why:
     - energy 0.95 vs target 0.92 (+1.46)
     - acousticness 0.03 vs target 0.08 (+0.47)

4. Iron Cathedral - Black Tessera
   Score: 1.91 pts   [metal, aggressive]
   Why:
     - energy 0.97 vs target 0.92 (+1.43)
     - acousticness 0.04 vs target 0.08 (+0.48)

5. Sunrise City - Neon Echo
   Score: 1.80 pts   [pop, happy]
   Why:
     - energy 0.82 vs target 0.92 (+1.35)
     - acousticness 0.18 vs target 0.08 (+0.45)
```

### Adversarial: Sad but Energetic

```
============================================================
  Adversarial: Sad but Energetic
  Profile: genre=classical, mood=melancholy, energy=0.95, acousticness=0.9
============================================================

1. Nocturne in Rain - Elise Varga
   Score: 3.88 pts   [classical, melancholy]
   Why:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.22 vs target 0.95 (+0.41)
     - acousticness 0.95 vs target 0.90 (+0.48)

2. Neon Pulse - Circuit Bloom
   Score: 1.56 pts   [edm, euphoric]
   Why:
     - energy 0.95 vs target 0.95 (+1.50)
     - acousticness 0.03 vs target 0.90 (+0.07)

3. Gym Hero - Max Pulse
   Score: 1.55 pts   [pop, intense]
   Why:
     - energy 0.93 vs target 0.95 (+1.47)
     - acousticness 0.05 vs target 0.90 (+0.08)

4. Storm Runner - Voltline
   Score: 1.54 pts   [rock, intense]
   Why:
     - energy 0.91 vs target 0.95 (+1.44)
     - acousticness 0.10 vs target 0.90 (+0.10)

5. Iron Cathedral - Black Tessera
   Score: 1.54 pts   [metal, aggressive]
   Why:
     - energy 0.97 vs target 0.95 (+1.47)
     - acousticness 0.04 vs target 0.90 (+0.07)
```

### Adversarial: Unknown Genre (k-pop)

```
============================================================
  Adversarial: Unknown Genre (k-pop)
  Profile: genre=k-pop, mood=bubbly, energy=0.8, acousticness=0.2
============================================================

1. Sunrise City - Neon Echo
   Score: 1.96 pts   [pop, happy]
   Why:
     - energy 0.82 vs target 0.80 (+1.47)
     - acousticness 0.18 vs target 0.20 (+0.49)

2. Concrete Crown - Rhyme Atlas
   Score: 1.93 pts   [hip hop, confident]
   Why:
     - energy 0.78 vs target 0.80 (+1.47)
     - acousticness 0.12 vs target 0.20 (+0.46)

3. Night Drive Loop - Neon Echo
   Score: 1.91 pts   [synthwave, moody]
   Why:
     - energy 0.75 vs target 0.80 (+1.42)
     - acousticness 0.22 vs target 0.20 (+0.49)

4. Rooftop Lights - Indigo Parade
   Score: 1.86 pts   [indie pop, happy]
   Why:
     - energy 0.76 vs target 0.80 (+1.44)
     - acousticness 0.35 vs target 0.20 (+0.43)

5. Storm Runner - Voltline
   Score: 1.78 pts   [rock, intense]
   Why:
     - energy 0.91 vs target 0.80 (+1.33)
     - acousticness 0.10 vs target 0.20 (+0.45)
```

### Adversarial: Lofi Label, Metal Numbers

```
============================================================
  Adversarial: Lofi Label, Metal Numbers
  Profile: genre=lofi, mood=chill, energy=0.97, acousticness=0.04
============================================================

1. Midnight Coding - LoRoom
   Score: 3.84 pts   [lofi, chill]
   Why:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.42 vs target 0.97 (+0.67)
     - acousticness 0.71 vs target 0.04 (+0.17)

2. Library Rain - Paper Lanterns
   Score: 3.66 pts   [lofi, chill]
   Why:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy 0.35 vs target 0.97 (+0.57)
     - acousticness 0.86 vs target 0.04 (+0.09)

3. Focus Flow - LoRoom
   Score: 2.77 pts   [lofi, focused]
   Why:
     - genre match (+2.0)
     - energy 0.40 vs target 0.97 (+0.65)
     - acousticness 0.78 vs target 0.04 (+0.13)

4. Iron Cathedral - Black Tessera
   Score: 2.00 pts   [metal, aggressive]
   Why:
     - energy 0.97 vs target 0.97 (+1.50)
     - acousticness 0.04 vs target 0.04 (+0.50)

5. Neon Pulse - Circuit Bloom
   Score: 1.96 pts   [edm, euphoric]
   Why:
     - energy 0.95 vs target 0.97 (+1.47)
     - acousticness 0.03 vs target 0.04 (+0.49)

============================================================
```

---

## Experiments You Tried

**Weight shift: double energy, halve genre.** Run with `python -m src.main --experiment`. Genre goes from 2.0 to 1.0 and energy from 1.5 to 3.0. The maximum possible score rises from 5.0 to 5.5, but scores are still a sum of non-negative terms, so the math stays valid.

| Profile | Baseline top 3 | Experiment top 3 |
|---|---|---|
| High-Energy Pop | Sunrise City, Gym Hero, Rooftop Lights | same order |
| Chill Lofi | Midnight Coding, Library Rain, Focus Flow | same order |
| Deep Intense Rock | Storm Runner, Gym Hero, Neon Pulse | same order |
| Sad but Energetic | Nocturne in Rain (3.88), then a 1.5 pt pack | Nocturne in Rain (3.29), with the pack now at ~3.0 |
| Unknown Genre (k-pop) | Sunrise City, Concrete Crown, Night Drive Loop | same order |
| Lofi Label, Metal Numbers | Midnight Coding, Library Rain, Focus Flow | Midnight Coding, **Iron Cathedral**, Neon Pulse |

For normal profiles the change made the scores bigger but did not change the order, so it was not more accurate, just different in scale. It only mattered for the contradictory profile, where the energy and acousticness numbers now pull the result toward Iron Cathedral and Neon Pulse. That is arguably closer to what the numbers ask for, but it also made the sad-but-energetic profile less sure of its top pick (3.29 vs. 3.06 for second place).

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



