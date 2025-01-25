FROM python:3.11-bookworm
RUN pip install poetry
ADD pyproject.toml .
RUN poetry install --only=main
COPY /src /src
WORKDIR .