# Telegram File Storage Bot - Production Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements-standalone.txt .
RUN pip install --no-cache-dir -r requirements-standalone.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p templates logs

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Default command (webhook mode)
CMD ["gunicorn", "-c", "gunicorn_config.py", "webhook_server:app"]