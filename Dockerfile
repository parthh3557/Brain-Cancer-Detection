# Use the official Python slim image for a smaller footprint
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the raw logs
ENV PYTHONUNBUFFERED True

# Set the working directory
WORKDIR /app

# Copy local code to the container image
COPY . ./

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies.
# The `requirements.txt` has `--extra-index-url https://download.pytorch.org/whl/cpu`
# to ensure the CPU version of Torch is installed, saving significant space.
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup using gunicorn.
# Increase workers and threads if needed, keeping memory in mind.
# Also set a longer timeout for ML predictions if necessary.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
