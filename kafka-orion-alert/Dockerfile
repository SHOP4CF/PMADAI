# Set base image (host OS)
FROM python:3.8

# This microservice has the context of the entire project in order to be able to access deployment_utils and avoid using docker volume.
COPY kafka-orion-alert/config.yml .

# Setup oracle instantclient libraries
WORKDIR    /opt/oracle
RUN        apt-get update && apt-get install -y libaio1 wget unzip \
            && wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip \
            && unzip instantclient-basiclite-linuxx64.zip \
            && rm -f instantclient-basiclite-linuxx64.zip \
            && cd /opt/oracle/instantclient* \
            && rm -f *jdbc* *occi* *mysql* *README *jar uidrvci genezi adrci \
            && echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf \
            && ldconfig

# Copy the dependencies file to the working directory
COPY /kafka-orion-alert/requirements.txt /kafka-orion-alert/

# Install dependencies
RUN pip install -r /kafka-orion-alert/requirements.txt

# Set the working directory in the container
WORKDIR /kafka-orion-alert/src/

# Copy the content of the local src directory to the working directory
COPY /kafka-orion-alert/src/ .

WORKDIR ../

COPY deployment_utils/ /kafka-orion-alert/deployment_utils/

# Set pythonpath
ENV PYTHONPATH "${PYTHONPATH}:/"

# Command to run on container start
CMD python src/main.py