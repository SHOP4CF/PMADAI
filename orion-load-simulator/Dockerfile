# Set base image (host OS)
FROM python:3.8

COPY config.yml .

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Copy and unzip simulation data
COPY simulation_data.zip .
RUN apt-get update && apt-get install -y unzip
RUN unzip simulation_data.zip && rm simulation_data.zip

# Install dependencies
RUN pip install -r requirements.txt

# Set the working directory in the container
WORKDIR /src

# Copy the content of the local src directory to the working directory
COPY src/ .

WORKDIR ../

# Set pythonpath
ENV PYTHONPATH "${PYTHONPATH}:/"

# Command to run on container start
CMD python src/main.py