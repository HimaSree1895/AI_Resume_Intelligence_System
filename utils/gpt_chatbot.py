from openai import OpenAI
import os

# Safe initialization
api_key = os.getenv("OPENAI_API_KEY")

client = None
if api_key:
    client = OpenAI(api_key=api_key)


def fallback_response(user_input, score, missing, role):
    """Local fallback AI (no API needed)"""

    user_input = user_input.lower()

    if "improve" in user_input:
        return f"To improve your resume for {role}, focus on: {missing}"

    elif "skills" in user_input:
        return f"You should learn these skills for {role}: {missing}"

    elif "roadmap" in user_input:
        return f"Step-by-step roadmap:\n1. Learn basics\n2. Build projects\n3. Practice interviews"

    elif "project" in user_input:
        return f"Suggested projects for {role}: Mini project, real-world project, advanced project"

    elif "interview" in user_input:
        return f"Prepare DSA, core subjects and mock interviews for {role}"

    else:
        return "Ask about resume improvement, skills, roadmap or projects."


def get_chatbot_response(user_input, score, missing_skills, role):

    # If no API key → fallback
    if client is None:
        return fallback_response(user_input, score, missing_skills, role)

    try:
        prompt = f"""
You are an AI Career Assistant.

User target role: {role}
Resume score: {score}
Missing skills: {missing_skills}

User question: {user_input}

Give helpful, clear and concise answers.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI career assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception:
        # If quota exceeded or error → fallback
        return fallback_response(user_input, score, missing_skills, role)