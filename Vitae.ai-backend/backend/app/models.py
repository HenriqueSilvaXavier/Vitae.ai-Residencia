from sqlalchemy import Column, Integer, String
from .database import Base

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    content = Column(String)  # Conteúdo do currículo em texto
    feedback = Column(String)  # Feedback gerado pelo LLM
