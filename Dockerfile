# Stage 1: Builder (установка зависимостей)
FROM python:3.12-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Создаем виртуальное окружение для production
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.base.txt .
RUN pip install --no-cache-dir -r requirements.base.txt

# Stage 2: Development / Testing (все зависимости)
FROM python:3.12-slim as dev

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

COPY --from=builder /opt/venv /opt/venv
COPY requirements.base.txt requirements.dev.txt ./

# Доустанавливаем dev зависимости
RUN pip install --no-cache-dir -r requirements.dev.txt

COPY . .

# Stage 3: Production
FROM python:3.12-slim as prod

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

# Копируем только venv с продовыми либами
COPY --from=builder /opt/venv /opt/venv
COPY . .

# Используем непривилегированного пользователя
RUN useradd -m appuser && chown -R appuser /app
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
