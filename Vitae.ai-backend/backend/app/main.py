from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from db.database import init_db, get_db, Resume
from endpoint.upload_resume import UploadResume
import os
import openai
import PyPDF2
import json

from dotenv import load_dotenv
import os

# Inicialização do Flask e Flask-RESTful
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

# Adicionando os recursos à API
api.add_resource(UploadResume, '/upload_resume/')

if __name__ == '__main__':
    # Inicializa o banco de dados
    init_db()
    app.run(debug=True)
