from pydantic import BaseModel

class ResumeSchema(BaseModel):
    filename:      str
    jd_skills:     str
    resume_skills: str
    match_score:   float
    matched:       str
    missing:       str

    class Config:
        from_attributes = True