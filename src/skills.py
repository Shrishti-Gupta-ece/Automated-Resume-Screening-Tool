"""
src/skills.py
Module for skill extraction, experience detection, and keyword stuffing analysis.

Provides:
- SKILLS: Dictionary mapping canonical skill names to known aliases.
- extract_skills(text): Extracts canonical skills present in text using whole-word regex.
- years_experience(text): Identifies the maximum years of experience mentioned in text.
- is_keyword_stuffed(text, limit=6): Detects if any skill is repeated more than `limit` times.
"""

import re
from typing import Dict, List, Union


# ---------------------------------------------------------------------------
# Canonical Skills to Aliases mapping
# ---------------------------------------------------------------------------
SKILLS: Dict[str, List[str]] = {
    "python": ["python", "python3"],
    "sql": ["sql", "mysql", "postgresql", "postgres", "t-sql", "tsql", "pl/sql", "sqlite"],
    "excel": ["excel", "ms excel", "microsoft excel", "spreadsheets", "spreadsheet"],
    "power bi": ["power bi", "powerbi", "power-bi", "ms power bi"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "machine learning": ["machine learning", "ml"],
    "git": ["git", "github", "gitlab"],
    "docker": ["docker"],
    "aws": ["aws", "amazon web services"],
    "tableau": ["tableau", "tableau desktop"],
}


def _build_skill_pattern(aliases: List[str]) -> str:
    """
    Constructs a whole-word regular expression pattern for a list of aliases.
    Sorts aliases by length in descending order so that longer compound terms
    (e.g., 't-sql', 'postgresql') match before shorter ones ('sql').
    """
    # Sort aliases from longest to shortest to prevent prefix shadowing
    sorted_aliases = sorted(aliases, key=len, reverse=True)
    # Join escaped aliases inside a non-capturing group bounded by word boundaries (\b)
    escaped_group = "|".join(re.escape(alias) for alias in sorted_aliases)
    return rf"\b(?:{escaped_group})\b"


def extract_skills(text: str) -> List[str]:
    """
    Extracts canonical skill names found in the given text using whole-word regex.
    No fuzzy matching is performed to avoid false positives.

    Parameters:
        text (str): The raw or cleaned text of a resume or job description.

    Returns:
        List[str]: A sorted list of unique canonical skill names detected in the text.
    """
    if not text or not isinstance(text, str):
        return []

    text_lower = text.lower()
    matched_skills = set()

    for canonical_name, aliases in SKILLS.items():
        pattern = _build_skill_pattern(aliases)
        if re.search(pattern, text_lower):
            matched_skills.add(canonical_name)

    return sorted(matched_skills)


def years_experience(text: str) -> float:
    """
    Extracts and returns the largest 'N years' value found in the text.
    
    Supports:
    - Integer and decimal numbers (e.g., '3 years', '3.5 years', '2+ years', '5 yrs').
    - Various suffixes: 'year', 'years', 'yr', 'yrs', optionally with '+'.

    Parameters:
        text (str): The text to analyze.

    Returns:
        float: The maximum years of experience found (e.g., 4.0, 3.5), or 0.0 if none.
    """
    if not text or not isinstance(text, str):
        return 0.0

    # Pattern matches numbers followed by 'year', 'years', 'yr', 'yrs'
    # e.g., "4 years", "3.5 yrs", "2+ years"
    pattern = r"\b(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)\b"
    matches = re.findall(pattern, text, flags=re.IGNORECASE)

    if not matches:
        return 0.0

    # Convert matches to float, filtering out calendar years (e.g., <= 50)
    valid_years = [float(val) for val in matches if float(val) <= 50.0]

    return max(valid_years) if valid_years else 0.0


def is_keyword_stuffed(text: str, limit: int = 6) -> bool:
    """
    Determines if the text appears to be keyword-stuffed by repeating any single
    skill keyword more than the allowed limit.

    Parameters:
        text (str): The resume or document text.
        limit (int): The threshold count above which a skill is considered stuffed (default 6).

    Returns:
        bool: True if any skill appears more than `limit` times, False otherwise.
    """
    if not text or not isinstance(text, str):
        return False

    text_lower = text.lower()

    for canonical_name, aliases in SKILLS.items():
        pattern = _build_skill_pattern(aliases)
        occurrences = len(re.findall(pattern, text_lower))
        if occurrences > limit:
            return True

    return False
