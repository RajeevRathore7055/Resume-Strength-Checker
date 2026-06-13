from fastapi import FastAPI, File, UploadFile, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import json

from database import SessionLocal, engine, Base
from models   import Resume
from matcher  import extract_text, extract_skills, match_skills
from fastapi.responses import FileResponse



Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Resume Matcher")

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
# def root():
@app.get("/")
def home():
    return FileResponse("static/index.html")
    return {"status": "ok", "message": "AI Resume Matcher API is running!"}


@app.post("/upload-jd/")
async def upload_jd(file: UploadFile = File(...)):
    file_bytes = await file.read()
    text       = extract_text(file_bytes, file.filename)
    jd_skills  = extract_skills(text)

    return {
        "jd_skills": jd_skills,
        "message":   "JD processed successfully"
    }


@app.post("/upload-resume/")
async def upload_resume(
    file:      UploadFile = File(...),
    jd_skills: str        = Form(...),
    db:        Session    = Depends(get_db)
):
    file_bytes    = await file.read()
    text          = extract_text(file_bytes, file.filename)
    resume_skills = extract_skills(text)

    # FIX 1: jd_skills empty hone par safe handling
    if not jd_skills or jd_skills.strip() == "":
        jd_skills_list = []
    else:
        try:
            jd_skills_list = json.loads(jd_skills)
        except json.JSONDecodeError:
            jd_skills_list = []

    result = match_skills(jd_skills_list, resume_skills)

    # FIX 2: sirf purane columns save karo (matched/missing nahi)
    db_entry = Resume(
        filename      = file.filename,
        jd_skills     = json.dumps(jd_skills_list),
        resume_skills = json.dumps(resume_skills),
        match_score   = result["score"],
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    return {
        "filename":      file.filename,
        "jd_skills":     jd_skills_list,
        "resume_skills": resume_skills,
        "match_score":   result["score"],
        "matched":       result["matched"],
        "missing":       result["missing"],
    }
