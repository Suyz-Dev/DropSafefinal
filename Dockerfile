# DropSafe - Student Risk Assessment Platform
# Dockerfile for containerized deployment

# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8499
ENV STREAMLIT_SERVER_HEADLESS=true

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports for all services
EXPOSE 8499 8501 8502 8504

# Create non-root user
RUN adduser --disabled-password --gecos '' dropsafe
RUN chown -R dropsafe:dropsafe /app
USER dropsafe

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8499/healthz || exit 1

# Run the application
CMD ["./run.sh"]