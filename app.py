import streamlit as st
import pandas as pd
import numpy as np
import base64
from src.pdf_parser import extract_text
from src.skill_extractor import extract_skills
from src.matcher import match_skills
from src.education_detector import detect_education


# --------------------------
# PAGE CONFIG
# --------------------------

st.set_page_config(page_title="ATS Resume Screening System",page_icon="📄",layout="wide")
with open("apexium_logo.png", "rb") as image_file:
    logo_base64 = base64.b64encode(image_file.read()).decode()
# --------------------------
# CUSTOM CSS
# --------------------------

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.big-title{
    text-align:center;
    color:white;
    font-size:45px;
    font-weight:bold;
}



.sub-title{
    text-align:center;
    color:#A0A0A0;
    font-size:18px;
}

.metric-card{
    background:#1E1E1E;
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;
}

</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="
background:white;
padding:25px;
border-radius:15px;
display:flex;
align-items:center;
margin-bottom:20px;
">

<img src="data:image/png;base64,{logo_base64}"
     width="120"
     style="margin-right:20px;">

<div style="
flex:1;
text-align:center;
">

<h1 style="
color:#0F172A;
margin:0;
font-size:46px;
font-weight:800;
">
ATS Resume Screening System
</h1>

<h4 style="
color:#0F172C;
margin-top:8px;
margin-bottom:0;
font-size:20px;
font-weight:600;
"><strong>
Powered by Apexium </strong>
</h4>

</div>

</div>
""", unsafe_allow_html=True)


# --------------------------
# INPUT SECTION
# --------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("📝 Job Description")

    job_description = st.text_area(
        "",
        height=250,
        placeholder="Paste Job Description Here..."
    )

with col2:

    st.subheader("📂 Upload Resume")

    uploaded_file = st.file_uploader(
        "Upload PDF Resume",
        type=["pdf"]
    )

# --------------------------
# BUTTON
# --------------------------

st.write("")

analyze = st.button(
    "🚀 Analyze Resume",
    use_container_width=True
)

# --------------------------
# RESULT
# --------------------------

if analyze:

    if uploaded_file is None:
        st.error("Please Upload Resume PDF")
        st.stop()

    if len(job_description.strip()) == 0:
        st.error("Please Enter Job Description")
        st.stop()

    st.success("Resume Analyzed Successfully")
    
    resume_text = extract_text(uploaded_file)

    education = detect_education(resume_text)

    skills = extract_skills(resume_text)

    st.subheader("📄 Resume Summary")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🎓 Education")
        st.success(education)

        st.markdown("### 🛠 Skills")

        if skills:
            st.info(", ".join(skills))
        else:
            st.warning("No skills found")

    with col2:

        st.markdown("### 📜 Certifications")

        cert_keywords = [
            "certification",
            "certificate",
            "bootcamp"
        ]

        found_cert = False

        for line in resume_text.split("\n"):

            line = line.strip()

            if len(line) > 10 and any(
                word.lower() in line.lower()
                for word in cert_keywords
            ):

                st.success(line)
                found_cert = True

        if not found_cert:
            st.warning("No certifications found")


    st.markdown("### 💼 Experience & Projects")

    keywords = [
        "developed",
        "built",
        "performed",
        "experience",
        "project"
    ]

    found = False

    for line in resume_text.split("\n"):

        line = line.strip()

        if len(line) > 20 and any(
            word.lower() in line.lower()
            for word in keywords
        ):

            st.write("✅", line)
            found = True

    if not found:
        st.warning("No experience found")










    
    skills = extract_skills(resume_text)
    matching_skills, missing_skills = match_skills(
    skills,
    job_description
)

    st.subheader("✅ Matching Skills")

    if matching_skills:
        for skill in matching_skills:
            st.success(skill)
    else:
        st.warning("No Matching Skills")

    st.subheader("❌ Missing Skills")

    if missing_skills:
        for skill in missing_skills:
            st.error(skill)
    else:
        st.success("No Missing Skills")



    st.subheader("🛠 Detected Skills")

    if skills:
        st.success(", ".join(skills))
    else:
        st.warning("No Skills Detected")

    # ATS SCORE CALCULATION

    total_required = len(matching_skills) + len(missing_skills)

    if total_required > 0:
        ats_score = int(
            (len(matching_skills) / total_required) * 100
        )
    else:
        ats_score = 0

    confidence = min(95, ats_score + 10)

    st.subheader("📊 ATS Analysis Report")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "ATS Score",
            f"{ats_score}%"
        )

    with c2:
        st.metric(
            "Matching Skills",
            len(matching_skills)
        )

    with c3:
        st.metric(
            "Missing Skills",
            len(missing_skills)
        )
    st.progress(ats_score / 100)

    # STATUS

    if ats_score >= 80:
        st.success("✅ Candidate Selected")

    elif ats_score >= 60:
        st.warning("⚠️ Candidate Needs Improvement")

    else:
        st.error("❌ Candidate Rejected")

    # RECOMMENDATION

    st.subheader("💡 Recommendation")

    if ats_score >= 80:
        st.success(
            "Strong profile. Proceed to Technical Interview."
        )

    elif ats_score >= 60:
        st.warning(
            "Candidate has partial skill match. Consider skill improvement."
        )

    else:
        st.error(
            "Profile does not meet job requirements."
        )
