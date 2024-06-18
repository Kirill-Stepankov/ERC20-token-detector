FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
    
WORKDIR /app

RUN pip install poetry==1.8.3

COPY ../pyproject.toml poetry.lock  ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY ./src /app/
