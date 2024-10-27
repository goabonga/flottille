# Use a specific version of the official Python 3.12 image as the base image
# This ensures that our application runs on Python 3.12
FROM python:3.12

# Set the working directory inside the container to /app/
# All subsequent commands will be executed inside this directory
WORKDIR /app/

# Install Poetry (Python dependency management and packaging tool)
# The POETRY_HOME environment variable specifies where Poetry will be installed
# The 'ln -s' command creates a symbolic link to Poetry in the global PATH
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy the required project files to the container
# - README.md, pyproject.toml, and poetry.lock are copied into /app/
# - poetry.lock is optional, as indicated by the wildcard (*) in case it doesn't exist
COPY ./README.md ./pyproject.toml ./poetry.lock* /app/

# Set the PYTHONPATH environment variable to /app to ensure that Python can find the code
ENV PYTHONPATH=/app

# Copy the source code from the host machine to the container's /app/src/ directory
COPY ./app /app/app

# Define an argument to allow the installation of dev dependencies if needed
# This argument will default to false unless explicitly set to true when building the image
ARG INSTALL_DEV=false

# Conditional installation of dependencies:
# - If INSTALL_DEV is true, install both dev and api dependencies
# - If false, install only the main and api dependencies
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --with dev --with api; else poetry install --with main --with api; fi"

# Define the default command that will run when the container starts
# - This runs Uvicorn, a fast ASGI server, to serve the FastAPI application
# - The app is located at user_clustering.api.main:app
# - The --workers 1 option ensures that Uvicorn runs with a single worker
CMD ["uvicorn", "--host", "0.0.0.0", "--workers", "1", "flottille.api.main:app"]
