FROM python:3.13-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY uv.lock .
COPY pyproject.toml .

RUN uv sync

COPY . .

EXPOSE 8000

ENTRYPOINT [ "uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
