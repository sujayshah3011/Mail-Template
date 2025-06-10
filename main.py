from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai
from database import SessionLocal, Lead, Template
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "LeadGen Email Assistant API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "generate_template": "POST /generate_template - Generate email templates using AI",
            "leads": "POST /leads - Create new leads",
            "templates": "POST /templates - Save generated templates"
        }
    }

# Pydantic models
class GenerateTemplateInput(BaseModel):
    company_name: str
    contact_name: str
    industry: str
    purpose: str

class LeadInput(BaseModel):
    company_name: str
    contact_name: str
    industry: str

class TemplateInput(BaseModel):
    lead_id: int
    subject: str
    body: str

# Generate email template
@app.post("/generate_template")
async def generate_template(input: GenerateTemplateInput, request: Request):
    logger.debug(f"Received /generate_template request: {await request.json()}")
    try:
        prompt = f"Generate a cold email with subject and body for {input.contact_name} at {input.company_name} in the {input.industry} industry. The purpose is {input.purpose}."
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        lines = response.text.split("\n")
        subject = lines[0].replace("Subject: ", "") if lines[0].startswith("Subject: ") else "Default Subject"
        body = "\n".join(lines[1:]) if len(lines) > 1 else response.text
        return {"subject": subject, "body": body}
    except Exception as e:
        logger.error(f"Error in /generate_template: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating template: {str(e)}")

# Create a lead
@app.post("/leads")
async def create_lead(lead: LeadInput, db: Session = Depends(get_db)):
    try:
        if not all([lead.company_name.strip(), lead.contact_name.strip(), lead.industry.strip()]):
            raise HTTPException(status_code=422, detail="All fields (company_name, contact_name, industry) must be non-empty")
        db_lead = Lead(
            company_name=lead.company_name,
            contact_name=lead.contact_name,
            industry=lead.industry,
            created_at=datetime.utcnow()
        )
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)
        logger.debug(f"Created lead: {db_lead.id}")
        return db_lead
    except HTTPException as e:
        logger.error(f"HTTP error in /leads: {str(e)}")
        raise e
    except Exception as e:
        db.rollback()
        logger.error(f"Error in /leads: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating lead: {str(e)}")

# Create a template
@app.post("/templates")
async def create_template(template: TemplateInput, db: Session = Depends(get_db)):
    try:
        lead = db.query(Lead).filter(Lead.id == template.lead_id).first()
        if not lead:
            raise HTTPException(status_code=400, detail="Invalid lead_id")
        if not all([template.subject.strip(), template.body.strip()]):
            raise HTTPException(status_code=422, detail="Subject and body must be non-empty")
        db_template = Template(
            lead_id=template.lead_id,
            generated_at=datetime.utcnow(),
            subject=template.subject,
            body=template.body
        )
        db.add(db_template)
        db.commit()
        db.refresh(db_template)
        logger.debug(f"Created template: {db_template.id}")
        return db_template
    except HTTPException as e:
        logger.error(f"HTTP error in /templates: {str(e)}")
        raise e
    except Exception as e:
        db.rollback()
        logger.error(f"Error in /templates: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating template: {str(e)}")