# Этап 1: Установка зависимостей через Poetry
FROM python:3.12.3-slim as poetry-deps

WORKDIR /app

# Устанавливаем Poetry
RUN pip install poetry

# Копируем ТОЛЬКО файлы зависимостей (чтобы не пересобирать при каждом изменении кода)
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости в виртуальное окружение (без текущего проекта)
RUN poetry config virtualenvs.in-project true && \
    poetry install --no-root --no-interaction --no-ansi

# Этап 2: Финальный образ
FROM python:3.12.3-slim

WORKDIR /app

# Копируем виртуальное окружение из первого этапа
COPY --from=poetry-deps /app/.venv ./.venv

# Копируем ВЕСЬ остальной код (после установки зависимостей)
COPY . .

# Добавляем виртуальное окружение в PATH
ENV PATH="/app/.venv/bin:$PATH"

# Запускаем приложение
CMD ["python", "src/main.py"]