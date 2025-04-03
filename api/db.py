from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://hariharan:hari1234@db:5432/tasks"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


from .models import Base  # Ensure models are imported

print("Creating tables if they don't exist...")
Base.metadata.create_all(bind=engine)