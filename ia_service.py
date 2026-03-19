from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

client = genai.Client(api_key=GEMINI_API_KEY)

def gerar_relatorio(total_ganhos: float,
    total_despesas: float, 
    saldo: float, 
    breakdown_ganhos: dict, 
    breakdown_despesas: dict, 
    mes: int, 
    ano: int
    )-> str: 
    
    ganhos_formatados = '\n'.join([f'- {categoria}: R$ {valor:.2f}' for categoria, valor in breakdown_ganhos.items()])
    despesas_formatadas = '\n'.join([f'- {categoria}: R$ {valor:.2f}' for categoria, valor in breakdown_despesas.items()])

    prompt = f'''
Você é um assistente financeiro pessoal. Analise os dados financeiros do usuário referentes a {mes}/{ano} e forneça dicas práticas de como melhorar a saúde financeira.

Dados do período:
    - Total de ganhos: R$ {total_ganhos:.2f}
    - Total de despesas: R$ {total_despesas:.2f}
    - Saldo final: R$ {saldo:.2f}

    Ganhos por categoria:
    {ganhos_formatados}    

    Despesas por categoria:
    {despesas_formatadas}

    Por favor, forneça:
    1. Um resumo geral da situação financeira
    2. Pontos de atenção
    3. Dicas práticas de melhoria
    '''

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt
    )

    return response.text