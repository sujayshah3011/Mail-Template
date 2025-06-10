from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True)
    company_name = Column(String)
    contact_name = Column(String)
    industry = Column(String)
    created_at = Column(DateTime)

class Template(Base):
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    generated_at = Column(DateTime)
    subject = Column(String)
    body = Column(String)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)