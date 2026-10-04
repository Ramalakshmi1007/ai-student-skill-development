"""Core AI/NLP engine: JD skill extraction, TF-IDF + cosine matching, skill-gap analysis, recommendations."""
import re
from collections import Counter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---- 1. Skill dictionary (category, aliases). Extend or load from the MySQL `skills` table. ----
SKILLS = {
    "Python": ("Programming", ["python"]), "SQL": ("Database", ["sql", "mysql", "postgresql"]),
    "Java": ("Programming", ["java"]), "JavaScript": ("Programming", ["javascript", "js"]),
    "React": ("Framework", ["react", "react.js", "reactjs"]), "HTML": ("Programming", ["html"]), "CSS": ("Programming", ["css"]),
    "Machine Learning": ("Technical", ["machine learning", "ml"]), "TensorFlow": ("Tool", ["tensorflow"]),
    "Data Analysis": ("Technical", ["data analysis", "data analytics", "analytics"]),
    "Excel": ("Tool", ["excel", "ms excel"]), "Power BI": ("Tool", ["power bi", "powerbi"]),
    "AWS": ("Cloud", ["aws", "cloud computing", "cloud"]), "Git": ("Tool", ["git", "github"]),
    "Communication": ("Professional", ["communication", "presentation"]),
    "Teamwork": ("Professional", ["teamwork", "collaboration"]), "Problem Solving": ("Professional", ["problem solving", "problem-solving"]),
}
LEVELS = {"Not Available": 0, "Beginner": 1, "Basic": 2, "Intermediate": 3, "Advanced": 4}

# ---- 2. Preprocessing: cleaning, lowercase, normalisation ----
def preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\- ]", " ", text)      # remove special characters
    return re.sub(r"\s+", " ", text).strip()

# ---- 3. Skill extraction from one JD ----
def extract_skills(jd_text: str) -> list[dict]:
    clean = preprocess(jd_text)
    found = []
    for skill, (cat, aliases) in SKILLS.items():
        if any(re.search(rf"(?<![a-z0-9]){re.escape(a)}(?![a-z0-9])", clean) for a in aliases):
            found.append({"skill": skill, "category": cat})
    return found                                      # duplicates are removed automatically

# ---- 4. Build a role profile from many JDs: importance = share of JDs mentioning the skill ----
def role_profile(jds: list[str]) -> dict[str, float]:
    c = Counter(s["skill"] for jd in jds for s in extract_skills(jd))
    return {k: round(v / len(jds), 2) for k, v in c.items()}

# ---- 5. Assessment score -> competency level ----
def level_from_score(score: float) -> str:
    return "Beginner" if score <= 25 else "Basic" if score <= 50 else "Intermediate" if score <= 75 else "Advanced"

# ---- 6. Skill-gap analysis with priority ----
def skill_gap(student: dict[str, str], role: dict[str, float], required_level="Intermediate") -> list[dict]:
    req = LEVELS[required_level]; out = []
    for skill, importance in role.items():
        have = LEVELS.get(student.get(skill, "Not Available"), 0)
        status = "Matched" if have >= req else "Missing" if have == 0 else "Developing"
        gap = max(req - have, 0)
        priority = round(0.6 * importance + 0.4 * gap / req, 2) if gap else 0.0   # weights are tunable
        out.append({"skill": skill, "required": required_level, "student_level": student.get(skill, "Not Available"),
                    "status": status, "priority": priority})
    return sorted(out, key=lambda r: -r["priority"])

# ---- 7. Recommendation: resource type depends on current level ----
RESOURCES = {  # skill -> topic; extend or store in the `resources` table
    "Power BI": "Power BI dashboards", "SQL": "SQL queries and joins", "AWS": "AWS cloud",
    "Machine Learning": "ML with scikit-learn", "Python": "Python programming", "Excel": "Excel for analysis",
}
def recommend(gaps: list[dict]) -> list[dict]:
    recs = []
    for g in gaps:
        if g["status"] == "Matched": continue
        topic = RESOURCES.get(g["skill"], g["skill"]); lvl = LEVELS[g["student_level"]]
        if lvl == 0:   plan = [f"Learn {topic} fundamentals", "Complete beginner exercises"]
        elif lvl <= 2: plan = [f"Practise {topic} with guided exercises", "Take a topic quiz"]
        else:          plan = [f"Advanced {topic} problems", f"Mini-project using {g['skill']}"]
        recs.append({"skill": g["skill"], "priority": g["priority"], "plan": plan})
    return recs

# ---- 8. Job-role matching with cosine similarity over a skill vector space ----
def match_roles(student: dict[str, str], roles: dict[str, dict[str, float]]) -> list[dict]:
    vocab = sorted(SKILLS)
    sv = np.array([[LEVELS.get(student.get(s, "Not Available"), 0) / 4 for s in vocab]])
    res = []
    for name, prof in roles.items():
        rv = np.array([[prof.get(s, 0) * 0.75 for s in vocab]])        # 0.75 = 'Intermediate' target
        res.append({"role": name, "match_percent": round(float(cosine_similarity(sv, rv)[0][0]) * 100, 1)})
    return sorted(res, key=lambda r: -r["match_percent"])

# ---- 9. Optional: JD-to-JD similarity using TF-IDF text vectors ----
def jd_similarity(jds: list[str]):
    m = TfidfVectorizer(stop_words="english").fit_transform([preprocess(j) for j in jds])
    return cosine_similarity(m)
