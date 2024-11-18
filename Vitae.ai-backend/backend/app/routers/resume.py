from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.services.resume_analysis import analyze_resume
from app.database import get_db
from app import models

router = APIRouter()

@router.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...), area: str = "general", db: Session = Depends(get_db)):
    content = await file.read()  # Leitura do arquivo do currículo
    content_text = content.decode("utf-8")
    
    # Analisar o currículo
    feedback = analyze_resume(content_text, area)
    
    # Salvar currículo e feedback no banco de dados
    resume = models.Resume(name=file.filename, content=content_text, feedback=feedback)
    db.add(resume)
    db.commit()
    db.refresh(resume)
    
    return {"filename": file.filename, "feedback": feedback}
