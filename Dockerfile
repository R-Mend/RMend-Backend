# Setup base image from ubuntu 20.04 image
FROM ubuntu:20.04

# STEP 2: Set working directory for install requirements
WORKDIR ./app

# STEP 3: Add requirements.txt file for dependencies
ADD ./requirement.txt .

# STEP 4: Install rdependencies to container
RUN pip install -r requirements.txt

# STEP 5: Copy project file and folders
COPY . .
