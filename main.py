"""
main.py
Main command-line entry point for Automated Resume Screening Tool.

Workflow:
1. Loads all resumes from 'resumes/' (PDF, DOCX, TXT).
2. Loads the target job description from 'data/job_description.txt'.
3. Scores and ranks resumes using the scoring engine in 'src/scorer.py'.
4. Displays formatted ranked table and status summary in console.
5. Exports reports to 'outputs/':
   - outputs/ranking_report.csv (Full ranked dataset)
   - outputs/shortlisted.csv (Shortlisted candidates)
   - outputs/rejected.csv (Rejected candidates)
"""

import os
from pathlib import Path
import pandas as pd

from src.extractor import list_resumes, read_resume
from src.scorer import score_resumes


def get_project_root() -> Path:
    """Returns the root directory of the project."""
    return Path(__file__).resolve().parent


def run_screening():
    project_root = get_project_root()
    resumes_dir = project_root / "resumes"
    jd_path = project_root / "data" / "job_description.txt"
    outputs_dir = project_root / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print(" AUTOMATED RESUME SCREENING PIPELINE")
    print("=" * 80)

    # 1. Verify and read Job Description
    if not jd_path.exists():
        print(f"Error: Job description file not found at '{jd_path}'")
        return

    print(f"\n[1/4] Loading Job Description from: {jd_path.name}")
    jd_text = read_resume(jd_path)

    # 2. Discover and extract resumes
    resume_files = list_resumes(resumes_dir)
    if not resume_files:
        print(f"Error: No supported resume files found in '{resumes_dir}'")
        return

    print(f"[2/4] Discovered {len(resume_files)} resumes in '{resumes_dir.name}/'")
    names = [f.name for f in resume_files]
    raw_texts = [read_resume(f) for f in resume_files]

    # 3. Define requirements & parameters
    must_have = ["python", "sql", "excel"]
    nice_to_have = ["power bi", "pandas", "git"]
    min_years = 2.0
    threshold = 0.60
    min_must_coverage = 0.60

    print("\n[3/4] Screening parameters:")
    print(f"  - Must-have skills      : {', '.join(must_have)}")
    print(f"  - Nice-to-have skills   : {', '.join(nice_to_have)}")
    print(f"  - Minimum Experience    : {min_years} years")
    print(f"  - Score Threshold       : {threshold}")
    print(f"  - Min Must Coverage     : {min_must_coverage}")

    # 4. Score and Rank Resumes
    print("\n[4/4] Executing scoring and TF-IDF similarity model...")
    df = score_resumes(
        names=names,
        raw_texts=raw_texts,
        jd_text=jd_text,
        must_have=must_have,
        nice_to_have=nice_to_have,
        min_years=min_years,
        threshold=threshold,
        min_must_coverage=min_must_coverage,
    )

    # -------------------------------------------------------------
    # Console Output: Ranked Table
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print(" RANKED SCREENING RESULTS")
    print("=" * 80)

    display_df = df.copy()
    display_df["matched_skills_str"] = display_df["matched_skills"].apply(lambda s: ", ".join(s) if s else "None")
    
    # Format printout
    print(f"{'Rank':<5} | {'Resume':<35} | {'Score':<7} | {'TF-IDF':<7} | {'MustCov':<7} | {'Exp':<5} | {'Status':<14}")
    print("-" * 90)
    for _, row in display_df.iterrows():
        print(
            f"{row['rank']:<5} | "
            f"{row['resume']:<35} | "
            f"{row['score']:<7.4f} | "
            f"{row['tfidf_similarity']:<7.4f} | "
            f"{row['must_have_coverage']:<7.2f} | "
            f"{row['years_experience']:<5.1f} | "
            f"{row['status']:<14}"
        )

    # -------------------------------------------------------------
    # Console Output: Status Summary
    # -------------------------------------------------------------
    status_counts = df["status"].value_counts().to_dict()
    shortlisted_count = status_counts.get("Shortlisted", 0)
    manual_review_count = status_counts.get("Manual Review", 0)
    rejected_count = status_counts.get("Rejected", 0)
    total_count = len(df)

    print("\n" + "=" * 80)
    print(" STATUS SUMMARY")
    print("=" * 80)
    print(f"Total Resumes Processed : {total_count}")
    print(f"  - Shortlisted         : {shortlisted_count} ({(shortlisted_count / total_count) * 100:.1f}%)")
    print(f"  - Manual Review       : {manual_review_count} ({(manual_review_count / total_count) * 100:.1f}%) [Keyword Stuffed]")
    print(f"  - Rejected            : {rejected_count} ({(rejected_count / total_count) * 100:.1f}%)")

    # -------------------------------------------------------------
    # Export CSV Reports
    # -------------------------------------------------------------
    export_df = df.copy()
    # Format list columns for clean CSV presentation
    export_df["matched_skills"] = export_df["matched_skills"].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
    export_df["missing_must_have"] = export_df["missing_must_have"].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)

    # 1. Full ranking report
    ranking_report_path = outputs_dir / "ranking_report.csv"
    export_df.to_csv(ranking_report_path, index=False)

    # 2. Shortlisted resumes
    shortlisted_df = export_df[export_df["status"] == "Shortlisted"].copy()
    shortlisted_path = outputs_dir / "shortlisted.csv"
    shortlisted_df.to_csv(shortlisted_path, index=False)

    # 3. Rejected resumes
    rejected_df = export_df[export_df["status"] == "Rejected"].copy()
    rejected_path = outputs_dir / "rejected.csv"
    rejected_df.to_csv(rejected_path, index=False)

    print("\n" + "=" * 80)
    print(" EXPORTED REPORTS")
    print("=" * 80)
    print(f"Full Report Saved to    : {ranking_report_path}")
    print(f"Shortlisted Saved to    : {shortlisted_path} ({len(shortlisted_df)} records)")
    print(f"Rejected Saved to       : {rejected_path} ({len(rejected_df)} records)")
    print("=" * 80)


if __name__ == "__main__":
    run_screening()
