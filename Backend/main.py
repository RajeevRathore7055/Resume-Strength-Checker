from fastapi import FastAPI, File, UploadFile, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import FileResponse
import os
from sqlalchemy.orm import Session

import json

from database import SessionLocal, engine, Base
from models import Resume
from matcher import extract_text, extract_skills, match_skills
from pathlib import Path

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Resume Matcher API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# @app.get("/")
# def home():
#     return {"message": "Resume Matcher Backend Running"}
# @app.get("/")
# def home():
#     return FileResponse(
#         os.path.join(
#             "Frontend",
#             "index.html"
#         )
#     )
@app.get("/")
def home():

    current_dir = Path(__file__).parent

    frontend_path = (
        current_dir.parent /
        "Frontend" /
        "index.html"
    )

    return FileResponse(frontend_path)

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload-jd/")
async def upload_jd(file: UploadFile = File(...)):

    text = extract_text(file)

    jd_skills = extract_skills(text)

    return {
        "jd_skills": jd_skills,
        "message": "JD processed successfully"
    }


@app.post("/upload-resume/")
async def upload_resume(
        file: UploadFile = File(...),
        jd_skills: str = Form(...),
        db: Session = Depends(get_db)
):

    text = extract_text(file)

    resume_skills = extract_skills(text)

    jd_skills_list = json.loads(jd_skills)

    score = match_skills(
        jd_skills_list,
        resume_skills
    )

    db_entry = Resume(
        filename=file.filename,
        jd_skills=json.dumps(jd_skills_list),
        resume_skills=json.dumps(resume_skills),
        match_score=score
    )

    db.add(db_entry)

    db.commit()

    db.refresh(db_entry)

    return {
        "filename": file.filename,
        "jd_skills": jd_skills_list,
        "resume_skills": resume_skills,
        "match_score": score
    }
