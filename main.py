"""FastAPI backend. Run: pip install fastapi uvicorn scikit-learn numpy ; uvicorn main:app --reload
In-memory store for the demo; replace ROLES with MySQL queries (SQLAlchemy / mysql-connector) using schema.sql."""
from fastapi import FastAPI
from pydantic import BaseModel
from engine import extract_skills, role_profile, skill_gap, recommend, match_roles, level_from_score

app = FastAPI(title="AI Student Skill Development")
ROLES: dict[str, dict[str, float]] = {}          # role name -> {skill: importance}

class JD(BaseModel):  role: str; texts: list[str]
class Student(BaseModel): skills: dict[str, str]; role: str; required_level: str = "Intermediate"
class Score(BaseModel): score: float

@app.post("/jd/process")                          # Admin uploads JDs -> skills stored per role
def process_jd(jd: JD):
    ROLES[jd.role] = role_profile(jd.texts)
    return {"role": jd.role, "skills": ROLES[jd.role], "first_jd": extract_skills(jd.texts[0])}

@app.post("/assessment/level")
def level(s: Score): return {"level": level_from_score(s.score)}

@app.post("/gap")
def gap(s: Student): return skill_gap(s.skills, ROLES[s.role], s.required_level)

@app.post("/recommend")
def rec(s: Student): return recommend(skill_gap(s.skills, ROLES[s.role], s.required_level))

@app.post("/match")
def match(s: Student): return match_roles(s.skills, ROLES)
