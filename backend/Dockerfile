FROM python:3.11-slim
WORKDIR /app
# Мы добавили "backend/" к пути, потому что контекст теперь — корень проекта
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "backend/app.py"]