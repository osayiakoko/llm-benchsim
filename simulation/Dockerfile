# Use an official Python runtime as the base image
FROM python:3.11.9-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy needed folders and files into the container at /app
COPY alembic/ alembic/
COPY alembic.ini alembic.ini
COPY src/ src/

# Create an entrypoint script
RUN echo '#!/bin/sh' > /entrypoint.sh && \
    echo 'alembic upgrade head' >> /entrypoint.sh && \
    echo 'exec python -m src.main' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Set the entrypoint script as the entrypoint
ENTRYPOINT ["/entrypoint.sh"]
