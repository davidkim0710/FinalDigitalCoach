# Use a more specific base image
FROM python:3.12-slim-bullseye AS builder

# Install build dependencies and create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy only requirements first to leverage cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir tf-keras

# Start fresh with a new stage
FROM python:3.12-slim-bullseye

# Copy only the necessary ffmpeg libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    libglib2.0-0 \
    libsm6 \
    libxrender1 && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app/backend

# Copy the entire backend package
COPY ./ /app/backend

# Set environment variables
ENV PYTHONPATH="/app:$PYTHONPATH" 
ENV PYTHONUNBUFFERED=1

EXPOSE 5000





