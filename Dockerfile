FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml and source code
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install dependencies and project package
RUN pip install --no-cache-dir .

ENV PYTHONPATH=/app
ENV POLARS_MAX_THREADS=1

CMD ["python", "src/main.py"]
