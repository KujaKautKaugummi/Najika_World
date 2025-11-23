# Najika World Backend Dockerfile
# Multi-stage build for optimized production image

# ============================================================================
# Stage 1: Builder
# ============================================================================
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# ============================================================================
# Stage 2: Runtime
# ============================================================================
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 najika && \
    chown -R najika:najika /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/najika/.local

# Copy application code
COPY --chown=najika:najika backend/ ./backend/
COPY --chown=najika:najika digivice/ ./digivice/
COPY --chown=najika:najika DOCS/ ./DOCS/

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/models && \
    chown -R najika:najika /app

# Switch to non-root user
USER najika

# Add local bin to PATH
ENV PATH=/home/najika/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
