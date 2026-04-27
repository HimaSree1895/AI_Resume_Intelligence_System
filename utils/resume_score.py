import pandas as pd

skills_df = pd.read_csv("dataset/skills_dataset.csv")

def calculate_score(text, target_role):

    role_data = skills_df[
        skills_df["Role"] == target_role
    ]

    required_skills = role_data["Skills"].values[0].split()

    matched_skills = []

    for skill in required_skills:
        if skill.lower() in text:
            matched_skills.append(skill)

    # Career-based scoring
    score = (len(matched_skills) /
             len(required_skills)) * 100

    return int(score), matched_skills, required_skills
