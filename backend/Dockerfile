FROM python:3.11-slim

WORKDIR /app

# Сначала копируем зависимости и ставим их
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Указываем путь поиска модулей, чтобы main.py видел db.py
ENV PYTHONPATH=/app/backend

# Запускаем сервер
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]