FROM python:3.8.3-slim-buster as base
EXPOSE 8000

# Prevent writing .pyc files on the import of source modules
# and set unbuffered mode to ensure logging outputs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

    
# Install requirements
COPY ./requirements.txt . 
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org --upgrade pip
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

################# DEVELOPMENT ####################################
FROM base as development
RUN pip install  --trusted-host pypi.org --trusted-host files.pythonhosted.org bandit pylint safety mypy
COPY . .
RUN bandit -r . \
  && pylint . \
  && safety check -r requirements.txt 


################# PRODUCTION ####################################
FROM base as production
COPY . .
CMD hypercorn main:app --bind 0.0.0.0:8000 --reload