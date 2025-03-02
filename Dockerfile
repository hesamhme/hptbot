FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set environment variables (dotenv will load from .env)
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app


CMD ["python", "main.py"]
