# Model Card - Retrieval-Aware Music Recommender

## 1. Model Name
ContextTune Recommender v1

## 2. Intended Use
This model recommends top songs from a small classroom dataset using user genre, mood, and target energy.  
It is for educational experimentation, not for production personalization.

## 3. How It Works
The system first retrieves a subset of songs that match user context (genre/mood/tempo range), then ranks retrieved songs with a weighted scoring function.  
It outputs song recommendations with a confidence score and short rationale.

## 4. Data
- Source: `data/songs.csv`
- Size: 12 songs
- Fields: title, artist, genre, mood, energy, tempo
- Limitation: small and non-representative catalog

## 5. Strengths
- Transparent and interpretable scoring
- Fast and reproducible behavior
- Guardrails prevent invalid input requests

## 6. Limitations and Bias
- Limited catalog creates genre and mood imbalance
- Hand-crafted weights embed designer assumptions
- Confidence reflects scoring certainty, not user truth

## 7. Evaluation
System reliability is checked by:
- Unit tests for validation and recommendation behavior
- A 6-case evaluation loop that reports pass-rate and average confidence

## 8. Future Work
- Add diversity constraints
- Learn ranking weights from feedback
- Expand data coverage across genres and regions

## 9. Personal Reflection
Building this system showed how much recommendation quality depends on context retrieval and guardrails, not only ranking formulas.  
I learned that even simple recommenders can appear "accurate" while still being biased due to limited data and fixed assumptions.
