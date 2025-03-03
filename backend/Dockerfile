FROM python:3.11-bookworm

RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --only=main --no-root
COPY src ./src
WORKDIR /app

CMD ["poetry", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "5005"]