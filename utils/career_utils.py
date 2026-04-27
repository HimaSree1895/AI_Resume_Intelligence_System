import pandas as pd

skills_df = pd.read_csv("dataset/skills_dataset.csv")

def career_recommendation(predicted_role, user_skills):

    role_data = skills_df[
        skills_df["Role"] == predicted_role
    ]

    required_skills = role_data["Skills"].values[0].split()

    missing_skills = list(
        set(required_skills) - set(user_skills)
    )

    return required_skills, missing_skills
