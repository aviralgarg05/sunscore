FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

# Create non-root user first
RUN useradd -m -u 1000 appuser

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary source files (exclude large data files)
COPY *.py ./
COPY README.md ./

# Create necessary directories with proper permissions
RUN mkdir -p ./data ./logs && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV RUN_ENV=docker
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "main.py"]