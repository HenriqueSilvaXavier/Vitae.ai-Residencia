import openai
import os
import PyPDF2

from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Obtém a chave da API do OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Verifica se a chave está configurada
if not openai.api_key:
    raise ValueError("A chave da API do OpenAI não foi configurada. Verifique o arquivo .env ou as variáveis de ambiente.")

# Função para análise do currículo
def analyze_resume(content_text, area):
    try:
        prompts = [
            f"Analise o seguinte currículo e forneça dicas de como ele pode melhorar. Faça isso de forma breve, por meio de 3 frases e não liste informações que já tem no currículo, no formato texto corrido: {content_text}",
            f"Diga como ele pode melhorar o apontamento de cada habilidade técnica no currículo e faça isso de forma breve, por meio de, no máximo, 2 frases, no formato texto corrido: {content_text}",
            f"Sugira melhorias de como ele pode melhorar a forma de falar sobre as experiências profissionais. Faça isso de forma breve, usando no máximo 4 frases, no formato texto corrido: {content_text}"
        ]

        responses = []
        for prompt in prompts:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente que analisa currículos e fornece dicas de melhoria."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1024,
                temperature=0.5
            )
            text = response.choices[0].message['content'].replace("\n", " ")
            responses.append(text)

        return {
            "estrutura_valida": verificar_estrutura(content_text),
            "dicas_melhoria": responses[0],  # Texto corrido
            "habilidades_tecnicas": responses[1],  # Texto corrido
            "areas_experiencia": responses[2]  # Texto corrido
        }
    except Exception as e:
        return {"error": str(e)}


# Função para verificar a estrutura do currículo
def verificar_estrutura(curriculo):
    tokens = curriculo.lower().split()  # Divide o texto por espaços e converte para minúsculas
    return "experiência" in tokens and ("educação" in tokens or "formação" in tokens)

# Função para processar o PDF e extrair texto
def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        content = ""
        for page in pdf_reader.pages:
            content += page.extract_text()  # Extrai texto de cada página
        return content
    except Exception as e:
        raise ValueError(f"Erro ao processar o PDF: {str(e)}")