# import io
# import PyPDF2

# def extract_text(file_bytes: bytes, filename: str) -> str:
#     """Extract text from .txt or .pdf file bytes."""
#     fname = filename.lower()

#     if fname.endswith(".txt"):
#         return file_bytes.decode("utf-8", errors="ignore")

#     elif fname.endswith(".pdf"):
#         reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
#         text = ""
#         for page in reader.pages:
#             text += page.extract_text() or ""
#         return text

#     return ""


# def extract_skills(text: str) -> list:
#     """Match skills from text against skills database."""
#     text = text.lower()

#     skills_db = [
#         "python", "java", "javascript", "typescript",
#         "react", "node", "node.js", "express",
#         "html", "css", "tailwind",
#         "fastapi", "flask", "django",
#         "mysql", "postgresql", "mongodb", "redis", "sql",
#         "docker", "kubernetes", "aws", "git",
#         "machine learning", "deep learning", "nlp",
#         "langchain", "llm", "rag", "ai",
#         "pandas", "numpy", "scikit-learn",
#     ]

#     return [skill for skill in skills_db if skill in text]


# def match_skills(jd_skills: list, resume_skills: list) -> dict:
#     """
#     Returns:
#       score   — match percentage
#       matched — skills present in both JD and resume
#       missing — skills in JD but not in resume
#     """
#     jd_set     = set(jd_skills)
#     resume_set = set(resume_skills)

#     if not jd_set:
#         return {"score": 0, "matched": [], "missing": []}

#     matched = list(jd_set & resume_set)
#     missing = list(jd_set - resume_set)
#     score   = round(len(matched) / len(jd_set) * 100, 2)

#     return {"score": score, "matched": matched, "missing": missing}


import io
import PyPDF2

def extract_text(file_bytes, filename):
    if filename.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")

    if filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for p in reader.pages:
            text += p.extract_text() or ""
        return text

    return ""

def extract_skills(text):
    text = text.lower()

    skills = [
        "python","java","javascript","react","node","fastapi","django",
        "mysql","mongodb","sql","html","css","aws","docker",
        "machine learning","ai","nlp"
    ]

    return [s for s in skills if s in text]

def match_skills(jd, resume):
    jd_set = set(jd)
    res_set = set(resume)

    if not jd_set:
        return {"score": 0, "matched": [], "missing": []}

    matched = list(jd_set & res_set)
    missing = list(jd_set - res_set)

    score = round(len(matched)/len(jd_set)*100, 2)

    return {
        "score": score,
        "matched": matched,
        "missing": missing
    }
