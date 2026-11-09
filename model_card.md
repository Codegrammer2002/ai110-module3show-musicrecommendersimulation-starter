# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

The system rewards exact label matches, so a user whose tastes don't line up with the catalog's labels gets weaker results. With the "k-pop / bubbly" profile, nothing matches on genre or mood, so every song is ranked by energy and acousticness alone, and the top five land within 0.2 points of each other (1.96 down to 1.78). Sunrise City came first, but it beat a hip hop track and a moody synthwave track by only 0.03 to 0.05 points, purely because its energy was a hair closer. Genre is also worth a lot (2.0 of 5.0 points), so the "Lofi Label, Metal Numbers" profile still got three mellow lofi songs first, even though its energy target of 0.97 is nowhere near their 0.35 to 0.42. The catalog adds to the problem: lofi has 3 songs, pop has 2, and every other genre has 1, so a lofi fan gets three good matches while a reggae or folk fan gets one good match and four filler songs. Finally, the system never penalizes a song for being far from what the user wants, it only gives fewer bonus points, so nothing is ever pushed out of the list.

---

## 7. Evaluation  

**Profiles tested.** Three normal profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) and three adversarial ones (Sad but Energetic, Unknown Genre k-pop, Lofi Label with Metal Numbers). Full terminal output is in the README under "Stress Test Output". I looked at whether the top result matched my own sense of the music, whether the "because" lines made sense, and whether the same songs kept showing up.

**What matched my intuition.** Chill Lofi gave Midnight Coding, Library Rain and Focus Flow, which is exactly the "study playlist" I would expect. Deep Intense Rock put Storm Runner far ahead (4.97 vs. 2.97 for second place), and the next picks were the loudest, least acoustic songs in the catalog.

**Pair comparisons.**

- **High-Energy Pop vs. Chill Lofi:** The two lists share no songs. Pop moves to loud, bright, electronic tracks (energy near 0.9, almost no acoustic sound), while lofi moves to quiet, soft, acoustic ones (energy around 0.4). That is the system doing its job: the energy and acousticness targets sit at opposite ends.
- **High-Energy Pop vs. Deep Intense Rock:** Both want very high energy, so Gym Hero, Storm Runner and Neon Pulse show up in both lists. What separates them is the labels: pop users get Sunrise City first because of "pop" and "happy", and rock users get Storm Runner first because of "rock" and "intense". This makes sense, since the two tastes are close in loudness but different in mood.
- **Chill Lofi vs. Deep Intense Rock:** These are the cleanest opposites. Nothing overlaps, and the top scores are 4.95 and 4.97, so the system is equally confident in both.
- **Deep Intense Rock vs. Sad but Energetic:** Both ask for very high energy, and both lists have Neon Pulse, Gym Hero, Storm Runner and Iron Cathedral in them. The difference is that the sad profile puts a quiet classical piece (energy 0.22) first, because it is the only song that matches the "classical" and "melancholy" labels. Those labels outweigh the energy request, so the top song is the opposite of what the energy number asked for. The rest of the list then drifts to loud songs.
- **High-Energy Pop vs. Unknown Genre (k-pop):** The k-pop profile asks for similar energy, but with no label matches the scores drop from 4.84 to 1.96 at the top and the list is dominated by whichever songs have the closest energy. Sunrise City still comes first, which seems reasonable for a "bubbly" listener, but only by luck.
- **Chill Lofi vs. Lofi Label, Metal Numbers:** The same genre and mood labels are given, but the numbers flip from mellow to extreme. The top three barely change (the same lofi songs, with lower scores of 3.84 instead of 4.95), and Iron Cathedral only shows up in fourth place. Labels beat numbers.

**Why does Gym Hero keep showing up for people who only want "Happy Pop"?** Think of it as points on a scorecard. Gym Hero is a pop song, which is worth 2 points, and its energy is almost exactly what a high-energy listener asked for. The only thing it misses is the "happy" label, because it is tagged "intense", and that costs it just 1 point. With only two pop songs in the catalog, and the other one (Sunrise City) already taking first place, Gym Hero is next in line. The system has no way to say "this is pop but it feels aggressive, not cheerful", because mood is a yes-or-no label, not a scale. Rooftop Lights, which is actually happy, comes third because "indie pop" is not an exact match for "pop", so it never gets the 2 genre points.

**What surprised me.** (1) How little the three normal profiles changed when I doubled the weight of energy and halved genre: the rankings stayed identical, so the experiment only changed the scores, not the quality. (2) How strongly a single label can override the numbers: the sad classical piece won the "very energetic" profile just by matching two labels.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
