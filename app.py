import streamlit as st
import PyPDF2
import matplotlib.pyplot as plt

# -------------------------------
# Skills List
# -------------------------------
skills_list = [
    "python", "java", "c", "c++", "sql", "mysql",
    "html", "css", "javascript", "react",
    "node", "django", "flask",
    "machine learning", "data science",
    "excel", "power bi", "tableau",
    "communication", "teamwork", "problem solving"
]

# -------------------------------
# Job Roles
# -------------------------------
job_roles = {
    "Data Analyst": ["python", "sql", "excel", "power bi", "tableau"],
    "Web Developer": ["html", "css", "javascript", "react", "node"],
    "Machine Learning Engineer": ["python", "machine learning", "data science"],
    "Backend Developer": ["python", "java", "sql", "django", "flask"],
    "Software Engineer": ["c", "c++", "java", "problem solving"]
}

# -------------------------------
# Functions
# -------------------------------
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

def extract_skills(text):
    text = text.lower()
    return list(set([skill for skill in skills_list if skill in text]))

def match_jobs(skills):
    scores = {}
    for job, req_skills in job_roles.items():
        match_count = sum(1 for skill in req_skills if skill in skills)
        scores[job] = round((match_count / len(req_skills)) * 100, 2)
    return scores

def calculate_ats_score(text, skills):
    score = min(len(skills) * 4, 40)

    keywords = ["project", "experience", "internship", "developed", "team"]
    score += sum(6 for word in keywords if word in text.lower())

    word_count = len(text.split())
    if word_count > 300:
        score += 30
    elif word_count > 150:
        score += 20
    else:
        score += 10

    return min(score, 100)

def skill_gap_analysis(skills, job_scores):
    best_job = max(job_scores, key=job_scores.get)
    missing = [s for s in job_roles[best_job] if s not in skills]
    return best_job, missing

# -------------------------------
# UI
# -------------------------------
st.title("🚀 AI Career Copilot")
st.write("Smart Resume Analyzer + Career Guidance System")

uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf"])

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    skills = extract_skills(resume_text)
    job_scores = match_jobs(skills)
    ats_score = calculate_ats_score(resume_text, skills)
    best_job, missing_skills = skill_gap_analysis(skills, job_scores)

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Resume", "🧠 Skills", "🎯 Jobs", "🚀 Career"])

    # ---------------- TAB 1 ----------------
    with tab1:
        st.subheader("Resume Content")
        st.text_area("", resume_text, height=300)

    # ---------------- TAB 2 ----------------
    with tab2:
        st.subheader("Detected Skills")
        st.write(skills)

    # ---------------- TAB 3 ----------------
    with tab3:
        st.subheader("Job Match Scores")
        st.write(job_scores)

        # Graph
        fig, ax = plt.subplots()
        ax.bar(job_scores.keys(), job_scores.values())
        plt.xticks(rotation=30)
        st.pyplot(fig)

    # ---------------- TAB 4 ----------------
    with tab4:
        st.subheader("ATS Score")
        st.success(f"{ats_score}/100")

        st.subheader("Best Role")
        st.write(best_job)

        st.subheader("Missing Skills")
        if missing_skills:
            st.write(missing_skills)
        else:
            st.success("You are job ready!")
