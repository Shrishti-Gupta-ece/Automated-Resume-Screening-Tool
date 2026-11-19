"""
app.py
Interactive Streamlit application for Automated Resume Screening.

Features:
- Paste or edit a Job Description.
- Configure Must-Have and Nice-To-Have skills, Minimum Experience, and Score Threshold.
- Upload multiple resumes in PDF, DOCX, or TXT formats.
- Safe temporary file management for Windows OS.
- Displays comprehensive candidate ranking table with status metrics.
- Interactive score distribution bar chart (Altair).
- One-click CSV report export.
- Human-in-the-loop ethical AI advisory caption.
"""

from pathlib import Path
import tempfile
import altair as alt
import pandas as pd
import streamlit as st

from src.extractor import list_resumes, read_resume
from src.scorer import score_resumes


# -----------------------------------------------------------------------------
# Streamlit Page Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Automated Resume Screening Tool",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Helper to locate local project files
PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_JD_PATH = PROJECT_ROOT / "data" / "job_description.txt"
SAMPLE_RESUMES_DIR = PROJECT_ROOT / "resumes"


def load_default_jd() -> str:
    """Reads default job description if present."""
    if DEFAULT_JD_PATH.exists():
        try:
            return read_resume(DEFAULT_JD_PATH)
        except Exception:
            pass
    return (
        "Job Title: Data Analyst\n"
        "Experience: Minimum 2 years of experience\n\n"
        "Required Skills:\n"
        "- Python: Data extraction, manipulation, and analysis.\n"
        "- SQL: Complex queries, joins, and aggregations.\n"
        "- Excel: Advanced formulas, pivot tables, and data modeling.\n\n"
        "Preferred / Plus Skills:\n"
        "- Power BI: Interactive dashboards and KPI reports.\n"
        "- Pandas: Data manipulation and exploratory analysis.\n"
        "- Git: Version control and collaboration."
    )


# -----------------------------------------------------------------------------
# Sidebar: Configuration & Parameters
# -----------------------------------------------------------------------------
st.sidebar.header("⚙️ Screening Settings")

st.sidebar.subheader("1. Skill Requirements")
must_have_input = st.sidebar.text_input(
    "Must-Have Skills (comma-separated):",
    value="python, sql, excel",
    help="Core non-negotiable skills required for the role.",
)

nice_to_have_input = st.sidebar.text_input(
    "Nice-To-Have Skills (comma-separated):",
    value="power bi, pandas, git",
    help="Preferred bonus skills that boost candidate ranking.",
)

st.sidebar.subheader("2. Experience & Thresholds")
min_years_input = st.sidebar.number_input(
    "Minimum Years of Experience:",
    min_value=0.0,
    max_value=20.0,
    value=2.0,
    step=0.5,
    help="Target minimum professional experience required.",
)

score_threshold_input = st.sidebar.slider(
    "Passing Score Threshold:",
    min_value=0.10,
    max_value=1.00,
    value=0.60,
    step=0.05,
    help="Candidates with overall score and must-have coverage at or above this threshold pass.",
)

min_must_coverage_input = st.sidebar.slider(
    "Min Must-Have Coverage:",
    min_value=0.10,
    max_value=1.00,
    value=0.60,
    step=0.05,
    help="Minimum required percentage of must-have skills candidate must possess.",
)

# Parse skills lists
must_have_skills = [s.strip().lower() for s in must_have_input.split(",") if s.strip()]
nice_to_have_skills = [s.strip().lower() for s in nice_to_have_input.split(",") if s.strip()]


# -----------------------------------------------------------------------------
# Main Panel: Header & Inputs
# -----------------------------------------------------------------------------
st.title("📄 Automated Resume Screening Tool")
st.markdown(
    "Screen, score, and rank candidate resumes against a job description using "
    "**skill matching**, **TF-IDF cosine similarity**, and **keyword stuffing detection**."
)

col_left, col_right = st.columns([1, 1], gap="medium")

with col_left:
    st.subheader("📋 1. Job Description")
    jd_text = st.text_area(
        "Paste Job Description here:",
        value=load_default_jd(),
        height=260,
        help="Paste the full job description text including responsibilities and qualifications.",
    )

with col_right:
    st.subheader("📂 2. Upload Resumes")
    uploaded_files = st.file_uploader(
        "Choose PDF, DOCX, or TXT resumes:",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="Upload candidate resumes in PDF (.pdf), Microsoft Word (.docx), or Plain Text (.txt).",
    )

    use_sample_resumes = False
    if not uploaded_files and SAMPLE_RESUMES_DIR.exists():
        sample_files = list_resumes(SAMPLE_RESUMES_DIR)
        if sample_files:
            use_sample_resumes = st.checkbox(
                f"Use {len(sample_files)} sample resumes from 'resumes/' directory",
                value=True,
                help="Check this to test the screening pipeline using the synthetic sample dataset.",
            )

st.markdown("---")

# -----------------------------------------------------------------------------
# Screening Execution
# -----------------------------------------------------------------------------
screen_button = st.button("🚀 Screen Resumes", type="primary", use_container_width=True)

if screen_button:
    if not jd_text.strip():
        st.error("Please provide a Job Description before screening.")
    else:
        names = []
        raw_texts = []

        with st.spinner("Extracting and parsing resumes..."):
            # Handle uploaded files using safe Windows temporary directory
            if uploaded_files:
                # Use ignore_cleanup_errors=True for robust Windows file handling
                with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
                    temp_dir_path = Path(temp_dir)
                    for file in uploaded_files:
                        safe_path = temp_dir_path / file.name
                        # Write the uploaded file buffer to a temporary file
                        with open(safe_path, "wb") as f_out:
                            f_out.write(file.getbuffer())
                        try:
                            # Extract text using our extractor
                            extracted = read_resume(safe_path)
                            names.append(file.name)
                            raw_texts.append(extracted)
                        except Exception as e:
                            st.warning(f"Could not read '{file.name}': {e}")
            elif use_sample_resumes and SAMPLE_RESUMES_DIR.exists():
                for sample_path in list_resumes(SAMPLE_RESUMES_DIR):
                    try:
                        extracted = read_resume(sample_path)
                        names.append(sample_path.name)
                        raw_texts.append(extracted)
                    except Exception as e:
                        st.warning(f"Could not read sample '{sample_path.name}': {e}")

        if not names:
            st.warning("No valid resumes were found or parsed. Please upload files to begin.")
        else:
            with st.spinner("Scoring resumes and running TF-IDF similarity model..."):
                results_df = score_resumes(
                    names=names,
                    raw_texts=raw_texts,
                    jd_text=jd_text,
                    must_have=must_have_skills,
                    nice_to_have=nice_to_have_skills,
                    min_years=min_years_input,
                    threshold=score_threshold_input,
                    min_must_coverage=min_must_coverage_input,
                )

            # Store results in session state for persistence
            st.session_state["results_df"] = results_df
            st.session_state["screened_count"] = len(results_df)

# -----------------------------------------------------------------------------
# Results Display
# -----------------------------------------------------------------------------
if "results_df" in st.session_state:
    df = st.session_state["results_df"]

    st.header("📊 Screening Results & Candidate Rankings")

    # Metric KPI Cards
    status_counts = df["status"].value_counts().to_dict()
    shortlisted_count = status_counts.get("Shortlisted", 0)
    manual_review_count = status_counts.get("Manual Review", 0)
    rejected_count = status_counts.get("Rejected", 0)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Resumes Screened", len(df))
    m2.metric("✅ Shortlisted", shortlisted_count)
    m3.metric("⚠️ Manual Review", manual_review_count, help="Candidates that passed thresholds but were flagged for keyword stuffing.")
    m4.metric("❌ Rejected", rejected_count)

    # -------------------------------------------------------------
    # Interactive Score Bar Chart
    # -------------------------------------------------------------
    st.subheader("📈 Candidate Score Comparison")

    chart_df = df.copy()
    chart_df["display_name"] = chart_df["rank"].astype(str) + ". " + chart_df["resume"]

    status_color_scale = alt.Scale(
        domain=["Shortlisted", "Manual Review", "Rejected"],
        range=["#28a745", "#ffc107", "#dc3545"],
    )

    chart = (
        alt.Chart(chart_df)
        .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
        .encode(
            x=alt.X("score:Q", title="Composite Score", scale=alt.Scale(domain=[0, 1.0])),
            y=alt.Y("display_name:N", sort=alt.EncodingSortField(field="rank", order="ascending"), title="Candidate Resume"),
            color=alt.Color("status:N", title="Status", scale=status_color_scale),
            tooltip=[
                alt.Tooltip("rank:Q", title="Rank"),
                alt.Tooltip("resume:N", title="Resume"),
                alt.Tooltip("score:Q", title="Score", format=".4f"),
                alt.Tooltip("status:N", title="Status"),
                alt.Tooltip("years_experience:Q", title="Experience (Yrs)"),
                alt.Tooltip("must_have_coverage:Q", title="Must-Have Coverage", format=".0%"),
                alt.Tooltip("keyword_stuffing:N", title="Keyword Stuffed"),
            ],
        )
        .properties(height=max(280, len(chart_df) * 35))
    )

    # Add a vertical threshold indicator line
    threshold_line = (
        alt.Chart(pd.DataFrame({"threshold": [score_threshold_input]}))
        .mark_rule(color="#0066cc", strokeDash=[4, 4], size=2)
        .encode(x="threshold:Q")
    )

    st.altair_chart(chart + threshold_line, use_container_width=True)

    # -------------------------------------------------------------
    # Ranked Table
    # -------------------------------------------------------------
    st.subheader("📋 Candidate Ranking Table")

    table_display = df.copy()
    # Format list columns for readable table display
    table_display["matched_skills"] = table_display["matched_skills"].apply(
        lambda x: ", ".join(x) if isinstance(x, list) and x else "None"
    )
    table_display["missing_must_have"] = table_display["missing_must_have"].apply(
        lambda x: ", ".join(x) if isinstance(x, list) and x else "None"
    )

    st.dataframe(
        table_display,
        use_container_width=True,
        column_config={
            "rank": st.column_config.NumberColumn("Rank", width="small"),
            "resume": st.column_config.TextColumn("Candidate Resume", width="medium"),
            "score": st.column_config.ProgressColumn(
                "Score",
                format="%.4f",
                min_value=0.0,
                max_value=1.0,
                width="medium",
            ),
            "tfidf_similarity": st.column_config.NumberColumn("TF-IDF Sim", format="%.4f", width="small"),
            "must_have_coverage": st.column_config.NumberColumn("Must-Have Cov", format="%.0%", width="small"),
            "years_experience": st.column_config.NumberColumn("Exp (Yrs)", format="%.1f", width="small"),
            "matched_skills": st.column_config.TextColumn("Matched Skills", width="large"),
            "missing_must_have": st.column_config.TextColumn("Missing Must-Have", width="medium"),
            "keyword_stuffing": st.column_config.CheckboxColumn("Keyword Stuffed?", width="small"),
            "status": st.column_config.TextColumn("Decision Status", width="medium"),
        },
        hide_index=True,
    )

    # -------------------------------------------------------------
    # Download Button
    # -------------------------------------------------------------
    csv_data = table_display.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Screening Report (CSV)",
        data=csv_data,
        file_name="resume_screening_report.csv",
        mime="text/csv",
        help="Export full ranked results and metrics as a CSV spreadsheet.",
    )

# -----------------------------------------------------------------------------
# Ethical Advisory Caption
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "⚠️ **Disclaimer & Advisory**: The scores and rankings generated by this tool are "
    "intended as an automated prioritization and screening aid, **not a final hiring decision**. "
    "All employment outcomes should be validated through comprehensive human review."
)
