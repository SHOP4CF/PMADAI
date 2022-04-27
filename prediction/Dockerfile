# Set base image (host OS)
FROM python:3.8

# Copy and unzip models data
COPY models_data.zip .
RUN apt-get update && apt-get install -y unzip
RUN unzip models_data.zip && rm models_data.zip

COPY config.yml .
RUN mkdir ./data
# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Set the working directory in the container
WORKDIR /src

# Copy the content of the local src directory to the working directory
COPY src/ .

WORKDIR ../

# Set pythonpath
ENV PYTHONPATH "${PYTHONPATH}:/"