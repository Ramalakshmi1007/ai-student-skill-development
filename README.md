# SkillBridge – AI-Based Personalised Student Skill Development for Academia–Industry Collaboration

Final-year project (CS624301) – PSN College of Engineering and Technology, Tirunelveli.

Analyses job descriptions with NLP (TF-IDF, cosine similarity), compares them with student skill profiles,
identifies skill gaps and generates personalised learning recommendations and job-role matches.

## Project structure
| Folder | Contents |
|---|---|
| `docs/` | Web app (`index.html`) – login, dashboard, profile, job description, assessment, skill gap, recommendations, progress, job matching, admin |
| `backend/` | Python engine (`engine.py`), FastAPI app (`main.py`), sample run (`demo.py`) |
| `database/` | MySQL schema (`schema.sql`) |

## Run the web app
Open `docs/index.html` in a browser (no installation needed).
Optional live demo: GitHub repo → Settings → Pages → Branch `main`, folder `/docs`.

## Run the backend
```
cd backend
pip install -r requirements.txt
python demo.py
uvicorn main:app --reload   # API docs at http://127.0.0.1:8000/docs
```

## Tech stack
React.js (planned), Python, FastAPI, MySQL, scikit-learn, pandas.

## Status
Web app is a working prototype (browser-side logic). Next: connect it to the FastAPI backend and MySQL.
