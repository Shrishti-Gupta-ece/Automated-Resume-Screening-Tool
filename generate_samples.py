"""
generate_samples.py
Script to generate 10 synthetic resumes in the 'resumes/' directory:
- 7 as .txt files
- 3 as .docx files (using python-docx)

Profiles included:
1. Strong Data Analyst (TXT) - Aarav Sharma
2. Strong Data Analyst (DOCX) - Elena Rostova
3. Strong Data Analyst (TXT) - Marcus Chen
4. Partial Skills: SQL + Excel, No Python (TXT) - Priya Patel
5. Partial Skills: Python + Excel, No SQL (DOCX) - Liam O'Connor
6. Fresher / Entry Level Data Analyst (TXT) - Ananya Iyer
7. Data Scientist / ML Engineer (DOCX) - Dr. Julian Vance
8. Full Stack Web Developer (TXT) - Carlos Ramirez
9. Digital Marketing Specialist (TXT) - Sophie Dubois
10. Keyword-Stuffed Resume (TXT) - Vikram Malhotra
"""

import os
from pathlib import Path
from docx import Document


def get_project_root():
    return Path(__file__).resolve().parent


def create_txt_resume(filepath: Path, content: str):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created TXT resume: {filepath.name}")


def create_docx_resume(filepath: Path, title: str, sections: list):
    doc = Document()
    doc.add_heading(title, level=0)

    for heading, paragraphs, bullets in sections:
        if heading:
            doc.add_heading(heading, level=1)
        for p in paragraphs:
            doc.add_paragraph(p)
        for b in bullets:
            doc.add_paragraph(b, style="List Bullet")

    doc.save(filepath)
    print(f"Created DOCX resume: {filepath.name}")


def generate_resumes():
    base_dir = get_project_root()
    resumes_dir = base_dir / "resumes"
    resumes_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------
    # 1. Strong Data Analyst (TXT) - Aarav Sharma
    # -------------------------------------------------------------
    aarav_content = """
AARAV SHARMA
Email: aarav.sharma.analytics@example.com | Phone: +1 (555) 234-5678 | Location: Chicago, IL
LinkedIn: linkedin.com/in/aaravsharma-analytics | Portfolio: github.com/aaravsharma-data

PROFESSIONAL SUMMARY
Results-driven Data Analyst with 4 years of experience extracting, transforming, and interpreting data to drive strategic business decisions. Proven expertise in relational database querying using SQL, Python scripting with Pandas for ETL and exploratory analysis, and advanced Excel modeling. Experienced in delivering executive dashboards using Power BI and maintaining collaborative codebases using Git.

SKILLS
- Programming & Databases: Python, SQL (PostgreSQL, MySQL)
- Data Libraries & Tools: Pandas, NumPy, Scikit-learn
- BI & Visualization: Power BI, Microsoft Excel (Power Query, Pivot Tables, Advanced Formulas, VBA)
- Tools & Workflows: Git, JIRA, Agile/Scrum
- Analytical Techniques: Exploratory Data Analysis (EDA), Statistical Modeling, Cohort Analysis, A/B Testing

PROFESSIONAL EXPERIENCE
Senior Data Analyst | FinTech Solutions Inc. | Chicago, IL
June 2022 – Present (2+ years)
- Developed and maintained automated data pipelines using Python (Pandas) and database feeds, reducing weekly reporting cycles by 35%.
- Wrote optimized SQL queries across complex relational databases exceeding 5M+ transaction records.
- Created interactive Power BI dashboards tracking business KPIs, revenue projections, and customer churn metrics.
- Utilized Git for version control across analytical scripts and shared data repositories.

Junior Data Analyst | RetailIQ Analytics | Columbus, OH
July 2020 – May 2022 (2 years)
- Conducted deep-dive customer purchase behavior analysis using advanced Excel and relational data modeling.
- Formulated automated Excel reporting templates with Pivot Tables and Power Query, saving 10 team hours per week.
- Assisted engineering team in Python data cleaning scripts to ingest vendor catalog records.

EDUCATION
Bachelor of Science in Information Systems & Statistics
University of Illinois at Urbana-Champaign | 2016 – 2020

CERTIFICATIONS
- Microsoft Certified: Power BI Data Analyst Associate
- Database Administration and Query Specialist Certification
"""
    create_txt_resume(resumes_dir / "aarav_sharma_data_analyst.txt", aarav_content)

    # -------------------------------------------------------------
    # 2. Strong Data Analyst (DOCX) - Elena Rostova
    # -------------------------------------------------------------
    elena_sections = [
        (
            "",
            [
                "Email: elena.rostova@example.com | Phone: +1 (555) 345-6789 | Location: New York, NY",
                "LinkedIn: linkedin.com/in/elena-rostova-data | Portfolio: github.com/elena-rostova",
            ],
            [],
        ),
        (
            "Professional Summary",
            [
                "Analytical and detail-oriented Data Analyst with 3.5 years of industry experience across healthcare and business intelligence. High proficiency in writing complex SQL queries, building Python data cleaning workflows with Pandas, and constructing executive dashboards in Power BI and Advanced Excel. Regular practitioner of Git for collaborative version control."
            ],
            [],
        ),
        (
            "Core Competencies",
            [],
            [
                "Languages: Python, SQL (PostgreSQL, SQL Server, MySQL)",
                "Analytics & Libraries: Pandas, NumPy, Matplotlib, Data Cleaning & Preprocessing",
                "Reporting & Spreadsheets: Microsoft Excel (VLOOKUP, INDEX/MATCH, Pivot Tables, Macros), Power BI",
                "Version Control & Collaboration: Git, GitHub, GitLab, Confluence",
                "Business Acumen: KPI Tracking, Data Visualization, Cross-Functional Team Leadership",
            ],
        ),
        (
            "Work Experience",
            [
                "Data Analyst | HealthMetrics Corp | New York, NY (Jan 2023 – Present)",
                "Business Intelligence Analyst | CloudSys Technologies | Boston, MA (July 2021 – Dec 2022)",
            ],
            [
                "Extracted and merged healthcare claims datasets utilizing advanced SQL joins, subqueries, and window functions.",
                "Engineered automated data preprocessing routines in Python utilizing Pandas, handling missing data and outliers.",
                "Designed and launched 12+ company-wide Power BI dashboards used by senior executives daily.",
                "Managed all analytical scripts and queries in a centralized Git repository, following strict code review workflows.",
                "Audited and cleaned legacy financial models in Microsoft Excel, improving calculation efficiency and auditability.",
            ],
        ),
        (
            "Education",
            [
                "Bachelor of Science in Applied Mathematics & Statistics",
                "Boston University, graduated May 2021",
            ],
            [],
        ),
    ]
    create_docx_resume(
        resumes_dir / "elena_rostova_data_analyst.docx",
        "Elena Rostova - Data Analyst",
        elena_sections,
    )

    # -------------------------------------------------------------
    # 3. Strong Data Analyst (TXT) - Marcus Chen
    # -------------------------------------------------------------
    marcus_content = """
MARCUS CHEN
Austin, TX | marcus.chen.analyst@example.com | (555) 456-7890 | github.com/mchen-analytics

SUMMARY
Data Analyst with 3 years of commercial experience translating complex enterprise datasets into actionable insights. Expert in writing efficient SQL queries, programming in Python (Pandas/NumPy) for automated data extraction and transformation, and building interactive visual reports in Power BI and Excel. Experienced in version control with Git within agile teams.

CORE SKILLS
- Core Tech: Python, SQL, Excel, Power BI, Pandas, Git
- Database Systems: PostgreSQL, Snowflake, Microsoft SQL Server
- Spreadsheet Modeling: Advanced Excel (VLOOKUP, XLOOKUP, Pivot Tables, Power Pivot)
- Analysis Methods: Predictive Trend Analysis, Cohort Segmentation, Data Hygiene, Root-Cause Analysis

EXPERIENCE
Data Analyst | E-Commerce Direct | Austin, TX
March 2023 – Present (2+ years)
- Queried large-scale customer transaction databases using SQL to track sales conversions, customer retention, and cart abandonment.
- Built reusable Python ETL scripts with Pandas to clean and consolidate messy API exports from multiple marketplace channels.
- Deployed and maintained 8 production Power BI dashboards tracking order fulfillment metrics and sales performance.
- Maintained code repositories using Git for analytics scripts, automated reports, and database migrations.

Data Operations Associate | OmniRetail Solutions | Dallas, TX
June 2021 – February 2023 (1.5+ years)
- Handled daily inventory reporting using Microsoft Excel advanced functions and automated macros.
- Executed ad-hoc SQL queries to troubleshoot stock discrepancies across regional warehouses.
- Collaborated with business managers to evaluate promotional discount impacts.

EDUCATION
B.S. in Economics, Minor in Data Science | University of Texas at Austin (2017 – 2021)
"""
    create_txt_resume(resumes_dir / "marcus_chen_data_analyst.txt", marcus_content)

    # -------------------------------------------------------------
    # 4. Partial Skills: SQL + Excel, No Python (TXT) - Priya Patel
    # -------------------------------------------------------------
    priya_content = """
PRIYA PATEL
Email: priya.patel.reports@example.com | Phone: (555) 567-8901 | Atlanta, GA

PROFESSIONAL SUMMARY
Business & Reporting Analyst with 3 years of experience specializing in SQL querying, Excel data modeling, and Power BI visualization. Proven track record of consolidating operational metrics and presenting executive summaries to business leaders. Currently expanding technical skillset into automated scripting.

TECHNICAL SKILLS
- Databases & Querying: SQL (PostgreSQL, Oracle DB, SQL Server)
- Spreadsheets: Microsoft Excel (VLOOKUP, XLOOKUP, Nested IF, Pivot Tables, Power Query)
- Business Intelligence: Power BI, Tableau Desktop
- Other Tools: JIRA, MS PowerPoint, Sharepoint, SAP

PROFESSIONAL EXPERIENCE
Reporting Analyst | Logistics Hub International | Atlanta, GA
August 2021 – Present (3+ years)
- Executed complex SQL queries to extract shipment tracking data, carrier metrics, and regional transit times.
- Built comprehensive Excel operational workbooks using Pivot Tables, complex formulas, and conditional formatting.
- Designed executive Power BI dashboards displaying key shipping performance indicators and SLA adherence.
- Collaborated with business managers to identify operational bottlenecks and recommend process improvements.
- Standardized monthly reporting packages distributed to executive stakeholders.

EDUCATION
Bachelor of Business Administration (BBA) in Information Systems
Georgia State University | Graduated 2021
"""
    create_txt_resume(resumes_dir / "priya_patel_sql_excel.txt", priya_content)

    # -------------------------------------------------------------
    # 5. Partial Skills: Python + Excel, No SQL (DOCX) - Liam O'Connor
    # -------------------------------------------------------------
    liam_sections = [
        (
            "",
            [
                "Email: liam.oconnor@example.com | Phone: (555) 678-9012 | Denver, CO",
                "GitHub: github.com/liam-oconnor-ops",
            ],
            [],
        ),
        (
            "Profile",
            [
                "Operations Analyst with 2.5 years of experience automating data munging and operational reporting using Python and Excel. Adept at cleaning flat files, parsing CSVs/JSON with Pandas, and maintaining scripts under Git version control. Looking to leverage programming and analytical foundations in a dedicated analytics role."
            ],
            [],
        ),
        (
            "Skills",
            [],
            [
                "Languages & Libraries: Python, Pandas, NumPy",
                "Tools & Version Control: Git, GitHub, Jupyter Notebooks",
                "Spreadsheets: Microsoft Excel (Formulas, Pivot Tables, Charts, Data Validation)",
                "Methodologies: Workflow Automation, Process Improvement, Data Auditing",
            ],
        ),
        (
            "Experience",
            [
                "Operations Analyst | SupplyFlow Logistics | Denver, CO (Feb 2022 – Present)",
            ],
            [
                "Engineered Python scripts using Pandas to clean and merge disparate monthly CSV supply chain logs.",
                "Automated recurring inventory tracking reports in Microsoft Excel, reducing manual data entry time by 40%.",
                "Maintained internal data cleaning automation scripts with Git for version control and change documentation.",
                "Performed exploratory variance analysis on vendor invoices against contracted purchase orders.",
            ],
        ),
        (
            "Education",
            [
                "B.A. in Supply Chain Management & Quantitative Methods",
                "University of Colorado Boulder | 2018 – 2022",
            ],
            [],
        ),
    ]
    create_docx_resume(
        resumes_dir / "liam_oconnor_python_excel.docx",
        "Liam O'Connor - Operations Analyst",
        liam_sections,
    )

    # -------------------------------------------------------------
    # 6. Fresher / Entry Level Data Analyst (TXT) - Ananya Iyer
    # -------------------------------------------------------------
    ananya_content = """
ANANYA IYER
San Jose, CA | ananya.iyer.grad@example.com | (555) 789-0123 | github.com/ananya-iyer

OBJECTIVE
Motivated and detail-oriented recent graduate with a Bachelor's degree in Computer Science seeking an entry-level Data Analyst position. Solid foundational knowledge of Python, SQL, Excel, and Pandas developed through academic coursework, capstone projects, and a 3-month summer internship.

EDUCATION
Bachelor of Science in Computer Science
San Jose State University, CA | Graduated: May 2024
GPA: 3.8/4.0
Relevant Coursework: Database Management Systems, Data Analysis with Python, Statistics and Probability, Applied Linear Algebra.

TECHNICAL SKILLS
- Programming: Python, SQL
- Data Analysis Libraries: Pandas, NumPy, Matplotlib
- Business Intelligence & Spreadsheets: Microsoft Excel, Power BI (Foundations)
- Version Control: Git, GitHub

ACADEMIC & INTERNSHIP EXPERIENCE
Data Analytics Intern | TechStart Analytics | San Jose, CA
June 2023 – August 2023 (3 months)
- Assisted data team in writing SQL queries to pull customer feedback surveys.
- Preprocessed survey responses in Python utilizing Pandas for text categorization.
- Created summary charts and tables in Microsoft Excel for presentation to senior mentors.

PROJECTS
E-Commerce Sales Analysis Dashboard (Academic Capstone) | Python, SQL, Power BI, Git
- Wrote SQL scripts to clean and aggregate 100,000+ transaction records.
- Conducted exploratory data analysis using Python (Pandas) to detect seasonal purchasing spikes.
- Visualized findings via an interactive Power BI dashboard and tracked project milestones with Git.
"""
    create_txt_resume(resumes_dir / "ananya_iyer_fresher.txt", ananya_content)

    # -------------------------------------------------------------
    # 7. Data Scientist / ML Engineer (DOCX) - Dr. Julian Vance
    # -------------------------------------------------------------
    julian_sections = [
        (
            "",
            [
                "Email: julian.vance.phd@example.com | Phone: (555) 890-1234 | San Francisco, CA",
                "Google Scholar / GitHub: github.com/dr-julian-vance",
            ],
            [],
        ),
        (
            "Summary",
            [
                "Principal Data Scientist and Machine Learning Researcher with 5 years of post-doctorate experience designing and deploying deep learning models, natural language processing pipelines, and high-throughput predictive systems. Proven publication record in AI/ML conferences and extensive experience with Python, Scikit-learn, PyTorch, and distributed computing."
            ],
            [],
        ),
        (
            "Technical Expertise",
            [],
            [
                "Core Languages: Python, C++, SQL",
                "Machine Learning / Deep Learning: PyTorch, TensorFlow, Scikit-learn, XGBoost, HuggingFace Transformers",
                "MLOps & Big Data: Docker, Kubernetes, MLflow, Spark, Git, AWS SageMaker",
                "Specializations: NLP, Computer Vision, Bayesian Inference, Neural Architecture Search",
            ],
        ),
        (
            "Professional Experience",
            [
                "Senior Data Scientist | DeepCognition AI | San Francisco, CA (2021 – Present)",
                "Machine Learning Engineer | NeuralScale Inc. | Palo Alto, CA (2019 – 2021)",
            ],
            [
                "Architected and trained transformer-based NLP models with PyTorch and Scikit-learn, cutting inference latency by 45%.",
                "Implemented distributed training pipelines processing over 20TB of unstructured text datasets.",
                "Engineered feature extraction queries in SQL and structured MLOps deployment pipelines via Git and Docker.",
                "Authored 4 peer-reviewed research papers on self-supervised representation learning.",
            ],
        ),
        (
            "Education",
            [
                "Ph.D. in Computer Science (Machine Learning Focus) | Stanford University (2019)",
                "B.S. in Computer Science | UC Berkeley (2015)",
            ],
            [],
        ),
    ]
    create_docx_resume(
        resumes_dir / "julian_vance_data_scientist.docx",
        "Dr. Julian Vance - Senior Data Scientist",
        julian_sections,
    )

    # -------------------------------------------------------------
    # 8. Full Stack Web Developer (TXT) - Carlos Ramirez
    # -------------------------------------------------------------
    carlos_content = """
CARLOS RAMIREZ
Miami, FL | carlos.ramirez.dev@example.com | (555) 901-2345 | github.com/carlosramirez-dev

PROFESSIONAL SUMMARY
Dynamic Full Stack Web Developer with 4 years of experience building scalable, responsive, and robust web applications. High proficiency in modern JavaScript/TypeScript ecosystems including React, Next.js, Node.js, and Express. Adept with document databases like MongoDB and CSS frameworks like Tailwind CSS.

SKILLS
- Front-End: JavaScript (ES6+), TypeScript, React, Next.js, Redux, HTML5, CSS3, Tailwind CSS
- Back-End: Node.js, Express, RESTful APIs, GraphQL
- Databases: MongoDB, Mongoose, Redis
- DevOps & Tools: Git, GitHub, Docker, Webpack, Postman, Vercel

EXPERIENCE
Full Stack Developer | WebForge Studios | Miami, FL
April 2020 – Present (4 years)
- Designed and built responsive client-side user interfaces using React, Next.js, and Tailwind CSS.
- Developed scalable backend services and microservices with Node.js and Express.
- Designed schemas and query mechanisms for NoSQL databases utilizing MongoDB.
- Integrated third-party payment gateways (Stripe) and authentication flows (OAuth, JWT).
- Utilized Git for daily branching, pull requests, and continuous integration deployments.

EDUCATION
Bachelor of Science in Web Design & Software Development
Florida International University | 2016 – 2020
"""
    create_txt_resume(resumes_dir / "carlos_ramirez_web_developer.txt", carlos_content)

    # -------------------------------------------------------------
    # 9. Digital Marketing Specialist (TXT) - Sophie Dubois
    # -------------------------------------------------------------
    sophie_content = """
SOPHIE DUBOIS
Los Angeles, CA | sophie.dubois.marketing@example.com | (555) 012-3456

PROFESSIONAL SUMMARY
Creative and analytical Digital Marketing Specialist with 4 years of hands-on experience in search engine optimization (SEO), pay-per-click advertising (PPC), social media campaigns, and brand storytelling. Proven history of boosting organic website traffic by 65% and managing high-ROI multi-platform ad budgets.

AREAS OF EXPERTISE
- Digital Marketing Strategy, Search Engine Optimization (SEO), Search Engine Marketing (SEM)
- Google Ads, Facebook Ads Manager, TikTok Ads
- Copywriting, Content Creation, Email Marketing (Mailchimp, Klaviyo)
- Web Analytics: Google Analytics 4 (GA4), Google Search Console
- Creative: Canva, Adobe Photoshop, Social Media Management

PROFESSIONAL EXPERIENCE
Digital Marketing Manager | BrandElevate Agency | Los Angeles, CA
January 2021 – Present (3+ years)
- Managed quarterly paid acquisition budgets exceeding $300,000 across Google Ads and Meta platforms.
- Supervised comprehensive SEO on-page and off-page strategy, resulting in a 65% boost in non-brand organic search clicks.
- Conducted conversion rate optimization (CRO) audits on client landing pages to improve sales conversion rates.
- Authored persuasive email newsletters and promotional campaigns achieving an average 28% open rate.

Marketing Coordinator | Horizon Media | San Diego, CA
June 2019 – December 2020 (1.5 years)
- Coordinated social media editorial calendars and scheduled daily brand posts.
- Monitored engagement metrics using Google Analytics and prepared bi-weekly client performance summaries.

EDUCATION
Bachelor of Arts in Marketing & Public Relations
University of Southern California (USC) | 2015 – 2019
"""
    create_txt_resume(resumes_dir / "sophie_dubois_marketing.txt", sophie_content)

    # -------------------------------------------------------------
    # 10. Keyword-Stuffed Resume (TXT) - Vikram Malhotra
    # -------------------------------------------------------------
    vikram_content = """
VIKRAM MALHOTRA
Email: vikram.malhotra.keywords@example.com | Phone: (555) 111-2222 | Seattle, WA

DATA ANALYST | PYTHON | SQL | EXCEL | POWER BI | PANDAS | GIT

PROFESSIONAL SUMMARY
Data Analyst with 2 years of experience. Python Python Python SQL SQL SQL Excel Excel Excel Power BI Power BI Power BI Pandas Pandas Pandas Git Git Git. Highly skilled in Python, SQL, Excel, Power BI, Pandas, Git. Passionate about Python programming, SQL databases, Excel spreadsheets, Power BI reporting, Pandas dataframe manipulations, and Git repository version control.

TECHNICAL SKILLS & KEYWORDS
Python, SQL, Excel, Power BI, Pandas, Git, Python, SQL, Excel, Power BI, Pandas, Git,
Python, SQL, Excel, Power BI, Pandas, Git, Python, SQL, Excel, Power BI, Pandas, Git,
Python, SQL, Excel, Power BI, Pandas, Git, Python, SQL, Excel, Power BI, Pandas, Git,
Python, SQL, Excel, Power BI, Pandas, Git, Python, SQL, Excel, Power BI, Pandas, Git,
Python, SQL, Excel, Power BI, Pandas, Git, Python, SQL, Excel, Power BI, Pandas, Git,
Python, SQL, Excel, Power BI, Pandas, Git, Python, SQL, Excel, Power BI, Pandas, Git.

WORK EXPERIENCE
Data Analyst | Keyword Analytics LLC | Seattle, WA
January 2022 – January 2024 (2 years)
- Used Python to write Python code for Python data scripts.
- Executed SQL queries in SQL database using SQL joins and SQL aggregations.
- Formatted Excel spreadsheets with Excel formulas, Excel VLOOKUP, and Excel Pivot Tables.
- Built Power BI dashboards using Power BI visuals and Power BI DAX expressions.
- Used Pandas for Pandas dataframes, Pandas data cleaning, and Pandas manipulation.
- Pushed Git commits with Git add, Git commit, Git push, and Git branch workflows.
- Python SQL Excel Power BI Pandas Git repeated daily for maximum analytical efficiency.

EDUCATION
B.S. in Data Analytics | Python SQL Excel University (2018 - 2022)
"""
    create_txt_resume(resumes_dir / "vikram_malhotra_keyword_stuffed.txt", vikram_content)

    print("\nSuccessfully generated all 10 synthetic resumes (7 .txt, 3 .docx).")


if __name__ == "__main__":
    generate_resumes()
