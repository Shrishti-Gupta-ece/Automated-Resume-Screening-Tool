"""
src/scorer.py
Module for scoring, ranking, and classifying resumes against a job description.

Combines:
- Must-have skills coverage (50% weight)
- Nice-to-have skills coverage (15% weight)
- TF-IDF with (1, 2) n-grams & cosine similarity (25% weight)
- Experience score (10% weight)

Rules:
- Shortlist only if must-have coverage >= min_must_coverage (default 0.6) and score >= threshold.
- Candidates that pass both thresholds but are keyword-stuffed are flagged for "Manual Review".
- All other candidates are "Rejected".
"""

from typing import Iterable, List, Sequence, Union
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.cleaner import clean_text
from src.skills import extract_skills, is_keyword_stuffed, years_experience


def score_resumes(
    names: Sequence[str],
    raw_texts: Sequence[str],
    jd_text: str,
    must_have: Iterable[str],
    nice_to_have: Iterable[str],
    min_years: float = 2.0,
    threshold: float = 0.60,
    min_must_coverage: float = 0.60,
) -> pd.DataFrame:
    """
    Scores and ranks candidate resumes against a job description.

    Parameters:
        names (Sequence[str]): List of resume names or filenames.
        raw_texts (Sequence[str]): List of raw extracted text strings for each resume.
        jd_text (str): The raw text of the job description.
        must_have (Iterable[str]): Required skill names (e.g. ['python', 'sql', 'excel']).
        nice_to_have (Iterable[str]): Preferred skill names (e.g. ['power bi', 'pandas', 'git']).
        min_years (float): Minimum required years of experience (default 2.0).
        threshold (float): Minimum composite score required to pass (default 0.60).
        min_must_coverage (float): Minimum must-have skill coverage required to pass (default 0.60).

    Returns:
        pd.DataFrame: Ranked dataframe sorted by score descending with columns:
            [rank, resume, score, tfidf_similarity, must_have_coverage,
             years_experience, matched_skills, missing_must_have,
             keyword_stuffing, status]
    """
    output_columns = [
        "rank",
        "resume",
        "score",
        "tfidf_similarity",
        "must_have_coverage",
        "years_experience",
        "matched_skills",
        "missing_must_have",
        "keyword_stuffing",
        "status",
    ]

    # Handle edge case where no resumes are provided
    if not names or not raw_texts:
        return pd.DataFrame(columns=output_columns)

    # Normalize skill requirements to lowercase
    must_have_list = [skill.lower().strip() for skill in must_have if skill.strip()]
    nice_to_have_list = [skill.lower().strip() for skill in nice_to_have if skill.strip()]

    # Clean job description and candidate texts for TF-IDF
    cleaned_jd = clean_text(jd_text)
    cleaned_resumes = [clean_text(text) for text in raw_texts]

    # Compute TF-IDF representation (unigrams + bigrams, English stop words)
    corpus = [cleaned_jd] + cleaned_resumes
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Calculate cosine similarity of each resume (rows 1..N) against JD (row 0)
    jd_vector = tfidf_matrix[0:1]
    resume_vectors = tfidf_matrix[1:]
    cosine_sims = cosine_similarity(resume_vectors, jd_vector).flatten()

    rows = []
    for i, name in enumerate(names):
        raw_text = raw_texts[i]
        candidate_skills = extract_skills(raw_text)

        # 1. Must-have skill coverage
        matched_must = [s for s in must_have_list if s in candidate_skills]
        missing_must = [s for s in must_have_list if s not in candidate_skills]
        if must_have_list:
            must_have_cov = len(matched_must) / len(must_have_list)
        else:
            must_have_cov = 1.0

        # 2. Nice-to-have skill coverage
        matched_nice = [s for s in nice_to_have_list if s in candidate_skills]
        if nice_to_have_list:
            nice_to_have_cov = len(matched_nice) / len(nice_to_have_list)
        else:
            nice_to_have_cov = 1.0

        # 3. TF-IDF Cosine Similarity
        sim_score = float(cosine_sims[i])
        # Ensure similarity stays within [0.0, 1.0]
        sim_score = max(0.0, min(1.0, sim_score))

        # 4. Years of experience & experience score
        exp_years = years_experience(raw_text)
        if min_years <= 0:
            exp_score = 1.0
        else:
            exp_score = min(exp_years / min_years, 1.0)
        exp_score = max(0.0, exp_score)

        # Composite score calculation:
        # 50% must-have + 15% nice-to-have + 25% similarity + 10% experience
        composite_score = (
            (0.50 * must_have_cov)
            + (0.15 * nice_to_have_cov)
            + (0.25 * sim_score)
            + (0.10 * exp_score)
        )

        # Check for keyword stuffing
        is_stuffed = is_keyword_stuffed(raw_text, limit=6)

        # Qualification check:
        # Candidate passes only if must-have coverage >= min_must_coverage and score >= threshold
        passes = (must_have_cov >= min_must_coverage) and (composite_score >= threshold)

        if passes:
            status = "Manual Review" if is_stuffed else "Shortlisted"
        else:
            status = "Rejected"

        rows.append(
            {
                "resume": name,
                "score": round(composite_score, 4),
                "tfidf_similarity": round(sim_score, 4),
                "must_have_coverage": round(must_have_cov, 4),
                "years_experience": exp_years,
                "matched_skills": candidate_skills,
                "missing_must_have": missing_must,
                "keyword_stuffing": is_stuffed,
                "status": status,
            }
        )

    df = pd.DataFrame(rows)

    # Sort candidates by score in descending order
    df = df.sort_values(by=["score", "must_have_coverage"], ascending=[False, False]).reset_index(drop=True)

    # Add 1-based rank
    df["rank"] = range(1, len(df) + 1)

    # Order columns as specified
    return df[output_columns]
