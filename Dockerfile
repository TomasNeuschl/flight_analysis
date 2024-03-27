# Use a Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python -

# Make Poetry available in the PATH
ENV PATH="/opt/poetry/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Copy the Poetry files
COPY pyproject.toml poetry.lock /app/

# Install Python dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --only main

# Copy the Django application code
COPY . /app/

# Run Django migrations to create database tables
RUN python manage.py migrate

# Create a default superuser
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('user', 'user@example.com', 'password')" | python manage.py shell

# Expose the port that Django runs on
EXPOSE 8000

# Run Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
