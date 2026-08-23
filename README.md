# notIFica

Uma plataforma para gerenciamento de postagens e notícias publicadas por alunos, servidores e serviços externos, pensada para a comunicação institucional do IFRN Ceará-Mirim.

A exibição do conteúdo será feita através de televisores institucionais pelo campus.

## Tabela de conteúdos

- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Como rodar](#como-rodar)
- [Autores](#autores)

## Tecnologias

- Python 3.13+;
- Flask;
- Marshmallow;
- MySQL/MariaDB;
- SQLAlchemy;
- Alembic;
- Cloudinary;
- DeepSeek API;

## Estrutura do projeto

- `app/auth`: contém a autenticação e integração com o SUAP;
- `app/postagens`: engloba as postagens e moderação de conteúdo;
- `app/noticias`: as notícias e coleta periódica por RSS;
- `app/carrossel`: seleção e ordenação dos conteúdos exibidos;
- `migrations`: versionamento ativo do schema de dados;
- `main.py`: ponto de entrada da aplicação;

## Como rodar

Clone o repositório:

```bash
git clone <URL_DO_REPOSITÓRIO - https/.git>
cd notifica
```

Instale as dependências com `uv`:

```bash
uv sync 
```

Copie as configurações de ambiente:

```bash
cp .env.example .env
```

Defina as variáveis de ambiente:

```bash
SECRET_KEY=

SQLALCHEMY_DATABASE_URI=

JWT_SECRET_KEY=

SUAP_CLIENT_ID=
SUAP_CLIENT_SECRET=

DEEPSEEK_API_KEY=

CLOUDINARY_URL=

BASE_FRONTEND_URL=
```

Aplique as migrações do banco:
```bash
uv run flask db upgrade
```

### Execução

Inicie o servidor de desenvolvimento:

```bash
uv run flask --app main run
```

A aplicação estará disponível em `http://localhost:5000/`. A documentação (swagger-ui) estará em `http://localhost:5000/docs/`

### Coleta de notícias

O script de notícias pode ser executado através do comando:

```bash
uv run python3 -m app.noticias.coletor
```

O coletor consulta feeds RSS, normaliza os campos disponíveis e persiste as notícias diretamente no banco de dados.

Sua execução periódica depende do ambiente de configuração.

## To do

- Implementação de blueprint para administradores;
- Sistema robusto para deduplicação de notícias;

## Autores

- **Leo Silva**, coordenador do projeto.
- **Matheus Lemos**, desenvolvedor front-end.
- **Yuri Teixeira**, desenvolvedor back-end.
