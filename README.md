# notIFica

Uma API que registra postagens e comunicados de alunos e servidores para display em carrossel de conteúdo via TVs disponibilizadas pelo campus.

Pensado para melhorar a ala de comunicação da escola em meio a proibição de celulares.

## Tabela de Conteúdos

1. [Tecnologias](#tecnologias)
2. [Como instalar](#como-instalar)
4. [Créditos](#créditos)

## Tecnologias

- **Python (3.12 ou superior)**: principal linguagem de programação;
- **Django e DRF**: framework para desenvolvimento de APIs REST;
- **MySQL**: persistência de dados da aplicação;
- **Celery**: execução de tarefas de forma assíncrona;
- **Redis**: broker de dados para o celery;
- **Requests**: cliente HTTP;
- **Feedparser**: parser de RSS para scraping eficiente;
- **BeautifulSoup4**: parser de HTML para crawling em páginas web.

## Como instalar

Para a instalação do projeto, é necessário clonar o repositório com o git, usando o terminal para rodar os comandos a seguir:

```bash
git clone https://github.com/yuriteixeirac/notifica

cd notifica
```

Para a instalação das dependências, ative um ambiente virtual e instale com Poetry como no exemplo a seguir:

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install poetry    # caso não o tenha instalado
poetry install
```

Para as variáveis de ambiente, o projeto conta com um exemplo para um arquivo `.env`, que requer informações como as credenciais do banco de dados, do serviço de armazenamento Cloudinary, a chave da API do Gemini e a chave secreta da aplicação.

```
# Para funcionamento interno do Django e DRF
SECRET_KEY=

# Serviço de armazenamento
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

# Chave da API para verificação de postagem
GEMINI_API_KEY=

# Credenciais para acesso ao banco de dados
DB_NAME=
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_PORT=

# Credenciais para o funcionamento dos crawlers
SUPER_USER_USERNAME=
SUPER_USER_PASSWORD=
```

Ao configurar cada uma dessas variáveis, o backend está pronto para rodar.

## Créditos

- Leo Silva, coordenador do projeto.
- Matheus Lemos, desenvolvedor front-end.
- Yuri Teixeira, desenvolvedor back-end.
