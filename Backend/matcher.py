import PyPDF2


def extract_text(file):

    filename = file.filename.lower()

    if filename.endswith(".txt"):
        return file.file.read().decode("utf-8")

    elif filename.endswith(".pdf"):

        reader = PyPDF2.PdfReader(file.file)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    return ""


def extract_skills(text):

    text = text.lower()

    skills_db = [
        "python",
        "java",
        "react",
        "node",
        "mysql",
        "mongodb",
        "fastapi",
        "flask",
        "aws",
        "docker",
        "html",
        "css",
        "javascript"
    ]

    found = []

    for skill in skills_db:
        if skill in text:
            found.append(skill)

    return found


def match_skills(jd_skills, resume_skills):

    jd_set = set(jd_skills)

    resume_set = set(resume_skills)

    if len(jd_set) == 0:
        return 0

    matched = jd_set.intersection(resume_set)

    score = (len(matched) / len(jd_set)) * 100

    return round(score, 2)
