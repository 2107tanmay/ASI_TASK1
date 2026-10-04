# Dockerfile for FastAPI backend
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential libpoppler-cpp-dev git && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
