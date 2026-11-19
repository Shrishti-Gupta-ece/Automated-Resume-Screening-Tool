# Architecture and Workflow

## Pipeline
```
resumes/ (PDF, DOCX, TXT)        data/job_description.txt
            |                                |
            v                                v
     Text extraction  (src/extractor.py)
            |
            v
     Text cleaning    (src/cleaner.py)
            |
            v
     Skill extraction (src/skills.py)
            |
            v
     TF-IDF + cosine similarity, weighted score (src/scorer.py)
            |
            v
     Ranking + shortlist rules
            |
            v
     outputs/ranking_report.csv, shortlisted.csv, rejected.csv
     Streamlit dashboard (app.py)
```

## Scoring formula
score = 0.50 x must-have coverage + 0.15 x nice-to-have coverage
      + 0.25 x TF-IDF similarity + 0.10 x experience score

## Decision rules
- Shortlisted: must-have coverage >= 60% and score >= threshold
- Manual Review: passes the rules but keyword stuffing is detected
- Rejected: everything else

## Limitations
- Keyword matching can miss synonyms and context.
- Tested only on synthetic resumes.
- Scores are a ranking aid; a human makes the final decision.