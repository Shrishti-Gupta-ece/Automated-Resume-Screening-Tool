"""
src/extractor.py
Module for reading and discovering resume files.

Supported formats:
- Plain Text (.txt)
- Microsoft Word (.docx) via python-docx
- Adobe PDF (.pdf) via pdfplumber
"""

from pathlib import Path
from typing import List, Union
import docx
import pdfplumber


# List of file extensions supported by the resume screening tool
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def list_resumes(folder: Union[str, Path]) -> List[Path]:
    """
    Scans a folder and returns a sorted list of Path objects for all supported resume files.
    
    Parameters:
        folder (str | Path): Path to the folder containing resume files.
        
    Returns:
        List[Path]: List of Path objects matching .pdf, .docx, or .txt extensions.
    """
    folder_path = Path(folder)
    
    # Check if folder exists
    if not folder_path.exists() or not folder_path.is_dir():
        print(f"Warning: Directory '{folder_path}' does not exist or is not a directory.")
        return []

    resume_files = []
    # Loop over all items in the directory
    for item in folder_path.iterdir():
        # Check if item is a file and has a supported extension (case-insensitive)
        # Also ignore temporary Office files starting with ~$
        if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS:
            if not item.name.startswith("~$"):
                resume_files.append(item)

    # Sort files alphabetically for consistent ordering
    return sorted(resume_files)


def _read_txt(file_path: Path) -> str:
    """Helper function to read a plain text resume."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()


def _read_docx(file_path: Path) -> str:
    """Helper function to extract text from a .docx file using python-docx."""
    doc = docx.Document(file_path)
    paragraphs = []
    
    # Extract text from paragraphs
    for p in doc.paragraphs:
        if p.text.strip():
            paragraphs.append(p.text.strip())

    # Extract text from tables if any exist
    for table in doc.tables:
        for row in table.rows:
            row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
            if row_text:
                paragraphs.append(" | ".join(row_text))

    return "\n".join(paragraphs)


def _read_pdf(file_path: Path) -> str:
    """Helper function to extract text from a PDF file using pdfplumber."""
    pages_text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text)
                
    return "\n".join(pages_text)


def read_resume(path: Union[str, Path]) -> str:
    """
    Reads and extracts text from a single resume file (PDF, DOCX, or TXT).
    
    Parameters:
        path (str | Path): The path to the resume file.
        
    Returns:
        str: Extracted plain text content from the file.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file format is not supported (.pdf, .docx, .txt).
    """
    file_path = Path(path)

    # Verify that the file actually exists
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: '{file_path}'")

    extension = file_path.suffix.lower()

    if extension == ".txt":
        return _read_txt(file_path)
    elif extension == ".docx":
        return _read_docx(file_path)
    elif extension == ".pdf":
        return _read_pdf(file_path)
    else:
        raise ValueError(
            f"Unsupported file format '{extension}' for file '{file_path.name}'. "
            f"Supported formats are: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )
