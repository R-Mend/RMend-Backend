# Setup base image from python:3.7-slim-buster image
FROM python:3.7

# STEP 2: Set working directory for install requirements
WORKDIR /usr/scr/rmend_project

# STEP 3: Set environment variables for python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# STEP 4: Install postgis database requirements
RUN apt-get update && apt-get install gcc python3-dev musl-dev gdal-bin -y

# STEP 5: Update pip if there's a new version avaliable
RUN pip install --upgrade pip

# STEP 6: Copy requirements.txt file for project dependencies
COPY ./requirements.txt .

# STEP 7: Install requiremnts to container
RUN pip install -r requirements.txt

# STEP 8: Copy project files to container
COPY . .