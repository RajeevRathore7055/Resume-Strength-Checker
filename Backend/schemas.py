from pydantic import BaseModel

class ResumeSchema(BaseModel):
    filename: str
    jd_skills: str
    resume_skills: str
    match_score: float

    class Config:
        from_attributes = True