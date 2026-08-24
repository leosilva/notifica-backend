FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY uv.lock .
COPY pyproject.toml .

RUN uv sync

COPY . .

EXPOSE 8000

ENTRYPOINT [ "uv", "run", "flask", "--app", "app", "run", "--port=8000", "--host=0.0.0.0" ]
