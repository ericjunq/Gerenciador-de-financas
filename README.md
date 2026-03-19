💰 Gerenciador Financeiro Pessoal — Backend
API REST para gerenciamento de finanças pessoais, com autenticação JWT, registro de ganhos e despesas, e geração de relatórios com dicas financeiras via IA (Google Gemini).

🚀 Tecnologias

Python + FastAPI
SQLAlchemy + SQLite
Pydantic — validação de dados
pwdlib — criptografia de senhas
python-jose — autenticação JWT
Google Gemini API — geração de relatórios com IA


📁 Estrutura do Projeto
├── main.py                  # Ponto de entrada da aplicação
├── database.py              # Configuração do banco de dados
├── models.py                # Tabelas do banco (SQLAlchemy)
├── schemas.py               # Schemas de validação (Pydantic)
├── security.py              # JWT, criptografia e autenticação
├── dependencies.py          # Dependências globais (sessão do banco)
├── validations.py           # Validação de CPF
├── auth_routers.py          # Rotas de autenticação
├── despesas_routers.py      # Rotas de despesas
├── ganhos_routers.py        # Rotas de ganhos
├── relatorio_routers.py     # Rota de relatório com IA
└── ia_service.py            # Integração com Google Gemini

⚙️ Configuração
1. Clone o repositório
bashgit clone https://github.com/ericjunq/Gerenciador-de-financas.git
cd seu-repositorio
2. Instale as dependências
bashpip install fastapi uvicorn sqlalchemy pydantic[email] python-jose pwdlib python-dotenv google-generativeai
3. Configure o arquivo .env
Crie um arquivo .env na raiz do projeto com as seguintes variáveis:
envDATABASE_URL=sqlite:///./banco.db
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRES_MINUTES=30
REFRESH_TOKEN_EXPIRES_DAYS=7
GEMINI_API_KEY=sua_chave_gemini_aqui

A chave da API do Gemini pode ser obtida gratuitamente em aistudio.google.com

4. Rode a aplicação
bashuvicorn main:app --reload
A API estará disponível em http://localhost:8000
Documentação interativa: http://localhost:8000/docs

🔐 Autenticação
A API utiliza autenticação via JWT (Bearer Token). O fluxo é:

Criar conta em POST /users/criar_conta
Fazer login em POST /users/login e receber access_token e refresh_token
Usar o access_token no header das requisições protegidas: Authorization: Bearer <token>
Quando o access_token expirar, renovar em POST /users/refresh usando o refresh_token


📌 Rotas
Usuários — /users
MétodoRotaDescriçãoPOST/users/criar_contaCadastro de novo usuárioPOST/users/loginLogin e geração de tokensPOST/users/refreshRenovação do access token
Despesas — /despesas 🔒
MétodoRotaDescriçãoPOST/despesas/adicionar_despesaRegistrar nova despesaGET/despesas/listar_despesasListar despesas com total (filtro: dia, semana, mes)DELETE/despesas/deletar_despesa/{id}Deletar uma despesa
Ganhos — /ganhos 🔒
MétodoRotaDescriçãoPOST/ganhos/adicionar_ganhoRegistrar novo ganhoGET/ganhos/listar_ganhosListar ganhos com total (filtro: dia, semana, mes)DELETE/ganhos/deletar_ganho/{id}Deletar um ganho
Relatório — /relatorio 🔒
MétodoRotaDescriçãoPOST/relatorio/gerar_relatorioGerar relatório financeiro com dicas via IA

🔒 Rotas protegidas exigem token JWT no header.


📊 Categorias disponíveis
Despesas:
alimentacao · transporte · moradia · saude · educacao · vestuario · esporte · outros
Ganhos:
salario · freelance · investimento · bonus · outros

🤖 Relatório com IA
O endpoint POST /relatorio/gerar_relatorio utiliza o Google Gemini para analisar os dados financeiros do mês informado e retornar:

Resumo geral da situação financeira
Pontos de atenção
Dicas práticas de melhoria

Parâmetros (query params):

mes — mês desejado (padrão: mês atual)
ano — ano desejado (padrão: ano atual)
