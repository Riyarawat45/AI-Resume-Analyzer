from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from xml.sax.saxutils import escape

import streamlit as st
import fitz
from google import genai
import re


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# ==================================================
# GEMINI CONFIG
# ==================================================

try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=GEMINI_API_KEY)

except Exception:
    client = None


# ==================================================
# PROFESSIONAL CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #eef2ff,
        #f5f3ff,
        #e0e7ff
    );
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

h1, h2, h3 {
    color: #312e81 !important;
    font-weight: 700;
}

.main-title {
    text-align: center;
    font-size: 46px;
    font-weight: 800;

    background: linear-gradient(
        90deg,
        #4338ca,
        #9333ea,
        #6366f1
    );

    background-size: 200% auto;

    color: #4338ca;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    animation: gradientMove 4s linear infinite;
}

@keyframes gradientMove {
    to {
        background-position: 200% center;
    }
}

.subtitle {
    text-align: center;
    font-size: 17px;
    color: #64748b;
    margin-bottom: 30px;
}

.card {
    background: rgba(255,255,255,0.95);
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #ddd6fe;

    box-shadow: 0 5px 20px rgba(79,70,229,0.08);

    transition: all 0.3s ease;
    min-height: 135px;
}

.card:hover {
    transform: translateY(-7px);
    box-shadow: 0 12px 30px rgba(79,70,229,0.18);
}

.card h3 {
    color: #4338ca !important;
    font-size: 20px;
}

.card p {
    color: #64748b !important;
}

[data-testid="stMetric"] {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #ddd6fe;

    box-shadow: 0 5px 18px rgba(79,70,229,0.08);

    transition: 0.3s;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(79,70,229,0.15);
}

[data-testid="stMetricValue"] {
    color: #4338ca !important;
    font-weight: 800;
}

div.stButton > button,
div.stDownloadButton > button {

    background: linear-gradient(
        90deg,
        #6366f1,
        #9333ea
    );

    color: white !important;
    border: none;
    border-radius: 12px;

    padding: 12px 22px;
    font-weight: bold;

    transition: 0.3s;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {

    transform: translateY(-3px);

    box-shadow: 0 8px 20px rgba(99,102,241,0.3);
}

[data-testid="stFileUploader"] {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border: 2px dashed #818cf8;
}

textarea {
    background: white !important;
    color: #1f2937 !important;
    border-radius: 12px !important;
}

.stProgress > div > div > div > div {

    background: linear-gradient(
        90deg,
        #6366f1,
        #9333ea
    );

    border-radius: 20px;
}

.streamlit-expanderHeader {
    background: white;
    border-radius: 10px;
    color: #4338ca;
    font-weight: bold;
}

.stAlert {
    border-radius: 12px;
}

hr {
    border-color: #c7d2fe;
}

footer {
    visibility: hidden;
}
/* ===== TEXT VISIBILITY FIX ===== */

/* All normal text */
.stMarkdown p,
.stMarkdown li,
.stMarkdown span,
.stMarkdown div {
    color: #1e293b !important;
}

/* Headings */
.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3,
.stMarkdown h4 {
    color: #312e81 !important;
}

/* AI Analysis text */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] strong {
    color: #1e293b !important;
}

/* Expander text */
.streamlit-expanderContent {
    color: #1e293b !important;
}

/* Success and info messages */
[data-testid="stAlert"] p {
    color: #1e293b !important;
}

/* General text */
.stApp {
    color: #1e293b !important;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="main-title">📄 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Analyze your resume and improve your career opportunities with AI.</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div style="
    background: linear-gradient(120deg,#4338ca,#7c3aed);
    padding: 28px;
    border-radius: 18px;
    margin-top: 20px;
    margin-bottom: 25px;
    box-shadow: 0 8px 25px rgba(67,56,202,0.2);
">

<h2 style="color:white !important;">
Welcome to Your AI Resume Dashboard 👋
</h2>

<p style="color:white !important; font-size:16px;">
Upload your resume, discover your strengths,
check job compatibility and improve your career profile.
</p>

</div>
""", unsafe_allow_html=True)


# ==================================================
# FEATURE CARDS
# ==================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>📄 Resume Analysis</h3>
        <p>Upload your PDF resume and analyze it.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>🎯 Skill Detection</h3>
        <p>Find technical skills mentioned in your resume.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>🤖 AI Suggestions</h3>
        <p>Get intelligent suggestions to improve your resume.</p>
    </div>
    """, unsafe_allow_html=True)


# ==================================================
# SKILLS LIST
# ==================================================

skills = [
    "Python",
    "Java",
    "C",
    "C++",
    "JavaScript",
    "HTML",
    "CSS",
    "SQL",
    "MySQL",
    "Machine Learning",
    "Artificial Intelligence",
    "Deep Learning",
    "Data Science",
    "Data Structures",
    "Algorithms",
    "Git",
    "GitHub",
    "React",
    "Node.js",
    "Flask",
    "Django",
    "Streamlit",
    "Power BI",
    "Excel",
    "Communication",
    "Problem Solving",
    "Leadership",
    "Teamwork"
]


# ==================================================
# RESUME QUALITY SCORE FUNCTION
# ==================================================

def calculate_quality_score(text):

    text_lower = text.lower()

    scores = {}
    suggestions = {}

    # EDUCATION - 20 MARKS

    education_keywords = [
        "education",
        "academic",
        "qualification",
        "university",
        "college",
        "bachelor",
        "degree",
        "bca",
        "b.tech"
    ]

    education_found = any(
        word in text_lower for word in education_keywords
    )

    education_score = 20 if education_found else 0

    scores["Education"] = education_score

    if education_score < 20:

        suggestions["Education"] = (
            "Add your degree, college name, "
            "graduation year and academic details."
        )

    # PROJECTS - 25 MARKS

    project_keywords = [
        "project",
        "projects",
        "developed",
        "built",
        "created",
        "implemented"
    ]

    project_found = any(
        word in text_lower for word in project_keywords
    )

    project_score = 0

    if project_found:
        project_score += 15

    if any(word in text_lower for word in [
        "technologies",
        "tools",
        "framework",
        "python",
        "java",
        "javascript"
    ]):
        project_score += 5

    if any(word in text_lower for word in [
        "github",
        "live demo",
        "deployed",
        "result"
    ]):
        project_score += 5

    scores["Projects"] = project_score

    if project_score < 25:

        suggestions["Projects"] = (
            "Add 2-3 projects with descriptions, "
            "technologies used and your contribution."
        )

    # EXPERIENCE - 20 MARKS

    experience_keywords = [
        "experience",
        "internship",
        "intern",
        "work experience",
        "professional experience",
        "employment",
        "training"
    ]

    experience_found = any(
        word in text_lower for word in experience_keywords
    )

    experience_score = 0

    if experience_found:

        experience_score = 15

        if any(word in text_lower for word in [
            "responsibilities",
            "achievement",
            "managed",
            "worked",
            "contributed"
        ]):
            experience_score += 5

    scores["Experience"] = experience_score

    if experience_score < 20:

        suggestions["Experience"] = (
            "Add internship or work experience if available. "
            "Freshers can include practical training and projects."
        )

    # FORMATTING - 20 MARKS

    formatting_score = 0

    section_keywords = [
        "education",
        "skills",
        "projects",
        "experience",
        "certifications"
    ]

    sections_found = sum(
        1 for word in section_keywords
        if word in text_lower
    )

    formatting_score += min(sections_found * 4, 12)

    if 300 <= len(text.split()) <= 1200:
        formatting_score += 5

    if "\n" in text:
        formatting_score += 3

    scores["Formatting"] = formatting_score

    if formatting_score < 20:

        suggestions["Formatting"] = (
            "Use clear section headings, consistent formatting "
            "and bullet points. Keep your resume easy to read."
        )

    # CONTACT AND LINKS - 15 MARKS

    contact_score = 0

    email_found = bool(
        re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )
    )

    phone_found = bool(
        re.search(
            r"(?:\+91[\s-]?)?[6-9]\d{9}",
            text
        )
    )

    linkedin_found = "linkedin" in text_lower
    github_found = "github" in text_lower

    if email_found:
        contact_score += 4

    if phone_found:
        contact_score += 4

    if linkedin_found:
        contact_score += 4

    if github_found:
        contact_score += 3

    scores["Contact & Links"] = contact_score

    if contact_score < 15:

        suggestions["Contact & Links"] = (
            "Add your professional email, phone number, "
            "LinkedIn and GitHub profile."
        )

    total_score = sum(scores.values())

    return total_score, scores, suggestions


# ==================================================
# RESUME UPLOAD
# ==================================================

st.markdown("---")

st.header("📤 Upload Your Resume")

st.info(
    "Privacy note: Your uploaded resume is processed for this session. "
    "Its extracted text is sent to Google Gemini only when you click "
    "\"Analyze Resume with AI\". Do not upload documents containing "
    "information you do not want processed by this service."
)

uploaded_file = st.file_uploader(
    "Choose your resume PDF",
    type=["pdf"],
    key="resume_upload"
)


if uploaded_file is not None:

    st.success("Resume uploaded successfully! 🎉")

    st.info(
        f"File Name: {uploaded_file.name} | "
        f"File Size: {uploaded_file.size / 1024:.2f} KB"
    )

    # ==================================================
    # PDF TEXT EXTRACTION
    # ==================================================

    resume_text = ""
    page_count = 0

    try:

        with fitz.open(
            stream=uploaded_file.getvalue(),
            filetype="pdf"
        ) as pdf_document:

            page_count = len(pdf_document)

            for page in pdf_document:

                resume_text += page.get_text() + "\n"

    except Exception as e:

        st.error(f"Unable to read PDF: {e}")
        st.stop()

    if not resume_text.strip():

        st.warning(
            "No readable text found. Please upload a text-based PDF."
        )

        st.stop()

    resume_lower = resume_text.lower()

    with st.expander("📖 View Extracted Resume Text"):

        st.write(resume_text)


    # ==================================================
    # SKILL DETECTION
    # ==================================================

    st.markdown("---")

    st.header("🧠 Skills Detected")

    detected_skills = []

    for skill in skills:

        pattern = (
            r"(?<!\w)"
            + re.escape(skill.lower())
            + r"(?!\w)"
        )

        if re.search(pattern, resume_lower):

            detected_skills.append(skill)

    if detected_skills:

        st.success("Skills found in your resume:")

        st.write(", ".join(detected_skills))

    else:

        st.warning("No skills detected.")


    # ==================================================
    # SKILL MATCH SCORE
    # ==================================================

    st.header("📊 Resume Skill Score")

    total_skills = len(skills)
    found_skills = len(detected_skills)

    score = int(
        (found_skills / total_skills) * 100
    )

    st.progress(score / 100)

    st.metric(
        "Skill Match Score",
        f"{score}%"
    )

    st.caption(
        "This score represents the percentage of predefined "
        "skills found in your resume. It is not an overall "
        "resume quality score."
    )


    # ==================================================
    # RESUME QUALITY SCORE
    # ==================================================

    st.markdown("---")

    st.header("🏆 Resume Quality Score")

    quality_score, category_scores, quality_suggestions = (
        calculate_quality_score(resume_text)
    )

    if quality_score >= 80:

        quality_label = "Excellent 🌟"

    elif quality_score >= 60:

        quality_label = "Good 👍"

    elif quality_score >= 40:

        quality_label = "Average 📈"

    else:

        quality_label = "Needs Improvement 💡"

    st.metric(
        "Overall Resume Quality",
        f"{quality_score}/100",
        quality_label
    )

    st.progress(quality_score / 100)


    # ==================================================
    # PROFESSIONAL DASHBOARD
    # ==================================================

    st.markdown("---")

    st.subheader("📊 Resume Analytics Dashboard")

    dash1, dash2, dash3, dash4 = st.columns(4)

    with dash1:

        st.metric(
            "Resume Quality",
            f"{quality_score}/100"
        )

    with dash2:

        st.metric(
            "Skills Detected",
            len(detected_skills)
        )

    with dash3:

        st.metric(
            "PDF Pages",
            page_count
        )

    with dash4:

        st.metric(
            "Quality Status",
            quality_label
        )


    # ==================================================
    # CATEGORY-WISE SCORE
    # ==================================================

    st.markdown("---")

    st.subheader("📈 Category-wise Score")

    maximum_marks = {
        "Education": 20,
        "Projects": 25,
        "Experience": 20,
        "Formatting": 20,
        "Contact & Links": 15
    }

    for category, marks in category_scores.items():

        col1, col2 = st.columns([3, 1])

        with col1:

            st.write(f"**{category}**")

            st.progress(
                marks / maximum_marks[category]
            )

        with col2:

            st.write(
                f"**{marks}/{maximum_marks[category]}**"
            )

    st.caption(
        "This is a preliminary rule-based assessment using "
        "extracted PDF text. It does not verify actual visual "
        "formatting, factual accuracy or ATS compatibility."
    )


    # ==================================================
    # QUALITY SUGGESTIONS
    # ==================================================

    st.subheader("💡 Quality Improvement Suggestions")

    if quality_suggestions:

        for suggestion in quality_suggestions.values():

            st.write("🔹", suggestion)

    else:

        st.success(
            "Your resume covers all the basic checks! 🎉"
        )


    # ==================================================
    # JOB DESCRIPTION MATCHER
    # ==================================================

    st.markdown("---")

    st.header("🎯 Job Description Matcher")

    job_description = st.text_area(
        "Paste the job description here:",
        height=180,
        placeholder="Paste the job requirements..."
    )

    if st.button("Check Job Match"):

        if job_description.strip():

            job_lower = job_description.lower()

            job_skills = []

            for skill in skills:

                pattern = (
                    r"(?<!\w)"
                    + re.escape(skill.lower())
                    + r"(?!\w)"
                )

                if re.search(pattern, job_lower):

                    job_skills.append(skill)

            matched_skills = [
                skill for skill in job_skills
                if re.search(
                    r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)",
                    resume_lower
                )
            ]

            missing_skills = [
                skill for skill in job_skills
                if skill not in matched_skills
            ]

            if job_skills:

                match_score = int(
                    (len(matched_skills) / len(job_skills)) * 100
                )

                st.subheader("Job Match Result")

                st.progress(match_score / 100)

                st.metric(
                    "Job Match Percentage",
                    f"{match_score}%"
                )

                st.write("✅ Matching Skills:")

                if matched_skills:

                    st.success(
                        ", ".join(matched_skills)
                    )

                else:

                    st.write("No matching skills found.")

                st.write("❌ Missing Skills:")

                if missing_skills:

                    st.warning(
                        ", ".join(missing_skills)
                    )

                else:

                    st.success(
                        "All detected job skills are present!"
                    )

                st.subheader("📚 Suggested Learning Roadmap")

                for skill in missing_skills:

                    st.write(f"• Learn and practice {skill}")

            else:

                st.warning(
                    "No supported skills were detected "
                    "in the job description."
                )

        else:

            st.warning(
                "Please paste a job description first."
            )


    # ==================================================
    # BASIC RESUME IMPROVEMENTS
    # ==================================================

    st.markdown("---")

    st.header("💡 Resume Improvement Suggestions")

    suggestions = []

    if "education" not in resume_lower:

        suggestions.append(
            "Add an Education section."
        )

    if "project" not in resume_lower:

        suggestions.append(
            "Add your academic or personal projects."
        )

    if "experience" not in resume_lower:

        suggestions.append(
            "Add an Experience or Internship section if applicable."
        )

    if "skills" not in resume_lower:

        suggestions.append(
            "Add a separate Skills section."
        )

    if "@" not in resume_lower:

        suggestions.append(
            "Add your contact information and email address."
        )

    if "linkedin" not in resume_lower:

        suggestions.append(
            "Consider adding your LinkedIn profile."
        )

    if "github" not in resume_lower:

        suggestions.append(
            "Consider adding your GitHub profile."
        )

    if suggestions:

        for suggestion in suggestions:

            st.write("🔹", suggestion)

    else:

        st.success(
            "Your resume includes the basic sections checked here!"
        )


    # ==================================================
    # GEMINI AI ANALYSIS
    # ==================================================

    st.markdown("---")

    st.header("🤖 AI Resume Analysis")

    st.write(
        "Get detailed feedback about your resume using Gemini AI."
    )

    if st.button("Analyze Resume with AI"):

        if client is None:

            st.error(
                "Gemini API key is not configured. "
                "Please check your .streamlit/secrets.toml file."
            )

        else:

            prompt = f"""
            You are an expert resume reviewer and career advisor.

            Analyze the following resume of a student.

            Give your answer in simple English using these headings:

            1. Overall Resume Review
            2. Strengths
            3. Weaknesses
            4. Missing Skills
            5. Projects and Experience Feedback
            6. Formatting and Content Improvements
            7. Suggestions for a Better Resume
            8. Final Recommendations

            Be honest, helpful and beginner-friendly.

            Resume Quality Score:
            {quality_score}/100

            Category Scores:
            {category_scores}

            Resume:
            {resume_text}
            """

            with st.spinner(
                "Gemini AI is analyzing your resume..."
            ):

                try:

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )

                    st.subheader("✨ AI Analysis Result")

                    st.session_state["gemini_analysis"] = (
                        response.text
                    )

                    st.markdown(response.text)

                except Exception as e:

                    error_message = str(e)

                    if "429" in error_message:

                        st.warning(
                            "Gemini API free quota has been reached. "
                            "Please wait and try again later."
                        )

                    elif "503" in error_message:

                        st.warning(
                            "Gemini AI is currently busy. "
                            "Please try again after some time."
                        )

                    else:

                        st.error(
                            f"AI Analysis Error: {error_message}"
                        )


    # ==================================================
    # PDF REPORT DOWNLOAD
    # ==================================================

    st.markdown("---")

    st.header("📄 Download PDF Report")

    if st.button("Generate PDF Report"):

        pdf_buffer = BytesIO()

        document = SimpleDocTemplate(
            pdf_buffer,
            pagesize=A4,
            rightMargin=45,
            leftMargin=45,
            topMargin=45,
            bottomMargin=45
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "TitleStyle",
            parent=styles["Title"],
            textColor=colors.HexColor("#4338ca"),
            fontSize=22,
            spaceAfter=20
        )

        heading_style = ParagraphStyle(
            "HeadingStyle",
            parent=styles["Heading2"],
            textColor=colors.HexColor("#4338ca"),
            spaceBefore=15,
            spaceAfter=8
        )

        normal_style = styles["BodyText"]

        content = []

        content.append(
            Paragraph(
                "AI RESUME ANALYSIS REPORT",
                title_style
            )
        )

        content.append(Spacer(1, 10))

        content.append(
            Paragraph(
                f"<b>Resume File:</b> {escape(uploaded_file.name)}",
                normal_style
            )
        )

        content.append(
            Paragraph(
                f"<b>PDF Pages:</b> {page_count}",
                normal_style
            )
        )

        # Skill Score

        content.append(
            Paragraph(
                "1. Resume Skill Score",
                heading_style
            )
        )

        content.append(
            Paragraph(
                f"Skill Match Score: {score}%",
                normal_style
            )
        )

        # Quality Score

        content.append(
            Paragraph(
                "2. Resume Quality Score",
                heading_style
            )
        )

        content.append(
            Paragraph(
                f"Overall Quality: {quality_score}/100",
                normal_style
            )
        )

        for category, marks in category_scores.items():

            content.append(
                Paragraph(
                    f"{escape(category)}: {marks}/{maximum_marks[category]}",
                    normal_style
                )
            )

        # Detected Skills

        content.append(
            Paragraph(
                "3. Detected Skills",
                heading_style
            )
        )

        if detected_skills:

            for skill in detected_skills:

                content.append(
                    Paragraph(
                        f"• {escape(skill)}",
                        normal_style
                    )
                )

        else:

            content.append(
                Paragraph(
                    "No skills detected.",
                    normal_style
                )
            )

        # Quality Suggestions

        content.append(
            Paragraph(
                "4. Quality Improvement Suggestions",
                heading_style
            )
        )

        if quality_suggestions:

            for suggestion in quality_suggestions.values():

                content.append(
                    Paragraph(
                        f"• {escape(suggestion)}",
                        normal_style
                    )
                )

        else:

            content.append(
                Paragraph(
                    "No quality suggestions.",
                    normal_style
                )
            )

        # Basic Suggestions

        content.append(
            Paragraph(
                "5. Resume Improvement Suggestions",
                heading_style
            )
        )

        if suggestions:

            for suggestion in suggestions:

                content.append(
                    Paragraph(
                        f"• {escape(suggestion)}",
                        normal_style
                    )
                )

        else:

            content.append(
                Paragraph(
                    "No basic improvement suggestions.",
                    normal_style
                )
            )

        # Gemini Analysis

        content.append(
            Paragraph(
                "6. Gemini AI Analysis",
                heading_style
            )
        )

        ai_analysis = st.session_state.get(
            "gemini_analysis",
            ""
        )

        if ai_analysis:

            for line in ai_analysis.splitlines():

                if line.strip():

                    content.append(
                        Paragraph(
                            escape(line),
                            normal_style
                        )
                    )

                    content.append(Spacer(1, 5))

        else:

            content.append(
                Paragraph(
                    "Gemini AI analysis has not been generated yet.",
                    normal_style
                )
            )

        content.append(Spacer(1, 20))

        content.append(
            Paragraph(
                "Generated by AI Resume Analyzer",
                normal_style
            )
        )

        document.build(content)

        pdf_buffer.seek(0)

        st.download_button(
            label="⬇️ Download PDF Report",
            data=pdf_buffer.getvalue(),
            file_name="AI_Resume_Analysis_Report.pdf",
            mime="application/pdf"
        )

        st.success(
            "Your PDF report is ready! 🎉"
        )


# ==================================================
# FOOTER
# ==================================================

else:

    st.info(
        "👆 Please upload your PDF resume to get started."
    )

st.write("---")

st.markdown(
    "<center>Made with ❤️ using Python, Streamlit and Gemini AI</center>",
    unsafe_allow_html=True
)