from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT = genai.Client(
    api_key=os.getenv('GEMINI_API_KEY')
)

def validar_postagem(corpo: str) -> bool:
    validacao = CLIENT.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"""
            Verifique: ofensas (pessoais, intolerância, 
            escola, calão) ou burla (criptografia, substituições, 
            espaços). Resposta: S ou N\n\n{corpo}
        """
    ).text

    return validacao == 'N'
