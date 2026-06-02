FROM python:3.12-slim AS builder

# Evita arquivos .pyc e garante saída sem buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Poetry
    POETRY_VERSION=2.2.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"

# Dependências de sistema para compilar pacotes nativos
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        libpq-dev \
        default-libmysqlclient-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Instala Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

# Copia apenas os manifests primeiro (aproveitamento do cache de layers)
COPY pyproject.toml poetry.lock ./

# Instala somente dependências de produção (sem dev)
RUN poetry install --only main --no-root


# ──────────────────────────────────────────────
#  Stage 2 – runtime: imagem final enxuta
# ──────────────────────────────────────────────
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Aponta para o venv criado no builder
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Dependências de runtime (sem headers de compilação)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libmariadb3 \
        curl \
        netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Usuário não-root para segurança
RUN groupadd --gid 1001 appgroup \
    && useradd --uid 1001 --gid appgroup --no-create-home appuser

WORKDIR /app

# Copia o venv pronto do builder
COPY --from=builder /app/.venv /app/.venv

# Copia o código-fonte
COPY --chown=appuser:appgroup . .

# Script de entrypoint
COPY --chown=appuser:appgroup docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER appuser

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]
