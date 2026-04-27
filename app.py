import streamlit as st
import joblib
from streamlit_option_menu import option_menu

from utils.resume_parser import extract_resume_text
from utils.resume_score import calculate_score
from utils.job_market import predict_job_demand
from utils.ai_chatbot import get_chatbot_response


# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="AI Resume Intelligence Platform",
    layout="wide",
    page_icon="🚀"
)

# =====================================================
# MODERN UI STYLE
# =====================================================
st.markdown("""
<style>

/* Upload Section */
.upload-box{
background:#020617;
padding:25px;
border-radius:15px;
border:1px solid #1e293b;
}

/* Skill Container */
.skill-container{
background:#020617;
padding:30px;
border-radius:18px;
border:1px solid #1e293b;
margin-top:20px;
}

/* Skill Chips */
.skill-chip{
display:inline-block;
padding:7px 15px;
margin:6px;
border-radius:18px;
font-size:14px;
font-weight:500;
}

.required{background:#2563eb;color:white;}
.detected{background:#16a34a;color:white;}
.missing{background:#dc2626;color:white;}

</style>
""", unsafe_allow_html=True)


# =====================================================
# LOAD MODELS
# =====================================================
resume_model = joblib.load("model/resume_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")


# =====================================================
# SIDEBAR (CONTROL CENTER)
# =====================================================
with st.sidebar:

    st.title("🤖 Career AI")

    page = option_menu(
        "Workspace",
        ["Dashboard",
         "Skill Intelligence",
         "Market Insights",
         "Career Guidance",
         "AI Assistant"],
        icons=["speedometer","cpu","bar-chart","person"],
        default_index=0
    )

    st.divider()

    desired_role = st.selectbox(
        "🎯 Target Career Path",
        [
            "Data Science",
            "Web Designing",
            "Python Developer",
            "Java Developer",
            "DevOps Engineer"
        ]
    )

    st.caption("AI Career Intelligence System")


# =====================================================
# MAIN HEADER + UPLOAD
# =====================================================
st.title("🚀 AI Resume Intelligence Platform")

st.markdown("""
Upload your resume to receive intelligent insights about  
your **career readiness, skill alignment and market demand**.
""")

uploaded_file = st.file_uploader(
    "📄 Upload Resume (PDF)",
    type=["pdf"]
)

# =====================================================
# PROCESS RESUME
# =====================================================
analysis_ready = False

if uploaded_file:

    text = extract_resume_text(uploaded_file)

    vec = vectorizer.transform([text])
    predicted_role = resume_model.predict(vec)[0]

    score, skills, required = calculate_score(
        text,
        desired_role
    )

    missing = list(set(required) - set(skills))
    placement = min(95, score * 0.9)
    demand = predict_job_demand(desired_role)

    analysis_ready = True


# =====================================================
# DASHBOARD
# =====================================================
if page == "Dashboard":

    st.header("📊 Career Overview Dashboard")

    st.write("""
Provides a quick summary of your resume performance,
placement readiness and alignment with industry demand.
""")

    if analysis_ready:

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Resume Score", f"{score}%")
        c2.metric("Placement Probability", f"{int(placement)}%")
        c3.metric("Market Demand", demand)
        c4.metric("Career Match", predicted_role)

        st.progress(score / 100)

        st.success(
            "Higher scores indicate stronger industry alignment."
        )

    else:
        st.info("Upload resume to generate dashboard insights.")


# =====================================================
# SKILL INTELLIGENCE
# =====================================================
elif page == "Skill Intelligence":

    st.header("🧠 Skill Intelligence")

    st.write("""
Compare your resume skills with industry expectations
for your selected career path.
""")

    if analysis_ready:

        st.markdown('<div class="skill-container">',
                    unsafe_allow_html=True)

        # Required Skills
        st.subheader("✅ Required Skills")
        st.markdown(
            "".join([
                f"<span class='skill-chip required'>{s}</span>"
                for s in required
            ]),
            unsafe_allow_html=True
        )

        st.divider()

        # Detected Skills
        st.subheader("🎯 Skills Identified")
        if skills:
            st.markdown(
                "".join([
                    f"<span class='skill-chip detected'>{s}</span>"
                    for s in skills
                ]),
                unsafe_allow_html=True
            )
        else:
            st.warning("No relevant skills detected.")

        st.divider()

        # Missing Skills
        st.subheader("🚀 Skills To Improve")
        if missing:
            st.markdown(
                "".join([
                    f"<span class='skill-chip missing'>{s}</span>"
                    for s in missing
                ]),
                unsafe_allow_html=True
            )
        else:
            st.success("Perfect Skill Alignment ✅")

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.info("Upload resume to analyze skills.")


# =====================================================
# MARKET INSIGHTS
# =====================================================
elif page == "Market Insights":

    st.header("📈 Job Market Insights")

    st.write("""
Forecast of hiring demand based on historical
industry recruitment trends.
""")

    if analysis_ready:

        st.metric("Expected Job Openings (2025)", demand)

        if demand > 3000:
            st.success("🔥 High Growth Career Domain")
        elif demand > 2000:
            st.info("Stable Hiring Market")
        else:
            st.warning("Moderate Hiring Demand")

    else:
        st.info("Upload resume to view market insights.")


# =====================================================
# CAREER GUIDANCE
# =====================================================
elif page == "Career Guidance":

    st.header("🎯 Career Guidance")

    st.write("""
Personalized improvement suggestions based on
resume strength and skill alignment.
""")

    if analysis_ready:

        if score < 40:
            st.error(
                "Focus on foundational skills and academic projects."
            )
        elif score < 70:
            st.warning(
                "Improve through internships and advanced tools."
            )
        else:
            st.success(
                "Excellent profile! Industry ready."
            )

    else:
        st.info("Upload resume to receive guidance.")

# =====================================================
# AI CHATBOT
# =====================================================
elif page == "AI Assistant":

    st.header("🤖 AI Career Assistant")

    if not analysis_ready:
        st.warning("Upload resume first.")
    else:

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        prompt = st.chat_input("Ask your question...")

        if prompt:

            st.session_state.messages.append(
                {"role": "user", "content": prompt}
            )

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):

                    response = get_chatbot_response(
                        prompt,
                        score,
                        missing,
                        desired_role
                    )

                    st.markdown(response)

            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )