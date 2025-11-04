# 🐍 Base Python image
FROM python:3.11-slim

# 🧩 Environment setup
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# 🛠️ Install system deps
RUN apt-get update && apt-get install -y \
    build-essential curl git \
    && rm -rf /var/lib/apt/lists/*

# 🐍 Copy requirements first (for caching)
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 🧠 Copy full source
COPY . .

# ⚙️ Default command (API server)
CMD ["python", "api/server.py"]
