FROM python:3.13-slim

# Set environment variables for 12-factor compliance
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files and README.md (required by pyproject.toml)
COPY pyproject.toml uv.lock README.md ./

# Install Python dependencies with uv (including dev dependencies for development)
RUN uv sync --frozen
RUN uv sync --frozen --extra dev

# Copy project
COPY . .

# Create static and media directories
RUN mkdir -p static media

# Create non-root user for security
RUN groupadd -r django && useradd -r -g django django
RUN chown -R django:django /app

# Create cache directory for uv with proper permissions
RUN mkdir -p /home/django/.cache/uv && chown -R django:django /home/django

USER django

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health/ || exit 1

# Run the application using the installed venv
CMD [".venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
