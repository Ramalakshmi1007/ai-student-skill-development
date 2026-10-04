# AI-Based Personalised Student Skill Development for Academia–Industry Collaboration

Final-year project (CS624301) – PSN College of Engineering and Technology, Tirunelveli.

Analyses job descriptions with NLP (TF-IDF, cosine similarity), compares them with student skill profiles,
identifies skill gaps and generates personalised learning recommendations and job-role matches.

## Files
- `engine.py` – skill extraction, skill-gap analysis, recommendation, job matching
- `main.py` – FastAPI backend
- `schema.sql` – MySQL database schema
- `demo.py` – sample end-to-end run

## Run
```
pip install -r requirements.txt
python demo.py
uvicorn main:app --reload   # API docs at http://127.0.0.1:8000/docs
```

## Tech stack
React.js (planned frontend), Python, FastAPI, MySQL, scikit-learn, pandas.
