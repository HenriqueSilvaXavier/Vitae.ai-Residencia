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
def analyze_resume(content_text):
    try:
        prompt = f"""
        Aja como um especialista em recrutamento. 
        Você vai analisar um currículo considerando os aspectos visuais.
        Os critérios que deve analisar estão listados a seguir:

        1. layout: o layout do currículo deve ser limpo, organizado e atraente, fácil de ler e seguir.
        2. estrutura: deve ter espaçamento e margens uniformes para manter a consistência visual do currículo.
        3. cores: deve ter uma paleta de cores coerente e profissional, como azul, cinza ou verde escuro.
        4. fonte e tamanho: escolha uma fonte profissional e um tamanho legível, como Times New Roman ou Arial, em tamanho de 12 a 14.

        Sempre responda em formato JSON.
        ## Sua resposta deve ser apenas o objeto JSON, seguindo as chaves: layout, estrutura, cores e fonte.
        Em cada critério, adicione um criterio_detail, como layout_detail, detalhando por que o critério deve ser seguido.
        Exemplo de resposta em formato JSON:
        {{
            "layout": "...",
            "layout_detail": "...",
            "estrutura": "...",
            "estrutura_detail": "...",
            "cores": "...",
            "cores_detail": "...",
            "fonte": "...",
            "fonte_detail": "..."
        }}

        Análise do currículo:
        {content_text}
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um especialista em recrutamento que analisa currículos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
            temperature=0.5
        )

        # Extrai e retorna a resposta da IA
        return response.choices[0].message['content']

    except Exception as e:
        return {"error": str(e)}


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
