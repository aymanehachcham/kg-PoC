# Use an official Python runtime as the parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Update apt repositories and install required system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install required system dependencies
RUN pip3 install poetry

# Configure the virtual env to be created in the project directory
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi --only prod


# Modify PATH to use poetry's virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Copy the current directory contents into the container at /app
COPY . /app

WORKDIR /app

# Update the PYTHON PATH
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

# Specify the command to run on container start
CMD ["sh", "-c", "poetry shell && cd kg_poc && weasel run all"]
