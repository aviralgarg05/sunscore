FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 appuser

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy source files
COPY *.py ./
COPY README.md ./

# Copy actual CSV and shapefiles (no fallbacks)
COPY uszips.csv ./uszips.csv
COPY shapefiles/ ./shapefiles/

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set required env variables
ENV PYTHONUNBUFFERED=1
ENV ZIP_DATA_FILE=uszips.csv
ENV RUN_ENV=docker
ENV DOCKER_CONTAINER=true
CMD ["python", "main.py"]