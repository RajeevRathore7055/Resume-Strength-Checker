import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Railway MySQL credentials — Render pe Environment Variables mein set karna
MYSQL_HOST     = os.getenv("MYSQLHOST",     "localhost")
MYSQL_PORT     = os.getenv("MYSQLPORT",     "3306")
MYSQL_USER     = os.getenv("MYSQLUSER",     "root")
MYSQL_PASSWORD = os.getenv("MYSQLPASSWORD", "qwerty1234")
MYSQL_DATABASE = os.getenv("MYSQLDATABASE", "resume_db")

DB_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

engine       = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base         = declarative_base()