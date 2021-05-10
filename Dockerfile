FROM python:3.8.3-slim-buster as base
EXPOSE 8000
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Prevent writing .pyc files on the import of source modules
# and set unbuffered mode to ensure logging outputs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Add default user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME
    
# Install requirements
COPY requirements requirements
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org --upgrade pip
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements/prod.txt

################# DEVELOPMENT ####################################
FROM base as development
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements/dev.txt

RUN pip install  --trusted-host pypi.org --trusted-host files.pythonhosted.org bandit pylint safety mypy
COPY . .
RUN bandit -r . \
  && pylint . \
  && safety check -r requirements/prod.txt

################# PRODUCTION ####################################
FROM base as production
COPY . .
USER $USERNAME
CMD hypercorn main:app --bind 0.0.0.0:8000 --reload