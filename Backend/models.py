from sqlalchemy import Column, Integer, String, Float, Text

from database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String(255))

    jd_skills = Column(Text)

    resume_skills = Column(Text)

    match_score = Column(Float)
