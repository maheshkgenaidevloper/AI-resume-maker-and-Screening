
import re
from io import BytesIO

import csv
import math
import re
from collections import Counter
from io import BytesIO, StringIO


import streamlit as st
from pypdf import PdfReader
from docx import Document


from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


st.set_page_config(
    page_title="AI Resume Maker & Screening",
    page_icon="📄",
    layout="wide"
)

st.title("🤖 AI Resume Maker & Resume Screening")
st.caption("Create resumes, compare candidates and identify relevant skills.")

# Skills used for the initial screening prototype
SKILLS = [
    "Python", "SQL", "Machine Learning", "Deep Learning",
    "NLP", "Generative AI", "LLM", "RAG", "Streamlit",
    "Power BI", "Excel", "Pandas", "Scikit-learn",
    "TensorFlow", "PyTorch", "Data Analysis", "Java",
    "C++", "AWS", "Azure", "Docker", "Git",
    "Communication", "Project Management", "Data Science"
]


def extract_text(uploaded_file):
    """Extract text from a PDF or DOCX file."""
    try:
        if uploaded_file.name.lower().endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            return "\n".join(
                page.extract_text() or "" for page in reader.pages
            )

        if uploaded_file.name.lower().endswith(".docx"):
            doc = Document(uploaded_file)
            return "\n".join(p.text for p in doc.paragraphs)

    except Exception as exc:
        st.warning(f"Could not read {uploaded_file.name}: {exc}")

    return ""


def find_skills(text):
    """Find known skills in text, ignoring letter case."""
    found = []
    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, text, re.IGNORECASE):
            found.append(skill)
    return found


def calculate_match(resume_text, job_description):
    """Combine text similarity and job skill coverage."""
    if not resume_text.strip() or not job_description.strip():
        return 0, [], []

    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        matrix = vectorizer.fit_transform(
            [resume_text, job_description]
        )
        similarity = float(
            cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        )
    except ValueError:
        similarity = 0.0

    job_skills = find_skills(job_description)
    resume_skills = find_skills(resume_text)

    matched = [s for s in job_skills if s in resume_skills]
    missing = [s for s in job_skills if s not in resume_skills]

    skill_score = (
        len(matched) / len(job_skills)
        if job_skills else similarity
    )

    score = (0.60 * similarity + 0.40 * skill_score) * 100
    return round(score, 2), matched, missing


def create_resume_pdf(details):
    """Create a downloadable resume PDF."""
    buffer = BytesIO()
    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=40,
        bottomMargin=40
    )
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(details["name"], styles["Title"]))
    story.append(Paragraph(details["email"], styles["Normal"]))
    story.append(Spacer(1, 12))

    sections = [
        ("Professional Summary", details["summary"]),
        ("Skills", details["skills"]),
        ("Work Experience", details["experience"]),
        ("Education", details["education"]),
        ("Projects", details["projects"]),
    ]

    for heading, content in sections:
        story.append(Paragraph(heading, styles["Heading2"]))
        safe_content = (
            content.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br/>")
        )
        story.append(
            Paragraph(safe_content or "Not provided", styles["BodyText"])
        )
        story.append(Spacer(1, 10))

    pdf.build(story)
    buffer.seek(0)
    return buffer.getvalue()


tab1, tab2, tab3 = st.tabs([
    "📝 Resume Maker",
    "🔎 Resume Screening",
    "📊 Screening Results"
])

# ---------------- RESUME MAKER ----------------
with tab1:
    st.header("Create Your Professional Resume")

    with st.form("resume_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        summary = st.text_area(
            "Professional Summary",
            placeholder="Describe your experience and career goals."
        )
        skills = st.text_area(
            "Skills",
            placeholder="Python, SQL, Machine Learning, NLP"
        )
        experience = st.text_area(
            "Work Experience",
            placeholder="Job title, company, dates and responsibilities."
        )
        education = st.text_area("Education")
        projects = st.text_area(
            "Projects",
            placeholder="Project name, tools used and key results."
        )

        generate = st.form_submit_button("Generate Resume PDF")

    if generate:
        if not name.strip() or not email.strip():
            st.error("Please enter your name and email.")
        else:
            details = {
                "name": name.strip(),
                "email": email.strip(),
                "summary": summary.strip(),
                "skills": skills.strip(),
                "experience": experience.strip(),
                "education": education.strip(),
                "projects": projects.strip()
            }

            pdf_data = create_resume_pdf(details)
            st.success("Resume PDF generated successfully.")
            st.download_button(
                "Download Resume",
                data=pdf_data,
                file_name="my_resume.pdf",
                mime="application/pdf"
            )

# ---------------- RESUME SCREENING ----------------
with tab2:
    st.header("Screen Resumes Against a Job Description")

    job_description = st.text_area(
        "Paste the complete Job Description",
        height=200,
        placeholder="Enter job responsibilities and required skills..."
    )

    uploaded_files = st.file_uploader(
        "Upload candidate resumes (PDF or DOCX)",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if st.button("Screen Candidates"):
        if not job_description.strip():
            st.error("Please enter a job description.")
        elif not uploaded_files:
            st.error("Please upload at least one resume.")
        else:
            results = []

            for file in uploaded_files:
                resume_text = extract_text(file)

                if not resume_text.strip():
                    st.warning(
                        f"No readable text found in {file.name}. "
                        "Scanned PDFs may require OCR."
                    )
                    continue

                score, matched, missing = calculate_match(
                    resume_text, job_description
                )

                results.append({
                    "Resume": file.name,
                    "Match Score (%)": score,
                    "Matched Skills": ", ".join(matched) or "None detected",
                    "Missing Skills": ", ".join(missing) or "None detected"
                })

            if results:
                df = pd.DataFrame(results).sort_values(
                    "Match Score (%)", ascending=False
                ).reset_index(drop=True)

                st.session_state["screening_results"] = df
                st.success(f"Screened {len(df)} readable resume(s).")
                st.dataframe(df, use_container_width=True, hide_index=True)

                st.download_button(
                    "Download Screening Report (CSV)",
                    data=df.to_csv(index=False).encode("utf-8"),
                    file_name="screening_results.csv",
                    mime="text/csv"
                )

# ---------------- RESULTS DASHBOARD ----------------
with tab3:
    st.header("Recruiter Dashboard")

    df = st.session_state.get("screening_results")

    if df is None or df.empty:
        st.info("Screen resumes in the previous tab to see results here.")
    else:
        col1, col2, col3 = st.columns(3)

        col1.metric("Candidates", len(df))
        col2.metric(
            "Average Match",
            f"{df['Match Score (%)'].mean():.1f}%"
        )
        col3.metric(
            "Highest Match",
            f"{df['Match Score (%)'].max():.1f}%"
        )

        st.subheader("Candidate Match Scores")
        chart_data = df.set_index("Resume")[["Match Score (%)"]]
        st.bar_chart(chart_data)

        st.subheader("Ranked Candidates")
        st.dataframe(df, use_container_width=True, hide_index=True)