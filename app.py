import streamlit as st

import config
from utils.resume_parser import extract_text_from_cv
from utils.embedding_matcher import compute_similarity_score
from utils.azure_llm import analyze_fit

st.set_page_config(page_title="Candidate Fit Analyzer", layout="wide")

st.title("Candidate Fit Analyzer")
st.caption(
    "Upload a CV, paste the Job Description and Role — get a selection "
    "probability plus the skills/projects that would raise it."
)

# --- Startup config check ---
try:
    config.validate_config()
except EnvironmentError as e:
    st.error(str(e))
    st.stop()

# --- Inputs ---
col1, col2 = st.columns(2)

with col1:
    job_role = st.text_input("Job Role", placeholder="e.g. Data Scientist")
    jd_text = st.text_area("Job Description", height=280, placeholder="Paste the full JD here...")

with col2:
    uploaded_cv = st.file_uploader("Upload Candidate CV (PDF or DOCX)", type=["pdf", "docx"])
    if uploaded_cv:
        st.success(f"Uploaded: {uploaded_cv.name}")

analyze_clicked = st.button("Analyze Fit", type="primary", use_container_width=True)

# --- Analysis ---
if analyze_clicked:
    if not job_role or not jd_text or not uploaded_cv:
        st.warning("Please provide the Job Role, Job Description, and a CV file.")
        st.stop()

    with st.spinner("Extracting CV text..."):
        cv_text = extract_text_from_cv(uploaded_cv)

    if not cv_text:
        st.error("Couldn't extract any text from the CV. Try a different file.")
        st.stop()

    with st.spinner("Computing semantic match score..."):
        similarity_score = compute_similarity_score(cv_text, jd_text)

    with st.spinner("Running detailed AI analysis..."):
        try:
            result = analyze_fit(cv_text, jd_text, job_role)
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            st.stop()

    st.divider()

    # --- Results ---
    score_col, band_col, embed_col = st.columns(3)
    score_col.metric("Selection Probability", result.get("selection_probability", "N/A"))
    band_col.metric("Band", result.get("probability_band", "N/A"))
    embed_col.metric("Semantic Match Score", f"{similarity_score}%")

    st.subheader("Reasoning")
    st.write(result.get("reasoning", "—"))

    match_col, missing_col = st.columns(2)

    with match_col:
        st.subheader("Matching Skills")
        matching = result.get("matching_skills", [])
        if matching:
            for skill in matching:
                st.markdown(f"- {skill}")
        else:
            st.write("None identified.")

    with missing_col:
        st.subheader("Missing / Weak Skills")
        missing = result.get("missing_skills", [])
        if missing:
            for skill in missing:
                st.markdown(f"- {skill}")
        else:
            st.write("None identified.")

    st.subheader("Recommended Skills to Learn")
    recommended_skills = result.get("recommended_skills", [])
    if recommended_skills:
        for skill in recommended_skills:
            st.markdown(f"- {skill}")
    else:
        st.write("None identified.")

    st.subheader("Recommended Projects to Build")
    recommended_projects = result.get("recommended_projects", [])
    if recommended_projects:
        for proj in recommended_projects:
            st.markdown(f"**{proj.get('project', 'Untitled project')}** — {proj.get('reason', '')}")
    else:
        st.write("None identified.")