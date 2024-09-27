# Use an official Python runtime as a parent image
FROM python:3.11.9-alpine

# Set the working directory in the container
WORKDIR /app

# requirments.txt
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy needed folders and files into the container at /app
COPY alembic/ alembic/
COPY alembic.ini alembic.ini
COPY src/ src/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Set up the entrypoint
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]