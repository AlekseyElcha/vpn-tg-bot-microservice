FROM python:3.14-slim

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Устанавливаем uv
RUN pip install uv

WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости на уровне системы
RUN uv sync --frozen --no-dev

# Копируем весь проект
COPY . .

# Команда для запуска бота
CMD ["uv", "run", "main.py"]
