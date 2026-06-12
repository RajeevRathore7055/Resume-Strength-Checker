# from fastapi import FastAPI, File, UploadFile, Form, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
# import json

# from database import SessionLocal, engine, Base
# from models import Resume
# from matcher import extract_skills, match_skills

# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# # CORS FIX
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # DB Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # JD Upload
# @app.post("/upload-jd/")
# async def upload_jd(file: UploadFile = File(...)):
#     content = (await file.read()).decode("utf-8")

#     jd_skills = extract_skills(content)

#     return {"jd_skills": jd_skills}


# # Resume Upload + Match
# @app.post("/upload-resume/")
# async def upload_resume(
#     file: UploadFile = File(...),
#     jd_skills: str = Form(...),
#     db: Session = Depends(get_db)
# ):

#     content = (await file.read()).decode("utf-8")

#     resume_skills = extract_skills(content)

#     jd_skills_list = json.loads(jd_skills)

#     score = match_skills(jd_skills_list, resume_skills)

#     db_entry = Resume(
#         filename=file.filename,
#         jd_skills=json.dumps(jd_skills_list),
#         resume_skills=json.dumps(resume_skills),
#         match_score=score
#     )

#     db.add(db_entry)
#     db.commit()
#     db.refresh(db_entry)

#     return {
#         "filename": file.filename,
#         "jd_skills": jd_skills_list,
#         "resume_skills": resume_skills,
#         "match_score": score
#     }


from fastapi import FastAPI, File, UploadFile, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import json

from database import SessionLocal, engine, Base
from models import Resume
from matcher import extract_text, extract_skills, match_skills

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# JD Upload
@app.post("/upload-jd/")
async def upload_jd(file: UploadFile = File(...)):

    text = extract_text(file)
    jd_skills = extract_skills(text)

    return {
        "jd_skills": jd_skills,
        "message": "JD processed successfully"
    }


# Resume Upload + Match
@app.post("/upload-resume/")
async def upload_resume(
    file: UploadFile = File(...),
    jd_skills: str = Form(...),
    db: Session = Depends(get_db)
):

    text = extract_text(file)
    resume_skills = extract_skills(text)

    jd_skills_list = json.loads(jd_skills)

    score = match_skills(jd_skills_list, resume_skills)

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
