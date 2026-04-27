import os

# -------------------------
# GEMINI SETUP
# -------------------------
try:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    gemini_model = genai.GenerativeModel("gemini-pro")
except:
    gemini_model = None


# -------------------------
# OLLAMA SETUP
# -------------------------
try:
    import ollama
except:
    ollama = None


# -------------------------
# FALLBACK (ALWAYS WORKS)
# -------------------------
def fallback_response(user_input, score, missing, role):

    user_input = user_input.lower()

    if "improve" in user_input:
        return f"Improve your resume for {role} by learning: {', '.join(missing)}"

    elif "skills" in user_input:
        return f"For {role}, you should learn: {', '.join(missing)}"

    elif "roadmap" in user_input:
        return f"""Roadmap for {role}:
1. Learn fundamentals
2. Build projects
3. Practice problems
4. Prepare for interviews"""

    elif "project" in user_input:
        return f"""Projects for {role}:
1. Beginner project
2. Real-world project
3. Advanced project"""

    else:
        return "Ask about resume improvement, skills, roadmap, or projects."


# -------------------------
# GEMINI RESPONSE
# -------------------------
def gemini_response(prompt):
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except:
        return None


# -------------------------
# OLLAMA RESPONSE
# -------------------------
def ollama_response(prompt):
    try:
        response = ollama.chat(
            model="mistral",   # ✅ stable model
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]
    except Exception as e:
        print("Ollama error:", e)
        return None


# -------------------------
# MAIN ENGINE
# -------------------------
def get_chatbot_response(user_input, score, missing, role):

    prompt = f"""
You are an AI Career Assistant.

User target role: {role}
Resume score: {score}
Missing skills: {missing}

User question: {user_input}

Give helpful and clear answers.
"""

    # 1️⃣ Try Gemini
    if gemini_model:
        result = gemini_response(prompt)
        if result:
            return result

    # 2️⃣ Try Ollama
    if ollama:
        result = ollama_response(prompt)
        if result:
            return result

    # 3️⃣ Final fallback
    return fallback_response(user_input, score, missing, role)