from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
import os

# ConfiguraçãoLLM
llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Função analisar o currículo e gerar feedback
def analyze_resume(resume_text: str, area: str) -> str:
    prompt_template = PromptTemplate(
        input_variables=["resume_text", "area"],
        template="""
        Analise o seguinte currículo de um estudante para a área de {area}. 
        Sugira melhorias e dê um feedback detalhado:

        Currículo:
        {resume_text}

        Forneça suas recomendações:
        """
    )
    prompt = prompt_template.render({"resume_text": resume_text, "area": area})
    feedback = llm(prompt)
    
    return feedback
