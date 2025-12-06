FROM python:3.12.7-slim

WORKDIR /app

# Копируем файлы зависимостей
COPY ./uv.lock .
COPY ./pyproject.toml .

# Ставим uv и зависимости проекта
RUN pip install --upgrade pip \
    && pip install uv \
    && uv sync

COPY . /app

# Запуск приложения
CMD ["uv", "run", "python", "main.py"]

WORKDIR /app