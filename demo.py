from engine import *
JDS = {
 "Data Analyst": ["We need a Data Analyst with Python, SQL, Excel and Power BI. Strong communication.",
                  "Looking for analytics skills: SQL, Power BI, Excel, Python, problem solving.",
                  "Data analysis role. Python, SQL, Power BI, AWS exposure, teamwork."],
 "ML Engineer": ["ML Engineer: Python, machine learning, TensorFlow, SQL, Git.",
                 "Machine learning, Python, TensorFlow, AWS, problem solving."],
 "Web Developer": ["HTML, CSS, JavaScript, React, Git, teamwork."],
}
roles = {r: role_profile(j) for r, j in JDS.items()}
print("Extracted from first JD:", extract_skills(JDS["Data Analyst"][0]))
student = {"Python": level_from_score(82), "SQL": level_from_score(65), "Excel": "Intermediate",
           "Power BI": "Beginner", "Machine Learning": level_from_score(48), "Communication": "Intermediate"}
gaps = skill_gap(student, roles["Data Analyst"])
print("\nSKILL GAP (Data Analyst)");  [print(" ", g) for g in gaps]
print("\nRECOMMENDATIONS");           [print(" ", r) for r in recommend(gaps)]
print("\nJOB MATCH");                 [print(" ", m) for m in match_roles(student, roles)]
