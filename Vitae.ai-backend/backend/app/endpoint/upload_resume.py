from flask_restful import Resource
from flask import request
from db.database import get_db, Resume
from util.utils import analyze_resume, extract_text_from_pdf
import json

# Analisa o currículo e retorna um JSON estruturado
class UploadResume(Resource):
    def post(self):
        try:
            db = next(get_db())
            file = request.files["file"]
            area = request.form.get("area", "general")

            # Extrai o texto do PDF
            content = extract_text_from_pdf(file)

            # Analisa o currículo com a IA
            feedback = analyze_resume(content)

            # Salva no banco de dados
            resume = Resume(name=file.filename, content=content, feedback=json.dumps(feedback))
            db.add(resume)
            db.commit()
            db.refresh(resume)

            return {
                "filename": file.filename,
                "feedback": feedback  # Feedback estruturado da IA
            }, 201
        except Exception as e:
            return {"error": str(e)}, 500
