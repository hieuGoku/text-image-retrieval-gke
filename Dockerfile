# https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/master/docker-images/start.sh
# https://github.com/Swiple/swiple/blob/main/backend/Dockerfile
# https://github.com/michaeloliverx/python-poetry-docker-example/blob/master/docker/Dockerfile

# Base Python image
FROM python:3.10.14-slim AS python-base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Builder stage
FROM python-base AS builder-base

# Install system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    build-essential

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python -

# Install Python dependencies
WORKDIR $PYSETUP_PATH
COPY pyproject.toml ./
RUN poetry install --only main

# Development stage
FROM python-base AS development

ENV FASTAPI_ENV=development

# Copy Poetry and venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# Set up retrieval app directory
WORKDIR /retrieval_app
COPY . ./

EXPOSE 8001

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]

# Production stage
FROM python-base AS production

ENV FASTAPI_ENV=production

# Copy Poetry and venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl

# Set up app directory
WORKDIR /retrieval_app
COPY . ./

RUN chmod +x prestart.sh
# You must use ./start.sh to run the start.sh file from current directory. /start.sh run start.sh in root /, which does not exist.
ENTRYPOINT ./prestart.sh $0 $@

CMD ["poetry", "run", "gunicorn", "app.main:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8001"]