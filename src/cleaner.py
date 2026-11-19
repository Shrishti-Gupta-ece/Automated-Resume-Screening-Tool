"""
src/cleaner.py
Module for cleaning and preprocessing extracted resume text.

Provides:
- clean_text(text): Converts text to lowercase, removes emails & URLs, and collapses whitespace.
"""

import re


def clean_text(text: str) -> str:
    """
    Cleans and standardizes raw text from resumes or job descriptions.

    Transformations performed:
    1. Converts all characters to lowercase.
    2. Removes email addresses (e.g., user@example.com).
    3. Removes web URLs (e.g., https://linkedin.com/in/... or www.example.com).
    4. Collapses multiple spaces, tabs, and newlines into a single space.
    5. Trims leading and trailing whitespace.

    Parameters:
        text (str): The raw text to clean.

    Returns:
        str: The cleaned and normalized text.
    """
    # If the input is None or not a string, return an empty string safely
    if not text or not isinstance(text, str):
        return ""

    # Step 1: Convert all text to lowercase
    # This ensures that "Python", "PYTHON", and "python" are treated identically.
    cleaned = text.lower()

    # Step 2: Remove URLs (web links)
    # Matches URLs starting with http://, https://, or www.
    url_pattern = r"https?://\S+|www\.\S+"
    cleaned = re.sub(url_pattern, " ", cleaned)

    # Step 3: Remove email addresses
    # Matches standard email address structures: name@domain.extension
    email_pattern = r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
    cleaned = re.sub(email_pattern, " ", cleaned)

    # Step 4: Collapse multiple consecutive whitespace characters (spaces, tabs, newlines)
    # into a single space, and strip whitespace from both ends.
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned
